import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import pygame

CP_PREFIX = 130


class CPBar:
    def __init__(self):
        self.lower_orange = np.array([5, 50, 50])  # Lower bound for orange hue
        self.upper_orange = np.array([20, 255, 255])  # Upper bound for orange hue

        self.cp_sound_file = "files/cp.mp3"

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

        # Create a mask that identifies all the pixels
        mask = cv2.inRange(hsv_image, self.lower_orange, self.upper_orange)

        # Calculate the percentage of orange pixels
        orange_pixels = cv2.countNonZero(mask)
        total_pixels = image.shape[0] * image.shape[1]
        percentage = int((orange_pixels / total_pixels) * CP_PREFIX)

        if percentage < 100:
            self.__invoke_alert()

        return percentage

    def __invoke_alert(self) -> None:
        # Load the sound file
        pygame.mixer.music.load(self.cp_sound_file)

        # Play the sound
        pygame.mixer.music.play()
