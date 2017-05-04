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
        outName = get_out_name(filesToProcess[0]) + "_to_" + get_year(filesToProcess[-1])
        ncc.normal_process(filesToProcess,'testsite',outName)
    else:
        print "You did not pass multiple files."

def get_out_name(input):
    '''
    Returns testsite_year
    For example, Bondville_IL_95
    '''
    return "%s_%s" % (get_testsite(input),get_year(input))

def get_year(input):
    '''
    Returns the year of the file
    For example, bon95001.csv returns 95
    '''
    return get_filename(input)[3:5]

def get_filename(input):
    '''
    Returns the name of the file without the extension.
    For example:

    Input: "Test_01.csv"
    Output: "Test_01"
    '''
    return os.path.splitext(basename(input))[0]

def get_testsite(input):
    '''
    Grabs the initials from the filename and returns the full name of the test site
    '''
    base = get_filename(input)
    testsite = base[0:3]
    if testsite == "bon":
        return "Bondville_IL"
    elif testsite == "tbl":
        return "Boulder_CO"
    elif testsite == "dra":
        return "Desert_Rock_NV"
    elif testsite == "fpk":
        return "Fort_Peck_MT"
    elif testsite == "gwn":
        return "Goodwin_Creek_MS"
    elif testsite == "psu":
        return "Penn_State_PA"
    elif testsite == "sxf":
        return "Sioux_Falls_SD"
    else:
        print "no matching testing site for input file"
        return "no_test_site"

if __name__ == '__main__':
    main(sys.argv[1:])
