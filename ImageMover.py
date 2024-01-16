# ImageMover.py

import os
import shutil

def move_images(source_folder, destination_folder):
    """
    Moves image files from the source folder to the destination folder.

    Args:
    source_folder (str): The path of the source directory containing image files.
    destination_folder (str): The path of the destination directory where files will be moved.
    """
    # List of common image file extensions
    image_extensions = ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif']

    # Create destination folder if it does not exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for filename in os.listdir(source_folder):
        if filename.lower().endswith(tuple(image_extensions)):
            source_path = os.path.join(source_folder, filename)
            destination_path = os.path.join(destination_folder, filename)

            # Copy the image to the destination folder
            shutil.copy2(source_path, destination_path)
            print(f"Copied {filename} to {destination_folder}")

            # Delete the original file
            os.remove(source_path)
            print(f"Deleted {filename} from {source_folder}")

# Usage
source_folder_path = 'E:/tt'  # Replace with your source folder path
destination_folder_path = 'D:/Dataset/training'  # Replace with your destination folder path
move_images(source_folder_path, destination_folder_path)
