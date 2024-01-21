import os
import cv2
import hashlib
import time
import gc
import torch
import json
import numpy as np
from datetime import datetime, timedelta
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from transformers import SegformerImageProcessor, AutoModelForSemanticSegmentation

# Function to check if JPEG file is corrupted
def is_jpeg_corrupted(file_path):
    try:
        with open(file_path, 'rb') as file:
            file.seek(-2, 2)
            return file.read() != b'\xff\xd9'  # JPEG files should end with these bytes
    except IOError:
        return True

# Function to check if a file is a video
def is_video_file(filename):
    return filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))

# Initialize the BLIP model with GPU support
device = "cuda" if torch.cuda.is_available() else "cpu"
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to(device)

# Function to generate a caption for an image
def generate_caption(image):
    inputs = processor(images=image, return_tensors="pt").to(device)
    outputs = model.generate(**inputs)
    caption = processor.decode(outputs[0], skip_special_tokens=True)
    return caption

# Function to get hash of an image
def get_image_hash(image):
    image_bytes = image.tobytes()
    return hashlib.md5(image_bytes).hexdigest()

# Function to check if video is corrupted
def is_corrupted(video_path):
    try:
        video = cv2.VideoCapture(video_path)
        if not video.isOpened():
            return True
        success, _ = video.read()
        video.release()
        return not success
    except:
        return True

# Function to process a video file
def process_video(video_path, output_folder, person_descriptors, undesired_captions, hashes, annotations, save_format="JPEG", frame_skip=10):
    if is_corrupted(video_path):
        print(f"Skipping corrupted or unreadable file: {video_path}")
        return

    video = cv2.VideoCapture(video_path)
    success, frame = video.read()
    frame_count = 0
    while success:
        if frame_count % frame_skip == 0:  # Process every nth frame
            try:
                image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                image = image.resize((256, 256))
                caption = generate_caption(image)
                image_hash = get_image_hash(image)

                if any(word in caption.lower() for word in person_descriptors) and image_hash not in hashes and all(undesired not in caption.lower() for undesired in undesired_captions):
                    hashes.add(image_hash)
                    frame_path = os.path.join(output_folder, f"{os.path.basename(video_path)}_frame{frame_count}.{save_format.lower()}")
                    image.save(frame_path, format=save_format)
                    annotations.append({'file_name': frame_path, 'caption': caption})
                    print(f"Frame {frame_count}: {caption} - Saved as {os.path.basename(frame_path)}")
                else:
                    print(f"Frame {frame_count}: {caption} - Deleted or Duplicate")

            except Exception as e:
                print(f"Error processing frame {frame_count} in {video_path}: {e}")

        video.set(cv2.CAP_PROP_POS_MSEC, (frame_count+1)*1000)
        success, frame = video.read()
        frame_count += 1

        gc.collect()  # Force garbage collection

    video.release()
    time.sleep(1)  # Pause between processing videos

# Load the SegFormer model and processor
seg_processor = SegformerImageProcessor.from_pretrained("mattmdjaga/segformer_b2_clothes")
seg_model = AutoModelForSemanticSegmentation.from_pretrained("mattmdjaga/segformer_b2_clothes").to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))

def perform_segmentation(image):
    inputs = seg_processor(images=image, return_tensors="pt")
    outputs = seg_model(**inputs)
    logits = outputs.logits.cpu()

    upsampled_logits = torch.nn.functional.interpolate(
        logits,
        size=image.size[::-1],
        mode="bilinear",
        align_corners=False,
    )

    pred_seg = upsampled_logits.argmax(dim=1)[0]
    return pred_seg

# Modify the process_image function to include clothes segmentation
def process_image(file_path):
    try:
        if file_path.lower().endswith('.jpg') or file_path.lower().endswith('.jpeg'):
            if is_jpeg_corrupted(file_path):
                raise IOError("Corrupt JPEG file.")

        image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
        if image is None:
            raise IOError("Invalid or corrupt file.")

        if len(image.shape) == 2 or image.shape[2] == 1:
            # Convert to RGB and add a dark blue pixel
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            image[0, 0] = [0, 0, 139]  # Adding a dark blue pixel at the top-left corner
            new_file_path = os.path.splitext(file_path)[0] + '.png'
            cv2.imwrite(new_file_path, image)
            if new_file_path != file_path:
                os.remove(file_path)
            return f"Processed and converted {os.path.basename(file_path)}"
        else:
            # File is already in RGB format, no action taken
            return None
    except Exception as e:
        print(f"Error processing {os.path.basename(file_path)}: {e}")
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                return f"Corrupt or invalid file {os.path.basename(file_path)} removed successfully"
            except Exception as delete_error:
                return f"Failed to remove corrupt file {os.path.basename(file_path)}: {str(delete_error)}"
        else:
            return f"Corrupt or invalid file {os.path.basename(file_path)} not found or already removed"

def convert_to_rgb_and_png(folder_path):
    files = os.listdir(folder_path)
    files.reverse()  # Processing from the end
    total_files = len(files)

    start_time = datetime.now()
    completed_tasks = 0
    for filename in files:
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            message = process_image(file_path)
            if message:  # Print message only if there is one
                print(message)
            completed_tasks += 1

        current_time = datetime.now()
        if completed_tasks % 10 == 0 or completed_tasks == total_files:  # Update every 10 files or at the end
            elapsed_time = current_time - start_time
            estimated_total_time = (elapsed_time / completed_tasks) * total_files if completed_tasks else timedelta(0)
            estimated_remaining_time = estimated_total_time - elapsed_time
            #print(f"Progress: {int((completed_tasks / total_files) * 100)}% complete")
            #print(f"Estimated remaining time: {estimated_remaining_time}")

if __name__ == "__main__":
    folder_location = "location"
    convert_to_rgb_and_png(folder_location)

    # User input for the video folder path
    video_folder = input("Enter the path to your video folder: ")
    output_folder = input("Enter the path to the output folder: ")
    person_descriptors = ["man", "woman", "person", "boy", "girl", "human"]
    undesired_captions = ["there is a black background with a picture of a woman in a bikini", "there is a black background with a black and white photo of a man"]
    save_format = "JPEG"  # Specify the desired image format here

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    hashes = set()
    annotations = []
    video_paths = [os.path.join(video_folder, f) for f in os.listdir(video_folder) if is_video_file(f)]
    for path in video_paths:
        process_video(path, output_folder, person_descriptors, undesired_captions, hashes, annotations, save_format=save_format)

    # Save annotations to a JSON file
    annotations_path = os.path.join(output_folder, "annotations.json")
    with open(annotations_path, "w", encoding="utf-8") as file:
        json.dump(annotations, file)

    print(f"Annotations saved in {annotations_path}")
