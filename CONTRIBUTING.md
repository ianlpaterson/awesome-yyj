# Contributing to awesome-yyj

## Adding or updating a business

1. Fork the repo
2. Edit `data/businesses.csv`
3. Open a PR with a short description of what you added/changed

## PR checklist

- [ ] Address includes full street address, city, and province (e.g. `123 Fort St Victoria BC V8V 3K3`)
- [ ] Website is domain only - no `https://` prefix (e.g. `example.com` not `https://example.com`)
- [ ] Category matches an existing value from the schema (open an issue to propose a new one)
- [ ] No duplicate entries - search the CSV for the business name before adding
- [ ] Notes column used for anything non-obvious (ownership changes, sub-venues, seasonal closures)

## Address quality matters

Precise addresses make the maps work. Tips:

- Include postal code when you have it
- For businesses inside other buildings, use the building address (e.g. `810 Humboldt St Suite A02 Victoria BC`)
- For businesses outside downtown Victoria, add a note (e.g. `Saanich - outside downtown`)

## Suggesting a new category

Open an issue. Categories should be broad enough to be useful as a map filter but specific enough to be meaningful.

## Data license

By contributing, you agree your additions are released under [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
