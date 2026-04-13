# Leaflet Map Embeds for YYJ Business Directory

Self-contained HTML snippets that render interactive Leaflet.js maps on WordPress pages.
No build step. No server-side code. No API keys.

---

## Files

| File | Purpose |
|------|---------|
| `leaflet-map-template.html` | Master template. Edit and paste into WP. |
| `leaflet-examples/hotels-map.html` | Hotels |
| `leaflet-examples/coworking-map.html` | Coworking spaces (3 category variants) |
| `leaflet-examples/coffee-map.html` | Coffee shops |
| `leaflet-examples/restaurants-map.html` | Restaurants (Upscale + Casual) |
| `leaflet-examples/breweries-map.html` | Breweries, Bars, Private Clubs |
| `leaflet-examples/attractions-map.html` | Attractions + Landmarks |

---

## How to use the template

1. Open `leaflet-map-template.html` in a text editor.
2. Edit `MAP_CONFIG` at the top of the file:

```js
const MAP_CONFIG = {
  categories: ["Hotel"],          // which categories to show
  center: [48.4284, -123.3656],   // map center [lat, lng]
  zoom: 13,                       // zoom level
  height: "450px",                // map height
  csvUrl: "https://raw.githubusercontent.com/ianlpaterson/awesome-yyj/main/data/businesses.csv",
};
```

3. Copy the entire file content.
4. Paste into a WordPress HTML block (see below).

---

## Changing categories

Edit the `categories` array in `MAP_CONFIG`. Values must match the `Category` column in the CSV exactly (case-insensitive matching is applied at runtime, but it is best to match case for clarity).

Single category:
```js
categories: ["Coffee Shop"],
```

Multiple categories:
```js
categories: ["Brewery", "Bar", "Bar / Private Club"],
```

To find all available category values, open the CSV at:
`https://raw.githubusercontent.com/ianlpaterson/awesome-yyj/main/data/businesses.csv`
and look at the Category column.

---

## Lat/Lng requirement

The map plots markers from the `Lat` and `Lng` columns of the CSV. If those columns are absent or empty for a row, that business is silently skipped. The map still renders - it just shows no markers.

To add coordinates: add `Lat` and `Lng` columns to `businesses.csv` and populate them. The snippet requires no changes.

---

## Pasting into a WordPress HTML block

1. In the WordPress block editor, click the "+" to add a block.
2. Search for "HTML" and select the "Custom HTML" block.
3. Paste the full snippet (everything from the opening comment to the closing `</script>` tag) into the block.
4. Switch to Preview to verify the map loads.
5. Publish or Update the page.

**Note:** WordPress's visual editor sometimes strips or escapes HTML if you accidentally switch from Code view to Visual/Preview and back. Always edit map embeds in the HTML/Code view of the Custom HTML block, never in the visual editor.

---

## Multiple maps on one page

Paste multiple copies of the snippet into separate HTML blocks on the same page. Each copy generates a random unique ID at runtime, so there are no conflicts between maps. Each can have different `MAP_CONFIG` settings.

---

## Customizing the map appearance

All visual styles are in the `<style>` block near the top of the snippet. Class names are prefixed `.yyj-map-wrap` to avoid conflicts with WP theme styles.

Key classes:
- `.yyj-popup-name` - business name in popup
- `.yyj-popup-address` - address line
- `.yyj-popup-website` - website link
- `.yyj-popup-notes` - notes (smaller, italic)
- `.yyj-map-error` - error banner (yellow, shown if CSV fails to load)

---

## Tile layer and attribution

Uses OpenStreetMap tiles (free, no API key). Attribution is rendered automatically by Leaflet as required by OSM terms.

---

## CDN versions

Leaflet 1.9.4 from unpkg.com with SRI integrity hashes. To upgrade: update the version in both the `<link>` and `<script>` tags and update the integrity hashes (get them from https://unpkg.com/leaflet).
