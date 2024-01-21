# JPEGCorruptionCleaner.py

import os
import cv2
import multiprocessing
from datetime import datetime

def process_file(file_path, output_queue):
    """
    Process a single file to check for corruption and delete if necessary.

    Args:
    file_path (str): The path to the file to be processed.
    output_queue (multiprocessing.Queue): A queue to output messages for logging.
    """
    try:
        image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
        if image is None:
            raise IOError("Invalid or corrupt file.")
        output_queue.put(None)  # No issue with the file
    except Exception as e:
        os.remove(file_path)
        output_queue.put(f"Deleted corrupt file: {os.path.basename(file_path)}")

def delete_corrupt_jpegs(folder_path):
    """
    Delete corrupt JPEG files in a specified folder.

    Args:
    folder_path (str): Path to the folder containing JPEG files to be checked.
    """
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg'))]
    total_files = len(files)

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    manager = multiprocessing.Manager()
    output_queue = manager.Queue()

    start_time = datetime.now()
    for filename in files:
        file_path = os.path.join(folder_path, filename)
        pool.apply_async(process_file, args=(file_path, output_queue,))

    deleted_files = 0
    for _ in range(total_files):
        message = output_queue.get()
        if message:
            print(message)
            deleted_files += 1

    pool.close()
    pool.join()

    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print(f"Completed in {elapsed_time}")
    print(f"Total files checked: {total_files}")
    print(f"Total deleted files: {deleted_files}")

if __name__ == "__main__":
    folder_location = "location"
    delete_corrupt_jpegs(folder_location)
