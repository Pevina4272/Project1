#!/bin/bash

# q1_system_info.sh
# system Information 


echo "==========System information============="


echo "IP Address:"
ip -4 addr show | grep inet | awk '{print $2}' | grep -v 127.0.0.1

echo "Hostname: $(hostname)"

echo "Current User: $(whoami)"

echo "Date & Time: $(date)"

echo "uptime:"
uptime -p

echo "Disk Usage:"
df -h | grep "^/dev"

echo "Memory Usage"
free -h

echo "========================================="

