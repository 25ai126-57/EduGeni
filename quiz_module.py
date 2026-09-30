import json
import re

from pydantic import BaseModel, Field, ValidationError

from gemini_client import generate_text


class QuizItem(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    answer: str


def _clean_json_block(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    match = re.search(r"\[[\s\S]*\]", text)
    return match.group(0) if match else text


def generate_quiz(passage: str, num_questions: int = 3) -> list[QuizItem]:
    prompt = f"""Create {num_questions} multiple-choice questions from the passage below.
Return ONLY valid JSON, with no Markdown and no commentary.
Schema:
[
  {{"question": "...", "options": ["...", "...", "...", "..."], "answer": "exactly one option text"}}
]
Rules:
- Exactly four options per question.
- Exactly one correct answer.
- The answer must exactly match one option.
- Questions must be answerable from the passage.

Passage:
{passage}
"""
    raw = generate_text(prompt)
    try:
        data = json.loads(_clean_json_block(raw))
        if not isinstance(data, list):
            raise ValueError("Quiz response is not a JSON list.")
        items = [QuizItem.model_validate(item) for item in data]
        if len(items) != num_questions:
            raise ValueError(f"Expected {num_questions} questions but received {len(items)}.")
        for item in items:
            if item.answer not in item.options:
                raise ValueError("A quiz answer does not exactly match one of its options.")
        return items
    except (json.JSONDecodeError, ValidationError, ValueError) as exc:
        raise RuntimeError(f"Could not parse Gemini quiz output: {exc}") from exc
