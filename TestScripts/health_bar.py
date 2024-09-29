import cv2
import numpy as np
from PIL import Image
from io import BytesIO

BAR_PREFIX = 37


class HealthBar:
    def __init__(self):
        # Initialize HSV range for detecting red color
        self.lower_red = np.array([0, 120, 70])
        self.upper_red = np.array([10, 255, 255])

    def calculate_red_bar_percentage(self, img_byte_arr: BytesIO) -> int:
        """
        Processes an image to calculate the percentage of red in the health bar.

        Args:
            img_byte_arr: A BytesIO object containing the image.

        Returns:
            int: The approximate percentage of red in the health bar.
        """
        # Convert the in-memory image (BytesIO) to a numpy array
        img_byte_arr.seek(0)  # Ensure you're reading from the start of the BytesIO object
        pil_image = Image.open(img_byte_arr)

        # Convert the PIL image to a format OpenCV can work with (numpy array)
        image = np.array(pil_image)

        # Convert RGB (PIL format) to BGR (OpenCV format)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Convert the image to HSV color space
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Create a mask for the red color using initialized HSV range
        red_mask = cv2.inRange(hsv_image, self.lower_red, self.upper_red)

        # Find the total width of the bar (both red and empty parts)
        bar_height, bar_width = red_mask.shape

        # Find the number of red pixels
        red_pixels = cv2.countNonZero(red_mask)

        # Calculate the percentage of red pixels
        approx_percentage = (red_pixels / bar_width) * BAR_PREFIX

        return int(approx_percentage)


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

    # Find the number of red pixels
    red_pixels = cv2.countNonZero(red_mask)

    bar_prefix = 37

    # Calculate the percentage of red pixels
    approx_percentage = (red_pixels / bar_width) * bar_prefix

    return int(approx_percentage)
