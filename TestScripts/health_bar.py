import cv2
import numpy as np
from PIL import Image


def calculate_red_bar_percentage(img_byte_arr):
    # Convert the in-memory image (BytesIO) to a numpy array
    img_byte_arr.seek(0)  # Ensure you're reading from the start of the BytesIO object
    pil_image = Image.open(img_byte_arr)

    # Convert the PIL image to a format OpenCV can work with (numpy array)
    image = np.array(pil_image)

    # Convert RGB (PIL format) to BGR (OpenCV format)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the HSV range for detecting red color
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])

    # Create a mask for the red color
    red_mask = cv2.inRange(hsv_image, lower_red, upper_red)

    # Find the total width of the bar (both red and empty parts)
    bar_height, bar_width = red_mask.shape
    print("bar_height", bar_height)
    print("bar_width", bar_width)

    # Find the number of red pixels
    red_pixels = cv2.countNonZero(red_mask)

    # Calculate the percentage of red pixels
    red_percentage = (red_pixels / bar_width) * 100

    return red_percentage