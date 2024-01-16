# ImageFormatConverter.py

import os
from PIL import Image

def clean_and_convert_to_png(directory):
    """
    Convert all image files in a directory to PNG format and remove non-image files.

    Args:
    directory (str): The path to the directory containing the files to be processed.
    """
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # Check if the file is in a recognized image format
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            try:
                with Image.open(file_path) as img:
                    png_path = os.path.splitext(file_path)[0] + '.png'
                    img.save(png_path)
                if file_path != png_path:
                    os.remove(file_path)  # Remove the original file if it's different from the new PNG
                    print(f"Converted and deleted original file: {filename}")
            except Exception as e:
                print(f"Failed to convert {file_path}: {e}")
                os.remove(file_path)  # Delete the file if conversion fails
        else:
            # Remove non-image files
            print(f"Non-image file detected and deleted: {filename}")
            os.remove(file_path)

# Usage
folder_path = 'G:/myfolder/images'  # Replace with your folder path
clean_and_convert_to_png(folder_path)
