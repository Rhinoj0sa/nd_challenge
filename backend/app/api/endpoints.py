from fastapi import APIRouter, UploadFile, File, HTTPException
import time

import os
from dotenv import load_dotenv
from app.ocr.ocr_utils import extract_text
from app.vector_db.vector_search import DocumentVectorDB
from app.llm.entity_extraction import extract_entities_llm
from app.models.schemas import ExtractEntitiesResponse


load_dotenv()

router = APIRouter()


@router.get("/")
async def read_main():
    return {"message": "Hello to the PDF Document Type Identifier API"}


# Load or initialize vector db and entity fields
vector_db = DocumentVectorDB()


DOC_TYPE_FIELDS = {
    "Invoice": ["invoice_number", "date", "total_amount", "vendor_name"],
    "Receipt": ["receipt_number", "date", "total_amount", "vendor_name"],
    # Add more document types and fields as needed
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

    doc_type, confidence = vector_db.search(text)
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
