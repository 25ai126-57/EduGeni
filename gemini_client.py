from functools import lru_cache

from google import genai

from config import settings


class GeminiNotConfiguredError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def get_client() -> genai.Client:
    if not settings.gemini_api_key:
        raise GeminiNotConfiguredError(
            "GEMINI_API_KEY is not configured. Copy .env.example to .env and add your Google Gemini API key."
        )
    return genai.Client(api_key=settings.gemini_api_key)


def generate_text(prompt: str) -> str:
    client = get_client()
    response = client.models.generate_content(model=settings.gemini_model, contents=prompt)
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text.strip()
