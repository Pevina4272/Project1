#!/bin/bash

# Assignment01.sh
# -------------------------------
# Function 1: System Information
# -------------------------------
system_info() {
    echo "===== SYSTEM INFORMATION ====="
    echo "Hostname: $(hostname)"
    echo "User: $(whoami)"
    echo "Date & Time: $(date)"
    echo "Uptime:"
    uptime -p
    echo "Disk Usage:"
    df -h | grep "^/dev"
    echo "Memory Usage:"
    free -h
    echo "==============================="
}

# -------------------------------
# Function 2: File Manager
# -------------------------------
file_manager() {
    echo "----- FILE MANAGER -----"
    echo "1. List files"
    echo "2. Create directory"
    echo "3. Delete file"
    echo "4. Move file"
    read -p "Choose option: " option

    case $option in
        1) ls -lh ;;
        2)
            read -p "Enter directory name: " dirname
            mkdir -p "$dirname"
            echo "Directory created."
            ;;
        3)
            read -p "Enter file name to delete: " file
            if [ -f "$file" ]; then
                rm "$file"
                echo "File deleted."
            else
                echo "File not found."
            fi
            ;;
        4)
            read -p "Enter file name: " file
            read -p "Enter destination folder: " dest
            if [ -f "$file" ] && [ -d "$dest" ]; then
                mv "$file" "$dest"
                echo "File moved successfully."
            else
                echo "File or folder not found."
            fi
            ;;
        *) echo "Invalid option." ;;
    esac
}

# -------------------------------
# Function 3: Log Analyzer
# -------------------------------
log_analyzer() {
    read -p "Enter log file path: " logfile

    if [ ! -f "$logfile" ]; then
        echo "Log file not found."
        return
    fi

    echo "Total Log Entries: $(wc -l < "$logfile")"
    echo "Failed Logins: $(grep -c "Failed password" "$logfile")"
    echo "Successful Logins: $(grep -c "Accepted password" "$logfile")"

    echo "Top 5 IP Addresses:"
    grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}' "$logfile" | \
    sort | uniq -c | sort -nr | head -5
}

# -------------------------------
# Function 4: Backup Script
# -------------------------------
backup_script() {
    read -p "Enter directory to backup: " source

    if [ ! -d "$source" ]; then
        echo "Directory not found."
        return
    fi

    mkdir -p backups
    timestamp=$(date +%Y-%m-%d_%H-%M-%S)
    filename=$(basename "$source")_backup_$timestamp.tar.gz

    tar -czf backups/$filename "$source"
    echo "$(date): Backup created - $filename" >> backup.log

    echo "Backup created successfully."
}

# -------------------------------
# Function 5: User Report
# -------------------------------
user_report() {
    echo "----- USER REPORT -----"
    echo "Username | UID | Home | Shell"
    awk -F: '{print $1 " | " $3 " | " $6 " | " $7}' /etc/passwd

    echo "Total Users: $(wc -l < /etc/passwd)"

    echo "Users with UID 0:"
    awk -F: '$3==0 {print $1}' /etc/passwd
}

# ===============================
# Main Menu Loop
# ===============================

while true
do
    echo ""
    echo "========== MAIN MENU =========="
    echo "1. System Information"
    echo "2. File Manager"
    echo "3. Log Analyzer"
    echo "4. Backup Directory"
    echo "5. User Report"
    echo "6. Exit"
    echo "==============================="

    read -p "Select option: " choice

    case $choice in
        1) system_info ;;
        2) file_manager ;;
        3) log_analyzer ;;
        4) backup_script ;;
        5) user_report ;;
        6) echo "Exiting..."; exit 0 ;;
        *) echo "Invalid choice. Try again." ;;
    esac
done