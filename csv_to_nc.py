"""
This module should accept .csv files and return .nc files.
"""

import sys
from os.path import basename
import os
import pandas as pd
import xarray as xr

def main(filesToProcess):
    numOfFiles = len(filesToProcess)
    if numOfFiles>1:
        outName = get_out_name(filesToProcess[0])
        for count,input in enumerate(filesToProcess):
            filename = get_filename(input)
            print "Processing %s -- %i out of %i" % (filename,count+1,numOfFiles)
            df1 = csv_to_dataframe(input)
            df1 = filter_qc(df1)
            df1 = format_headers(df1)
            df1 = replace_nan(df1)
            if count == 0:
                df2 = df1
                del df1
            else:
                df2 = pd.concat([df2, df1])
                del df1
        write_netcdf(df2, outName)
    else:
        input = filesToProcess[0]
        filename = get_filename(input)
        print "Processing %s" % (filename)
        input = filesToProcess[0]
        df1 = csv_to_dataframe(input)
        df1 = filter_qc(df1)
        df1 = format_headers(df1)
        df1 = replace_nan(df1)
        write_netcdf(df1, filename)

def get_out_name(input):
    return "%s_%s" % (get_testsite(input),get_year(input))

def get_year(input):
    return get_filename(input)[3:5]

def get_julian_day(input):
    return get_filename(input)[5:8]

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

def replace_nan(df1):
    '''
    The value "-9999.9" is specified to be a placeholder for non-existent values. This replaces those values with "NaN"
    '''
    df1.replace(to_replace="-9999.9",value="NaN", inplace=True)
    return df1

def format_headers(df1):
    '''
    Deletes white space and extra quotes from headers. Often necessary for the NetCDF writer
    '''
    df1.columns = [s.strip(' ') for s in list(df1)]
    df1.columns = [s.strip('\"') for s in list(df1)]
    return df1

def filter_qc(df1):
    '''
    Drops all the qc columns
    '''
    df1.drop(list(df1.filter(like="qc")), axis=1, inplace=True)
    df1.drop(df1.columns[[0,1,2]], axis=1, inplace=True)
    return df1

def write_netcdf(df1, name):
    '''
    Writes the dataframe into a NetCDF4 file
    '''
    xds = xr.Dataset.from_dataframe(df1)
    xds.to_netcdf("Data/nc/" + name + ".nc")

def csv_to_dataframe(input):
    '''
    Loads a csv into a Pandas dataframe.
    Uses the Year, Julian Day, Hour, and Minute to create an index column of "Date".
    Adds the test site as a column
    '''
    with open(input, 'r') as input_file:
        df1=pd.read_csv(input_file,
            sep=",",
            parse_dates = {'Date': [0,1,4,5]},
            date_parser = lambda x: pd.to_datetime(x, format="%Y %j %H %M"),
            index_col = ['Date'])
        df1.loc[:,'TestSite'] = get_testsite(input)
    return df1

if __name__ == '__main__':
    main(sys.argv[1:])
