#!/usr/bin/env python3
# License: CC0 https://creativecommons.org/publicdomain/zero/1.0/

import requests
from bs4 import BeautifulSoup
import csv
import re
import sys


def main():
    url = "https://www.hewlett.org/grants/page/{}/"
    page = 1
    first = True
    with open("data.csv", "w", newline="") as f:
        fieldnames = ["grantee", "url", "amount", "date", "cause_area",
                      "cause_area_url", "notes"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        while True:
            print("Doing page", page, file=sys.stderr)
            r = requests.get(url.format(str(page)))
            soup = BeautifulSoup(r.content, "lxml")

            if soup.body.find_all(text=re.compile('Sorry, no content was found')):
                # We have reached the end, so stop
                break

            for grant in soup.find_all("article", {"class": "callout"}):
                d = {}
                d['grantee'] = grant.find("h2").text.strip()
                d['url'] = (grant.find("a", {"class": "listing-highlight-link"})
                                 .get("href"))
                d['amount'] = (grant.find_all("div", {"class": "byline-item"})[1]
                                    .text.strip())
                assert d['amount'].startswith("$"), d['amount']
                awarded = grant.find("time").text
                assert awarded.startswith("Awarded ")
                d['date'] = awarded[len("Awarded "):]
                d['notes'] = (grant.find("div", {"class": "callout-excerpt"})
                                   .text.strip())
                d['cause_area'] = (grant.find("a", {"class": "hero-eyebrow"})
                                        .text)
                d['cause_area_url'] = (grant.find("a", {"class": "hero-eyebrow"})
                                            .get("href"))
                writer.writerow(d)

            page += 1

if __name__ == "__main__":
    main()
