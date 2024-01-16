# Telegram Cleaner Script

## Description
This script is designed to process chat export folders from Telegram. It organizes photos and videos into main directories, removes unwanted folders, and deletes thumbnail files.

## Requirements
- Python 3.x

This script uses standard libraries (`os`, `shutil`) included in Python's standard distribution, so no additional installation of packages is required.

## Setup and Running the Script
1. **Set the Main Folder Path:**
   - Locate the following line in the script: `main_folder = 'G:/Database Porn Backup'`
   - Replace `'G:/Database Porn Backup'` with the path to your main folder containing the chat export subfolders.

2. **Run the Script:**
   - Open a terminal or command prompt.
   - Navigate to the directory containing the script.
   - Run the script using Python: `python telegramcleaner.py`

## Note
- The script will create `mainphotos` and `mainvideos` directories in the specified `main_folder` to store organized photos and videos.
- Ensure that the provided path in `main_folder` is correct and accessible.
- The script will delete folders and files as part of its process. Make sure to have backups if necessary.
