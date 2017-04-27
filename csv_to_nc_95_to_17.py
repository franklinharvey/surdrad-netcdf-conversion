import os
import time

def main():
    years = ["95","96","97","98","99","00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17"]
    sites = ["bon","tbl","dra","fpk","gwn","psu","sxf"]
    for site in sites:
        if site == "dra" or site == "psu":
            for year in years[3:]:
                now = time.time()
                call = "python csv_to_nc.py Data/csv/%s%s*.csv" % (site,year)
                os.system(call)
                print time.time() - now
        elif site == "sfk":
            for year in years[8:]:
                now = time.time()
                call = "python csv_to_nc.py Data/csv/%s%s*.csv" % (site,year)
                os.system(call)
                print time.time() - now
        else:
            for year in years:
                now = time.time()
                call = "python csv_to_nc.py Data/csv/%s%s*.csv" % (site,year)
                os.system(call)
                print time.time() - now

if __name__ == '__main__':
    main()
