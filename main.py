import argparse
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

CATEGORIES = ("permit", "zoning", "tax", "flood", "violation", "school")

def dossier(request):
    subject = request["subject"].strip().casefold()
    if not subject:
        raise ValueError("Provide a non-empty address or parcel ID")
    parcels = {row["parcel_id"]: row for row in request["parcels"]
               if subject in {row["parcel_id"].strip().casefold(), row["address"].strip().casefold()}}
    if len(parcels) != 1:
        return {"status": "ambiguous" if parcels else "no_match", "parcels": list(parcels.values())}
    parcel = next(iter(parcels.values()))
    groups = {category: [] for category in CATEGORIES}
    sources = set()
    excluded = 0
    for row in request["records"]:
        if row.get("parcel_id") != parcel["parcel_id"]:
            excluded += 1
            continue
        url = urlsplit(row["source_url"])
        if url.scheme != "https" or url.hostname not in request["official_hosts"] or url.username or url.password:
            raise ValueError("Record source must belong to the official source configuration")
        date.fromisoformat(row["checked_date"])
        groups[row["category"]].append(row)
        sources.add(url.hostname)
    missing = [category for category, values in groups.items() if not values]
    previous = set(request.get("previous_permit_ids", []))
    permits = [row for row in groups["permit"] if row.get("record_id") and row["record_id"] not in previous]
    return {"status": "partial" if missing or len(sources) < 3 else "complete", "parcel": parcel,
            "records": groups, "missing": missing, "official_source_count": len(sources),
            "excluded_other_parcel": excluded, "new_permits": permits if "previous_permit_ids" in request else None}

def report(result):
    if "parcel" not in result:
        return f"Parcel lookup: {result['status']}"
    lines = [f"{result['parcel']['address']} ({result['parcel']['parcel_id']})", f"Coverage: {result['status']}"]
    for category, rows in result["records"].items():
        lines.append(category.title())
        lines.extend(f"  {row['summary']} ({row['source_url']})" for row in rows)
        if not rows:
            lines.append("  No sourced record supplied.")
    return "\n".join(lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--report", action="store_true")
    args = parser.parse_args()
    result = dossier(json.loads(args.input.read_text(encoding="utf-8")))
    print("Offline input\n" + report(result) if args.report else json.dumps({"mode": "offline_input", **result}, indent=2))
