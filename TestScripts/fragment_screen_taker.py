import logging
import time
import pyautogui
from io import BytesIO


class FragmentScreenTaker:
    def __init__(self, left=400, top=100, width=360, height=80):
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
        screenshot.save(f"save_{start_time}.png")

        # Return the in-memory object
        return img_byte_arr, screenshot
