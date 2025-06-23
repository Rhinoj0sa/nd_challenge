from fastapi import APIRouter, UploadFile, File, HTTPException
import time

import os
from dotenv import load_dotenv
from app.ocr.ocr_utils import extract_text
# from app.vector_db.vector_search import DocumentVectorDB
from app.llm.entity_extraction import extract_entities_llm
from app.models.schemas import ExtractEntitiesResponse

from app.vector_db.vector_search import classify_doc_type

load_dotenv()

router = APIRouter()


@router.get("/")
async def read_main():
    return {"message": "Hello to the PDF Document Type Identifier API"}


# Sample document types and their representative text snippets for classification


DOC_TYPE_FIELDS = {
    "Invoice": ["invoice_number", "date", "total_amount", "vendor_name"],
    "Receipt": ["receipt_number", "date", "total_amount", "vendor_name"],
    "Contract": ["contract_number", "date", "parties_involved", "contract_terms"],
    "Report": ["report_title", "author", "date", "summary"],
    "Letter": ["sender_name", "recipient_name", "date", "subject"],
    "Resume": ["name", "contact_info", "education", "work_experience", "skills"],
    "Tax Document": ["tax_year", "taxpayer_name", "tax_id", "total_tax_due"],
    "Legal Document": ["case_number", "court_name", "parties_involved", "filing_date"],
    "Medical Record": ["patient_name", "date_of_birth", "medical_conditions", "treatment_history"],
    "Bank Statement": ["account_number", "statement_period", "transactions", "balance"],
    "Email": ["sender", "recipient", "subject", "date", "body"],

}
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")


@router.post("/extract_entities/", response_model=ExtractEntitiesResponse)
async def extract_entities(file: UploadFile = File(...)):
    """
    Endpoint to extract entities from an uploaded file.

    This endpoint accepts a file upload, extracts text from the file (using OCR if necessary),
    determines the document type and its confidence using a vector database, and then extracts
    entities from the text using an LLM based on the document type. Returns the document type,
    confidence score, extracted entities, and processing time.

    Args:
        file (UploadFile): The file to be processed.

    Returns:
        ExtractEntitiesResponse: An object containing the document type, confidence score,
        extracted entities, and processing time.

    Raises:
        HTTPException: If text extraction (OCR) fails.
    """
    start_time = time.time()
    content = await file.read()
    try:
        text = extract_text(content, file.filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OCR failed: {e}")

    doc_type, confidence = classify_doc_type(text)
    field_list = DOC_TYPE_FIELDS.get(doc_type, [])
    entities: dict[str, str] = extract_entities_llm(
        text, doc_type, field_list, OPENAI_API_KEY
    )
    elapsed = f"{time.time() - start_time:.2f}s"
    return ExtractEntitiesResponse(
        document_type=doc_type,
        confidence=confidence,
        entities=entities,
        processing_time=elapsed,
    )
