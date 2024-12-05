import logging
import pytesseract
from PIL import Image
from io import BytesIO
import pygame
import re
from ..consts import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

INVALID_REGEX_PATTERN = r'Invalid'
CANNOT_REGEX_PATTERN = r'Cannot'
DISTANCE_REGEX_PATTERN = r'distance'
MP_REGEX_PATTERN = r'Not enough MP'
USE_REGEX_PATTERN = r'You use'
ATT_REGEX_PATTERN = r'cted'
SLEEP_REGEX_PATTERN = r'Crokian'


class ChatReader:

    def __init__(self):
        # self.tv_sound_file = "files/tv.mp3"

        # Initialize the pygame mixer
        # pygame.mixer.init()
        pass

    def extract_text_from_image(self, img_byte_arr: BytesIO) -> bool:
        """
        Extracts text from an image provided as a BytesIO object.

        Args:
            img_byte_arr (BytesIO): Image in memory from which to extract text.

        Returns:
            str: The extracted text from the image.
        """
        # Load image from BytesIO
        img_byte_arr.seek(0)  # Reset the stream position to the start
        img = Image.open(img_byte_arr)

        # Use pytesseract to extract text from the image
        extracted_text = pytesseract.image_to_string(img)
        logger.debug(f"Chat extracted_text: {extracted_text}")
        
        result = {}
        invalid_matches = re.findall(INVALID_REGEX_PATTERN, extracted_text, re.IGNORECASE)
        cannot_matches = re.findall(CANNOT_REGEX_PATTERN, extracted_text, re.IGNORECASE)
        distance_matches = re.findall(DISTANCE_REGEX_PATTERN, extracted_text, re.IGNORECASE)
        mp_matches = re.findall(MP_REGEX_PATTERN, extracted_text, re.IGNORECASE)
        use_matches = re.findall(USE_REGEX_PATTERN, extracted_text, re.IGNORECASE)
        att_matches = re.findall(ATT_REGEX_PATTERN, extracted_text, re.IGNORECASE)
        sleep_matches = re.findall(SLEEP_REGEX_PATTERN, extracted_text, re.IGNORECASE)

        result["is_invalid"] = len(invalid_matches) > 0
        result["is_cannot_see"] = len(cannot_matches) > 0
        result["is_distance"] = len(distance_matches) > 0
        result["is_not_mp"] = len(mp_matches) > 0
        result["is_use"] = len(use_matches) > 0
        result["is_att"] = len(att_matches) > 0
        result["is_sleep"] = len(sleep_matches) > 0
        


        # if result:
        #     self.__invoke_alert()

        return result

    def __invoke_alert(self) -> None:
        # Load the sound file
        pygame.mixer.music.load(self.tv_sound_file)

        # Play the sound
        pygame.mixer.music.play()
