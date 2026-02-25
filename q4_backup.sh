#!/bin/bash

source_dir=$1

[ ! -d "$source_dir" ] && exit 1

timestamp=$(date +"%Y%m%d_%H%M%S")

tar -czf backup_$timestamp.tar.gz "$source_dir"
