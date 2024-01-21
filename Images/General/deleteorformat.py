import os
from PIL import Image

def convert_images(folder_path):
    try:
        # Check if the folder exists
        if not os.path.exists(folder_path):
            print(f"Folder '{folder_path}' does not exist.")
            return

        # List all files in the folder
        files = os.listdir(folder_path)

        for file in files:
            file_path = os.path.join(folder_path, file)

            # Check if the file is an image (PNG or JPG)
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                try:
                    # Open the image and re-save it as PNG or JPG
                    img = Image.open(file_path)
                    img.save(file_path)
                    print(f"Converted '{file}' to PNG/JPG.")
                except Exception as e:
                    print(f"Error converting '{file}': {e}")
            else:
                # Delete non-image files
                os.remove(file_path)
                print(f"Deleted '{file}'.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Provide the folder path here
folder_path = "location"
convert_images(folder_path)
