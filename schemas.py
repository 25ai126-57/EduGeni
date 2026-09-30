from pydantic import BaseModel, Field, field_validator


class TextRequest(BaseModel):
    text: str = Field(..., min_length=3, max_length=20000)

    @field_validator("text")
    @classmethod
    def clean_text(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 3:
            raise ValueError("Input must contain at least 3 characters.")
        return value


class QARequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=5000)


class ExplainRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=300)


class QuizRequest(TextRequest):
    num_questions: int = Field(default=3, ge=1, le=10)


class SummaryRequest(TextRequest):
    pass


class LearningPathRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=300)
    level: str = Field(default="beginner", pattern="^(beginner|intermediate|advanced)$")


class QAResponse(BaseModel):
    answer: str


class ExplainResponse(BaseModel):
    explanation: str


class SummaryResponse(BaseModel):
    summary: str


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(..., min_length=4, max_length=4)
    answer: str


class QuizResponse(BaseModel):
    questions: list[QuizQuestion]


class LearningPathResponse(BaseModel):
    recommendations: str
