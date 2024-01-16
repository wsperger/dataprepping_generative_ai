import os
from PIL import Image

def find_truncated_images(folder_path):
    truncated_images = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                try:
                    with Image.open(os.path.join(root, file)) as img:
                        img.load()
                except (OSError, IOError):
                    truncated_images.append(os.path.join(root, file))
    return truncated_images

folder_path = 'D:\\Dataset\\training'  # Replace with your dataset folder
truncated_files = find_truncated_images(folder_path)
print(f"Found {len(truncated_files)} truncated images.")
for file in truncated_files:
    print(file)
