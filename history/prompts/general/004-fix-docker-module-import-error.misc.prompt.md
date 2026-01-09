---
id: "004"
title: "Fix Docker module import error"
stage: "misc"
date: "2026-01-09"
surface: "agent"
model: "sonnet-4-5-20250929"
feature: "none"
branch: "001-phase-ii-fullstack-todo"
user: "Debug runtime error: ModuleNotFoundError: No module named 'app'"
command: "Debug and fix Docker runtime error"
labels: ["bugfix","docker","python"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "backend/Dockerfile"
tests:
  - "None - manual verification required"
---

## Prompt

Runtime error when deploying to Hugging Face Spaces:
```
ModuleNotFoundError: No module named 'app'
```

The error occurs in `/app/api/index.py` line 22:
```python
from app.main import app as fastapi_app
```

Container logs show the uvicorn server cannot import the app module.

## Response snapshot

Identified root cause: The Dockerfile sets `WORKDIR /app` but the Python module structure is `/app/backend/app/`. Without `PYTHONPATH` set, Python cannot find the `app` module.

Fixed by:
1. Adding `ENV PYTHONPATH=/app/backend` to allow Python to find the `app` module
2. Correcting `APP_MODULE=api.index:handler` → `api.index:app` (the FastAPI instance is named `app`, not `handler`)

## Outcome

- ✅ Impact: Fixed Docker deployment module import issue for Hugging Face Spaces
- 🧪 Tests: Manual verification required - rebuild and redeploy container
- 📁 Files: Modified `backend/Dockerfile`
- 🔁 Next prompts: Rebuild and redeploy to Hugging Face Spaces
- 🧠 Reflection: The import path worked locally because the working directory was `backend/`, but in Docker with `WORKDIR /app`, the relative paths broke. PYTHONPATH is the standard fix for this.

## Evaluation notes (flywheel)

- Failure modes observed: ModuleNotFoundError - wrong Python import path
- Graders run and results (PASS/FAIL): N/A - manual verification
- Prompt variant (if applicable): N/A
- Next experiment (if needed): Could add a `__main__.py` entry point as alternative
