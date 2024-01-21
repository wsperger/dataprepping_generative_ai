# SmallFileCleaner.py

import os
import multiprocessing
from datetime import datetime

def process_file(file_path, size_threshold_bytes, output_queue):
    """
    Process a single file to check if it's below the size threshold and delete if necessary.

    Args:
    file_path (str): The path to the file to be processed.
    size_threshold_bytes (int): The size threshold in bytes.
    output_queue (multiprocessing.Queue): A queue to output messages for logging.
    """
    if os.path.getsize(file_path) < size_threshold_bytes:
        os.remove(file_path)
        output_queue.put(f"Deleted {file_path}")
    else:
        output_queue.put(None)

def delete_small_files(directory, size_threshold_kb):
    """
    Delete files in a specified folder that are smaller than a given size threshold.

    Args:
    directory (str): Path to the folder containing files to be checked.
    size_threshold_kb (int): Size threshold in kilobytes.
    """
    files = os.listdir(directory)
    total_files = len(files)
    size_threshold_bytes = size_threshold_kb * 1024  # Convert KB to bytes

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    manager = multiprocessing.Manager()
    output_queue = manager.Queue()

    start_time = datetime.now()
    for filename in files:
        file_path = os.path.join(directory, filename)
        pool.apply_async(process_file, args=(file_path, size_threshold_bytes, output_queue,))

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
    folder_path = "location"  # Replace with your folder path
    delete_small_files(folder_path, 20)  # Deletes files smaller than 20 KB
