import pyautogui
import time
import logging
from PIL import Image
import pytesseract
import re
from io import BytesIO
from health_bar import calculate_red_bar_percentage, HealthBar
# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

health_bar = HealthBar()
def take_screenshot_in_memory():
    logging.info("Starting screenshot process...")

    # Measure the start time
    start_time = time.time()

    left = 400  # X-coordinate of the top-left corner of the region
    top = 100  # Y-coordinate of the top-left corner of the region
    width = 360  # Width of the region
    height = 80  # Height of the region

    # Take a screenshot (but do not save it)
    screenshot = pyautogui.screenshot(region=(left, top, width, height))

    # Save screenshot
    # screenshot.save(f"save_{start_time}.png")

    # Measure the time after taking the screenshot
    screenshot_time = time.time()
    logging.info(f"Screenshot taken in {screenshot_time - start_time:.4f} seconds.")

    # Convert the screenshot to an in-memory object (BytesIO)
    img_byte_arr = BytesIO()
    screenshot.save(img_byte_arr, format='PNG')

    # approx_target_hp = calculate_red_bar_percentage(img_byte_arr)
    approx_target_hp = health_bar.calculate_red_bar_percentage(img_byte_arr)
    print("approx_target_hp", approx_target_hp)
    # Rewind the buffer to the beginning, so it can be read
    img_byte_arr.seek(0)

    # Total time taken for screenshot in-memory processing
    total_time = time.time() - start_time
    logging.info(f"Total time for screenshot process in memory: {total_time:.4f} seconds.")

    # Return the in-memory screenshot (BytesIO object)
    return img_byte_arr


def extract_text_from_image_in_memory(img_byte_arr):
    logging.info("Starting text extraction from in-memory image...")

    # Measure the start time for text extraction
    start_time = time.time()

    # Load the image from the in-memory object
    image = Image.open(img_byte_arr)

    # Use pytesseract to do OCR on the image
    text = pytesseract.image_to_string(image)

    # Measure the time after text extraction
    extraction_time = time.time()
    logging.info(f"Text extracted in {extraction_time - start_time:.4f} seconds.")

    return text


def find_is_target_killed(extracted_text: str) -> bool:
    logging.info("Starting pattern matching for 'XP (Bonus:'...")

    # Measure the start time for pattern matching
    start_time = time.time()

    pattern = r"XP \(Bonus:[^)]+\)"
    matches = re.findall(pattern, extracted_text)

    # Measure the time after pattern matching
    match_time = time.time()
    logging.info(f"Pattern matching completed in {match_time - start_time:.4f} seconds.")

    logging.info(f"Matches found: {matches}")

    return len(matches) > 0


# Start the process and measure total execution time
logging.info("Starting the entire process...")

process_start_time = time.time()

# Take a screenshot and keep it in memory
screenshot_in_memory = take_screenshot_in_memory()
#
# # Extract text from the in-memory screenshot
# extracted_text = extract_text_from_image_in_memory(screenshot_in_memory)
#
# # Check if the target is killed based on the pattern
# is_target_killed = find_is_target_killed(extracted_text)
# logging.info(f"Is the target killed: {is_target_killed}")
#
# # Measure total execution time
# process_end_time = time.time()
# logging.info(f"Total process completed in {process_end_time - process_start_time:.4f} seconds.")
#
# # Print result for final output
# print("is_target_killed", is_target_killed)
