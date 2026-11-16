"""Build NYC dossier records from parcel-specific Agent and Fetch evidence."""

import argparse
import json
import re
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from uuid import UUID

from main import dossier, report
from tinyfish import API, request

OPEN_DATA = "https://data.cityofnewyork.us/resource/"
FINANCE = "https://a836-pts-access.nyc.gov/care/datalets/datalet.aspx"


def source_urls(bbl, bin_number, tax_year):
    if not re.fullmatch(r"[1-5]\d{9}", bbl) or not re.fullmatch(r"[1-5]\d{6}", bin_number):
        raise ValueError("Provide a ten-digit NYC BBL and a seven-digit BIN")
    return {
        "zoning": OPEN_DATA + "64uk-42ks.json?" + urlencode({
            "bbl": bbl, "$select": "bbl,address,zonedist1", "$limit": 3,
        }),
        "tax": FINANCE + "?" + urlencode({
            "LMparent": 20, "UseSearch": "no", "jur": 65,
            "mode": f"asmt_fin_{tax_year}", "pin": bbl, "taxyr": tax_year,
        }),
        "permit": OPEN_DATA + "rbx6-tga4.json?" + urlencode({
            "bin": bin_number, "$select": "work_permit,block,lot,borough,bin",
            "$order": "work_permit DESC", "$limit": 20,
        }),
    }


def json_rows(text):
    # TinyFetch Markdown can escape underscores in JSON keys.
    return json.loads(text.replace(r"\_", "_")) if text else []


def build_dossier(bbl, bin_number, tax_year, urls, pages, agent):
    checked = datetime.now(timezone.utc).date().isoformat()
    parcels = [row for row in json_rows(pages.get(urls["zoning"]))
               if str(row.get("bbl", "")).split(".")[0] == bbl and row.get("address")]
    payload = {
        "subject": bbl, "parcels": [], "records": [],
        "official_hosts": ["data.cityofnewyork.us", "a836-pts-access.nyc.gov"],
    }
    if len(parcels) != 1:
        return dossier(payload)
    parcel = parcels[0]
    payload["parcels"].append({"parcel_id": bbl, "address": parcel["address"]})

    def add(category, record_id, summary, agency):
        payload["records"].append({
            "parcel_id": bbl, "category": category, "record_id": record_id,
            "summary": summary, "source_url": urls[category],
            "checked_date": checked, "agency": agency,
        })

    if parcel.get("zonedist1"):
        add("zoning", bbl, f"Primary zoning district {parcel['zonedist1']}", "NYC City Planning")
    tax_text = " ".join(pages.get(urls["tax"], "").split())
    assessment = re.search(r"Taxes Will Be Based On\s+([\d,]+)", tax_text, re.IGNORECASE)
    if assessment and re.search(r"Property Address\s+" + re.escape(parcel["address"]) + r"(?:\s|$)",
                                tax_text, re.IGNORECASE):
        add("tax", str(tax_year), f"Assessment used to calculate taxes: {assessment[1]}",
            "NYC Department of Finance")
    agent_ids = {row.get("work_permit") for row in agent
                 if str(row.get("bin")) == bin_number}
    seen = set()
    for row in json_rows(pages.get(urls["permit"])):
        permit_id = row.get("work_permit")
        if (permit_id and permit_id in agent_ids and permit_id not in seen
                and str(row.get("bin")) == bin_number
                and str(row.get("block", "")).zfill(5) == bbl[1:6]
                and str(row.get("lot", "")).zfill(4) == bbl[6:]):
            add("permit", permit_id, f"DOB NOW approved permit {permit_id} for BIN {bin_number}",
                "NYC Department of Buildings")
            seen.add(permit_id)
    result = dossier(payload)
    result["official_agency_count"] = len({row["agency"] for row in payload["records"]})
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("bbl")
    parser.add_argument("bin")
    parser.add_argument("--tax-year", type=int, default=date.today().year + 1)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--agent-run", type=UUID, help="Reuse a completed permit lookup")
    action.add_argument("--start-agent", action="store_true", help="Start one billable permit lookup")
    args = parser.parse_args()
    urls = source_urls(args.bbl, args.bin, args.tax_year)
    if args.start_agent:
        queued = request(API + "/v1/automation/run-async", {
            "url": urls["permit"],
            "goal": f"Read only the supplied NYC DOB endpoint for BIN {args.bin}. "
                    "Return JSON {records:[{work_permit,block,lot,borough,bin}]} with up to three distinct "
                    "permit IDs, or an empty list if the source is empty. Exclude personal information.",
            "agent_config": {"max_duration_seconds": 60},
        })
        print(json.dumps({"run_id": str(UUID(queued["run_id"]))}))
        raise SystemExit(0)
    run = request(API + "/v1/runs/" + str(args.agent_run))
    if run.get("status") != "COMPLETED":
        parser.error("The supplied Agent run must be complete")
    raw = run.get("result")
    result = json.loads(raw) if isinstance(raw, str) else raw
    if not isinstance(result, dict) or not isinstance(result.get("records"), list):
        parser.error("The Agent run must return a structured permit record list")
    fetched = request("https://api.fetch.tinyfish.ai", {
        "urls": list(urls.values()), "format": "markdown", "ttl": 0,
    })
    pages = {row["url"]: row["text"] for row in fetched.get("results", [])
             if row["url"] in urls.values() and (row.get("final_url") or row["url"]) == row["url"]}
    result = build_dossier(args.bbl, args.bin, args.tax_year, urls, pages, result["records"])
    print(json.dumps({"mode": "provider_lookup", "agent_run_id": str(args.agent_run),
                      **result, "report": report(result)}, indent=2))
