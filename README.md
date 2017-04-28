
# Converting Radiation Surfrad .dat Files to NetCDF4

All of the examples will be data from `Bondville_IL/`, and from the year 2016. Such files will be names `bon16###` where `###` denotes the julian day of the year. 

## Structuring Your Directory

As of April 28, 2017, these files assume this directory is laid out in this manner:

    Project
     |
     +-- Python Files
     |
     +-- Shell Files
     |    
     +-- Data\
     |  |  
     |  +-- Bondville_IL\
     |  |   |
     |  |   +--1995\
     |  |   |  |
     |  |   |  +--bon95001.dat
     |  |   |  |
     |  |   |  +--bon95002.dat
     |  |   |  |
     |  |   |  +--etc.
     |  |   |
     |  |   +--1996\
     |  |   |
     |  |   +--etc.
     |  |
     |  +-- Boulder_CO\
     |  |
     |  +-- csv\
     |  |
     |  +-- nc\

This is necessary because many of the converison scripts will try and write to `Data\csv\` or `Data\nc`.

## Headers

Radiation's Surfrad files have numerous headers:

    YEAR DDD MM DD HH mm hh.mmm ZNAGL dw_psp qc uw_psp qc direct qc diffuse qc dw_pir qc dwCasTmp qc dwDomTmp qc uw_pir qc uwCastmp qc uwDomtmp qc uvb qc par qc netSolar qc netIr qc totalNet qc temp qc rh qc windSp qc winsDir qc Baro qc
    
All of those items, seperated by whitespace, are headers. An initial observation would show that the `qc` header shows up multiple times -- these are quality control flags for the preceding header. A `qc` value of 0 indicated values within an expected range, a value of 1 indicates a value outside of a physically possible range, a value of 2 indicates a value that is physically possible but "should be used with scrutiny". Missing values are indicated by a value of "-9999.9" and should always have a corresponding `qc` of "1".

## Converting to .csv

The .dat files are plain-text files delimited by whitespace. These files have no headers, only minimal site info and raw data. Here are the first several rows of the file `bon16001.dat`:

     Bondville
       40.05  -88.37  213 m version 1
     2016   1  1  1  0  0  0.000 105.13    -3.4 0     0.0 0     0.8 0    -0.1 0   275.8 0   272.5 0   272.2 0   305.1 0   271.0 0   271.0 0     0.0 0     0.2 0     0.0 0   -29.3 0   -29.3 0    -2.2 0    76.5 0     6.8 0   270.0 0  1001.5 0
     2016   1  1  1  0  1  0.017 105.32    -3.6 0     0.0 0     0.8 0    -0.1 0   267.7 0   272.5 0   272.1 0   304.4 0   271.0 0   271.0 0     0.0 0     0.2 0     0.0 0   -36.7 0   -36.7 0    -2.2 0    76.1 0     6.4 0   268.2 0  1001.5 0
     2016   1  1  1  0  2  0.033 105.50    -3.6 0     0.0 0     0.7 0    -0.2 0   260.6 0   272.5 0   272.1 0   303.8 0   271.0 0   271.0 0     0.0 0     0.2 0     0.0 0   -43.1 0   -43.1 0    -2.2 0    77.3 0     6.0 0   272.1 0  1001.5 0
     2016   1  1  1  0  3  0.050 105.68    -3.7 0     0.0 0     0.4 0    -0.1 0   252.5 0   272.5 0   272.1 0   303.1 0   270.9 0   270.9 0     0.0 0     0.2 0     0.0 0   -50.7 0   -50.7 0    -2.2 0    76.7 0     6.6 0   273.9 0  1001.5 0
     2016   1  1  1  0  4  0.067 105.86    -3.8 0     0.0 0     0.4 0    -0.1 0   246.8 0   272.5 0   272.0 0   302.4 0   270.9 0   270.9 0     0.0 0     0.2 0     0.0 0   -55.6 0   -55.6 0    -2.2 0    77.0 0     6.0 0   278.4 0  1001.5 0

Converting these files to .csv will essentially double the amount of storage needed for all the data. However, it seems to be a necessary step, due to the nature of the .dat files. The first step is to include the headers in the new .csv file. I've made a file called `headers.txt` (and a matching `headers.dat`) which contains all the headers that match up with Surfrad .dat files (and are delimited by whitespace).

What follows can be found in the file `dat_to_csv.py`.


```python
import sys
from os.path import basename
import os
```


```python
with open("headers.dat", 'r') as header_file:
    for line in header_file:
        headers = line.split() # this is an array of all the headers
headers = ('%s') % ','.join(headers) # this formats the headers as a comma-delimited string

print headers
```

    YEAR,DDD,MM,DD,HH,mm,hh.mmm,ZNAGL,dw_psp,qc,uw_psp,qc,direct,qc,diffuse,qc,dw_pir,qc,dwCasTmp,qc,dwDomTmp,qc,uw_pir,qc,uwCastmp,qc,uwDomtmp,qc,uvb,qc,par,qc,netSolar,qc,netIr,qc,totalNet,qc,temp,qc,rh,qc,windSp,qc,winsDir,qc,Baro,qc



```python
input = "bon16001.dat" # this is the file for this example, normally passed in via command line
base = os.path.splitext(basename(input))[0] # this gets the name of the file (e.g "bon16001.dat" -> "bon16001")
out_name = (base + ".csv") # this is the name for the file to be written

