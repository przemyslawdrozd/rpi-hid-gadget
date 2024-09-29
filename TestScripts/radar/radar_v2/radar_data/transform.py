import os
import shutil

# Function to scan the directory, rename files, and move them
def scan_and_move_files(source_dir, destination_dir, prefix="triangle_"):
    # Create destination directory if it doesn't exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # List all files in the source directory
    for index, filename in enumerate(os.listdir(source_dir)):
        # Create full path to the file
        source_file_path = os.path.join(source_dir, filename)

        # Check if it's a file (not a directory)
        if os.path.isfile(source_file_path):
            # Generate new filename (can adjust the pattern as needed)
            new_filename = f"{prefix}{index + 1}{os.path.splitext(filename)[1]}"

            # Full path to the destination file
            destination_file_path = os.path.join(destination_dir, new_filename)

            # Move and rename the file
            shutil.move(source_file_path, destination_file_path)
            print(f"Moved: {filename} -> {new_filename}")

# Example usage
source_directory = "./"
destination_directory = "/training_data"

scan_and_move_files(source_directory, destination_directory)
