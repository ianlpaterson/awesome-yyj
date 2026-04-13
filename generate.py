#!/usr/bin/env python3
"""
generate.py - Regenerate YYJ business listing tables on WordPress pages.

Reads businesses.csv and updates HTML table sections in WP pages/posts
via the WP REST API. Only sections wrapped in YYJ marker comments are
touched; narrative content is left intact.

Usage:
    python generate.py                      # regenerate all pages with a non-None page_id
    python generate.py --page where_to_work # regenerate one page
    python generate.py --dry-run            # print what would be sent, no API calls
    python generate.py --list-pages         # show all configured pages and their IDs
"""

import argparse
import base64
import csv
import json
import os
import re
import sys
import urllib.request
from urllib.error import HTTPError, URLError

# ---------------------------------------------------------------------------
# Page / section configuration
# ---------------------------------------------------------------------------

PAGES = {
    "where_to_work": {
        "page_id": 2000,
        "page_type": "post",
        "sections": [
            {
                "key": "coworking",
                "heading": "Victoria Coworking Spaces",
                "emit_heading": False,  # Page already has narrative H2 "Victoria's 10 Best Coworking Spaces"
                "categories": ["Coworking", "Coworking / Tech Hub", "Coworking / Indigenous Tech"],
                "columns": ["Name", "Address", "Website", "Notes"],
            },
            {
                "key": "coffee",
                "heading": "Best Coffee Shops for Working",
                "emit_heading": False,  # Page already has narrative H2 "Best Coffee Shops for Working in Victoria BC"
                "categories": ["Coffee Shop"],
                "columns": ["Name", "Address", "Website", "Notes"],
            },
        ],
    },
    "visitors_guide": {
        "page_id": 2130,
        "page_type": "page",
        "sections": [
            {
                "key": "hotels",
                "heading": "Hotels",
                "categories": ["Hotel"],
                "columns": ["Name", "Address", "Website", "Notes"],
            },
            {
                "key": "restaurants_upscale",
                "heading": "Business Dining",
                "categories": ["Restaurant - Upscale"],
                "columns": ["Name", "Address", "Website", "Notes"],
            },
            {
                "key": "restaurants_casual",
                "heading": "Casual Dining",
                "categories": ["Restaurant - Casual"],
                "columns": ["Name", "Address", "Website", "Notes"],
            },
            {
                "key": "breweries",
                "heading": "Breweries & Bars",
                "emit_heading": False,  # Page already has narrative wp:heading "Breweries & Bars"
                "categories": ["Brewery", "Bar", "Bar / Private Club"],
                "columns": ["Name", "Address", "Website", "Notes"],
            },
            {
                "key": "attractions",
                "heading": "Attractions & Landmarks",
                "categories": ["Attraction", "Landmark"],
                "columns": ["Name", "Address", "Website", "Notes"],
            },
        ],
    },
    "tech_community": {
        "page_id": 1565,
        "page_type": "page",
        "sections": [
            {
                "key": "tech_companies",
                "heading": "Victoria Tech Companies",
                "categories": ["Tech Company", "Game Studio", "Tech Organization"],
                "columns": ["Name", "Address", "Website", "Notes"],
            },
        ],
    },
    "getting_to_from": {
        "page_id": 1575,
        "page_type": "page",
        "sections": [
            {
                "key": "transport",
                "heading": "Transport Operators",
                "categories": ["Transport Operator"],
                "columns": ["Name", "Address", "Website", "Notes"],
            },
        ],
    },
}

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

WP_BASE_URL = "https://ianlpaterson.com/wp-json/wp/v2"
CSV_PATH = os.path.join(os.path.dirname(__file__), "awesome-yyj", "data", "businesses.csv")

# ---------------------------------------------------------------------------
# CSV loading
# ---------------------------------------------------------------------------

def load_businesses(csv_path: str) -> list[dict]:
    """Load all rows from the businesses CSV."""
    businesses = []
    with open(csv_path, newline="", encoding="utf-8", errors="replace") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            # Normalise whitespace in every field
            businesses.append({k: (v.strip() if v else "") for k, v in row.items()})
    return businesses


def filter_businesses(businesses: list[dict], categories: list[str]) -> list[dict]:
    """Return rows whose Category matches any of the given categories (case-sensitive)."""
    return [b for b in businesses if b.get("Category", "") in categories]

# ---------------------------------------------------------------------------
# HTML table rendering
# ---------------------------------------------------------------------------

def _website_url(raw: str) -> str:
    """Ensure URL has a scheme."""
    raw = raw.strip()
    if not raw:
        return ""
    if raw.startswith("http://") or raw.startswith("https://"):
        return raw
    return "https://" + raw


