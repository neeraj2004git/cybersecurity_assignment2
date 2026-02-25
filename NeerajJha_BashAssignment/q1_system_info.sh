#!/bin/bash

# hostname prints the system name
echo "Hostname: $(hostname)"

# whoami shows the current logged-in user
echo "User: $(whoami)"

# date displays current date and time
echo "Date: $(date)"

# uptime -p shows how long system has been running
uptime -p

# lsb_release or /etc/os-release displays OS information
lsb_release -d 2>/dev/null || grep PRETTY_NAME /etc/os-release

# lscpu shows CPU model details
lscpu | grep "Model name"

# free -h shows memory usage
free -h

# df -h displays disk space usage
df -h
