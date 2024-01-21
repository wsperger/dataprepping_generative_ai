# annotation_helpers/face_detection.py
import os
import subprocess
import sqlite3

# Assuming the OpenFace binary is in the cloned OpenFace directory under `models`
OPENFACE_DIR = os.path.join('..', 'models', 'OpenFace')
OPENFACE_BINARY = os.path.join(OPENFACE_DIR, 'build', 'bin', 'FaceLandmarkImg')

DB_PATH = os.path.join('..', 'image_data_labels.db')

def detect_faces(image_path):
    """
    Uses OpenFace to detect faces and facial landmarks in an image.
    """
    output_dir = os.path.join('..', 'processed_images')
    os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists
    
    command = [
        OPENFACE_BINARY,
        '-f', image_path,
        '-out_dir', output_dir
    ]
    
    try:
        # Run the OpenFace face detection command
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Face detection completed for {image_path}")
        # You would need to add code to parse the output and extract the facial landmark data
        # For this example, we'll just return a dummy string
        return "landmark data"
    except subprocess.CalledProcessError as e:
        print(f"OpenFace failed to process {image_path}: {e}")
        return None

def write_to_db(image_path, landmark_data):
    """
    Writes the detected facial landmarks to the SQLite database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Assuming a table structure for your landmarks like so:
    # CREATE TABLE facial_landmarks (id INTEGER PRIMARY KEY, image_path TEXT, landmark_data TEXT);
    cursor.execute(
        "INSERT INTO facial_landmarks (image_path, landmark_data) VALUES (?, ?)",
        (image_path, landmark_data)
    )
    
    conn.commit()
    conn.close()

def process_image(image_path):
    """
    Process an image for face detection and write results to the database.
    """
    landmark_data = detect_faces(image_path)
    if landmark_data:
        write_to_db(image_path, landmark_data)
