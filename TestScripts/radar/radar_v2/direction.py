import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
import math

# Function to calculate the direction and place green dots at the triangle's edges
class TriangleDirectionCalculator:
    def __init__(self, image_path):
        self.image_path = image_path

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

    def calculate_direction(self):
        # Read the image
        img = cv2.imread(self.image_path)

        # Convert to HSV color space to filter the yellowish triangle
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Define lower and upper bounds for the yellowish color in HSV
        lower_yellow = np.array([10, 40, 100])
        upper_yellow = np.array([40, 255, 255])

        # Create a mask for the yellowish color
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Apply the mask to the image to keep only yellowish regions
        masked_img = cv2.bitwise_and(img, img, mask=mask)

        # Convert the masked image to grayscale for edge detection
        gray = cv2.cvtColor(masked_img, cv2.COLOR_BGR2GRAY)

        # Apply GaussianBlur to reduce noise and improve edge detection
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply Canny edge detector with a lower threshold for better edge detection
        edges = cv2.Canny(blurred, 20, 80)

        # Find contours of the detected edges
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            # Assuming the largest contour corresponds to the triangle
            largest_contour = max(contours, key=cv2.contourArea)

            # Get the moments of the contour to find its centroid
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])  # Centroid X
                cy = int(M["m01"] / M["m00"])  # Centroid Y

                # Get image center
                h, w = img.shape[:2]
                image_center = (w // 2, h // 2)

                # Get the corners (approximation of the triangle shape)
                epsilon = 0.05 * cv2.arcLength(largest_contour, True)  # Increase approximation tolerance
                approx = cv2.approxPolyDP(largest_contour, epsilon, True)

                if len(approx) >= 3:
                    # Find the point furthest from the centroid, which should be the valid direction tip
                    max_distance = 0
                    tip_point = None
                    for point in approx:
                        px, py = point[0]
                        distance = np.sqrt((px - cx)**2 + (py - cy)**2)
                        if distance > max_distance:
                            max_distance = distance
                            tip_point = (px, py)

                    if tip_point:
                        # Calculate the direction using the custom angle function
                        direction_degrees = self._calculate_angle_in_degrees(tip_point, image_center)

                        # Draw the contour and the tip/centroid points
                        img_contour = cv2.drawContours(img.copy(), [largest_contour], -1, (0, 255, 0), 1)
                        img_direction = cv2.circle(img_contour, tip_point, 2, (255, 0, 0), -1)  # Mark the valid direction (red dot)
                        img_direction = cv2.circle(img_direction, (cx, cy), 2, (0, 0, 255), -1)  # Centroid (blue dot)

                        # Add green dots to the 3 furthest corners of the triangle
                        corner_points = sorted(approx, key=lambda p: np.sqrt((p[0][0] - cx)**2 + (p[0][1] - cy)**2), reverse=True)[:3]
                        for point in corner_points:
                            px, py = point[0]
                            img_direction = cv2.circle(img_direction, (px, py), 2, (0, 255, 0), -1)  # Green dots for triangle corners

                        # Plot the original image, edge-detected image, and final image with direction and edge dots
                        fig, axs = plt.subplots(1, 3, figsize=(15, 5))
                        axs[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                        axs[0].set_title('Original Image')
                        axs[0].axis('off')

                        axs[1].imshow(edges, cmap='gray')
                        axs[1].set_title('Edge Detected Image (Masked)')
                        axs[1].axis('off')

                        axs[2].imshow(cv2.cvtColor(img_direction, cv2.COLOR_BGR2RGB))
                        axs[2].set_title(f'Direction: {direction_degrees:.2f}°')
                        axs[2].axis('off')

                        plt.show()

                        return direction_degrees
                else:
                    print("Could not detect 3 or more corners.")
                    return None
        return None
# Function to process and plot all images in the radar_data directory
def process_images_in_directory(directory_path):
    # Iterate through all files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            image_path = os.path.join(directory_path, filename)
            print(f"Processing image: {filename}")
            tdc = TriangleDirectionCalculator(image_path)
            direction = tdc.calculate_direction()
            if direction is not None:
                print(f"Direction for {filename}: {direction:.2f}°")
            else:
                print(f"Could not detect direction for {filename}.")

# Directory path for radar_data folder
directory_path = 'radar_data'

# Run the processing on all images in the radar_data directory
process_images_in_directory(directory_path)
# Example: Running the function on an image
# image_path = 'radar_data/NW.png'  # Replace with your file path
# direction = calculate_direction_from_triangle(image_path)
# print(f"Direction: {direction} degrees")
