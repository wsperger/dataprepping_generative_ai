import os
import cv2
from datetime import datetime, timedelta

def is_jpeg_corrupted(file_path):
    # Function to check if JPEG file is corrupted
    try:
        with open(file_path, 'rb') as file:
            file.seek(-2, 2)
            return file.read() != b'\xff\xd9'  # JPEG files should end with these bytes
    except IOError:
        return True

def process_image(file_path):
    try:
        if file_path.lower().endswith('.jpg') or file_path.lower().endswith('.jpeg'):
            if is_jpeg_corrupted(file_path):
                raise IOError("Corrupt JPEG file.")

        image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
        if image is None:
            raise IOError("Invalid or corrupt file.")

        if len(image.shape) == 2 or image.shape[2] == 1:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
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
