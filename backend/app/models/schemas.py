from pydantic import BaseModel
from typing import Dict, Any


class ExtractEntitiesResponse(BaseModel):
    document_type: str
    confidence: float
    entities: Dict[str, Any]
    processing_time: str
