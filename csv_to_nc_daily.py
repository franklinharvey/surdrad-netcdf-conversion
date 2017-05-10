"""
This module should accept .csv files and return .nc files.
"""

import sys
from os.path import basename
import os
import nc_convert as ncc

def main(filesToProcess):
    numOfFiles = len(filesToProcess)
    if numOfFiles>1:
        for count,input in enumerate(filesToProcess):
            outName = set_outName(input)
            ncc.normal_process(input, outName)
    else:
        input = filesToProcess[0]
        outName = set_outName(input)
        ncc.normal_process(input, outName)

def set_outName(input):
    '''
    Sets the output name for daily files
    '''
    site = ncc.get_testsite(input)
    year = ncc.get_year(input)
    month = ncc.get_month(input)
    day = ncc.get_day(input)
    return "Data/nc/daily/%s/%s/%s_%s_%s_%s.nc" % (site, year, site, year, month, day)

if __name__ == '__main__':
    main(sys.argv[1:])
