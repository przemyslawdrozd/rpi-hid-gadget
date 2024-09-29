import logging
import time
import pyautogui
from io import BytesIO
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model


class FragmentScreenTaker:
    def __init__(self, left=320, top=200, width=60, height=60):
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

    def take_screenshot_in_memory(self) -> BytesIO:
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

        # Return the in-memory object and PIL screenshot object
        return img_byte_arr, screenshot


# Load the trained model (Make sure the model is saved as 'angle_classification_model.h5')
model = load_model('angle_classification_model.h5')


def load_and_preprocess_image_from_bytes(img_byte_arr):
    """
    Convert a BytesIO image to a numpy array and preprocess it for model input.

    Args:
        img_byte_arr (BytesIO): The image in memory.

    Returns:
        np.array: The preprocessed image ready for model prediction.
    """
    img_byte_arr.seek(0)  # Reset the stream position to the beginning
    img = Image.open(img_byte_arr).convert('RGB')  # Open image and convert to RGB
    img = img.resize((60, 60))  # Resize to 60x60 as expected by the model
    img_array = np.array(img) / 255.0  # Normalize pixel values to [0, 1]
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array


def predict_direction_from_bytes(img_byte_arr):
    """
    Predict the direction angle from the screenshot (BytesIO).

    Args:
        img_byte_arr (BytesIO): The screenshot in memory.

    Returns:
        int: The predicted angle.
    """
    # Preprocess the image
    img_array = load_and_preprocess_image_from_bytes(img_byte_arr)

    # Make a prediction
    prediction = model.predict(img_array)
    direction_label = np.argmax(prediction)  # Get the class with the highest score

    # Convert the label back to the corresponding angle
    return direction_label * 10  # Label 0 corresponds to 0 degrees, 1 to 10 degrees, etc.


# Create an instance of the FragmentScreenTaker
screen_taker = FragmentScreenTaker()

# Take a screenshot and get the image in memory
img_byte_arr, screenshot = screen_taker.take_screenshot_in_memory()

# Predict the angle based on the screenshot
predicted_angle = predict_direction_from_bytes(img_byte_arr)

# Save screenshot
screenshot.save(f"save_{predicted_angle}.png")

# Print the result
print(f"Predicted direction: {predicted_angle} degrees")
