#!/bin/bash

logfile=$1

[ ! -f "$logfile" ] && exit 1

wc -l "$logfile"
grep -i error "$logfile" | wc -l
grep -i warning "$logfile" | wc -l
tr -s ' ' '\n' < "$logfile" | sort | uniq -c | sort -nr | head -5
