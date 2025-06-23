import pytest
import json
from unittest.mock import patch, MagicMock
from app.llm.entity_extraction import extract_entities_llm


@pytest.fixture
def mock_openai_response_json():
    return {
        "choices": [
            {
                "message": {
                    "content": '{"name": "John Doe", "email": "john@example.com"}'
                }
            }
        ]
    }


@pytest.fixture
def mock_openai_response_markdown_json():
    return {
        "choices": [
            {
                "message": {
                    "content": '```json\n{"name": "Jane Doe", "email": "jane@example.com"}\n```'
                }
            }
        ]
    }


def test_extract_entities_llm_success_plain_json(mock_openai_response_json):
    with patch(
        "app.llm.entity_extraction.openai.ChatCompletion.create",
        return_value=mock_openai_response_json,
    ):
        result = extract_entities_llm(
            document_text="Name: John Doe, Email: john@example.com",
            doc_type="resume",
            field_list=["name", "email"],
            openai_api_key="fake-key",
        )
        assert result == {"name": "John Doe", "email": "john@example.com"}


def test_extract_entities_llm_success_markdown_json(mock_openai_response_markdown_json):
    with patch(
        "app.llm.entity_extraction.openai.ChatCompletion.create",
        return_value=mock_openai_response_markdown_json,
    ):
        result = extract_entities_llm(
            document_text="Name: Jane Doe, Email: jane@example.com",
            doc_type="resume",
            field_list=["name", "email"],
            openai_api_key="fake-key",
        )
        assert result == {"name": "Jane Doe", "email": "jane@example.com"}


def test_extract_entities_llm_invalid_json():
    bad_response = {"choices": [{"message": {"content": "not a json"}}]}
    with patch(
        "app.llm.entity_extraction.openai.ChatCompletion.create",
        return_value=bad_response,
    ):
        result = extract_entities_llm(
            document_text="Some text",
            doc_type="invoice",
            field_list=["amount"],
            openai_api_key="fake-key",
        )
        assert "error" in result
        assert "Failed to parse LLM response" in result["error"]


from typing import Any, Dict


def test_extract_entities_llm_openai_exception():
    with patch(
        "app.llm.entity_extraction.openai.ChatCompletion.create",
        side_effect=Exception("API error"),
    ):
        result: Dict[str, Any] = extract_entities_llm(
            document_text="Some text",
            doc_type="invoice",
            field_list=["amount"],
            openai_api_key="fake-key",
        )
        print("^^" * 20)
        print("Result:", result)
        assert isinstance(result, dict)
        assert "error" in result
        assert "Failed to parse LLM response" in result["error"]
