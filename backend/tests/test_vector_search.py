import pytest
from unittest.mock import patch, MagicMock
from app.vector_db.vector_search import DocumentVectorDB


@pytest.fixture
def mock_model():
    mock = MagicMock()
    # 3 example embeddings, each 384-dim
    mock.encode.side_effect = lambda texts: [ # type: ignore
        [float(i + j) for j in range(384)] for i, _ in enumerate(texts) # type: ignore
    ]
    return mock

@pytest.fixture  # type: ignore
def mock_faiss(monkeypatch):  # type: ignore
    class MockIndex:  # type: ignore
        def __init__(self, dim):  # type: ignore
            self.vectors = []

        def add(self, arr):  # type: ignore
            self.vectors.append(arr[0])

        def search(self, arr, top_k):  # type: ignore
            # Always return index 0 with distance 0.5
            return [[0.5]], [[0]]

    monkeypatch.setattr("faiss.IndexFlatL2", MockIndex)  # type: ignore


def test_init_sets_up_model_and_examples(mock_model, mock_faiss, monkeypatch):  # type: ignore
    monkeypatch.setattr(
        "app.vector_db.vector_search.SentenceTransformer", lambda name: mock_model
    )
    db = DocumentVectorDB()
    assert db.model == mock_model
    assert db.doc_types == ["Invoice", "Resume", "Receipt"]
    assert len(db.example_texts) == 3


def test_add_document_adds_type_and_embedding(mock_model, mock_faiss, monkeypatch):  # type: ignore
    monkeypatch.setattr(
        "sentence_transformers.SentenceTransformer", lambda name: mock_model
    )
    db = DocumentVectorDB()
    db.embeddings = []
    db.index = MagicMock()
    db.doc_types = []
    db.add_document("Report", "Annual report for 2023")
    assert db.doc_types == ["Report"]
    assert len(db.embeddings) == 1
    db.index.add.assert_called_once()


def test_search_returns_doc_type_and_score(mock_model, mock_faiss, monkeypatch):  # type: ignore
    monkeypatch.setattr(
        "sentence_transformers.SentenceTransformer", lambda name: mock_model
    )
    db = DocumentVectorDB()
    db.doc_types = ["Invoice", "Resume", "Receipt"]
    db.index = MagicMock()
    db.index.search.return_value = ([[0.5]], [[1]])
    result = db.search("Some text", top_k=1)
    assert result[0] == "Resume"
    assert abs(result[1] - (1 / (1 + 0.5))) < 1e-6


def test_search_with_multiple_results(mock_model, mock_faiss, monkeypatch):  # type: ignore
    monkeypatch.setattr(
        "sentence_transformers.SentenceTransformer", lambda name: mock_model
    )
    db = DocumentVectorDB()
    db.doc_types = ["Invoice", "Resume", "Receipt"]
    db.index = MagicMock()
    db.index.search.return_value = ([[0.2, 0.5]], [[2, 0]])
    doc_type, score = db.search("Another text", top_k=2)
    assert doc_type == "Receipt"
    assert abs(score - (1 / (1 + 0.2))) < 1