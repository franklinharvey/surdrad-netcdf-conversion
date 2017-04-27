from os.path import basename
import os
import csv
import pandas as pd
import xarray as xr

def get_filename(input):
    return os.path.splitext(basename(input))[0]

def get_testsite(input):
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
    df1.replace(to_replace="-9999.9",value="NaN", inplace=True)
    return df1

def format_headers(df1):
    df1.columns = [s.strip(' ') for s in list(df1)]
    df1.columns = [s.strip('\"') for s in list(df1)]
    return df1

def filter_qc(df1):
    df1.drop(list(df1.filter(like="qc")), axis=1, inplace=True)
    df1.drop(df1.columns[[0,1,2]], axis=1, inplace=True)
    return df1

def write_netcdf(df1,input):
    xds = xr.Dataset.from_dataframe(df1)
    xds.to_netcdf("Data/nc/" + get_filename(input) + ".nc")

def main():
    input = "bon95001.csv"
    with open(input, 'r') as input_file:
        df1=pd.read_csv(input_file,
            sep=",",
            parse_dates = {'Date': [0,1,4,5]},
            date_parser = lambda x: pd.to_datetime(x, format="%Y %j %H %M"),
            index_col = ['Date'])
        df1.loc[:,'TestSite'] = get_testsite(input)

    df1 = filter_qc(df1)
    df1 = format_headers(df1)
    df1 = replace_nan(df1)
    write_netcdf(df1,input)

if __name__ == '__main__':
    main()
