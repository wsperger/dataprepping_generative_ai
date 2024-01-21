# DuplicateImageCleaner.py

import os
import time
import imagehash
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_file(file_path, index, total):
    """
    Process a single file to calculate its perceptual hash and track progress.

    Args:
    file_path (str): The path to the image file.
    index (int): The index of the file in the list.
    total (int): The total number of files to process.

    Returns:
    tuple: A tuple containing the image hash and the file path.
           Returns (None, file_path) if an error occurs.
    """
    try:
        with Image.open(file_path) as img:
            img_hash = str(imagehash.phash(img))
        return img_hash, file_path
    except Exception as e:
        return None, file_path

def find_duplicate_images(directory, num_workers):
    """
    Find duplicate images in a directory based on their perceptual hash.

    Args:
    directory (str): The directory to search for duplicate images.
    num_workers (int): The number of worker threads to use.

    Returns:
    list: A list of paths to duplicate images.
    """
    hashes = {}
    duplicates = []
    files_to_process = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                file_path = os.path.join(root, file)
                files_to_process.append(file_path)

    total_files = len(files_to_process)

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        for index, file_path in enumerate(files_to_process):
            future = executor.submit(process_file, file_path, index, total_files)
            hashes[future] = file_path

        for future in as_completed(hashes):
            img_hash, file_path = future.result()
            if img_hash:
                if img_hash in hashes:
                    duplicates.append(file_path)
                else:
                    hashes[img_hash] = file_path

    return duplicates

def delete_duplicates(directory, num_workers):
    """
    Delete duplicate images in a directory.

    Args:
    directory (str): The directory to clean up.
    num_workers (int): The number of worker threads to use.
    """
    start_time = time.time()
    duplicates = find_duplicate_images(directory, num_workers)
    total = len(duplicates)

    for index, file_path in enumerate(duplicates):
        os.remove(file_path)
        print(f"Deleted duplicate image: {file_path} ({index + 1}/{total} duplicates removed)")

    total_time = time.time() - start_time
    print(f"Deletion process completed. Total time: {total_time:.2f} seconds.")

# Usage
folder_path = "location"
num_workers = 40  
delete_duplicates(folder_path, num_workers)
