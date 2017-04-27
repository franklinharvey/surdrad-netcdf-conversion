import sys
import os

def main(selection):
    call = "python csv_to_nc.py Data/csv/%s*.csv" % (selection)
    os.system(call)

if __name__ == '__main__':
    main(sys.argv[1])