with open(input, 'r') as input_file:
    with open(out_name, 'w') as output_file:
        output_file.write(headers + "\n") # this writes the headers to the new file
        for count, line in enumerate(input_file):
            if count < 2: # we can skip the first two lines of the input
                pass
            else:
                if line.split()[0]=='\x1a': # skip empty rows
                    pass
                else: # write the data delimited by commas
                    outLine = ",".join(line.split())
                    output_file.write(outLine + '\n')
```

I made a shell script which will find all the .dat files in your directory and convert them into .csv files in the `Data/csv` directory. You will need to have the `dat_to_csv.py` file in your directory along with `_dat_to_csv.sh`. You can then run

    ./_dat_to_csv.sh


## Converting to .nc

### Part One - Dataframes for Daily Files

Even after all the trouble of converting to .csv files, we still can't convert directly to NetCDF files. The data must again be converted, this time into Pandas dataframes. However, dataframes are stored in memory, not in disk, so these are not extra files to be storing.

This method is for one-to-one conversions; each input file will get its own output file. The method to create combined files will be in Part Two - Dataframes for Annual Files.

What follows can be found in `csv_to_nc_daily.py`.


```python
import sys
from os.path import basename
import os
import pandas as pd
import xarray as xr
```


```python
def get_testsite(input):
    '''
    Grabs the initials from the filename and returns the full name of the test site
    '''
    base = os.path.splitext(basename(input))[0]
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
```


```python
input = "bon16001.csv"
filename = os.path.splitext(basename(input))[0] # same as before: "bon16001"

with open(input, 'r') as input_file:
    df1=pd.read_csv(input_file,
        sep=",", # comma-delimited
        parse_dates = {'Date': [0,1,4,5]},
        date_parser = lambda x: pd.to_datetime(x, format="%Y %j %H %M"), # using Year, Julian Day, Hour, and Minute 
        index_col = ['Date']) # sets the index to the new "Date" column
    df1.loc[:,'TestSite'] = get_testsite(input) # adds new column with test site (e.g "Bondville_IL)
```


```python
# If you decide you don't need all the qc columns, here's a handy function to get rid of them
def filter_qc(df1):
    '''
    Drops all the qc columns
    '''
    df1.drop(list(df1.filter(like="qc")), axis=1, inplace=True)
    df1.drop(df1.columns[[0,1,2]], axis=1, inplace=True)
    return df1

# Since we know that "-9999.9" indicates a "NaN" value, we can replace them like this
def replace_nan(df1):
    '''
    The value "-9999.9" is specified to be a placeholder for non-existent values. This replaces those values with "NaN"
    '''
    df1.replace(to_replace="-9999.9",value="NaN", inplace=True)
    return df1
```


```python
# To actually write out to a NetCDF file, use xarray
xds = xr.Dataset.from_dataframe(df1)
xds.to_netcdf(filename + ".nc")
```

### Part Two - Dataframes for Annual Files

If everything above makes sense, everything below should as well. The only difference is that instead of writing out files one-to-one, all the files are combined by year and testsite.


```python
import sys
from os.path import basename
import os
import pandas as pd
import xarray as xr
```


```python
# These are some functions to help
def get_out_name(input):
    '''
    Returns testsite_year
    For example, Bondville_IL_16
    '''
    return "%s_%s" % (get_testsite(input),get_year(input))

def get_year(input):
    '''
    Returns the year of the file
    For example, bon16001.csv returns 16
    '''
    return get_filename(input)[3:5]

def get_julian_day(input):
    '''
    Returns the julian day
    For example, bon16001.csv returns 001
    '''
    return get_filename(input)[5:8]

def get_filename(input):
    '''
    Returns the name of the file without the extension.
    For example:

    Input: "Test_01.csv"
    Output: "Test_01"
    '''
    return os.path.splitext(basename(input))[0]
```


```python
input1 = "bon16001.csv"
input2 = "bon16002.csv"
filesToProcess = [input1,input2] # make an array of all the files to combine
outName = get_out_name(filesToProcess[0])
```


```python
# These are necessary functions for conversion and are not very different from what is shown above

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

def write_netcdf(df1, name):
    '''
    Writes the dataframe into a NetCDF4 file
    '''
    xds = xr.Dataset.from_dataframe(df1)
    xds.to_netcdf(name + ".nc")
```


```python
for count,input in enumerate(filesToProcess):
    filename = get_filename(input)
    df1 = csv_to_dataframe(input)
    if count == 0: # move the first dataframe into df2, df2 will be a sort of "master" dataframe which we append to
        df2 = df1
        del df1
    else:
        df2 = pd.concat([df2, df1]) # combines the current dataframe with the "master" dataframe
        del df1
write_netcdf(df2, outName)

del df2
```

Specifically for annual files, an example would be

    python csv_to_nc_combine.py bon16*.csv
    
which would take all the Bondville_IL files from 2016 and combine them into a NetCDF file. You would need to point it to the correct directory which contains you data files. In my case that would be

    python csv_to_nc_combine.py Data/csv/bon16*.csv
    
There is nothing to stop you from trying

    python csv_to_nc_combine.py Data/csv/bon*.csv

which would combine all the Bondville_IL files. This will take a very long time to run.
