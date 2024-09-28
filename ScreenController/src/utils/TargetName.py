import time
import logging
from PIL import Image
import pytesseract
from io import BytesIO


class TargetName:

    @staticmethod
    def extract_text_from_image(img_byte_arr: BytesIO) -> str:
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

        return extracted_text
