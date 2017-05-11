from os.path import basename
import os
import datetime
import pandas as pd
import xarray as xr

def normal_process(input, outName):
    '''
    Converts all all files in 'input' into a single NetCDF file with name 'outName'
    '''
    if not isinstance(input, basestring):
        for count,day in enumerate(input):
            print "%s into %s -- %i/%i" % (get_filename(day), outName, count+1, len(input))
            df1 = csv_to_dataframe(day)
            df1 = filter_qc(df1)
            df1 = filter_dates(df1)
            df1 = set_headers(df1)
            df1 = replace_nan(df1)
            if count == 0:
                df2 = df1
            else:
                df2 = pd.concat([df2, df1])
            del df1
            write_netcdf(df2, outName)
    else:
        print "%s into %s" % (get_filename(input), outname)
        df1 = csv_to_dataframe(input)
        df1 = filter_qc(df1)
        df1 = filter_dates(df1)
        df1 = set_headers(df1)
        df1 = replace_nan(df1)
        write_netcdf(df1, outName)

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

def get_date_object(input):
    '''
    Returns the date object of the file
    For example, bon95365.csv returns 'datetime.datetime(1995, 12, 31, 0, 0)'
    '''
    date = get_filename(input)[3:]
    return datetime.datetime.strptime(date, '%y%j')

def get_year(input):
    '''
    Returns the year of the file
    For example, bon95001.csv returns '1995'
    '''
    date = get_date_object(input)
    return date.strftime('%Y')

def get_month(input):
    '''
    Returns the month of the file
    For example, bon95001.csv returns 'January'
    '''
    date = get_date_object(input)
    return date.strftime('%B')

def get_month_as_num(input):
    '''
    Returns the month of the file
    For example, bon95001.csv returns 'January'
    '''
    date = get_date_object(input)
    return int(date.strftime('%m'))

# DELETE
# def iterate_month(month):
#     if month == "January":
#         return "February"
#
#     elif month == "February":
#         return "March"
#
#     elif month == "March":
#         return "April"
#
#     elif month == "April":
#         return "May"
#
#     elif month == "May":
#         return "June"
#
#     elif month == "June":
#         return "July"
#
#     elif month == "July":
#         return "August"
#
#     elif month == "August":
#         return "September"
#
#     elif month == "September":
#         return "October"
#
#     elif month == "October":
#         return "November"
#
#     elif month == "November":
#         return "December"
#
#     elif month == "December":
#         return "January"

def get_day(input):
    '''
    Returns the day of the month as a zero-padded decimal number of the file
    For example, bon95001.csv returns '01'
    '''
    date = get_date_object(input)
    return date.strftime('%d')

def write_netcdf(df1, name):
    '''
    Writes the dataframe into a NetCDF4 file

    'name' should be the full path: "Data/nc/daily/bon/1995/Bondville_IL_1995_01_01.nc"
    '''
    xds = xr.Dataset.from_dataframe(df1)
    xds.to_netcdf(name)

def csv_to_dataframe(input):
    '''
    Loads a csv into a Pandas dataframe.
    Uses the Year, Julian Day, Hour, and Minute to create an index column of "Date".
    Adds the test site as a column
    '''
    with open(input, 'r') as input_file:
        df1=pd.read_csv(input_file,
            sep=",",
            parse_dates = {'date': [0,1,4,5]},
            date_parser = lambda x: pd.to_datetime(x, format="%Y %j %H %M"),
            index_col = ['date'])
    return df1

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

def set_headers(df1):
    '''
    Renames all the columns based off of "nc_headers.txt"
    '''
    input="nc_headers.txt"
    with open(input, 'r') as header_file:
        for line in header_file:
            headers = line.split()
    df1.columns = headers
    return df1
