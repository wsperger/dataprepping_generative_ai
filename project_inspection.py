import os

def print_directory_contents(path, detailed, ignored_dirs):
    """
    Print the contents of a directory, ignoring specified directories.

    Args:
    - path (str): Path of the directory to print.
    - detailed (bool): If True, prints file contents. If False, only prints file and folder names.
    - ignored_dirs (list): List of directory names to ignore.
    """
    for root, dirs, files in os.walk(path):
        # Skip ignored directories
        dirs[:] = [d for d in dirs if d not in ignored_dirs]

        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            # Skip system files
            if f.startswith('.'):
                continue
            print(f'{subindent}{f}')
            if detailed:
                try:
                    with open(os.path.join(root, f), 'r') as file:
                        content = file.read()
                        print(f'{subindent}--- File Content Start ---')
                        print(content)
                        print(f'{subindent}--- File Content End ---\n')
                except Exception as e:
                    print(f'{subindent}Could not read file: {e}')

# List of directories to ignore
ignored_dirs = ['.conda', '.idea', 'assets', 'venv', '.git']

# Ask the user for their choice
user_choice = input("Enter 'detailed' for full content or 'simple' for just structure: ").strip().lower()

# Validate user input and call the function accordingly
if user_choice == 'detailed':
    print_directory_contents('.', detailed=True, ignored_dirs=ignored_dirs)
elif user_choice == 'simple':
    print_directory_contents('.', detailed=False, ignored_dirs=ignored_dirs)
else:
    print("Invalid input. Please enter 'detailed' or 'simple'.")
