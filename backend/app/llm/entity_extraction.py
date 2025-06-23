import json
import os
import openai
import re

from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env into environment

openai.api_key = os.getenv("OPENAI_API_KEY")


def extract_json_from_markdown(content: str) -> str:
    # Remove Markdown code block markers
    match = re.search(r"```json\s*(.*?)\s*```", content, re.DOTALL)
    if match:
        return match.group(1)
    return content  # fallback if no code block found


def extract_entities_llm(
    document_text: str, doc_type: str, field_list: list[str], openai_api_key: str | None
) -> dict[str, str]:
    field_str = ", ".join(field_list)
    input = (
        f"Given the following text extracted from a document of type '{doc_type}', "
        f"extract these fields: {field_str}. Return your response as a valid JSON object with no additional text.\n"
    )
    openai.api_key = openai_api_key
    if not openai.api_key:
        raise ValueError("OpenAI API key is not set.")

    try:
        response = openai.ChatCompletion.create(  # type: ignore
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": input},
                {"role": "user", "content": document_text},
            ],
            temperature=0,
        )
        return json.loads(extract_json_from_markdown(response["choices"][0]["message"]["content"]))  # type: ignore
    except Exception as e:
        return {"error": f"Failed to parse LLM response: {str(e)}"}
