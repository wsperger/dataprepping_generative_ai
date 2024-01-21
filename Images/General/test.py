import os
from PIL import Image

def is_image_file(filename):
    return filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))

def process_image(file_path):
    try:
        with Image.open(file_path) as img:
            print(f"Processed {os.path.basename(file_path)} - Dimensions: {img.size}, Format: {img.format}")
    except Exception as e:
        print(f"Error processing {os.path.basename(file_path)}: {e}")

def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        if is_image_file(filename):
            file_path = os.path.join(folder_path, filename)
            process_image(file_path)

if __name__ == "__main__":
    folder_location = input("Enter the path to your image folder: ")
    process_folder(folder_location)
