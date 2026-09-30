from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import settings
from explanation_module import explain_topic
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from schemas import (
    ExplainRequest,
    ExplainResponse,
    LearningPathRequest,
    LearningPathResponse,
    QARequest,
    QAResponse,
    QuizRequest,
    QuizResponse,
    SummaryRequest,
    SummaryResponse,
)

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="EduGenie",
    description="Google Gemini powered learning assistant based on the supplied EduGenie project document.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"app_name": settings.app_name})


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "app": settings.app_name,
        "gemini_configured": bool(settings.gemini_api_key),
        "model": settings.gemini_model,
        "local_explanation_enabled": settings.enable_local_explanation,
    }


@app.post("/qa", response_model=QAResponse)
def qa(payload: QARequest):
    try:
        return QAResponse(answer=answer_question(payload.question))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/explain", response_model=ExplainResponse)
def explain(payload: ExplainRequest):
    try:
        return ExplainResponse(explanation=explain_topic(payload.topic))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/quiz", response_model=QuizResponse)
def quiz(payload: QuizRequest):
    try:
        return QuizResponse(questions=generate_quiz(payload.text, payload.num_questions))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/summarize", response_model=SummaryResponse)
def summarize(payload: SummaryRequest):
    try:
        return SummaryResponse(summary=summarize_text(payload.text))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/learn/recommendations", response_model=LearningPathResponse)
def learning_path(payload: LearningPathRequest):
    try:
        return LearningPathResponse(recommendations=get_learning_recommendations(payload.topic, payload.level))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