def render_table(rows: list[dict], columns: list[str], heading: str, emit_heading: bool = True) -> str:
    """Render an optional section heading + HTML table from a list of business dicts.

    Set emit_heading=False when the WP page already has a narrative H2 immediately
    before the YYJ marker block, to avoid a duplicate heading pair.
    """
    # Sort A-Z by Name
    rows = sorted(rows, key=lambda r: r.get("Name", "").lower())

    # Skip rows where all configured columns are empty
    rows = [
        r for r in rows
        if any(r.get(col, "").strip() for col in columns)
    ]

    lines = []
    if emit_heading:
        lines.append(f'<h2>{heading}</h2>')
    lines.append('<table class="yyj-listing-table">')
    lines.append("  <thead>")
    lines.append("    <tr>")
    for col in columns:
        lines.append(f"      <th>{col}</th>")
    lines.append("    </tr>")
    lines.append("  </thead>")
    lines.append("  <tbody>")

    for row in rows:
        website_raw = row.get("Website", "").strip()
        website_url = _website_url(website_raw)

        lines.append("    <tr>")
        for col in columns:
            value = row.get(col, "").strip()
            if col == "Website":
                if website_url:
                    cell = (
                        f'<a href="{website_url}" target="_blank" rel="noopener">'
                        f"{website_raw}</a>"
                    )
                else:
                    cell = ""
            elif col == "Name":
                if website_url:
                    cell = (
                        f'<a href="{website_url}" target="_blank" rel="noopener">'
                        f"{value}</a>"
                    )
                else:
                    cell = value
            else:
                cell = value
            lines.append(f"      <td>{cell}</td>")
        lines.append("    </tr>")

    lines.append("  </tbody>")
    lines.append("</table>")
    return "\n".join(lines)

# ---------------------------------------------------------------------------
# Marker injection
# ---------------------------------------------------------------------------

def make_block(key: str, inner_html: str) -> str:
    """Wrap inner HTML in a wp:html block with YYJ markers."""
    return (
        "<!-- wp:html -->\n"
        f"<!-- YYJ:{key}_start -->\n"
        f"{inner_html}\n"
        f"<!-- YYJ:{key}_end -->\n"
        "<!-- /wp:html -->"
    )


def inject_section(content: str, key: str, inner_html: str) -> tuple[str, bool]:
    """
    Replace content between YYJ markers for a given key.
    Returns (updated_content, was_found).
    WP sometimes stores HTML comments with a backslash before the bang
    inside block content; this function matches both variants.
    """
    # Match both <!-- and <\!-- (WP-escaped) comment forms
    start_pat = r"<\\?!-- YYJ:" + re.escape(key) + r"_start -->"
    end_pat   = r"<\\?!-- YYJ:" + re.escape(key) + r"_end -->"

    pattern = re.compile(start_pat + r".*?" + end_pat, re.DOTALL)

    # Always write back using standard <!-- form
    start_marker = f"<!-- YYJ:{key}_start -->"
    end_marker   = f"<!-- YYJ:{key}_end -->"
    new_block = f"{start_marker}\n{inner_html}\n{end_marker}"
    updated, count = pattern.subn(new_block, content)
    return updated, count > 0

# ---------------------------------------------------------------------------
# WP REST API
# ---------------------------------------------------------------------------

def _auth_header(user: str, password: str) -> str:
    token = base64.b64encode(f"{user}:{password}".encode()).decode()
    return f"Basic {token}"


def wp_get_content(page_id: int, page_type: str, auth: str) -> str:
    """Fetch raw post/page content from WP REST API."""
    endpoint = "posts" if page_type == "post" else "pages"
    url = f"{WP_BASE_URL}/{endpoint}/{page_id}?context=edit"
    req = urllib.request.Request(url, headers={"Authorization": auth})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            return data["content"]["raw"]
    except HTTPError as exc:
        body = exc.read().decode(errors="replace")
        print(f"  ERROR: GET {url} returned {exc.code}: {body}", file=sys.stderr)
        raise
    except URLError as exc:
        print(f"  ERROR: GET {url} failed: {exc.reason}", file=sys.stderr)
        raise


