import os
import fnmatch
import csv_to_nc_testsite as nct

def main():
    sites = ["bon", "tbl", "dra", "fpk", "gwn", "psu", "sxf"]

    for site in sites:
        path = "Data/csv/%s" % (site)
        a = [os.path.join(dirpath, f)
            for dirpath, dirnames, files in os.walk(path)
            for f in files if f.endswith('.csv')]
        if a:
            nct.main(a)

if __name__ == '__main__':
    main()
