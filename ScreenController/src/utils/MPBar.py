import logging

import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import pygame
from ..consts import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)
class MPBar:
    def __init__(self, prefix):
        # Adjust these values to better capture your specific blue shade range
        self.lower_blue = np.array([100, 100, 100])  # Adjust hue, saturation, and value as needed
        self.upper_blue = np.array([140, 255, 255])  # Adjust upper range as needed
        # self.cp_sound_file = "files/cp.mp3"
        self.prefix = prefix

        # Initialize the pygame mixer
        pygame.mixer.init()

    def calculate_percentage(self, img_byte_arr: BytesIO):
        # Convert BytesIO to a numpy array
        img = Image.open(img_byte_arr)
        img_np = np.array(img)

        # Convert the image to OpenCV format (BGR)
        image = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        # Convert the image to HSV (Hue, Saturation, Value) color space
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Create a mask that identifies all the pixels within the blue range
        mask = cv2.inRange(hsv_image, self.lower_blue, self.upper_blue)

        # Calculate the percentage of blue pixels
        blue_pixels = cv2.countNonZero(mask)
        logger.debug(f"blue_pixels: {blue_pixels}")
        total_pixels = image.shape[0] * image.shape[1]
        logger.debug(f"total_pixels: {total_pixels}")
        # percentage = int((blue_pixels / total_pixels) * MP_PREFIX)
        percentage = int((blue_pixels / total_pixels) * self.prefix)
        
        logger.debug(f"MP: {percentage}")
        return percentage

    def __invoke_alert(self) -> None:
        # Load the sound file
        pygame.mixer.music.load(self.cp_sound_file)

        # Play the sound
        pygame.mixer.music.play()
