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
image_path = "E:\ChatExport_2024-01-09\photos\photo_118@10-05-2022_03-00-40.jpg"
project_folder = "D:\Code\ppstylegan3"  # Replace with your project folder path
resize_and_save_image(image_path, project_folder)
