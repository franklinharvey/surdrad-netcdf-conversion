import sys
from os.path import basename
import os
from datetime import timedelta, date

def main(filesToProcess):
    for file in filesToProcess:
        month = get_month(file)
        year = get_year(file)
        filename = get_filename(file)
        site = get_site(file)
        pathFrom = "Data/csv/%s/%s" % (site, filename)
        pathTo = "Data/csv/%s/%s/%s/%s" % (site, year, month, filename)
        os.rename(pathFrom, pathTo)

def get_date_object(input):
    '''
    Returns the date object of the file
    For example, bon95001.csv returns 'datetime.datetime(1995, 12, 31, 0, 0)'
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

def get_filename(input):
    '''
    Returns the name of the file without the extension.
    For example:

    Input: "Test_01.csv"
    Output: "Test_01"
    '''
    return os.path.basename(input)

if __name__ == '__main__':
    main(sys.argv[1:])
