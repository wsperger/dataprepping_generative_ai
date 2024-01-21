import os
import shutil

def copy_images(src_directory, dst_directory):
    # Define image file extensions
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}

    # Create destination directory if it doesn't exist
    if not os.path.exists(dst_directory):
        os.makedirs(dst_directory)

    # Copy each image file
    for filename in os.listdir(src_directory):
        if any(filename.lower().endswith(ext) for ext in image_extensions):
            src_file = os.path.join(src_directory, filename)
            dst_file = os.path.join(dst_directory, filename)
            shutil.copy2(src_file, dst_file)  # copy2 preserves metadata

# Example usage
source_folder = "F:/HentaiGan"
destination_folder = "F:/mainphotos"
copy_images(source_folder, destination_folder)
