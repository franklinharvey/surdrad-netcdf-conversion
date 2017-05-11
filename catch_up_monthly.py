import os
import glob
import csv_to_nc_monthly as ncm

def main():
    sites = ["bon", "tbl", "dra", "fpk", "gwn", "psu", "sxf"]
    years = ["1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017"]
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    for site in sites:
        for year in years:
            for month in months:
                path = "Data/csv/%s/%s/%s" % (site, year, month)
                a = glob.glob(path + '/*.csv')
                if a:
                    ncm.main(a)
                else:
                    print "Nothing for %s-%s-%s" % (site,year,month)

if __name__ == '__main__':
    main()
