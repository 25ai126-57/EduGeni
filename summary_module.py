from gemini_client import generate_text


def summarize_text(text: str) -> str:
    prompt = f"""Summarize the educational text below for quick revision.
Keep the key ideas, definitions, important relationships, and facts.
Use short paragraphs or bullet points when that improves readability.
Do not add information that is not in the source.

Text:
{text}
"""
    return generate_text(prompt)
