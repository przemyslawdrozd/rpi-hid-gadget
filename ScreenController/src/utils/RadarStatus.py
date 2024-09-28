import cv2
import numpy as np
from io import BytesIO


class RadarStatus:

    def load_image(self, img_byte_arr):
        """
        Convert BytesIO object to a numpy array and decode into an image.
        Returns:
            image (numpy.ndarray): The loaded image.
        """
        img_byte_arr.seek(0)  # Reset the BytesIO pointer to the start
        np_arr = np.frombuffer(img_byte_arr.getvalue(), np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        return image

    def determine_direction_based_on_rectangle(self, image):
        """
        Determine the direction of the yellow triangle (representing direction) in the image.
        Returns:
            direction (str): The direction ('N', 'S', 'E', 'W', 'NE', 'SE', 'SW', 'NW') or None if no triangle found.
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

            # Calculate the center of the bounding rectangle (green box)
            rect_center_x = int(np.mean([point[0] for point in box]))
            rect_center_y = int(np.mean([point[1] for point in box]))

            # Compare the bounding box center with the image center
            direction = self._determine_quadrant((rect_center_x, rect_center_y), image_center)
            print(f'Triangle is located towards: {direction}')
            return direction
        else:
            print("No triangle found.")
            return None

    def _determine_quadrant(self, rect_center, image_center):
        rect_x, rect_y = rect_center
        image_center_x, image_center_y = image_center

        vertical_threshold = 5
        horizontal_threshold = 5

        if abs(rect_x - image_center_x) < horizontal_threshold and rect_y < image_center_y:
            return "N"
        elif abs(rect_x - image_center_x) < horizontal_threshold and rect_y > image_center_y:
            return "S"
        elif rect_x > image_center_x and abs(rect_y - image_center_y) < vertical_threshold:
            return "E"
        elif rect_x > image_center_x and rect_y < image_center_y:
            return "NE"
        elif rect_x > image_center_x and rect_y > image_center_y:
            return "SE"
        elif rect_x < image_center_x and abs(rect_y - image_center_y) < vertical_threshold:
            return "W"
        elif rect_x < image_center_x and rect_y < image_center_y:
            return "NW"
        elif rect_x < image_center_x and rect_y > image_center_y:
            return "SW"

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
