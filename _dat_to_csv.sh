#!/usr/bin/env bash
FILES=$(find Data -type f -name '*.dat')
for f in $FILES
do
  python dat_to_csv.py $f
done
