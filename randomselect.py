import os
import shutil
import random

def copy_random_images(source_dir, dest_dir, num_images=40000, extensions=['.jpg', '.jpeg', '.png']):
    # List all files in the source directory
    all_files = os.listdir(source_dir)

    # Filter out files that are not images
    image_files = [file for file in all_files if os.path.splitext(file)[1].lower() in extensions]

    # Check if there are enough images
    if len(image_files) < num_images:
        raise ValueError(f"Not enough images in the source directory. Found only {len(image_files)} images.")

    # Randomly select images
    selected_images = random.sample(image_files, num_images)

    # Copy selected images to the destination directory
    for image in selected_images:
        shutil.copy(os.path.join(source_dir, image), os.path.join(dest_dir, image))

# Usage example
source_directory = 'D:/Dataset/training'  # Replace with your source directory path
destination_directory = 'D:/Dataset/randomtraining'  # Replace with your destination directory path

copy_random_images(source_directory, destination_directory)
