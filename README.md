# DataPrepping_Generative_AI: A One-Stop Shop for Dataset Preparation

<p align="left">
  <img src="assets/images/prod_assets/Repo_logo_ps.png" alt="DataPrepping_Generative_AI Logo" style="float: left; width: 200px; margin-right: 20px;"/>
</p>

Welcome to DataPrepping_Generative_AI, a comprehensive suite of tools meticulously crafted to assist in the meticulous task of preparing datasets for cutting-edge generative AI models like StyleGAN3.

Our project is dedicated to simplifying the intricate process of dataset preparation, which is a critical step in the development of advanced generative AI systems. We understand that data annotation, cleaning, and transformation are often time-consuming and challenging tasks. Therefore, DataPrepping_Generative_AI is designed to be your trusted companion in this journey, offering a wide array of capabilities to ease your workload.

DataPrepping_Generative_AI is a versatile toolkit that has been thoughtfully designed to cater to the multifaceted needs of researchers and developers in the field of generative AI. We recognize the importance of high-quality data for training robust and accurate generative models. As such, our toolkit encompasses a diverse set of scripts and utilities that cover various aspects of data preparation, ensuring that your datasets are well-prepared and ready for the training process.

## Current Focus

- Image Processing: Our toolkit provides a range of scripts and utilities to process and manipulate image data, making it suitable for generative AI model training.

- Data Annotation: We offer tools for annotating images, facilitating the creation of labeled datasets for supervised learning tasks.

- Data Cleaning: Our scripts help clean and prepare image datasets by addressing various issues, enhancing data quality.

## Future Expansion

We have a roadmap for expanding our toolkit to cover additional data types:

- Video Processing: We plan to extend our capabilities to handle video data, including frame extraction, annotation, and video-specific data cleaning.

- Audio Processing: Our toolkit will include tools for processing audio data, enabling the preparation of audio datasets for generative AI models.

- Text Data: We aim to incorporate text data processing, supporting natural language processing (NLP) tasks within generative AI.

DataPrepping_Generative_AI is committed to becoming a comprehensive one-stop shop for all your dataset preparation needs in the field of generative AI. Stay tuned for updates and enhancements as we continue to evolve.


## Project Structure
DataPrepping_Generative_AI Project Structure (Dark Mode):

      📂 scss
      📂 dataprepping_generative_ai
      │
      ├── 📄 README.md
      ├── 📄 requirements.txt
      │
      ├── 📂 Images
      │   ├── 📂 data_extraction_cleaning
      │   │   ├── 📄 JPEGCorruptionCleaner.py
      │   │   ├── 📂 other
      │   │   └── 📂 telegram
      │   │       ├── 📄 delete_files_with_thumb.py
      │   │       └── 📄 telegram_cleaner.py
      │   │
      ├── 📂 General
      │   ├── 📄 colourchannelfix.py
      │   ├── 📄 colourchannels.py
      │   ├── ...
      │   ├── 📄 ImageCorruptionFilter.py
      │   ├── 📄 ImageMover.py
      │   ├── 📄 image_data.csv
      │   ├── 📄 image_data.db
      │   ├── ...
      │   └── 📄 test2.py
      │
      └── 📂 labelling
          ├── 📄 db_utils.py
          ├── 📄 helpers_config.txt
          ├── 📄 image_data_labels.db
          ├── 📄 labeling.md
          ├── 📄 labelling.py
          ├── 📄 main.py
          ├── 📄 tempdoc.txt
          ├── 📂 annotation_helpers
          │   ├── 📄 clothes_detection.py
          │   ├── 📄 description.py
          │   ├── ...
          │   └── 📄 pose_estimation.py
          │
          └── 📂 models
          
      📂 Storage
          
      📂 Videos
          └── 📄 checkvalid.py


## Setup and Installation

### Dependencies

- Python 3.8 or higher
- Libraries: torch, transformers, opencv-python, sqlite3, PIL, etc.
- Additional dependencies as per individual helper module requirements.

### Installation Steps

1. Clone this repository.
2. Navigate to the `dataprepping_generative_ai` directory.
3. Install required Python libraries: `pip install -r requirements.txt`.
4. Download and place necessary model files in the `Images/labelling/models/` directory.

## Usage

### Running the Main Script

`main.py` in the `labelling` directory coordinates the processing of images and videos. It uses helper functions from `annotation_helpers/` for specific annotations. Annotation results are stored in an SQLite database via `db_utils.py`.

### Database Utilities

`db_utils.py` handles all database operations, including table creation, data insertion, and batch processing.

### Annotation Helpers

Each helper module in `annotation_helpers/` specializes in a specific type of annotation. Modules can be activated individually in `main.py`.

## Key Features

- Face Detection (`face_detection.py`): Implements face detection using OpenFace or InsightFace. Detected faces and landmarks are written to the SQLite database.
- Description Generation (`description.py`): Generates detailed image descriptions using the BLIP model.
- Video Processing (`Videos/checkvalid.py`): Functions to validate and process video files, extracting frames and annotations.

## Contributing

We welcome contributions to DataPrepping_Generative_AI. Please ensure that your contributions align with the project's structure and coding style. For significant changes, we encourage opening an issue first to discuss what you would like to change or add.
