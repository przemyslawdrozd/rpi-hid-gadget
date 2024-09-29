import cv2
import numpy as np
import matplotlib.pyplot as plt
from math import atan2, degrees

# Function to calculate the direction based on the triangle's tip and centroid
def calculate_direction_with_centroid(image_path):
    # Read the image
    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and improve edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Canny edge detector
    edges = cv2.Canny(blurred, 50, 150)

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

            # Find the point furthest from the centroid, which should be the tip of the triangle
            max_distance = 0
            tip_point = None
            for point in largest_contour:
                px, py = point[0]
                distance = np.sqrt((px - cx)**2 + (py - cy)**2)
                if distance > max_distance:
                    max_distance = distance
                    tip_point = (px, py)

            if tip_point:
                # Calculate the direction using the vector from the centroid to the tip
                direction_radians = atan2(tip_point[1] - cy, tip_point[0] - cx)
                direction_degrees = (degrees(direction_radians) + 360) % 360

                # Draw the contour and the tip/centroid points
                img_contour = cv2.drawContours(img.copy(), [largest_contour], -1, (0, 255, 0), 2)
                img_direction = cv2.circle(img_contour, tip_point, 5, (255, 0, 0), -1)
                img_direction = cv2.circle(img_direction, (cx, cy), 5, (0, 0, 255), -1)

                # Plot the original image, edge-detected image, and final image with direction
                fig, axs = plt.subplots(1, 3, figsize=(15, 5))
                axs[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                axs[0].set_title('Original Image')
                axs[0].axis('off')

                axs[1].imshow(edges, cmap='gray')
                axs[1].set_title('Edge Detected Image')
                axs[1].axis('off')

                axs[2].imshow(cv2.cvtColor(img_direction, cv2.COLOR_BGR2RGB))
                axs[2].set_title(f'Detected Direction: {direction_degrees:.2f}°')
                axs[2].axis('off')

                plt.show()

                return direction_degrees
    return None

# Example: Running the function on an image
image_path = '90.png'  # Replace with your file path
direction_with_centroid = calculate_direction_with_centroid(image_path)
print(f"Detected direction: {direction_with_centroid} degrees")
