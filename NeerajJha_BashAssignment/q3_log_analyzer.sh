#!/bin/bash

# $1 stores the log file name passed as argument
logfile=$1

# -f checks if file exists
[ ! -f "$logfile" ] && exit 1

# wc -l counts total lines in file
wc -l "$logfile"

# grep -i searches for 'error' ignoring case
grep -i error "$logfile" | wc -l

# grep -i searches for 'warning' ignoring case
grep -i warning "$logfile" | wc -l

# tr replaces spaces with new lines
# sort arranges words
# uniq -c counts duplicates
# head -5 shows top 5 frequent words
tr -s ' ' '\n' < "$logfile" | sort | uniq -c | sort -nr | head -5
