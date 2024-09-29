import cv2
import numpy as np
from io import BytesIO
import math
from PIL import Image
from tensorflow.keras.models import load_model

class RadarStatus:

    def __init__(self):
        self.model = load_model("angle_classification_model.h5")

    def load_image(self, img_byte_arr) -> BytesIO:
        """
        Convert BytesIO object to a numpy array and decode into an image.
        Returns:
            image (numpy.ndarray): The loaded image.
        """
        img_byte_arr.seek(0)  # Reset the BytesIO pointer to the start
        np_arr = np.frombuffer(img_byte_arr.getvalue(), np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        return image

    def load_and_preprocess_image_from_bytes(self, img_byte_arr):
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

    def predict_direction_from_bytes(self, img_byte_arr):
        """
        Predict the direction angle from the screenshot (BytesIO).

        Args:
            img_byte_arr (BytesIO): The screenshot in memory.

        Returns:
            int: The predicted angle.
        """
        # Preprocess the image
        img_array = self.load_and_preprocess_image_from_bytes(img_byte_arr)

        # Make a prediction
        prediction = self.model.predict(img_array)
        direction_label = np.argmax(prediction)  # Get the class with the highest score

        # Convert the label back to the corresponding angle
        return direction_label * 10  # Label 0 corresponds to 0 degrees, 1 to 10 degrees, etc.

    def determine_direction_based_on_rectangle(self, image):
        """
        Determine the direction of the yellow triangle (representing direction) in the image.
        Returns:
            direction (float): The direction in degrees (0-360) or None if no triangle found.
        """
        height, width, _ = image.shape
        image_center = (width // 2, height // 2)

        # Convert to HSV for color segmentation
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_yellow = np.array([15, 100, 100])  # Adjusted lower bound for yellow
        upper_yellow = np.array([35, 255, 255])  # Adjusted upper bound for yellow
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Morphological operations to reduce noise
        kernel = np.ones((3, 3), np.uint8)
        mask_cleaned = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask_cleaned = cv2.morphologyEx(mask_cleaned, cv2.MORPH_CLOSE, kernel)

        # Find contours
        contours, _ = cv2.findContours(mask_cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            rect = cv2.minAreaRect(largest_contour)
            box = cv2.boxPoints(rect)
            box = np.int32(box)

            # Calculate the center of the bounding rectangle
            rect_center_x = int(np.mean([point[0] for point in box]))
            rect_center_y = int(np.mean([point[1] for point in box]))

            # Determine direction based on the angle between the centers
            direction_in_degrees = self._calculate_angle_in_degrees((rect_center_x, rect_center_y), image_center)
            print(f'Triangle is located towards: {direction_in_degrees:.2f} degrees')
            return direction_in_degrees
        else:
            print("No triangle found.")
            return None

    def _calculate_angle_in_degrees(self, rect_center, image_center):
        rect_x, rect_y = rect_center
        image_center_x, image_center_y = image_center

        # Calculate the angle in radians between the two points
        angle_radians = math.atan2(rect_y - image_center_y, rect_x - image_center_x)

        # Convert the angle from radians to degrees
        angle_degrees = math.degrees(angle_radians)

        # Adjust the angle to make "North" (upward) be 0 degrees and go clockwise
        angle_degrees = (angle_degrees + 90) % 360

        return int(angle_degrees)

    def count_red_dots(self, image):
        """
        Count the number of red dots in each quadrant of the image.
        Returns:
            quadrants (dict): A dictionary with the count of red dots in each quadrant ('NE', 'SE', 'SW', 'NW').
        """
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define color range for red (tweak these values for better accuracy)
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([180, 255, 255])

        # Mask the red dots
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        red_mask = mask1 + mask2

        # Find contours of the red dots
        contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Get image dimensions and divide into quadrants
        height, width = image.shape[:2]
        mid_x, mid_y = width // 2, height // 2

        quadrants = {'NE': 0, 'SE': 0, 'SW': 0, 'NW': 0}

        for cnt in contours:
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                # Determine which quadrant the dot is in
                if cX >= mid_x and cY <= mid_y:
                    quadrants['NE'] += 1
                elif cX >= mid_x and cY > mid_y:
                    quadrants['SE'] += 1
                elif cX < mid_x and cY > mid_y:
                    quadrants['SW'] += 1
                elif cX < mid_x and cY <= mid_y:
                    quadrants['NW'] += 1

        return quadrants
