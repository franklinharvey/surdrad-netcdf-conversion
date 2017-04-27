from os.path import basename
import os
import csv
import pandas as pd
import xarray as xr


with open("bon95001.csv", 'r') as input_file:
    df1=pd.read_csv(input_file,
        sep=",",
        parse_dates = {'Date': [0,1,4,5]},
        date_parser = lambda x: pd.to_datetime(x, format="%Y %j %H %M"),
        index_col = ['Date'])


df1.drop(list(df1.filter(like="qc")), axis=1, inplace=True)
df1.drop(df1.columns[[0,1,2]], axis=1, inplace=True)

df1.columns = [s.strip(' ') for s in list(df1)]
df1.columns = [s.strip('\"') for s in list(df1)]
df1.replace(to_replace="-9999.9",value="NaN", inplace=True)
print df1
xds = xr.Dataset.from_dataframe(df1)
xds.to_netcdf("test.nc")
