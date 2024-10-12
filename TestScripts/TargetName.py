import time
import logging
from PIL import Image
import pytesseract
from io import BytesIO

import logging
import time
import pyautogui
from io import BytesIO
import pygame


class FragmentScreenTaker:
    def __init__(self, left=420, top=75, width=360, height=40):
        """
        Initialize the region of the screen to capture.
        Args:
            left (int): X-coordinate of the top-left corner of the region.
            top (int): Y-coordinate of the top-left corner of the region.
            width (int): Width of the region.
            height (int): Height of the region.
        """
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def take_screenshot_in_memory(self):
        """
        Takes a screenshot of a specified region and returns it as an in-memory BytesIO object.

        Returns:
            BytesIO: The screenshot saved in an in-memory BytesIO object.
        """
        logging.info("Starting screenshot process...")

        # Measure the start time
        start_time = time.time()

        # Take a screenshot of the specified region (but do not save it)
        screenshot = pyautogui.screenshot(region=(self.left, self.top, self.width, self.height))

        # Measure the time after taking the screenshot
        screenshot_time = time.time()
        logging.info(f"Screenshot taken in {screenshot_time - start_time:.4f} seconds.")

        # Convert the screenshot to an in-memory object (BytesIO)
        img_byte_arr = BytesIO()
        screenshot.save(img_byte_arr, format='PNG')

        # Return the in-memory object
        return img_byte_arr, screenshot

class TargetName:
    def extract_text_from_image(self, img_byte_arr):
        """
        Extracts text from an image provided as a BytesIO object.

        Args:
            img_byte_arr (BytesIO): Image in memory from which to extract text.

        Returns:
            str: The extracted text from the image.
        """
        # Load image from BytesIO
        img_byte_arr.seek(0)  # Reset the stream position to the start
        img = Image.open(img_byte_arr)

        # Use pytesseract to extract text from the image
        extracted_text = pytesseract.image_to_string(img)

        return extracted_text

fst = FragmentScreenTaker()
buffer, screenshot = fst.take_screenshot_in_memory()
target_name = TargetName()

res = target_name.extract_text_from_image(buffer)
print("res", res)
screenshot.save(f"save_{res}.png")
