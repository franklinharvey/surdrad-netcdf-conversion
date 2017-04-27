#!/usr/bin/env bash
FILES=$(find Data -type f -name '*.csv')
for f in $FILES
do
  python nc_convert.py $f
done
