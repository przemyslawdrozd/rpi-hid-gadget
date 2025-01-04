import logging

import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import pygame
from ..consts import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

class HPBar:
    def __init__(self, prefix):
        # Adjust these values to better capture your specific blue shade range
        self.lower_red = np.array([0, 120, 70])
        self.upper_red = np.array([10, 255, 255]) 
        
        # Initialize the pygame mixer
        # pygame.mixer.init()

        self.prefix = prefix

    def calculate_percentage(self, img_byte_arr: BytesIO):
        # Convert BytesIO to a numpy array
        img = Image.open(img_byte_arr)
        img_np = np.array(img)

        # Convert the image to OpenCV format (BGR)
        image = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        # Convert the image to HSV (Hue, Saturation, Value) color space
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Create a mask that identifies all the pixels within the blue range
        mask = cv2.inRange(hsv_image, self.lower_red, self.upper_red)

        # Calculate the percentage of blue pixels
        red_pixels = cv2.countNonZero(mask)
        logger.debug(f"red_pixels: {red_pixels}")
        total_pixels = image.shape[0] * image.shape[1]
        logger.debug(f"HP total_pixels: {total_pixels}")
        percentage = int((red_pixels / total_pixels) * self.prefix)
        
        logger.debug(f"HP: {percentage}")
        return percentage

    def __invoke_alert(self) -> None:
        # Load the sound file
        pygame.mixer.music.load(self.cp_sound_file)

        # Play the sound
        pygame.mixer.music.play()
