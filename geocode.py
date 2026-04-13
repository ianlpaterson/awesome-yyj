#!/usr/bin/env python3
"""
Geocode addresses in businesses.csv using Nominatim API.
Adds Lat and Lng columns. Skips rows that already have valid Lat/Lng.
Run: python3 geocode.py
"""

import csv
import json
import time
import urllib.request
import urllib.parse
import sys

CSV_PATH = "/home/ianpaterson/awesome-yyj-list/awesome-yyj/data/businesses.csv"

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "awesome-yyj/1.0 (ianlpaterson.com)"
RATE_LIMIT_SEC = 1.1

FIELDNAMES = ["Name", "Address", "Category", "Website", "Article", "Notes", "Lat", "Lng"]


def geocode(address):
    """Return (lat_str, lng_str) or ('', '') on failure."""
    params = urllib.parse.urlencode({
        "q": address,
        "format": "json",
        "limit": 1,
    })
    url = f"{NOMINATIM_URL}?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        if data:
            lat = f"{float(data[0]['lat']):.6f}"
            lng = f"{float(data[0]['lon']):.6f}"
            return lat, lng
        return "", ""
    except Exception as e:
        print(f"  [ERROR] {e}", file=sys.stderr)
        return "", ""


def main():
    # Read existing CSV
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Ensure Lat/Lng keys exist on every row
    for row in rows:
        row.setdefault("Lat", "")
        row.setdefault("Lng", "")

    total = len(rows)
    geocoded = 0
    skipped = 0
    failed = 0
    needs_geocode = []

    for i, row in enumerate(rows):
        lat = row.get("Lat", "").strip()
        lng = row.get("Lng", "").strip()
        # Skip rows that already have valid float coords
        if lat and lng:
            try:
                float(lat)
                float(lng)
                skipped += 1
                continue
            except ValueError:
                pass
        needs_geocode.append(i)

    print(f"Total rows: {total}")
    print(f"Already geocoded (will skip): {skipped}")
    print(f"To geocode: {len(needs_geocode)}")
    print()

    for count, i in enumerate(needs_geocode, 1):
        row = rows[i]
        name = row.get("Name", "").strip()
        address = row.get("Address", "").strip()

        print(f"Geocoding [{count}/{len(needs_geocode)}] {name}...", end=" ", flush=True)

        if not address:
            print("SKIP (no address)")
            row["Lat"] = ""
            row["Lng"] = ""
            failed += 1
            if count % 10 == 0:
                _write_csv(rows)
            continue

        lat, lng = geocode(address)

        if lat and lng:
            row["Lat"] = lat
            row["Lng"] = lng
            geocoded += 1
            print(f"{lat}, {lng}")
        else:
            row["Lat"] = ""
            row["Lng"] = ""
            print(f"FAILED")
            failed += 1

        # Checkpoint every 10 requests
        if count % 10 == 0:
            _write_csv(rows)
            print(f"  [checkpoint saved at {count}/{len(needs_geocode)}]")

        if count < len(needs_geocode):
            time.sleep(RATE_LIMIT_SEC)

    # Final write
    _write_csv(rows)

    print()
    print("=" * 50)
    print(f"Done.")
    print(f"  Successfully geocoded: {geocoded}")
    print(f"  Failed / no result:    {failed}")
    print(f"  Already had coords:    {skipped}")
    print(f"  Total rows:            {total}")
    print(f"  CSV written to:        {CSV_PATH}")


def _write_csv(rows):
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
