import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "EduGenie")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "").strip()
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()
    enable_local_explanation: bool = os.getenv("ENABLE_LOCAL_EXPLANATION", "false").lower() in {"1", "true", "yes", "on"}
    local_explanation_model: str = os.getenv("LOCAL_EXPLANATION_MODEL", "MBZUAI/LaMini-Flan-T5-783M").strip()
    max_input_chars: int = int(os.getenv("MAX_INPUT_CHARS", "20000"))


settings = Settings()
