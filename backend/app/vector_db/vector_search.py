from typing import Tuple
import numpy as np

from sentence_transformers import SentenceTransformer
import faiss

# List of document types and representative samples for each
DOC_TYPES = [
    "Invoice", "Receipt", "Contract", "Report", "Letter", "Resume",
    "Tax Document", "Legal Document", "Medical Record"
]

DOC_TYPE_SAMPLES = [
    """Invoice #: INV-2045  
Date: 2025-06-15  
Billed To: Acme Corporation  
Description: Web Development Services (May 2025)  
Amount Due: $4,200.00  
Due Date: 2025-06-30  
Payment Terms: Net 15  
Issued by: Tech Solutions Ltd., 123 Park Ave, NY""",

    """Store: FreshMart Supermarket  
Transaction ID: 987654321  
Date: 2025-06-10 14:22  
Items:  
 - Milk 2L: $3.50  
 - Bread: $2.00  
 - Eggs: $4.00  
Subtotal: $9.50  
Tax: $0.76  
Total Paid: $10.26  
Payment Method: Credit Card (VISA)""",

    """This Service Agreement ("Agreement") is made on March 1, 2025, between Spark Agency, Inc. ("Provider") and Olivia Reed ("Client").  
The Provider agrees to deliver social media management services for a term of six (6) months, starting April 1, 2025.  
Compensation: $1,000 per month  
Termination: Either party may terminate with 30 days’ written notice.""",

    """Quarterly Sales Report – Q1 2025  
Prepared by: James Tucker  
Date: April 10, 2025  
Summary:  
The company's total revenue increased by 12% compared to Q4 2024. The North American region led with $3.2M in sales, followed by Europe at $2.1M.  
Recommendations: Expand marketing in Asia-Pacific to meet projected growth targets.""",

    """June 5, 2025  
Mr. Alan Becker  
45 Brookline Dr.  
Dear Mr. Becker,  
Thank you for your interest in our graduate program. After careful consideration, we are pleased to inform you that you have been accepted.  
Sincerely,  
Admissions Office  
University of Springfield""",

    """Name: Sarah L. Kim  
Email: sarah.kim@example.com  
Experience:  
- Software Engineer, ByteTech Inc. (2022–Present)  
- Junior Developer, NetPro Solutions (2020–2022)  
Education:  
- B.S. in Computer Science, Stanford University, 2020  
Skills: Python, JavaScript, SQL, Git, Agile""",

    """IRS Form 1040  
Tax Year: 2024  
Filing Status: Single  
Name: Marcus T. Allen  
SSN: XXX-XX-1234  
Wages: $58,200  
Federal Tax Withheld: $6,800  
Refund: $1,250  
Signature: Marcus T. Allen, April 10, 2025""",

    """Case No. 2025-CV-11234  
IN THE DISTRICT COURT OF HARRIS COUNTY  
Plaintiff: Maria Lopez  
Defendant: Orion Logistics LLC  
Complaint: Plaintiff alleges breach of contract and seeks damages of $75,000 due to non-delivery of goods.  
Filed: March 12, 2025  
Attorney for Plaintiff: Richard Yates, Esq.""",

    """Patient Name: David Lin  
DOB: 07/21/1980  
Visit Date: 2025-06-05  
Chief Complaint: Persistent cough and shortness of breath  
Diagnosis: Bronchitis  
Prescribed Medication: Azithromycin 250mg for 5 days  
Physician: Dr. Julia Ahmed, MD  
Follow-up: In 2 weeks"""
]

# Load Sentence Transformer model once for efficiency
_sentence_model = None
_faiss_index = None
_doc_type_embeddings = None

def _load_model_and_index():
    global _sentence_model, _faiss_index, _doc_type_embeddings
    if _sentence_model is None:
        _sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
    if _doc_type_embeddings is None:
        _doc_type_embeddings = _sentence_model.encode(DOC_TYPE_SAMPLES, convert_to_numpy=True, normalize_embeddings=True)
    if _faiss_index is None:
        dim = _doc_type_embeddings.shape[1]
        _faiss_index = faiss.IndexFlatIP(dim)
        _faiss_index.add(_doc_type_embeddings)

def classify_doc_type(text: str) -> Tuple[str, float]:
    """
    Classifies the document type from text using Sentence Transformers and FAISS.
    Returns:
        (doc_type, score_percent) -- e.g., ("Invoice", 98.6)
    """
    _load_model_and_index()
    # Get embedding for input text
    emb = _sentence_model.encode([text], convert_to_numpy=True, normalize_embeddings=True)
    # Search for the most similar doc type
    D, I = _faiss_index.search(emb, k=1)
    idx = int(I[0][0])
    score = float(D[0][0])  # cosine similarity in [-1, 1]
    # Convert cosine similarity to percent (from 0–100)
    score_percent = max(0.0, min(100.0, (score + 1) / 2 * 100))
    return DOC_TYPES[idx], score_percent
