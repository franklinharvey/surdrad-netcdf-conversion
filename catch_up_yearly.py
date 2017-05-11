import os
import fnmatch
import csv_to_nc_yearly as ncy

def main():
    sites = ["bon", "tbl", "dra", "fpk", "gwn", "psu", "sxf"]
    years = ["1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017"]

    for site in sites:
        for year in years:
            path = "Data/csv/%s/%s" % (site, year)
            a = [os.path.join(dirpath, f)
                for dirpath, dirnames, files in os.walk(path)
                for f in files if f.endswith('.csv')]
            if a:
                ncy.main(a)
            else:
                print "Nothing for %s-%s" % (site,year)

if __name__ == '__main__':
    main()
