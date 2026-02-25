#!/bin/bash

# cut extracts usernames from /etc/passwd
cut -d: -f1 /etc/passwd | wc -l

# awk filters regular users with UID >= 1000
awk -F: '$3>=1000 {print $1}' /etc/passwd

# grep -v removes users with nologin shell
grep -v nologin /etc/passwd | cut -d: -f1

# awk finds users with UID 0 (root)
awk -F: '$3==0 {print $1}' /etc/passwd

# sudo required to read /etc/shadow
# awk checks for locked accounts starting with !
sudo awk -F: '$2 ~ /^!/ {print $1}' /etc/shadow 2>/dev/null
