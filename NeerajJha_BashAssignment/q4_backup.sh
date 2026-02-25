#!/bin/bash

# $1 stores directory name passed as argument
source_dir=$1

# -d checks if directory exists
[ ! -d "$source_dir" ] && exit 1

# date generates timestamp for unique backup name
timestamp=$(date +"%Y%m%d_%H%M%S")

# tar -czvf creates compressed archive
# -c create, -z compress, -v verbose, -f filename
tar -czvf backup_$timestamp.tar.gz "$source_dir"
