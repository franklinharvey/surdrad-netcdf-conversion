import sys
from os.path import basename
import os
import datetime

def main(filesToProcess):
	if len(filesToProcess)>1: # if list of 2 or more files
		for input in filesToProcess:
			dat_to_csv(input)
	else: # if just single file
		dat_to_csv(filesToProcess[0])

def dat_to_csv(input):
	headers = get_headers()
	base = get_filename(input)
	month = get_month(input)
	year = get_year(input)
	site = get_site(input)
	out_name = "Data/csv/%s/%s/%s/%s.csv" % (site, year, month, base)

	print "Processing %s" % base

	with open(input, 'r') as input_file:
		with open(out_name, 'w') as output_file:
			output_file.write(headers + "\n")
			for count, line in enumerate(input_file):
				if count < 2:
					pass
				else:
					if line.split()[0]=='\x1a':
						pass
					else:
						outLine = ",".join(line.split())
						output_file.write(outLine + '\n')

def get_headers(input="headers.txt", get_csv=True):
    headers = []
    with open(input, 'r') as header_file:
        for line in header_file:
            headers = line.split()
    if get_csv:
        return ('%s') % ','.join(headers)
    else: # leave the option of returning an array of headers instead
        return headers

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

def get_site(input):
	return get_filename(input)[0:3]

def get_filename(input):
	'''
	Returns the name of the file without the extension.
	For example:

	Input: "Test_01.dat"
	Output: "Test_01"
	'''
	return os.path.splitext(basename(input))[0]

if __name__ == '__main__':
    main(sys.argv[1:])
