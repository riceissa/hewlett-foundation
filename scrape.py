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
                assert d['grantee'].strip(), d['grantee']

                d['url'] = (grant.find("a", {"class": "listing-highlight-link"})
                                 .get("href"))
                assert d['url'].strip(), d['url']

                # There are two cases of bylines: those that link to a cause
                # area and those that don't. In the latter case there is no
                # "hero-eyebrow" class and instead one extra "byline-item".
                hero = grant.find("a", {"class": "hero-eyebrow"})
                byls = grant.find_all("div", {"class": "byline-item"})
                if hero:
                    d['cause_area'] = hero.text
                    d['cause_area_url'] = hero.get("href")
                    d['amount'] = (byls[1].text.strip())
                else:
                    d['cause_area'] = byls[0].text
                    d['amount'] = (byls[2].text.strip())

                assert d['amount'].startswith("$"), (d['amount'], d['grantee'])
                assert d['cause_area'].strip(), d['cause_area']

                awarded = grant.find("time").text
                assert awarded.startswith("Awarded ")
                d['date'] = awarded[len("Awarded "):]

                d['notes'] = (grant.find("div", {"class": "callout-excerpt"})
                                   .text.strip())
                writer.writerow(d)

            page += 1

if __name__ == "__main__":
    main()
