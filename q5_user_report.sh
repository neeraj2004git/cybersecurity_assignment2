#!/bin/bash
#users report
# total users
cut -d: -f1 /etc/passwd | wc -l

# regular users with UID >= 1000
awk -F: '$3>=1000 {print $1}' /etc/passwd

# users with login shell
grep -v nologin /etc/passwd | cut -d: -f1

# root privilege users 
awk -F: '$3==0 {print $1}' /etc/passwd

# locked accounts
sudo awk -F: '$2 ~ /^!/ {print $1}' /etc/shadow 2>/dev/null
