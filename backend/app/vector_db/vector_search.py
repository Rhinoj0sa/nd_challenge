from typing import Any, Tuple

"""
Module for vector-based document type classification using Sentence Transformers and FAISS.

Classes:
    DocumentVectorDB: Handles encoding, indexing, and searching of document embeddings.

Dependencies:
    - sentence_transformers
    - faiss
    - numpy

Classes:
    DocumentVectorDB:
        A simple vector database for classifying documents by type using semantic embeddings.

        Methods:
            __init__(model_name="all-MiniLM-L6-v2"):
                Initializes the SentenceTransformer model, FAISS index, example document types, and their embeddings.

            add_document(doc_type: str, text: str) -> None:
                Adds a new document type and its embedding to the index.

            search(text: str, top_k: int = 1) -> Tuple[str, float]:
                Searches for the most similar document type to the input text and returns the type and similarity score.
"""
from sentence_transformers import SentenceTransformer
import faiss  # type: ignore
import numpy as np


class DocumentVectorDB:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = faiss.IndexFlatL2(384)  # 384 for MiniLM
        self.doc_types = ["Invoice", "Resume", "Receipt"]
        self.example_texts = [
            "Invoice for services rendered to ABC Corp, total $450.00",
            "Curriculum Vitae: John Doe, Experience in software engineering",
            "Receipt for purchase at XYZ Store, total $23.99",
        ]
        self.embeddings = self.model.encode(self.example_texts)

    def add_document(self, doc_type: str, text: str) -> None:
        emb: Any = self.model.encode([text])[0]
        self.index.add(np.array([emb], dtype="float32"))
        self.doc_types.append(doc_type)
        self.embeddings.append(emb)

    def search(self, text: str, top_k: int = 1) -> Tuple[str, float]:
        emb = self.model.encode([text])[0]
        D, I = self.index.search(np.array([emb], dtype="float32"), top_k)
        idx = int(I[0][0])
        score = 1 / (1 + D[0][0])
        return self.doc_types[idx], score
