
# Converting Radiation Surfrad .dat Files to NetCDF4

All of the examples will be data from `Bondville_IL/`, and from the year 2016. Such files will be names `bon16###` where `###` denotes the julian day of the year. 

## Structuring Your Directory

As of April 28, 2017, these files assume this directory is laid out in this manner:

    Project
     |
     +-- .py Files
     |
     +-- .sh Files
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


### Important note on .csv conversion

The file `dat_to_csv.py` writes files to specific folders based on the date. This is very important for the NetCDF writer, as all the .csv files are alread grouped by month, year, and test site.

## Converting to .nc

All of the actual csv->nc conversion logic lies in `nc_convert.py`. Essentially it checks whether the input is a single file (`isinstance(input, basestring)`) or a set of files. Single files are daily files, anything else is combined into a single file. As I'm writing this, all qc columns are dropped and all headers are renamed based off of names supplied by John Augustine. 

The scripts `csv_to_nc_daily`, `csv_to_nc_monthly`, `csv_to_nc_yearly`, and `csv_to_nc_testsite` all handle the logic pertaining to naming NetCDF files and passing data to `nc_convert.py`. So `csv_to_nc_monthly` takes an input of exactly a month's worth of data, determines a name, and passes it to `nc_convert.py`.

The scripts `catch_up_daily`, `catch_up_monthly`, `catch_up_yearly`, and `catch_up_testsite` determine what data fits into a timespan and pass them to the `csv_to_nc*` scripts. These are specifically written to "catch up" on historical data (as they recursively walk the data directory and pass all the data in it). These can be reimagined to convert new incoming data.
