# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational assistant implemented from the supplied project document. It provides:

- Question answering (`/qa`)
- Beginner-friendly concept explanation (`/explain`)
- Multiple-choice quiz generation (`/quiz`)
- Text summarization (`/summarize`)
- Beginner → advanced learning recommendations (`/learn/recommendations`)
- A responsive HTML/CSS frontend served directly by FastAPI
- A health endpoint and automated API tests
- Optional local LaMini-Flan-T5 explanation support, matching the architecture described in the source document

The supplied document describes Gemini for Q&A, quiz, summarization and learning paths, and LaMini-Flan-T5 for explanations. This implementation preserves that module structure while using Google's current `google-genai` Python SDK and a configurable current Gemini model rather than hard-coding the document's older Gemini 1.5 Pro API integration.

## 1. Requirements

- Python 3.10 or newer
- VS Code
- Internet connection for Gemini API calls
- A Google Gemini API key

## 2. VS Code setup — Windows

Open the `EduGenie` folder in VS Code.

### Create a virtual environment

PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\.venv\Scripts\Activate.ps1
```

### Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Configure Gemini

1. Create a Gemini API key in Google AI Studio.
2. Copy `.env.example` to `.env`.
3. Put your key after `GEMINI_API_KEY=`.
4. Keep `.env` private; it is excluded by `.gitignore`.

Example:

```env
GEMINI_API_KEY=your_real_key_here
GEMINI_MODEL=gemini-3.8-flash
ENABLE_LOCAL_EXPLANATION=false
```

## 3. Run the application

From the project root:

```powershell
uvicorn main:app --reload
```

Open:

`http://127.0.0.1:8000`

FastAPI's interactive API documentation is also available at:

`http://127.0.0.1:8000/docs`

## 4. Test the application

Run automated tests:

```powershell
pytest -q
```

The tests do not call Gemini. They validate the app, health endpoint and representative module/API behavior with mocked AI output.

Check configuration manually:

```powershell
curl http://127.0.0.1:8000/health
```

A configured server returns `gemini_configured: true`.

## 5. Test Gemini features from the UI

### Q&A

Ask:

`Which is the largest ocean?`

### Explanation

Enter:

`Pythagoras theorem`

### Summary

Paste a paragraph from lecture notes.

### Quiz

Paste a passage and select 3, 5 or 10 questions. Each generated question has four options. Clicking an option immediately marks it and updates the score.

### Learning path

Try:

`SQL`

and choose Beginner, Intermediate or Advanced.

## 6. API examples

### Q&A

```powershell
curl -X POST http://127.0.0.1:8000/qa `
  -H "Content-Type: application/json" `
  -d '{"question":"Which is the largest ocean?"}'
```

### Explain

```powershell
curl -X POST http://127.0.0.1:8000/explain `
  -H "Content-Type: application/json" `
  -d '{"topic":"Pythagoras theorem"}'
```

### Quiz

```powershell
curl -X POST http://127.0.0.1:8000/quiz `
  -H "Content-Type: application/json" `
  -d '{"text":"The Earth revolves around the Sun and takes about one year to complete an orbit.","num_questions":3}'
```

### Summary

```powershell
curl -X POST http://127.0.0.1:8000/summarize `
  -H "Content-Type: application/json" `
  -d '{"text":"Paste your educational text here."}'
```

### Learning path

```powershell
curl -X POST http://127.0.0.1:8000/learn/recommendations `
  -H "Content-Type: application/json" `
  -d '{"topic":"SQL","level":"beginner"}'
```

## 7. Optional local explanation model

The source project describes LaMini-Flan-T5-783M as the local explanation model. To enable that path:

```powershell
pip install -r requirements-local.txt
```

Then change `.env`:

```env
ENABLE_LOCAL_EXPLANATION=true
LOCAL_EXPLANATION_MODEL=MBZUAI/LaMini-Flan-T5-783M
```

The model will be downloaded on first use. The application falls back to Gemini if the optional local model cannot be loaded.

For a simple college-project setup, leave `ENABLE_LOCAL_EXPLANATION=false`; this avoids installing the large PyTorch/Transformers stack unless you specifically need local inference.

## 8. Project structure

```text
EduGenie/
├── main.py
├── config.py
├── gemini_client.py
├── schemas.py
├── qna.py
├── explanation_module.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── requirements-local.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── app.js
│   └── style.css
└── tests/
    └── test_app.py
```

## 9. Troubleshooting

### `GEMINI_API_KEY is not configured`

Create `.env` from `.env.example` and set a real API key. Restart Uvicorn after changing environment variables.

### 401/403 from Gemini

Check that the API key is valid and that the Gemini API is available to the Google project associated with that key.

### Model not found

Set `GEMINI_MODEL` to a model currently available to your API account. The model is intentionally configurable so the project does not need code changes when Google changes model availability.

### Port already in use

Run on another port:

```powershell
uvicorn main:app --reload --port 8001
```

Then open `http://127.0.0.1:8001`.

## 10. Architecture

```text
Browser
  │
  ▼
FastAPI + Jinja2/static files
  │
  ├── /qa ───────────────────────► qna.py ────────────────► Gemini
  ├── /explain ──────────────────► explanation_module.py ─► Gemini / optional LaMini
  ├── /quiz ─────────────────────► quiz_module.py ────────► Gemini ─► JSON validation
  ├── /summarize ────────────────► summary_module.py ─────► Gemini
  └── /learn/recommendations ────► learning_path.py ──────► Gemini
```

## 11. Important implementation note

The supplied project document specifies Gemini 1.5 Pro and older-style Gemini integration. Those model/API details are dated. This project keeps the requested functionality and folder/module architecture but uses the current Google GenAI Python SDK and makes the Gemini model configurable through `.env`. That prevents the project from being tied to a model that may no longer be available.
