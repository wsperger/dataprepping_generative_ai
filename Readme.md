Image Processing Toolkit
This toolkit consists of several Python scripts, each designed for specific tasks related to image processing and organization. Below is an overview of each script and instructions for their use.

1. ColourChannelFix (colourchannelfix.py)
Description
Converts grayscale images to RGB and changes their format to PNG. Also removes any invalid or corrupted image files.

Usage
Run the script with the path of the folder containing the images.

python
Copy code
folder_location = "path/to/image/folder"
convert_to_rgb_and_png(folder_location)
2. ConsolidateTraining (consolidatetaining.py)
Description
Moves and renames image files from subdirectories into a main folder, renaming them sequentially.

Usage
Set the main_folder_path and run the script.

python
Copy code
main_folder_path = 'path/to/main/folder'
move_and_rename_images(main_folder_path)
3. DuplicateImageCleaner (DuplicateImageCleaner.py)
Description
Finds and deletes duplicate images in a directory based on their perceptual hash.

Usage
Specify the folder path and number of workers.

python
Copy code
folder_path = 'path/to/dataset'
num_workers = 40
delete_duplicates(folder_path, num_workers)
4. ImageCorruptionFilter (ImageCorruptionFilter.py)
Description
Processes images from a source folder, deletes corrupted images, logs deletions, and copies valid images to a destination folder.

Configuration
Set source_folder, destination_folder, and db_path before running the script.

5. ImageFormatConverter (ImageFormatConverter.py)
Description
Converts image files to PNG format and removes non-image files.

Usage
Specify the folder containing the images to be processed.

python
Copy code
folder_path = 'path/to/images'
clean_and_convert_to_png(folder_path)
6. ImageMover (ImageMover.py)
Description
Moves image files from a source folder to a destination folder.

Usage
Set source_folder_path and destination_folder_path.

python
Copy code
source_folder_path = 'path/to/source'
destination_folder_path = 'path/to/destination'
move_images(source_folder_path, destination_folder_path)
7. JPEGCorruptionCleaner (JPEGCorruptionCleaner.py)
Description
Identifies and deletes corrupt JPEG files.

Usage
Run with the folder path containing JPEG files.

python
Copy code
folder_location = "path/to/jpeg/folder"
delete_corrupt_jpegs(folder_location)
8. SmallFileCleaner (SmallFileCleaner.py)
Description
Deletes files smaller than a specified size threshold.

Usage
Set the directory and size threshold (in KB).

python
Copy code
folder_path = "path/to/folder"
delete_small_files(folder_path, size_threshold_kb)
9. TelegramCleaner (telegramcleaner.py)
Description
Organizes exported chat data by moving photos and videos to main directories and deleting unwanted files.

Usage
Set the main_folder path to the location of your chat exports.

python
Copy code
main_folder = 'path/to/chat/exports'
process_chat_exports(main_folder)
General Notes
Backup your data before using these scripts as they may move, rename, or delete files.
Modify the paths in the script according to your directory structure.
Ensure you have the required libraries installed (cv2, PIL, sqlite3, etc.)

1. For 32x32 resolution:
   ```python
   dataset_tool.py --source="D:\Dataset\training" --dest=D:\Dataset\CleanDatasSetsfortraining\01dataset-32x32.zip --resolution=32x32
For 64x64 resolution:

python
Copy code
dataset_tool.py --source="D:\Dataset\training" --dest=D:\Dataset\CleanDatasSetsfortraining\02dataset-64x64.zip --resolution=64x64
For 128x128 resolution:

python
Copy code
dataset_tool.py --source="D:\Dataset\training" --dest=D:\Dataset\CleanDatasSetsfortraining\03dataset-128x128.zip --resolution=128x128
For 256x256 resolution:

python
Copy code
dataset_tool.py --source="D:\Dataset\training" --dest=D:\Dataset\CleanDatasSetsfortraining\04dataset-256x256.zip --resolution=256x256
For 512x512 resolution:

python
Copy code
dataset_tool.py --source="D:\Dataset\training" --dest=D:\Dataset\CleanDatasSetsfortraining\05dataset-512x512.zip --resolution=512x512
For 1024x1024 resolution:

python
Copy code
dataset_tool.py --source="D:\Dataset\training" --dest=D:\Dataset\CleanDatasSetsfortraining\06dataset-1024x1024.zip --resolution=1024x1024
For 2048x2048 resolution:

python
Copy code
dataset_tool.py --source="D:\Dataset\training" --dest=D:\Dataset\CleanDatasSetsfortraining\07dataset-2048x2048.zip --resolution=2048x2048
For 4096x4096 (4K) resolution:

python
Copy code
dataset_tool.py --source="D:\Dataset\training" --dest=D:\Dataset\CleanDatasSetsfortraining\08dataset-4096x4096.zip --resolution=4096x4096
vbnet
Copy code

You can copy and paste these commands into a markdown file or a markdown editor to ma