def wp_update_content(page_id: int, page_type: str, auth: str, content: str) -> None:
    """Push updated content back to WP REST API."""
    endpoint = "posts" if page_type == "post" else "pages"
    url = f"{WP_BASE_URL}/{endpoint}/{page_id}"
    payload = json.dumps({"content": content}).encode()
    req = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={
            "Authorization": auth,
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            status = resp.status
            if status not in (200, 201):
                body = resp.read().decode(errors="replace")
                print(f"  WARNING: POST {url} returned {status}: {body}", file=sys.stderr)
            else:
                print(f"  Updated page_id={page_id} ({page_type}), HTTP {status}.")
    except HTTPError as exc:
        body = exc.read().decode(errors="replace")
        print(f"  ERROR: POST {url} returned {exc.code}: {body}", file=sys.stderr)
        raise

# ---------------------------------------------------------------------------
# Core processing
# ---------------------------------------------------------------------------

def process_page(
    page_name: str,
    page_cfg: dict,
    businesses: list[dict],
    auth: str,
    dry_run: bool,
) -> None:
    page_id = page_cfg["page_id"]
    page_type = page_cfg["page_type"]
    sections = page_cfg["sections"]

    if page_id is None:
        print(f"[SKIP] {page_name}: page_id is None (not yet created in WP).")
        return

    print(f"[{page_name}] page_id={page_id} ({page_type})")

    if dry_run:
        print("  (dry-run: skipping WP fetch)")
        content = ""
        # In dry-run mode we still render the tables and show them
        for section in sections:
            rows = filter_businesses(businesses, section["categories"])
            emit_h = section.get("emit_heading", True)
            table_html = render_table(rows, section["columns"], section["heading"], emit_heading=emit_h)
            print(f"\n  --- Section: {section['key']} ({len(rows)} rows) ---")
            print(make_block(section["key"], table_html))
        print()
        return

    # Fetch current content
    try:
        content = wp_get_content(page_id, page_type, auth)
    except Exception:
        print(f"  Skipping {page_name} due to fetch error.")
        return

    any_updated = False
    for section in sections:
        key = section["key"]
        rows = filter_businesses(businesses, section["categories"])
        emit_h = section.get("emit_heading", True)
        table_html = render_table(rows, section["columns"], section["heading"], emit_heading=emit_h)

        content, found = inject_section(content, key, table_html)
        if found:
            print(f"  Section '{key}': {len(rows)} rows injected.")
            any_updated = True
        else:
            print(
                f"  WARNING: marker '<!-- YYJ:{key}_start -->' not found in page {page_id}. "
                f"Skipping section '{key}'."
            )

    if any_updated:
        wp_update_content(page_id, page_type, auth, content)
    else:
        print(f"  No sections updated for {page_name}.")
    print()

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_list_pages() -> None:
    print(f"{'Page key':<25} {'page_id':<10} {'type':<6}  sections")
    print("-" * 70)
    for name, cfg in PAGES.items():
        section_keys = ", ".join(s["key"] for s in cfg["sections"])
        pid = str(cfg["page_id"]) if cfg["page_id"] is not None else "None"
        print(f"{name:<25} {pid:<10} {cfg['page_type']:<6}  {section_keys}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Regenerate YYJ business listing tables on WordPress pages."
    )
    parser.add_argument(
        "--page",
        metavar="PAGE_KEY",
        help="Regenerate a single page by its key in PAGES.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be sent without making any API calls.",
    )
    parser.add_argument(
        "--list-pages",
        action="store_true",
        help="List all configured pages and their IDs, then exit.",
    )
    args = parser.parse_args()

    if args.list_pages:
        cmd_list_pages()
        return

    # Load credentials - env vars take precedence, .netrc is the fallback
    wp_user = os.environ.get("WP_USER")
    wp_pass = os.environ.get("WP_APP_PASSWORD")
    if not wp_user or not wp_pass:
        try:
            import netrc as _netrc
            _auth = _netrc.netrc().authenticators("ianlpaterson.com")
            if _auth:
                wp_user = wp_user or _auth[0]
                wp_pass = wp_pass or _auth[2]
        except Exception:
            pass
    if not wp_user or not wp_pass:
        print(
            "ERROR: WP credentials not found.\n"
            "  Option 1: export WP_USER='admin' WP_APP_PASSWORD='xxxx xxxx xxxx xxxx'\n"
            "  Option 2: add 'machine ianlpaterson.com login admin password xxxx' to ~/.netrc",
            file=sys.stderr,
        )
        sys.exit(1)

    auth = _auth_header(wp_user, wp_pass)

    # Load CSV
    if not os.path.exists(CSV_PATH):
        print(f"ERROR: CSV not found at {CSV_PATH}", file=sys.stderr)
        sys.exit(1)
    businesses = load_businesses(CSV_PATH)
    print(f"Loaded {len(businesses)} businesses from {CSV_PATH}\n")

    # Determine which pages to process
    if args.page:
        if args.page not in PAGES:
            print(
                f"ERROR: '{args.page}' is not a known page key. "
                f"Known keys: {', '.join(PAGES)}",
                file=sys.stderr,
            )
            sys.exit(1)
        pages_to_run = {args.page: PAGES[args.page]}
    else:
        pages_to_run = {k: v for k, v in PAGES.items() if v["page_id"] is not None}
        if not pages_to_run:
            print("No pages with a non-None page_id found. Set page_id values in PAGES dict.")
            return

    for page_name, page_cfg in pages_to_run.items():
        process_page(page_name, page_cfg, businesses, auth, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
