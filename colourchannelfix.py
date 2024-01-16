# colourchannelfix.py

import os
import cv2
import multiprocessing
from datetime import datetime, timedelta

def process_image(file_path, output_queue):
    try:
        image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
        if image is None:
            raise IOError("Invalid or corrupt file.")

        if len(image.shape) == 2 or image.shape[2] == 1:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            new_file_path = os.path.splitext(file_path)[0] + '.png'
            cv2.imwrite(new_file_path, image)
            if new_file_path != file_path:
                os.remove(file_path)
            output_queue.put(f"Converted to RGB and saved {os.path.basename(new_file_path)}")
        else:
            output_queue.put(None)
    except Exception as e:
        os.remove(file_path)
        output_queue.put(f"Corrupt or invalid file {os.path.basename(file_path)} removed: {str(e)}")

def convert_to_rgb_and_png(folder_path):
    files = os.listdir(folder_path)
    files.reverse()  # Processing from the end
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
    last_update_time = datetime.now()
    while completed_tasks < total_files:
        if not output_queue.empty():
            message = output_queue.get()
            completed_tasks += 1
            if message:
                print(message)

        current_time = datetime.now()
        if (current_time - last_update_time).seconds >= 10:
            elapsed_time = current_time - start_time
            estimated_total_time = (elapsed_time / completed_tasks) * total_files if completed_tasks else timedelta(0)
            estimated_remaining_time = estimated_total_time - elapsed_time
            print(f"Progress: {int((completed_tasks / total_files) * 100)}% complete")
            print(f"Estimated remaining time: {estimated_remaining_time}")
            last_update_time = current_time

    pool.close()
    pool.join()

if __name__ == "__main__":
    folder_location = "D:/Dataset/training"
    convert_to_rgb_and_png(folder_location)
