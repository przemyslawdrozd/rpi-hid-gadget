import os
from collections import defaultdict


def process_files_and_print(directory):
    # Dictionary to store counts for each angle
    angle_counts = defaultdict(int)

    # Get all files in the directory
    files = os.listdir(directory)

    # Count the number of files
    total_files = len(files)

    # Process each file
    for file in files:
        # Assuming filenames are in the format "save-<timestamp>_<angle>.png"
        if file.endswith(".png"):
            try:
                # Extract the angle part from the filename
                angle = int(file.split('_')[-1].split('.')[0])
                # Increment the count for the corresponding angle
                angle_counts[angle] += 1
            except ValueError:
                # In case there is an issue parsing the angle
                print(f"Skipping file due to invalid format: {file}")

    # Print the results
    print(f"Total Files: {total_files}")
    print(f"{'Angle':<10}{'Count':<10}")

    # Print the angle counts (0 to 360 in steps of 10)
    for angle in range(0, 361, 10):
        count = angle_counts.get(angle, 0)
        print(f"{angle:<10}{count:<10}")


# Example usage
directory_path = './training_data'  # Replace with your directory path
process_files_and_print(directory_path)
