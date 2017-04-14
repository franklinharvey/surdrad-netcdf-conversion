"""
This module should accept .csv files and return .nc files.
"""

import sys
from os.path import basename
import os
import csv
import pandas as pd
import xarray as xr

def file_mgmt(filesToProcess):
	"""Initial function, used to seperate list of files from single file input."""
	if len(filesToProcess)>1: # if list of 2 or more files
		for input in filesToProcess:
			df = csv_to_df(input)
			df = replace_nan(df)
			out_name = get_output_filename(input)
			df_to_nc(df,out_name)
	else: # if just single file
		df = csv_to_df(filesToProcess[0])
	return df

def get_filename(input):
	"""Returns the name of the file without the file extension"""
	return os.path.splitext(basename(input))[0]

def get_testsite(input):
	"""Returns the name of the testing location"""
	base = get_filename(input)
	return base.split('_',1)[0]

def get_output_filename(input,change=False):
	if change:
		pass
	else:
		out_name="../../baselineRad/" + str(get_testsite(input)) + "/nc/" + str(get_filename(input))
	return out_name

def csv_to_df(input):
	"""Returns a pandas DataFrame from a .csv file"""
	print "Converting %s into NetCDF4" % get_filename(input)
	with open(input, 'r') as input_file:
		df1 = pd.read_csv(input_file,
	            sep = ",",
	            parse_dates = {'Date': [0,1,2,3,4]},
	            date_parser = lambda x: pd.to_datetime(x, format="%Y %m %d %H %M"),
	            index_col = ['Date'])
		df1.loc[:,'TestSite'] = get_testsite(input)
	return df1

def df_to_nc(df1,out_name):
	"""Writes a NetCDF4 file from a DataFrame input"""
	xds = xr.Dataset.from_dataframe(df1)
	xds.to_netcdf(str(out_name) + ".nc")

def replace_nan(df1):
    """Checks for values and returns a DataFrame with "NaN" values in their place"""
    df1.replace(to_replace="-999.00",value="NaN", inplace=True)
    return df1

if __name__ == '__main__':
	df = file_mgmt(sys.argv[1:])
