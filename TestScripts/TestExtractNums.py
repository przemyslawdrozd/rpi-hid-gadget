
import cv2
import pytesseract
import numpy as np
from matplotlib import pyplot as plt


# Load the image
image_path = 'cp.png'
image = cv2.imread(image_path)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Resize the image to make the digits clearer
gray_resized = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

# Apply basic thresholding
_, thresh = cv2.threshold(gray_resized, 120, 255, cv2.THRESH_BINARY_INV)

# Display the thresholded image (for debugging)
plt.imshow(thresh, cmap='gray')
plt.show()

# Use pytesseract to extract the digits from the thresholded image
custom_config = r'--oem 3 --psm 6 outputbase digits'
digits = pytesseract.image_to_string(thresh, config=custom_config)

# Print the extracted digits
print("Extracted Digits:", digits)
