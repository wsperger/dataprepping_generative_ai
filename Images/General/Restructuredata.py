import os
import sqlite3
import time
from PIL import Image
from datetime import datetime
import json
from concurrent.futures import ProcessPoolExecutor, as_completed
import torch
from torchvision.transforms import functional as TF

# Global variables
db_path = "image_data.db"
batch_size = 100
json_output = "image_data.json"

# Database functions
def create_database():
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS image_data (
                filename TEXT,
                dimensions TEXT,
                mode TEXT,
                timestamp TEXT,
                status TEXT,
                error_message TEXT
            )
        ''')
        conn.commit()

def insert_batch_data(batch_data):
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.executemany('INSERT INTO image_data (filename, dimensions, mode, timestamp, status, error_message) VALUES (?, ?, ?, ?, ?, ?)',
                      batch_data)
        conn.commit()

# Image processing functions
def is_image_file(filename):
    return filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))

# Function to process image using PyTorch (GPU if available)
def process_image_with_torch(file_path):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    try:
        # Load image with PIL and convert to PyTorch tensor
        pil_image = Image.open(file_path)
        torch_image = TF.to_tensor(pil_image).unsqueeze(0).to(device)

        # Process the image as required (example: resize)
        # Example: resized_image = TF.resize(torch_image, (new_height, new_width))

        # Convert back to PIL for saving
        pil_image = TF.to_pil_image(torch_image.cpu().squeeze(0))

        dimensions = f"{pil_image.width}x{pil_image.height}"
        mode = pil_image.mode
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        new_filename = f"{os.path.splitext(os.path.basename(file_path))[0]}_{dimensions}_{mode}.jpg"
        new_file_path = os.path.join(os.path.dirname(file_path), new_filename)

        pil_image.save(new_file_path)

        if new_file_path != file_path:
            os.remove(file_path)

        return new_filename, dimensions, mode, timestamp, "Processed", None
    except Exception as e:
        error_message = f"Error processing {os.path.basename(file_path)}: {str(e)}"
        if os.path.exists(file_path):
            os.remove(file_path)
        return os.path.basename(file_path), "", "", "", "Error", error_message

# Adjusted function to use ProcessPoolExecutor
def process_folder_parallel(folder_path):
    start_time = time.time()
    create_database()

    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if is_image_file(f)]
    total_files = len(files)
    batch_data = []

    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(process_image_with_torch, file_path): file_path for file_path in files}
        processed_count = 0
        for future in as_completed(futures):
            result = future.result()
            batch_data.append(result)

            processed_count += 1
            print(f"Processed {processed_count}/{total_files} files ({(processed_count/total_files)*100:.2f}%)")

            if len(batch_data) >= batch_size:
                insert_batch_data(batch_data)
                batch_data = []

    if batch_data:
        insert_batch_data(batch_data)

    elapsed_time = time.time() - start_time
    print(f"Processed {total_files} files in {elapsed_time:.2f} seconds")

def save_json_data():
    with sqlite3.connect(db_path) as conn, open(json_output, 'w') as json_file:
        c = conn.cursor()
        c.execute("SELECT filename, dimensions, mode, timestamp, status, error_message FROM image_data")
        rows = c.fetchall()
        json_data = [{
            "filename": row[0],
            "dimensions": row[1],
            "mode": row[2],
            "timestamp": row[3],
            "status": row[4],
            "error_message": row[5]
        } for row in rows]
        json.dump(json_data, json_file, indent=4)

# Main execution
if __name__ == "__main__":
    folder_location = input("Enter the path to your image folder: ")
    process_folder_parallel(folder_location)
    save_json_data()
    print("Image folder processing and JSON data saving complete.")
