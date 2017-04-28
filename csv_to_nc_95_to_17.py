'''
This module takes no arguments. It should be used to convert backlogged data.
This can be updated by appending new years to the years array.
'''

import os
import time

def main():
    years = ["95","96","97","98","99","00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17"]
    # the years to be converted
    sites = ["bon","tbl","dra","fpk","gwn","psu","sxf"]
    # the sites to be converted, as found in file names
    for site in sites:
        if site == "dra" or site == "psu":
            # these two sites only date back to 1998
            for year in years[3:]:
                call = "python csv_to_nc.py Data/csv/%s%s*.csv" % (site,year)
                os.system(call)
        elif site == "sfk":
            # this site only dates back to 2003
            for year in years[8:]:
                call = "python csv_to_nc.py Data/csv/%s%s*.csv" % (site,year)
                os.system(call)
        else:
            # all other sites date back to 1993
            for year in years:
                call = "python csv_to_nc.py Data/csv/%s%s*.csv" % (site,year)
                os.system(call)

if __name__ == '__main__':
    main()
