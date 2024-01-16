import os
import cv2
import multiprocessing
from datetime import datetime

def process_image(file_path, output_queue):
    try:
        # Attempt to read the image
        image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
        if image is None:
            # If the image cannot be read, raise an exception
            raise IOError("Invalid or corrupt file.")
    except Exception as e:
        # If an exception occurs, put the file name and error in the queue
        output_queue.put(f"Corrupt file detected {os.path.basename(file_path)}: {str(e)}")
        # Optionally, delete the file here if you want to automate deletion
        # os.remove(file_path)

def delete_corrupt_files(folder_path):
    files = os.listdir(folder_path)
    total_files = len(files)

    pool = multiprocessing.Pool(processes=20)
    manager = multiprocessing.Manager()
    output_queue = manager.Queue()

    start_time = datetime.now()
    for filename in files:
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            pool.apply_async(process_image, args=(file_path, output_queue,))

    completed_tasks = 0
    while completed_tasks < total_files:
        if not output_queue.empty():
            message = output_queue.get()
            completed_tasks += 1
            if message:
                print(message)

    pool.close()
    pool.join()
    print(f"Completed processing. Total files checked: {total_files}")

if __name__ == "__main__":
    folder_location = "D:/Dataset/training"
    delete_corrupt_files(folder_location)
