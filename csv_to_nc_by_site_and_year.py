'''
This module takes 1 argument. It should be used to convert one single file.
The argument should be formatted "sss##".

For example, for converting Bondville_IL in 1995, you'd call "python, csv_to_nc_by_site_and_year.py bon95"
'''

import sys
import os

def main(selection):
    call = "python csv_to_nc.py Data/csv/%s*.csv" % (selection)
    os.system(call)

if __name__ == '__main__':
    main(sys.argv[1])
