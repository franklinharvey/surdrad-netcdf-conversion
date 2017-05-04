from os.path import basename
import os
import pandas as pd
import xarray as xr

def normal_process(input,delta,outName,filterQC = False):
    '''
    Does all the filtering and converting done in a standard process.

    Essentially a 'main' function
    '''
    if not delta:
        print "No Time Delta specified. Please indicate 'daily', 'yearly', or 'testsite'"
        return

    if delta == 'daily':
        df1 = csv_to_dataframe(input)
        if filterQC:
            df1 = filter_qc(df1)
        df1 = filter_dates(df1)
        df1 = set_headers(df1)
        df1 = replace_nan(df1)
        write_netcdf(df1, outName)

    elif delta == 'yearly' or delta == 'testsite':
        for count,day in enumerate(input):
            print get_filename(day)
            df1 = csv_to_dataframe(day)
            if filterQC:
                df1 = filter_qc(df1)
            df1 = filter_dates(df1)
            df1 = set_headers(df1)
            df1 = replace_nan(df1)
            if count == 0:
                df2 = df1
                del df1
            else:
                df2 = pd.concat([df2, df1])
                del df1
        write_netcdf(df2, outName)

    else:
        print "Time Delta not recognized. Please indicate 'daily', 'yearly', or 'testsite'"
        return

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

def get_filename(input):
    '''
    Returns the name of the file without the extension.
    For example:

    Input: "Test_01.csv"
    Output: "Test_01"
    '''
    return os.path.splitext(basename(input))[0]

def replace_nan(df1):
    '''
    The value "-9999.9" is specified to be a placeholder for non-existent values. This replaces those values with "NaN"
    '''
    df1.replace(to_replace="-9999.9",value="NaN", inplace=True)
    return df1

def filter_qc(df1):
    '''
    Drops all the qc columns
    '''
    df1.drop(list(df1.filter(like="qc")), axis=1, inplace=True)
    return df1

def filter_dates(df1):
    '''
    Drops extra date columns
    '''
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

def set_headers(df1,input="nc_headers.txt"):
    '''
    Adds the preceeding column name to the each qc column
    '''
    headers = []
    with open(input, 'r') as header_file:
        for line in header_file:
            headers = line.split()
    df1.columns = headers
    return df1
