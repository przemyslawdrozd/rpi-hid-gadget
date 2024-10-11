import cv2
import numpy as np


def calculate_orange_percentage(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to HSV (Hue, Saturation, Value) color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range for orange color in HSV
    lower_orange = np.array([5, 50, 50])  # Lower bound for orange hue
    upper_orange = np.array([20, 255, 255])  # Upper bound for orange hue

    # Create a mask that identifies all the orangeish pixels
    mask = cv2.inRange(hsv_image, lower_orange, upper_orange)

    # Calculate the percentage of orangeish pixels
    orange_pixels = cv2.countNonZero(mask)
    total_pixels = image.shape[0] * image.shape[1]
    percentage_orange = (orange_pixels / total_pixels) * 100

    return percentage_orange


# Test the function on your images
image_paths = ["cp-100.png", "cp-85.png", "cp-15.png"]
for path in image_paths:
    percentage = calculate_orange_percentage(path)
    print(f"{path}: {percentage:.2f}% orange")
