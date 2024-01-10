# Import required libraries
import os
import json
from PIL import Image
from tqdm import tqdm
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

# Function to check if a file is an image
def is_image_file(filename):
    """Check if a file is an image based on its extension.
    
    Args:
    filename (str): The filename to check.

    Returns:
    bool: True if the file is an image, False otherwise.
    """
    return filename.lower().endswith(('.png', '.jpg', '.jpeg'))

# Initialize the BLIP model with GPU support
device = "cuda" if torch.cuda.is_available() else "cpu"
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to(device)

# Function to generate a caption for an image
def generate_caption(image_path):
    """Generate a caption for an image using the BLIP model.

    Args:
    image_path (str): The path to the image.

    Returns:
    str: The generated caption for the image.
    """
    image = Image.open(image_path)
    inputs = processor(images=image, return_tensors="pt").to(device)
    outputs = model.generate(**inputs)
    caption = processor.decode(outputs[0], skip_special_tokens=True)
    return caption

# User input for the image folder path
image_folder = input("Enter the path to your image folder: ")
image_paths = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if is_image_file(f)]

# Process images and generate captions
labels = []
for path in tqdm(image_paths, desc="Processing images"):
    try:
        caption = generate_caption(path)
        labels.append([path, caption])
    except Exception as e:
        print(f"Error processing {path}: {e}")

# Save the captions to dataset.json
dataset_path = os.path.join(image_folder, "dataset.json")
with open(dataset_path, "w", encoding="utf-8") as file:
    json.dump({"labels": labels}, file)

print(f"Captions saved in {dataset_path}")
