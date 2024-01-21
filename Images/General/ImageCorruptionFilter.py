# ImageCorruptionFilter.py

import os
import shutil
from PIL import Image
import sqlite3
import multiprocessing
from datetime import datetime

# Script Name: ImageCorruptionFilter

# Description:
# This script processes images from a source folder, checks for corruption,
# and performs the following actions:
# - Deletes corrupted images and logs the deletions in a SQLite database.
# - Copies valid images to a destination folder.

# Path configuration
source_folder = r'F:\12f2\12f2'
destination_folder = r'F:\your_project_root\stylegan_images'  # Change to your project root directory
db_path = r'F:\your_project_root\deleted_images.db'  # SQLite DB path

# Function to check if image is corrupted
def is_image_corrupted(file_path):
    """
    Check if the given image file is corrupted.

    Args:
    file_path (str): Path to the image file.

    Returns:
    bool: True if the image is corrupted, False otherwise.
    """
    try:
        img = Image.open(file_path)
        img.verify()  # Verify if it's corrupted
        img.close()
        return False
    except:
        return True

def process_file(subdir, file, output_queue):
    """
    Process a single file - copy if valid, delete and log if corrupted.

    Args:
    subdir (str): Subdirectory path.
    file (str): Filename.
    output_queue (multiprocessing.Queue): Queue for logging output messages.
    """
    source_file_path = os.path.join(subdir, file)
    destination_file_path = os.path.join(destination_folder, file)

    if is_image_corrupted(source_file_path):
        # Log to SQLite DB and delete file
        cursor.execute('INSERT INTO deleted_images (filepath) VALUES (?)', (source_file_path,))
        conn.commit()
        os.remove(source_file_path)
        output_queue.put(f"Deleted corrupted file: {source_file_path}")
    else:
        # Copy file to destination folder
        shutil.copy2(source_file_path, destination_file_path)
        output_queue.put(f"Copied file: {destination_file_path}")

# Create destination folder if it doesn't exist
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Set up SQLite database for logging deleted files
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS deleted_images (filepath TEXT)')
conn.commit()

# Initialize multiprocessing
pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
manager = multiprocessing.Manager()
output_queue = manager.Queue()

start_time = datetime.now()

# Process each file in the source folder
for subdir, dirs, files in os.walk(source_folder):
    for file in files:
        pool.apply_async(process_file, args=(subdir, file, output_queue,))

pool.close()
pool.join()

# Close database connection
conn.close()

# Output log messages
while not output_queue.empty():
    print(output_queue.get())

end_time = datetime.now()
elapsed_time = end_time - start_time
print(f"Script completed in {elapsed_time}")

