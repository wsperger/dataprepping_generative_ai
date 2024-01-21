import os

def delete_files_with_thumb(folder_path):
    try:
        for filename in os.listdir(folder_path):
            if "thumb" in filename.lower():
                file_path = os.path.join(folder_path, filename)
                os.remove(file_path)
                print(f"Deleted: {file_path}")
        print("Deletion complete.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    folder_path = "location"
    delete_files_with_thumb(folder_path)
