#!/usr/bin/env python3
# License: CC0 https://creativecommons.org/publicdomain/zero/1.0/

import pdb
import requests
from bs4 import BeautifulSoup
import csv
import re
import sys
import datetime
import dateutil.parser
import time


def get_query(year, page):
    url = "https://hewlett.org/wp-admin/admin-ajax.php"
    body = {
            "action": "update_results",
            "engine": "grant",
            "listing_type": "/grants/",
            "keyword": "",
            "sort": "date",
            "current_page": page,
            "years[]": year
            }

    try:
        r = requests.post(url, data=body)
        j = r.json()
    except:
        # Something went wrong, so try downloading again
        print("Downloading or decoding to JSON went wrong; trying again in a few seconds...",
              file=sys.stderr)
        time.sleep(3)
        r = requests.post(url, data=body)
        j = r.json()
    return j


def main():
    if len(sys.argv) != 1+1:
        print("Please give the output file as an argument to the command", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1], "w", newline="") as f:
        fieldnames = ["grantee", "url", "amount", "date", "program", "purpose"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        # The JS interface only shows up to year 2007, but there's data from
        # 2000-2006 that can be queried
        for year in range(2000, datetime.datetime.now().year + 1):
            max_page = 100
            page = 1
            while page <= max_page:
                print("Doing year %s, page %s/%s" % (year, page, max_page), file=sys.stderr)

                j = get_query(year, page)

                page_content = j['articles']['page']
                for item in page_content:
                    result = {}
                    result['url'] = item['url']
                    result['grantee'] = item['sections'][0]
                    result['purpose'] = item['sections'][1]
                    result['date'] = dateutil.parser.parse(item['date']).strftime("%Y-%m-%d")
                    result['amount'] = re.search(r"Amount (\$[0-9,]+)", item['body']).group(1).replace("$", "").replace(",", "")
                    result['program'] = re.search("Amount \\$[0-9,]+ Program (.+) Date Awarded", item['body']).group(1).strip()
                    writer.writerow(result)

                max_page = j['info']['num_pages']

                # The AJAX requester can only go to page 100 (?!) so if we
                # receive a max_page of greater than 100, we're in trouble and
                # need to filter the results even more to get this down too
                # 100.
                assert max_page <= 100

                page += 1


if __name__ == "__main__":
    main()
