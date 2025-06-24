import pytest
from app.vector_db.vector_search import classify_doc_type, DOC_TYPES


@pytest.mark.parametrize("text,expected_doc_type", [
    ("Invoice #: INV-1234\nAmount Due: $500", "Invoice"),
    ("Store: GroceryMart\nTotal Paid: $20.50", "Receipt"),
    ("This Agreement is made on January 1, 2025", "Contract"),
    ("Quarterly Sales Report – Q2 2025", "Report"),
    ("Dear Mr. Smith,\nThank you for your application.", "Letter"),
    ("Name: John Doe\nSkills: Python, JavaScript", "Resume"),
    ("IRS Form 1040\nTax Year: 2024", "Tax Document"),
    ("Case No. 2025-CV-12345\nPlaintiff: Jane Doe", "Legal Document"),
    ("Patient Name: Alice Brown\nDiagnosis: Flu", "Medical Record"),
])
def classifies_correct_doc_type(text, expected_doc_type):
    doc_type, score = classify_doc_type(text)
    assert doc_type == expected_doc_type
    assert 0 <= score <= 100

def handles_empty_text():
    doc_type, score = classify_doc_type("")
    assert doc_type in DOC_TYPES
    assert score == 0.0

def handles_unrelated_text():
    doc_type, score = classify_doc_type("This is a completely unrelated text.")
    assert doc_type in DOC_TYPES
    assert 0 <= score <= 100
