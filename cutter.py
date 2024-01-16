import os
import cv2
import numpy as np
import tensorflow as tf

# Load pre-trained MobileNetV2 model for segmentation
model = tf.keras.applications.MobileNetV2(weights='imagenet', input_shape=(224, 224, 3), include_top=False)

# Input and output folder paths
input_folder = 'G:/pornpics/consolidated'  # Replace with your input folder path containing images with people
output_folder = 'G:/experiments/humancutout'  # Replace with your desired output folder path for saving processed images

# Ensure the output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Function to remove people from an image
def remove_people(input_image_path, output_image_path):
    image = cv2.imread(input_image_path)
    input_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    input_image = tf.image.resize(input_image, (224, 224))  # Resize to match MobileNetV2 input size
    input_image = tf.keras.applications.mobilenet_v2.preprocess_input(input_image)  # Correct import

    # Expand dimensions and predict
    input_image = tf.expand_dims(input_image, axis=0)
    output = model.predict(input_image)

    # Assuming class 15 corresponds to people
    people_mask = np.argmax(output, axis=-1) == 15

    # Resize the people mask to match the input image size
    people_mask_resized = cv2.resize(people_mask[0].astype(np.uint8), (image.shape[1], image.shape[0]))

    # Apply the mask to the original image
    output_image = np.where(np.expand_dims(people_mask_resized, axis=-1), 0, image)
    cv2.imwrite(output_image_path, output_image)

# Process all images in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
        input_image_path = os.path.join(input_folder, filename)
        output_image_path = os.path.join(output_folder, filename)
        remove_people(input_image_path, output_image_path)

print("Processing complete. Images with people removed are saved in", output_folder)
