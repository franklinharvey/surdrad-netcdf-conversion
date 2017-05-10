import sys
from os.path import basename
import os
from datetime import timedelta, date

def main(filesToProcess):
    start_date = date(1995, 1, 1)
    end_date = date.today()
    for single_date in daterange(start_date, end_date):
        print single_date.strftime("%y%j")

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

if __name__ == '__main__':
    main(sys.argv[1:])


def maybe(files):
    for year in years:
        for month in months:
            for file in files:
                if get_year(file) == year and get_month(file) == month:
