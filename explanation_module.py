from functools import lru_cache

from config import settings
from gemini_client import generate_text


def _gemini_explanation(topic: str) -> str:
    prompt = f"""Explain the educational topic below for a beginner.
Use plain language, a simple analogy if helpful, and a small example.
Keep it concise but complete. Avoid unnecessary jargon.

Topic: {topic}
"""
    return generate_text(prompt)


@lru_cache(maxsize=1)
def _local_pipeline():
    """Optional local LaMini-Flan-T5 backend from the original project design.

    It is loaded only when ENABLE_LOCAL_EXPLANATION=true, keeping normal setup
    lightweight and avoiding a large ML download unless the user explicitly opts in.
    """
    from transformers import pipeline

    return pipeline(
        "text2text-generation",
        model=settings.local_explanation_model,
        device=-1,
    )


def explain_topic(topic: str) -> str:
    if settings.enable_local_explanation:
        try:
            generator = _local_pipeline()
            result = generator(
                f"Explain {topic} simply for a student. Give a short example.",
                max_new_tokens=180,
                do_sample=False,
            )
            if result and result[0].get("generated_text"):
                return result[0]["generated_text"].strip()
        except Exception:
            # If the optional local model cannot load, fall back to the cloud model.
            pass
    return _gemini_explanation(topic)
