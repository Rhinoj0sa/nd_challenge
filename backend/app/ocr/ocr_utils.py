import io
import tempfile
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import cv2
import numpy as np


def ocr_image(image: Image.Image) -> str:
    """Run OCR on a PIL image."""
    return pytesseract.image_to_string(image)


def ocr_pdf(pdf_path: str) -> str:
    """Convert PDF pages to images, then OCR each page."""
    images = convert_from_path(pdf_path)
    text = ""
    for image in images:
        text += ocr_image(image) + "\n"
    return text


def extract_text(file_bytes: bytes, filename: str) -> str:
    """Detect file type and run OCR."""
    if filename.lower().endswith(".pdf"):
        with tempfile.NamedTemporaryFile(suffix=".pdf") as temp:
            temp.write(file_bytes)
            temp.flush()
            return ocr_pdf(temp.name)
    else:
        # Use BytesIO to open image from bytes
        image = Image.open(io.BytesIO(file_bytes))
        return ocr_image(image)


# def extract_text(file_bytes: bytes, filename: str) -> str:
#     """Detect file type and run OCR."""
#     if filename.lower().endswith(".pdf"):
#         with tempfile.NamedTemporaryFile(suffix=".pdf") as temp:
#             temp.write(file_bytes)
#             temp.flush()
#             return ocr_pdf(temp.name)
#     else:
#         image = Image.open(tempfile.SpooledTemporaryFile())
#         image.file.write(file_bytes)
#         image.file.seek(0)
#         return ocr_image(image)
