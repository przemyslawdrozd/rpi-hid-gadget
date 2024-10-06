import cv2
import numpy as np
import math
from matplotlib import pyplot as plt

def calculate_direction(image_path):
    # Step 1: Load image
    img = cv2.imread(image_path)

    # Step 2: Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Step 3: Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Step 4: Edge detection using Canny
    edges = cv2.Canny(blurred, 50, 150)

    # Step 5: Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Step 6: Select the largest contour (assumed to be the wedge)
    largest_contour = max(contours, key=cv2.contourArea)

    # Step 7: Fit a bounding box to the largest contour
    rect = cv2.minAreaRect(largest_contour)
    box = cv2.boxPoints(rect)
    box = np.int32(box)  # Fix: Use int32 instead of int0

    # Step 8: Draw the contours and the bounding box (for visualization)
    img_with_box = img.copy()
    cv2.drawContours(img_with_box, [box], 0, (0, 255, 0), 1)

    # Step 9: Calculate the center of the bounding box
    box_center_x = int((box[0][0] + box[2][0]) / 2)
    box_center_y = int((box[0][1] + box[2][1]) / 2)

    # Step 10: Calculate the center of the image
    image_center_x = img.shape[1] // 2
    image_center_y = img.shape[0] // 2

    # Step 11: Calculate the angle between the image center and the bounding box center
    delta_x = box_center_x - image_center_x
    delta_y = image_center_y - box_center_y  # Invert y-axis for correct angle calculation

    # Step 12: Calculate the angle in degrees (atan2 gives the angle in radians)
    angle = math.degrees(math.atan2(delta_y, delta_x))

    # Adjust to ensure North is 0 degrees
    direction = (angle + 360) % 360

    # Step 13: Display the image with detected wedge and direction
    plt.imshow(cv2.cvtColor(img_with_box, cv2.COLOR_BGR2RGB))
    plt.scatter([box_center_x, image_center_x], [box_center_y, image_center_y], c='red', marker='x')
    plt.title(f"Direction: {direction:.2f} degrees")
    plt.show()

    return direction

# Example usage:
# image_path = "a_s_radar_45.png"  # Git
# image_path = "corupted_w.png"  # Git
# image_path = "corupted_w.png"  # Git
image_path = "s_radar_e.png"  # Git
# image_path = "s_radar_e_dark.png"  # Wrong

direction = calculate_direction(image_path)
print(f"The direction of the wedge is {direction:.2f} degrees.")
