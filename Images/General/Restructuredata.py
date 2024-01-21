import os
import sqlite3
import time
from PIL import Image
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv

# Global variables
db_path = "image_data.db"
csv_output = "image_data.csv"

# Define a variable for the progress interval
progress_interval = 1000

# Database functions
def create_database():
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS image_data (
                filename TEXT,
                dimensions TEXT,
                mode TEXT,
                timestamp TEXT,
                status TEXT,
                error_message TEXT
            )
        ''')
        conn.commit()

def insert_batch_data_from_csv():
    with sqlite3.connect(db_path) as conn, open(csv_output, 'r') as csv_file:
        c = conn.cursor()
        reader = csv.DictReader(csv_file)
        for row in reader:
            c.execute('INSERT INTO image_data (filename, dimensions, mode, timestamp, status, error_message) VALUES (?, ?, ?, ?, ?, ?)',
                      (row['filename'], row['dimensions'], row['mode'], row['timestamp'], row['status'], row['error_message']))
        conn.commit()

def extract_metadata_and_rename(file_path):
    try:
        with Image.open(file_path) as pil_image:
            dimensions = f"{pil_image.width}x{pil_image.height}"
            mode = pil_image.mode
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Rest of your code remains the same
        unique_number = int(time.time() * 1000)
        new_filename = f"{os.path.splitext(os.path.basename(file_path))[0]}_{dimensions}_{mode}_{unique_number}.jpg"
        new_file_path = os.path.join(os.path.dirname(file_path), new_filename)

        os.rename(file_path, new_file_path)

        return new_filename, dimensions, mode, timestamp, "Processed", None
    except Exception as e:
        error_message = f"Error processing {os.path.basename(file_path)}: {str(e)}"
        return os.path.basename(file_path), "", "", "", "Error", error_message


# Function to check if a file is an image
def is_image_file(filename):
    return filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))

# Function to process a folder of images and write to a CSV file
def process_folder_and_write_to_csv(folder_path):
    create_database()

    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if is_image_file(f)]
    total_files = len(files)

    with ThreadPoolExecutor() as executor, open(csv_output, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["filename", "dimensions", "mode", "timestamp", "status", "error_message"])

        processed_count = 0
        for future in as_completed([executor.submit(extract_metadata_and_rename, file_path) for file_path in files]):
            result = future.result()
            csv_writer.writerow(result)

            processed_count += 1

            # Print progress every 1000 rows
            if processed_count % progress_interval == 0:
                print(f"Processed {processed_count}/{total_files} files ({(processed_count/total_files)*100:.2f}%)")

# Main execution
if __name__ == "__main__":
    folder_location = input("Enter the path to your image folder: ")
    process_folder_and_write_to_csv(folder_location)
    insert_batch_data_from_csv()  # Transfer data from CSV to SQLite
    print("Image folder processing and data saving complete.")
