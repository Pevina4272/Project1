#!/bin/bash

# q4_backup.sh
# backup  with date

# input
if [ -z "$1" ]; then
    echo "Usage: $0 <folder_name>"
    exit 1
fi

FOLDER=$1
DATE=$(date +%Y-%m-%d)
tar -czf backup_$DATE.tar.gz "$FOLDER"

echo "Backup created: backup_$DATE.tar.gz"

echo "================================================="
