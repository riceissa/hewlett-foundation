# Hewlett Foundation

This repo is for work on Vipul Naik's [Donations List Website](https://github.com/vipulnaik/donations).

The issue that started this repo is: https://github.com/vipulnaik/donations/issues/7

For the data source, see https://www.hewlett.org/grants/

## How to use the scripts


```bash
# Get today's date
today=$(date -Idate)

# Get new data; this takes maybe 30 minutes
./scrape.py data-$today.csv

# Convert CSV to SQL
./proc.py data-$today.csv > out-$today.sql
```

There is also `proc_legacy.py`; for that, you need to run it like:

```bash
./proc.py > out.sql  # input CSV in data.csv
```

## License

CC0 for the scripts, not sure about data.
