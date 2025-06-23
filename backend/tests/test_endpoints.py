from typing import Any, Tuple
from fastapi.testclient import TestClient
import app
from app.api.endpoints import router
from fastapi import FastAPI
import io

app = FastAPI()
app.include_router(router)

client = TestClient(app)


# The commented out code `# def test_read_main():` is defining a test function named `test_read_main`
# that is meant to test the behavior of the API endpoint that responds to a GET request to the root
# URL ("/"). The test checks if the response status code is 200 (indicating a successful response) and
# if the JSON response body matches `{"message": "Hello to the PDF Document Type Identifier API"}`.
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello to the PDF Document Type Identifier API"
    }


MINIMAL_PDF = (
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


# def test_extract_entities_success(monkeypatch: Any) -> None:
#     # Mock extract_text
#     def mock_extract_text(content: str, filename: str) -> Any:
#         return "This is a sample invoice text with invoice_number 123, date 2024-06-01, total_amount $100, vendor_name ACME Corp."
#
#     monkeypatch.setattr("app.ocr.ocr_utils.extract_text", mock_extract_text)
#
#     # Mock vector_db.search
#     def mock_search(self: Any, text: str) -> Tuple[str, float]:
#         return "Invoice", 0.95
#
#     monkeypatch.setattr(
#         "app.vector_db.vector_search.DocumentVectorDB.search", mock_search
#     )
#
    # Mock extract_entities_llm
    # def mock_extract_entities_llm(
    #     text: str, doc_type: str, field_list: str, api_key: str
    # ):
    #     return {
    #         "invoice_number": "123",
    #         "date": "2024-06-01",
    #         "total_amount": "$100",
    #         "vendor_name": "ACME Corp.",
    #     }
    #
    # monkeypatch.setattr(
    #     "app.api.endpoints.extract_entities_llm", mock_extract_entities_llm
    # )
    #
    # file_content = MINIMAL_PDF
    # response = client.post(
    #     "/extract_entities/",
    #     files={
    #         "file": ("test_invoice.pdf", io.BytesIO(file_content), "application/pdf")
    #     },
    # )
    # print("^^" * 20)
    # print("Response:", response.status_code, response.json())
    # print(response.json())
    #
    # assert response.status_code == 200
    # data = response.json()
    # assert data["document_type"] == "Invoice"
    # assert data["confidence"] == 0.95
    # assert data["entities"] == {
    #     "invoice_number": "123",
    #     "date": "2024-06-01",
    #     "total_amount": "$100",
    #     "vendor_name": "ACME Corp.",
    # }
    # assert "processing_time" in data


def test_extract_entities_ocr_failure(monkeypatch: Any) -> None:
    def mock_extract_text(content: str, filename: str) -> Any:
        raise Exception("OCR error")

    monkeypatch.setattr("app.ocr.ocr_utils.extract_text", mock_extract_text)

    file_content = b"bad content"
    response = client.post(
        "/extract_entities/",
        files={"file": ("bad.pdf", io.BytesIO(file_content), "application/pdf")},
    )
    assert response.status_code == 400
    assert response.json()["detail"].startswith("OCR failed:")
