# telegramcleaner.py

import os
import shutil

def unique_file_name(destination, filename):
    """
    Generate a unique file name in the destination directory.

    Args:
    destination (str): The directory where the file will be moved.
    filename (str): The original filename.

    Returns:
    str: A unique file name for the destination directory.
    """
    base_name, extension = os.path.splitext(filename)
    counter = 1
    new_name = filename
    while os.path.exists(os.path.join(destination, new_name)):
        new_name = f"{base_name}_{counter}{extension}"
        counter += 1
    return new_name

def delete_unwanted_folders(root_path):
    """
    Delete folders in the given path that are not 'photos' or 'video_files'.

    Args:
    root_path (str): The path to search for and delete unwanted folders.
    """
    for folder in os.listdir(root_path):
        folder_path = os.path.join(root_path, folder)
        if os.path.isdir(folder_path) and folder not in ['photos', 'video_files']:
            shutil.rmtree(folder_path)

def delete_thumb_files(folder_path):
    """
    Delete thumbnail files in the given folder.

    Args:
    folder_path (str): The path of the folder from which to delete thumbnail files.
    """
    for filename in os.listdir(folder_path):
        if '_thumb' in filename:
            os.remove(os.path.join(folder_path, filename))
            print("Deleted thumbnail file:", filename)

def move_files(source_folder, destination_folder):
    """
    Move files from the source folder to the destination folder, ensuring unique file names.

    Args:
    source_folder (str): The folder from which to move files.
    destination_folder (str): The folder to which to move files.
    """
    files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
    total_files = len(files)
    for i, file in enumerate(files):
        unique_name = unique_file_name(destination_folder, file)
        shutil.move(os.path.join(source_folder, file), os.path.join(destination_folder, unique_name))
        print(f"Progress: {((i + 1) / total_files) * 100:.2f}%")

def process_chat_exports(main_folder):
    """
    Process chat export folders by organizing photos and videos into main directories.

    Args:
    main_folder (str): The main folder containing chat export subfolders.
    """
    # Create main directories for photos and videos if they don't exist
    if not os.path.exists(os.path.join(main_folder, 'mainphotos')):
        os.makedirs(os.path.join(main_folder, 'mainphotos'))
    if not os.path.exists(os.path.join(main_folder, 'mainvideos')):
        os.makedirs(os.path.join(main_folder, 'mainvideos'))

    for root, dirs, files in os.walk(main_folder):
        if 'ChatExport' in root:
            delete_unwanted_folders(root)
            if 'photos' in dirs:
                photos_path = os.path.join(root, 'photos')
                delete_thumb_files(photos_path)
                move_files(photos_path, os.path.join(main_folder, 'mainphotos'))
            if 'video_files' in dirs:
                videos_path = os.path.join(root, 'video_files')
                delete_thumb_files(videos_path)
                move_files(videos_path, os.path.join(main_folder, 'mainvideos'))

# Set the main folder path
main_folder = 'G:/Database Porn Backup'  # Replace with your main folder path
process_chat_exports(main_folder)
