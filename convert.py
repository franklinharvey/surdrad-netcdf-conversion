import sys
from os.path import basename
import os
import csv

def main(filesToProcess):
	if len(filesToProcess)>1: # if list of 2 or more files
		for input in filesToProcess:
			dat_to_csv(input)
	else: # if just single file
		dat_to_csv(filesToProcess[0])

def dat_to_csv(input):
    headers = get_headers(input)
    base = os.path.splitext(basename(input))[0]

    print "Processing %s" % base
    out_name = ("Data/csv/" + base + ".csv")

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

def get_headers(input, get_csv=True):
    headers = []
    with open("headers.dat", 'r') as header_file:
        for line in header_file:
            headers = line.split()
    if get_csv:
        return ('"%s"') % '", "'.join(headers)
    else:
        return headers

if __name__ == '__main__':
    main(sys.argv[1:])
