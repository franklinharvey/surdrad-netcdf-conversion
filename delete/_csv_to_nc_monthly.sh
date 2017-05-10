#!/usr/bin/env bash
FILES=( bon dra fpk gwn psu sxf tbl )
# python csv_to_nc_monthly.py Data/csv/bon/bon9*.csv
# python csv_to_nc_monthly.py Data/csv/bon/bon0*.csv
#

for f in "${FILES[@]}"
do
  python csv_to_nc_monthly.py Data/csv/$f/$f\9*.csv
  python csv_to_nc_monthly.py Data/csv/$f/$f\0*.csv
  python csv_to_nc_monthly.py Data/csv/$f/$f\1*.csv
done
