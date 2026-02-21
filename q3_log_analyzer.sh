#!/bin/bash

# q3_log_analyzer.sh
# This script checks login activity in a log file.

# Check if user gave file name
if [ -z "$1" ]; then
    echo "Usage: $0 <logfile>"
    exit 1
fi

LOGFILE=$1

# Count failed logins
echo "Failed Login Attempts:"
grep "Failed" "$LOGFILE" | wc -l

# Count successful logins
echo "Successful Login Attempts:"
grep "Accepted" "$LOGFILE" | wc -l

echo "Log analysis completed."




# sudo ./q3_log_analyzer.sh /var/log/auth.log