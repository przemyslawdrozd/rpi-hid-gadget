import cv2
import numpy as np
import math
import matplotlib.pyplot as plt

def determine_direction_based_on_rectangle(image_path, ax):
    # Step 1: Read the image and process it to get the mask
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    # Get the center of the image
    image_center = (width // 2, height // 2)

    # Define a Region of Interest (ROI) around the center
    roi_size = 100  # Adjust the size based on your image and expected triangle size
    roi_x1 = max(0, image_center[0] - roi_size)
    roi_y1 = max(0, image_center[1] - roi_size)
    roi_x2 = min(width, image_center[0] + roi_size)
    roi_y2 = min(height, image_center[1] + roi_size)

    # Crop the image to focus on the ROI
    roi = image[roi_y1:roi_y2, roi_x1:roi_x2]

    # Convert to HSV for color segmentation
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Adjust the color range to focus on the faded triangle
    lower_yellow = np.array([15, 50, 50])  # Adjusted lower bound for faded yellow
    upper_yellow = np.array([35, 255, 255])  # Adjusted upper bound for faded yellow
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Apply additional morphological operations to reduce noise and background interference
    kernel = np.ones((5, 5), np.uint8)
    mask_cleaned = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask_cleaned = cv2.morphologyEx(mask_cleaned, cv2.MORPH_CLOSE, kernel)

    # Find contours within the ROI
    contours, _ = cv2.findContours(mask_cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Assume the largest contour is the triangle
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)

        # Step 5: Calculate the bounding box
        rect = cv2.minAreaRect(largest_contour)  # Get the minimum bounding box
        box = cv2.boxPoints(rect)
        box = np.int32(box)

        # Adjust the coordinates of the bounding box to fit the full image
        box[:, 0] += roi_x1
        box[:, 1] += roi_y1

        # Calculate the center of the bounding rectangle (green box)
        rect_center_x = int(np.mean([point[0] for point in box]))
        rect_center_y = int(np.mean([point[1] for point in box]))

        # Step 6: Compare the bounding box center with the image center
        direction = calculate_angle_in_degrees((rect_center_x, rect_center_y), image_center)
        print(f'Triangle is located towards: {direction}')

        # Optional: Draw the bounding box and the center point for visualization
        cv2.drawContours(image, [box], 0, (0, 255, 0), 2)
        cv2.circle(image, (rect_center_x, rect_center_y), 5, (255, 0, 0), -1)

        # Display the image with Matplotlib
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB for Matplotlib
        ax.imshow(image_rgb)
        ax.set_title(f"Direction: {direction}°")

    else:
        print("No triangle found.")
        ax.set_title("No triangle found")
        ax.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))



def calculate_angle_in_degrees(rect_center, image_center):
    rect_x, rect_y = rect_center
    image_center_x, image_center_y = image_center

    # Calculate the angle in radians between the two points
    angle_radians = math.atan2(rect_y - image_center_y, rect_x - image_center_x)

    # Convert the angle from radians to degrees
    angle_degrees = math.degrees(angle_radians)

    # Adjust the angle to make "North" (upward) be 0 degrees and go clockwise
    angle_degrees = (angle_degrees + 90) % 360

    return int(angle_degrees)

# Example usage:
# image_paths = ['marked_71.png', 'corupted_w.png', 's_radar_e_dark.png']
image_paths = ['a_s_radar_45.png','save_N.png', 's_radar_ne_hq.png']

# Create a plot to display all images
fig, axes = plt.subplots(1, len(image_paths), figsize=(15, 5))

# Loop through all images and plot each one
for i, image_path in enumerate(image_paths):
    determine_direction_based_on_rectangle(image_path, axes[i])

plt.tight_layout()
plt.show()
