import cv2
import numpy as np

# Load the image
image = cv2.imread('mpfull.png')
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define the HSV range for detecting the blue color
lower_blue = np.array([90, 50, 50])
upper_blue = np.array([130, 255, 255])

# Create a mask for the blue regions
mask = cv2.inRange(hsv_image, lower_blue, upper_blue)
result = cv2.bitwise_and(image, image, mask=mask)

# Calculate the average intensity of the blue bar
gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
average_intensity = np.mean(gray)

# Assuming `average_intensity` ranges from min (0% fill) to max (100% fill), normalize it
min_intensity = 0   # Adjust these based on observed min intensity for dark blue
max_intensity = 255 # Adjust these based on observed max intensity for light blue
percentage_fill = (average_intensity - min_intensity) / (max_intensity - min_intensity) * 100
percentage_fill = max(0, min(100, percentage_fill))  # Clamp to 0-100%

print(f"The bar is approximately {percentage_fill:.2f}% filled.")
