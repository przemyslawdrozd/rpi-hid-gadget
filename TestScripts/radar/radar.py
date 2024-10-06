import cv2
import numpy as np

# Constants for the world directions
DIRECTIONS = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']


def count_red_dots(image):
    # Convert image to HSV to isolate the red dots
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

    # Count red dots in each quadrant
    quadrants = {'NE': 0, 'SE': 0, 'SW': 0, 'NW': 0}

    for cnt in contours:
        # Get the center of each red dot
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


def analyze_radar_image(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Count red dots in each quadrant
    red_dots = count_red_dots(image)

    # Show the mask and original image for visual debugging
    cv2.imshow("Original Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Return the result as a dictionary
    return {"targets": red_dots}


# Example usage
image_path = 'radar_1.png'  # Provide the path to the high-resolution image
result = analyze_radar_image(image_path)
print(result)
