# Hewlett Foundation

This repo is for work on Vipul Naik's [Donations List Website](https://github.com/vipulnaik/donations).

The issue that started this repo is: https://github.com/vipulnaik/donations/issues/7

For the data source, see https://www.hewlett.org/grants/

Scripts:

- `scrape.py`: scrapes grants info and puts it in `data.csv`. Scraping takes
  about 30 minutes.
- `proc.py`: uses `data.csv` to print a SQL insert file that can be used with
  the donations list website.

## License

CC0 for the scripts, not sure about data.
