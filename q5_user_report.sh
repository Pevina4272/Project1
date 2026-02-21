#!/bin/bash



# q5_user_report.sh

# This script shows basic user information from the system.



echo "===== USER R ====="



# Show all usernames

echo "List of users"

cut -d: -f1 /etc/passwd

# Count total users

echo "Total users:"
cat /etc/passwd | wc -l
echo "users with  UID 0:"
awk -F: '$3==0 {print $1}' /etc/passwd
echo "========================"
