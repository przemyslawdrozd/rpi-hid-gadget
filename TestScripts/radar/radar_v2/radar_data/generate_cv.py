import os
import csv

# Function to scan a directory and create a CSV with file names and their suffixes
def create_csv_from_filenames(directory, output_csv):
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['image_filename', 'angle'])  # Header row
        # target_angles = {"0", "90", "180", "270"}
        # Iterate over all files in the directory
        for filename in os.listdir(directory):
            if filename.endswith(".png"):
                # Extract suffix from filename (assuming it's after the underscore)
                parts = filename.split('_')
                if len(parts) > 1:
                    suffix = parts[-1].split('.')[0]  # Get the part after underscore and before the extension
                    # if suffix in target_angles:
                    writer.writerow([filename, suffix])

# Example usage
directory = 'training_data'  # Replace with your directory path
output_csv = 'labels.csv'  # Output CSV file
create_csv_from_filenames(directory, output_csv)
print(f"CSV file created: {output_csv}")

