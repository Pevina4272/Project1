#!/bin/bash

# q2_file_manager.sh
# file manager

echo "-----------file manager----------"

echo "1 . files in current Folder"
echo "2 . create a new file"
echo "3 . delete a file"
echo "4 . exit"

read -p "Enter your choice: " choice

if [ "$choice" -eq 1 ]; then
    ls
elif [ "$choice" -eq 2 ]; then
    read -p "Enter folder name: "floder
    mkdir "$floder"
    echo "Folder created ."
elif [ "Choice" -eq 3 ]; then
    read -p "Enter file name to delete: "file
    rm "$filr"
    echo "File Deleted ."
elif [ "$choice" -eq 4 ]; then
    echo "Exiting...."
else
    echo "Invalid choice ."
    fi

    echo "-----------------------------"
