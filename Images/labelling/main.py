# This is the main file executing the labelling logic

import os
import subprocess
import importlib.util

# Define the paths
CONFIG_FILE = 'Images/labelling/helpers_config.txt'
MODELS_DIR = 'Images/labelling/models'
HELPERS_DIR = 'Images/labelling/annotation_helpers'
IMAGES_DIR = 'F:/test'

def clone_repository(repo_url, model_name):
    """
    Clone a Git repository into the specified directory within the 'models' directory.
    """
    # Use MODELS_DIR to construct the path dynamically
    model_path = os.path.join(MODELS_DIR, model_name)
    if not os.path.exists(model_path):
        print(f"Cloning {model_name} from {repo_url} into {model_path}")
        subprocess.run(["git", "clone", repo_url, model_path], check=True)
    else:
        print(f"{model_name} already cloned.")

def load_helper(helper_name):
    """ Dynamically load a helper module by name. """
    module_path = os.path.join(HELPERS_DIR, f"{helper_name}.py")
    spec = importlib.util.spec_from_file_location(helper_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def process_images_with_helpers(helpers):
    """ Process each image in the directory with each loaded helper. """
    for image_file in os.listdir(IMAGES_DIR):
        image_path = os.path.join(IMAGES_DIR, image_file)
        if os.path.isfile(image_path):
            print(f"Processing {image_path}")
            for helper_name, helper_module in helpers.items():
                print(f"Using {helper_name} on {image_path}")
                # Assuming each helper module has a function named `process_image`
                helper_module.process_image(image_path)

def main():
    # Ensure the models directory exists
    os.makedirs(MODELS_DIR, exist_ok=True)

    # Read the helpers config file
    if not os.path.isfile(CONFIG_FILE):
        print(f"No config file found at {CONFIG_FILE}")
        return

    helpers = {}
    with open(CONFIG_FILE, 'r') as file:
        for line in file:
            if line.strip():
                helper_name, repo_url = line.strip().split(',')
                clone_repository(repo_url, helper_name)
                helpers[helper_name] = load_helper(helper_name)

    if helpers:
        process_images_with_helpers(helpers)
    else:
        print("No helpers loaded.")

if __name__ == "__main__":
    main()
