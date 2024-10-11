import cv2
import numpy as np
from PIL import Image
from io import BytesIO

class CPBar:
    def __init__(self):
        # Adjusted HSV range for detecting the color in the new images
        self.lower_color = np.array([90, 80, 50])
        self.upper_color = np.array([110, 160, 120])


    def calculate_orange_percentage(self, img_byte_arr):
        # Convert BytesIO to a numpy array
        img = Image.open(img_byte_arr)
        img_np = np.array(img)

        # Convert the image to OpenCV format (BGR)
        image = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

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