# awesome-yyj

A community-maintained directory of the Victoria BC (YYJ) tech and business scene.

Businesses, coworking spaces, hotels, restaurants, breweries, venues, tech companies, and organizations worth knowing about. Data sourced from [ianlpaterson.com](https://ianlpaterson.com) and maintained collaboratively.

## Featured in

- [Where to Work in Victoria BC](https://ianlpaterson.com/blog/where-to-work-victoria-bc/) - coffee shops and coworking spaces for remote workers and business travellers
- [Victoria BC Executive Visitor's Guide](https://ianlpaterson.com/victoria-bc-executive-visitors-guide/) - hotels, restaurants, breweries, and attractions for visiting executives
- [Guide to Victoria BC's Tech & Startup Community](https://ianlpaterson.com/guide-to-the-tech-startup-community-in-victoria-bc/) - tech companies, coworking, events, and ecosystem overview
- [Getting To & From Victoria BC](https://ianlpaterson.com/getting-to-from-victoria-bc/) - transport operators, ferries, floatplanes, and connections

## Data

The source of truth is [`data/businesses.csv`](data/businesses.csv). Maps and other views are generated from it.

### Schema

| Column | Description |
|--------|-------------|
| `Name` | Business name |
| `Address` | Full street address including city and province |
| `Category` | See categories below |
| `Website` | Domain only (no https://) |
| `Article` | Blog article where this business was featured (optional) |
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
- Website updates
- New categories (open an issue first)

## License

Data is [CC0](https://creativecommons.org/publicdomain/zero/1.0/) - public domain. Do whatever you want with it.
