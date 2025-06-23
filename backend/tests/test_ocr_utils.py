from typing import Any
import pytest
from PIL import Image
from io import BytesIO
from app.ocr.ocr_utils import extract_text


class DummyImage:
    def __init__(self):
        self.file = BytesIO()


@pytest.fixture
def fake_pdf_bytes():
    # Minimal PDF header
    return (
        b"%PDF-1.4\n"
        b"1 0 obj\n"
        b"<< /Type /Catalog /Pages 2 0 R >>\n"
        b"endobj\n"
        b"2 0 obj\n"
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>\n"
        b"endobj\n"
        b"3 0 obj\n"
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 200 200] >>\n"
        b"endobj\n"
        b"xref\n"
        b"0 4\n"
        b"0000000000 65535 f \n"
        b"0000000010 00000 n \n"
        b"0000000053 00000 n \n"
        b"0000000100 00000 n \n"
        b"trailer\n"
        b"<< /Root 1 0 R /Size 4 >>\n"
        b"startxref\n"
        b"147\n"
        b"%%EOF\n"
    )


def test_extract_text_pdf(monkeypatch, fake_pdf_bytes):
    # Mock convert_from_path to return a list with one dummy PIL Image
    dummy_image = Image.new("RGB", (10, 10), color="white")
    monkeypatch.setattr(
        "app.ocr.ocr_utils.convert_from_path", lambda path: [dummy_image]
    )
    # Mock pytesseract.image_to_string to return a known string
    monkeypatch.setattr(
        "app.ocr.ocr_utils.pytesseract.image_to_string", lambda img: "PDF OCR TEXT"
    )
    result = extract_text(fake_pdf_bytes, "test.pdf")
    assert "PDF OCR TEXT" in result


def test_extract_text_image(monkeypatch):
    # Prepare fake image bytes (simple 1x1 PNG)
    img = Image.new("RGB", (1, 1), color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    image_bytes = buf.getvalue()

    # Patch Image.open to return a dummy image
    monkeypatch.setattr("app.ocr.ocr_utils.Image.open", lambda file: img)
    # Patch pytesseract.image_to_string to return a known string
    monkeypatch.setattr(
        "app.ocr.ocr_utils.pytesseract.image_to_string", lambda img: "IMAGE OCR TEXT"
    )
    result = extract_text(image_bytes, "test.png")
    assert result == "IMAGE OCR TEXT"


def test_extract_text_pdf_calls(monkeypatch, fake_pdf_bytes):
    called = {}

    def fake_convert_from_path(path):
        called["convert"] = True
        return [Image.new("RGB", (10, 10))]

    def fake_image_to_string(img):
        called["ocr"] = True
        return "SOME TEXT"

    monkeypatch.setattr("app.ocr.ocr_utils.convert_from_path", fake_convert_from_path)
    monkeypatch.setattr(
        "app.ocr.ocr_utils.pytesseract.image_to_string", fake_image_to_string
    )
    extract_text(fake_pdf_bytes, "file.PDF")
    assert called.get("convert")
    assert called.get("ocr")


def test_extract_text_image_calls(monkeypatch):
    called = {}
    img = Image.new("RGB", (1, 1))

    def fake_open(file):
        called["open"] = True
        return img

    def fake_image_to_string(img):
        called["ocr"] = True
        return "IMG TEXT"

    monkeypatch.setattr("app.ocr.ocr_utils.Image.open", fake_open)
    monkeypatch.setattr(
        "app.ocr.ocr_utils.pytesseract.image_to_string", fake_image_to_string
    )
    buf = BytesIO()
    img.save(buf, format="PNG")
    extract_text(buf.getvalue(), "img.png")
    assert called.get("open")
    assert called.get("ocr")
