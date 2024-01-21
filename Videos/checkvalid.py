import os
import cv2
import hashlib
import random
import string
import sqlite3
from PIL import Image
import numpy as np
from imagehash import average_hash

# Database functions
def create_database(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS video_data (
            filename TEXT,
            average_hash TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_data(db_path, filename, average_hash):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('INSERT INTO video_data (filename, average_hash) VALUES (?, ?)', (filename, average_hash))
    conn.commit()
    conn.close()

# Video processing functions
def is_video_file(filename):
    return filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv'))

def is_valid_video(video_path):
    try:
        video = cv2.VideoCapture(video_path)
        if not video.isOpened():
            return False
        success, _ = video.read()
        video.release()
        return success
    except Exception as e:
        error_message = str(e)
        if "Input buffer exhausted before END element found" in error_message or \
           "Overread VUI by" in error_message:
            return False
        return False

def calculate_average_hash(video_path):
    video = cv2.VideoCapture(video_path)
    hashes = []
    while True:
        success, frame = video.read()
        if not success:
            break
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        hash = average_hash(pil_image)
        hashes.append(hash)
    video.release()
    if hashes:
        return str(np.mean(hashes))
    return None

def generate_random_hash(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def get_video_stats(video_path):
    video = cv2.VideoCapture(video_path)
    length = int(video.get(cv2.CAP_PROP_FRAME_COUNT)) / video.get(cv2.CAP_PROP_FPS)
    frame_rate = video.get(cv2.CAP_PROP_FPS)
    resolution = f"{int(video.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))}"
    video.release()
    return length, frame_rate, resolution

def rename_video_file(file_path):
    length, frame_rate, resolution = get_video_stats(file_path)
    hash_str = generate_random_hash()
    new_file_name = f"{length:.2f}s_{frame_rate:.2f}fps_{resolution}_{hash_str}{os.path.splitext(file_path)[1]}"
    new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
    os.rename(file_path, new_file_path)
    print(f"Renamed '{os.path.basename(file_path)}' to '{os.path.basename(new_file_path)}'")

def clean_and_rename_folder(folder_path, db_path):
    create_database(db_path)
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if not is_video_file(filename):
            print(f"Deleting non-video file: {filename}")
            os.remove(file_path)
        elif not is_valid_video(file_path):
            print(f"Deleting corrupted or unreadable video file: {filename}")
            os.remove(file_path)
        else:
            avg_hash = calculate_average_hash(file_path)
            if avg_hash:
                insert_data(db_path, filename, avg_hash)
            rename_video_file(file_path)

# User input for the folder path and database path
folder_path = input("Enter the path to your folder: ")
db_path = input("Enter the path for your database file: ")
clean_and_rename_folder(folder_path, db_path)

print("Folder processing complete.")
