import json
import os
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import build_opener, HTTPRedirectHandler, Request
from uuid import UUID

API = "https://agent.tinyfish.ai"
DRY_RUN = False
REQUEST_PLAN = []

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None

def request(url, body=None, *, method=None):
    if DRY_RUN:
        REQUEST_PLAN.append({"method": "GET" if body is None else "POST", "url": url, "body": body})
        return {}
    key = os.environ.get("TINYFISH_API_KEY", "").strip()
    private_config = Path(__file__).with_name(".env")
    if not key and private_config.is_file():
        for line in private_config.read_text(encoding="utf-8-sig").splitlines():
            name, _, value = line.partition("=")
            if name.strip() == "TINYFISH_API_KEY":
                key = value.strip().strip("\"'")
                break
    if not key:
        raise SystemExit("Set TINYFISH_API_KEY for this process.")
    req = Request(url, data=json.dumps(body).encode() if body is not None else None, method=method,
                  headers={"X-API-Key": key, "Content-Type": "application/json"})
    try:
        with build_opener(NoRedirect()).open(req, timeout=90) as result:
            return json.load(result)
    except HTTPError as error:
        raise SystemExit(f"TinyFish HTTP {error.code}. Check saved jobs before retrying a start.") from None
    except OSError as error:
        raise SystemExit(f"TinyFish request failed ({type(error).__name__}). Check saved jobs before retrying a start.") from None

def official_url(value, hosts):
    url = urlsplit(value)
    if url.scheme != "https" or url.hostname not in hosts or url.username or url.password or url.port not in (None, 443):
        raise ValueError("Expected an HTTPS URL on an explicitly configured official hostname")
    return value

def discover(url, goal, hosts, run_id=None):
    official_url(url, hosts)
    if run_id:
        data = request(API + "/v1/runs/" + str(UUID(run_id)))
        if data.get("goal") != goal:
            raise ValueError("Saved Agent run belongs to a different lookup")
    else:
        data = request(API + "/v1/automation/run", {
            "url": url, "goal": goal,
            "agent_config": {"max_duration_seconds": 60},
        })
    if data.get("status") != "COMPLETED":
        raise ValueError("Agent did not complete the lookup")
    result = data.get("result") or data.get("resultJson")
    result = json.loads(result) if isinstance(result, str) else result
    if not isinstance(result, dict):
        raise ValueError("Agent did not return a structured result")
    return result

def fetch_text(url, hosts):
    official_url(url, hosts)
    payload = request("https://api.fetch.tinyfish.ai", {"urls": [url], "format": "markdown", "ttl": 0})
    for row in payload.get("results", []):
        if row.get("url") == url and isinstance(row.get("text"), str):
            official_url(row.get("final_url") or url, hosts)
            return " ".join(row["text"].casefold().split())
    raise ValueError("Fetch could not corroborate the official record")

def create_monitor(url, hosts, purpose):
    return request(API + "/v1/monitors", {
        "type": "fetch", "config": {"url": official_url(url, hosts), "format": "markdown"},
        "schedule_cron": "0 */6 * * *", "purpose": purpose,
    })

import argparse
from datetime import datetime, timezone
from main import dossier, report, CATEGORIES

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--watch-permits", action="store_true", help="Create a billable monitor on a corroborated permit record")
    parser.add_argument("--dry-run", action="store_true", help="Validate input and print the request plan without network access")
    parser.add_argument("--reuse-run", nargs=2, action="append", default=[], metavar=("HOST", "RUN_ID"),
                        help="Use a saved Agent run for this source instead of starting another")
    args = parser.parse_args()
    DRY_RUN = args.dry_run
    data = json.loads(args.input.read_text(encoding="utf-8"))
    sources = data["sources"]
    if len({urlsplit(item["url"]).hostname for item in sources}) < 3:
        parser.error("Configure at least three official source hosts")
    hosts = data["official_hosts"]
    reused = dict(args.reuse_run)
    if set(reused) - {urlsplit(item["url"]).hostname for item in sources}:
        parser.error("A reused run must correspond to a configured source host")
    for run_id in reused.values():
        try:
            UUID(run_id)
        except ValueError:
            parser.error("A reused run ID must be a UUID")
    for source in sources:
        official_url(source["url"], hosts)
    if DRY_RUN:
        print(json.dumps({"mode": "dry_run", "agent_lookups": len(sources) - len(reused),
                          "reused_agent_runs": len(reused), "agent_duration_seconds_per_run": 60,
                          "recurring_monitor_requested": args.watch_permits,
                          "fetch": "Up to the corroboration limit per source"}, indent=2))
        raise SystemExit(0)
    data["parcels"], data["records"] = [], []
    unavailable = []
    unverified = {}
    for source in sources:
        origin = [urlsplit(source["url"]).hostname]
        try:
            found = discover(source["url"], "Search only this official public site for the exact supplied address "
                             "or parcel identifier. No sign-in, external navigation, or bypassing restrictions. "
                             "Return {parcels:[{parcel_id,address}],records:[{parcel_id,category,record_id,"
                             "summary,source_url}]} with short exact excerpts from the source, and no "
                             "invented ids or inferred parcel matches. Categories: " + ", ".join(CATEGORIES)
                             + ". Subject: " + json.dumps(data["subject"]), origin, reused.get(origin[0]))
            if not isinstance(found.get("records"), list) or len(found["records"]) > 12:
                raise ValueError("Lookup exceeded the twelve-record corroboration limit")
            verified_rows = []
            page_cache = {}
            for row in found["records"]:
                try:
                    url = row["source_url"]
                    if url not in page_cache:
                        page_cache[url] = fetch_text(url, origin)
                    text = page_cache[url]
                    summary = " ".join(row["summary"].casefold().split())
                    identity = str(row["parcel_id"]).strip().casefold()
                    if not summary or not identity or summary not in text or identity not in text:
                        raise ValueError("Fetch could not corroborate parcel and record")
                    if row["category"] not in CATEGORIES:
                        raise ValueError("Unexpected record category")
                except (AttributeError, ValueError, KeyError, TypeError):
                    unverified[source["url"]] = unverified.get(source["url"], 0) + 1
                    continue
                verified_rows.append({**row, "checked_date": datetime.now(timezone.utc).date().isoformat()})
            data["parcels"].extend(found["parcels"])
            data["records"].extend(verified_rows)
        except (ValueError, KeyError, TypeError):
            unavailable.append(source["url"])
    result = dossier(data)
    if (unavailable or unverified) and result["status"] == "complete":
        result["status"] = "partial"
    if args.watch_permits:
        permits = result.get("records", {}).get("permit", [])
        if not permits:
            parser.error("A watch requires a corroborated parcel-specific permit page")
        result["monitor"] = create_monitor(permits[0]["source_url"], hosts,
                                           "Flag relevant permit changes for parcel " + result["parcel"]["parcel_id"])
    print(json.dumps({"mode": "provider_lookup", **result, "unavailable_sources": unavailable,
                      "unverified_records_by_source": unverified,
                      "report": report(result)}, indent=2))
