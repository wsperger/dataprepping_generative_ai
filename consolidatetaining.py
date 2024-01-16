# consolidatetaining.py

import os
import shutil

def move_and_rename_images(main_folder):
    image_extensions = ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif']
    image_counter = 1

    for root, dirs, files in os.walk(main_folder):
        for file in files:
            if file.lower().endswith(tuple(image_extensions)):
                file_path = os.path.join(root, file)
                new_file_path = os.path.join(main_folder, f"{image_counter}{os.path.splitext(file)[-1]}")
                shutil.move(file_path, new_file_path)
                print(f"Moved and renamed {file} to {new_file_path}")
                image_counter += 1

# Usage
main_folder_path = 'D:/Dataset/training'  # Replace with your main folder path
move_and_rename_images(main_folder_path)
