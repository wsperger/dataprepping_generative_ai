from PIL import Image
import os


def resize_and_save_image(input_path, output_folder):
    try:
        # Open the image file
        with Image.open(input_path) as img:
            # Resize the image using LANCZOS (formerly ANTIALIAS) resampling
            resized_img = img.resize((32, 32), Image.Resampling.LANCZOS)

            # Extract the filename and create the output path
            filename = os.path.basename(input_path)
            output_path = os.path.join(output_folder, filename)

            # Save the resized image
            resized_img.save(output_path)

            print(f"Image saved successfully: {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Usage
image_path = "location"
project_folder = "location"
resize_and_save_image(image_path, project_folder)
