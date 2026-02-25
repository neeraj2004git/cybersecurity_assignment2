#!/bin/bash

echo "Hostname: $(hostname)"
echo "User: $(whoami)"
echo "Date: $(date)"

uptime -p

lsb_release -d 2>/dev/null || grep PRETTY_NAME /etc/os-release

lscpu | grep "Model name"

free -h
df -h
