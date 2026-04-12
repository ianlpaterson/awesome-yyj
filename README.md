# awesome-yyj

A community-maintained directory of the Victoria BC (YYJ) tech and business scene.

Businesses, coworking spaces, hotels, restaurants, breweries, venues, tech companies, and organizations worth knowing about.

## Data

The source of truth is [`data/businesses.csv`](data/businesses.csv). Maps and other views are generated from it.

### Schema

| Column | Description |
|--------|-------------|
| `Name` | Business name |
| `Address` | Full street address including city and province |
| `Category` | See categories below |
| `Website` | Domain only (no https://) |
| `Email` | Primary contact email |
| `Article` | ILP blog article where this business was featured (optional) |
| `In Outreach CSV` | Yes/No - internal tracking field |
| `Notes` | Anything useful: ownership, quirks, sub-venues |

### Categories

- `Attraction`
- `Bar`
- `Bar / Private Club`
- `Brewery`
- `Coffee Shop`
- `Community Event Venue`
- `Conference Venue`
- `Coworking`
- `Coworking / Indigenous Tech`
- `Coworking / Tech Hub`
- `Hotel`
- `Landmark`
- `Restaurant - Casual`
- `Restaurant - Upscale`
- `Tech Company`
- `Tech Organization`

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

PRs welcome for:
- New businesses
- Address corrections
- Email/website updates
- New categories (open an issue first)

## License

Data is [CC0](https://creativecommons.org/publicdomain/zero/1.0/) - public domain. Do whatever you want with it.
