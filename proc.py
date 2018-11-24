#!/usr/bin/env python3
# License: CC0 https://creativecommons.org/publicdomain/zero/1.0/

import csv
import datetime
import sys

## Maps Hewlett Foundation's cause area terminology to Donations List Website's

CAUSE_AREAS = {
    "Education" : "Education",
    "Environment" : "Environmentalism",
    "Population" : "Population",
    "Global Development and Population" : "Population",
    "Performing Arts" : "Art/performing arts",
    "Cyber" : "Science and Technology/Cyber",
    "Madison Initiative" : "Politics",
    "Effective Philanthropy" : "Effective altruism",
    "Philanthropy" : "Effective altruism",
    "SF Bay Area" : "SF Bay Area",
    "Special Projects" : "Special Projects",
    "Initiatives" : "Initiatives",
    "Global Development" : "Global development"
}

def mysql_quote(x):
    '''
    Quote the string x using MySQL quoting rules. If x is the empty string,
    return "NULL". Probably not safe against maliciously formed strings, but
    whatever; our input is fixed and from a basically trustable source..
    '''
    if not x:
        return "NULL"
    x = x.replace("\\", "\\\\")
    x = x.replace("'", "''")
    x = x.replace("\n", "\\n")
    return "'{}'".format(x)

def main():
    if len(sys.argv) != 1+1:
        print("Please give the input CSV file as an argument to the command", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1], "r") as f:
        reader = csv.DictReader(f)

        first = True

        print("""insert into donations (donor, donee, amount, donation_date,
        donation_date_precision, donation_date_basis, cause_area, url,
        donor_cause_area_url, notes, affected_countries,
        affected_regions) values""")

        for row in reader:

            amount = int(row['amount'])
            donation_date = row['date']

            cause_area = row['program']
            if cause_area in CAUSE_AREAS:
                cause_area = CAUSE_AREAS[cause_area]
            print(("    " if first else "    ,") + "(" + ",".join([
                mysql_quote("Hewlett Foundation"),  # donor
                mysql_quote(row['grantee']),  # donee
                str(amount),  # amount
                mysql_quote(donation_date),  # donation_date
                mysql_quote("day"),  # donation_date_precision
                mysql_quote("donation log"),  # donation_date_basis
                mysql_quote(cause_area),  # cause_area
                mysql_quote("https://www.hewlett.org/grants/"),  # url
                mysql_quote(""),  # donor_cause_area_url
                mysql_quote(row['purpose']),  # notes
                # FIXME these are only listed on each grant page, and there are
                # a HUGE number of grant pages
                mysql_quote(""),  # affected_countries
                mysql_quote(""),  # affected_regions
            ]) + ")")
            first = False
        print(";")

if __name__ == "__main__":
    main()
