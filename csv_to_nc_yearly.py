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
        outName = set_outName(filesToProcess[0])
        ncc.normal_process(filesToProcess, outName)
    else:
        print "Not enough files!"

def set_outName(input):
    '''
    Sets the output name for yearly files
    '''
    site = ncc.get_testsite(input)
    year = ncc.get_year(input)
    return "Data/nc/yearly/%s/%s_%s.nc" % (site, site, year)

if __name__ == '__main__':
    main(sys.argv[1:])
