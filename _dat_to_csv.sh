#!/usr/bin/env bash
FILES=$(find Data -type f -name '*.dat')
for f in $FILES
do
  python convert.py $f
done
