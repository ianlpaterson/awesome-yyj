# YYJ Listing Generator

Regenerates business listing tables on WordPress pages from `awesome-yyj/data/businesses.csv`.
Only sections wrapped in `<!-- YYJ:key_start -->` / `<!-- YYJ:key_end -->` markers are touched.
All other page content (intro, FAQ, tips) is left exactly as-is.

---

## Setup: credentials

The script reads credentials from environment variables. Never hardcode them.

```bash
export WP_USER='your-wordpress-username'
export WP_APP_PASSWORD='xxxx xxxx xxxx xxxx xxxx xxxx'
```

Generate an Application Password at:
`WordPress Admin > Users > Profile > Application Passwords`

---

## Running the script

```bash
# Regenerate all pages that have a non-None page_id
python generate.py

# Regenerate a single page
python generate.py --page where_to_work

# Dry-run: print what would be sent, make no API calls
python generate.py --dry-run
python generate.py --dry-run --page visitors_guide

# List all configured pages and their IDs
python generate.py --list-pages
```

---

## How markers work

Each generated section in a WP page must be wrapped in HTML comment markers
inside a `<!-- wp:html -->` block. Add these to the WP page/post editor
(Code Editor or Custom HTML block) where you want the table to appear:

```html
<!-- wp:html -->
<!-- YYJ:section_key_start -->
<!-- YYJ:section_key_end -->
<!-- /wp:html -->
```

The script replaces everything between the start and end markers on each run.
The markers themselves are preserved.

---

## Adding a new section

1. In the WP page editor, insert a Custom HTML block with markers:

   ```html
   <!-- wp:html -->
   <!-- YYJ:my_new_section_start -->
   <!-- YYJ:my_new_section_end -->
   <!-- /wp:html -->
   ```

2. In `generate.py`, add a section config to the relevant page entry in `PAGES`:

   ```python
   {
       "key": "my_new_section",
       "heading": "My New Heading",
       "categories": ["Category Name"],
       "columns": ["Name", "Address", "Website", "Notes"],
   }
   ```

3. If it is a brand-new WP page, set `page_id` to the integer ID and
   `page_type` to `"post"` or `"page"`.

4. Run `python generate.py --dry-run --page <page_key>` to preview output,
   then run without `--dry-run` to publish.

---

## CSV source of truth

File: `awesome-yyj/data/businesses.csv`

Schema: `Name,Address,Category,Website,Article,Notes,Lat,Lng`

All categories used in `PAGES` must exactly match the `Category` values in the CSV
(case-sensitive).
