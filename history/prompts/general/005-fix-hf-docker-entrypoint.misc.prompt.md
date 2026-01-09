---
id: "005"
title: "Fix Hugging Face Docker entry point"
stage: "misc"
date: "2026-01-09"
surface: "agent"
model: "sonnet-4-5-20250929"
feature: "none"
branch: "001-phase-ii-fullstack-todo"
user: "Fix Hugging Face Docker deployment - use Python entry point instead of uvicorn. Hugging Face Spaces requires running via Python file, not direct uvicorn command."
command: "Fix Hugging Face Docker deployment"
labels: ["bugfix","docker","huggingface","fastapi"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "backend/Dockerfile"
tests:
  - "None - manual verification required on HF Space"
---

## Prompt

Hugging Face + Docker deployment is failing with runtime errors. The issue is that Hugging Face expects:
1. Port 7860 specifically
2. Python file entry point (not direct uvicorn command)
3. Correct module path

Current Dockerfile issues:
- Uses `CMD ["uvicorn", "api.index:app", ...]` directly (wrong for HF)
- Needs to run via `python api/index.py`

## Response snapshot

Fixed the Dockerfile for Hugging Face Spaces compatibility:

```dockerfile
# Expose port 7860 (Hugging Face requires this port)
EXPOSE 7860

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/backend

# Command to run the app via Python (HF requirement - don't use uvicorn directly)
CMD ["python", "api/index.py"]
```

Key changes:
1. Removed `ENV APP_MODULE` - not needed
2. Changed CMD from uvicorn command to `python api/index.py`
3. Added comment explaining HF requirement
4. Kept `PYTHONPATH=/app/backend` for module imports

The `api/index.py` already has correct setup:
- `if __name__ == "__main__":` entry point (line 126)
- Uses `PORT` env var or defaults to 7860 (line 129)
- Proper CORS configuration for Vercel and HF Spaces

## Outcome

- ✅ Impact: Fixed Hugging Face Spaces Docker deployment by using correct Python entry point
- 🧪 Tests: Manual verification required - rebuild HF Space and check logs
- 📁 Files: Modified `backend/Dockerfile`
- 🔁 Next prompts: Rebuild Hugging Face Space and verify deployment
- 🧠 Reflection: Hugging Face Spaces has strict requirements - must run via Python entry point, port 7860, and correct PYTHONPATH. The api/index.py was already correctly configured; the Dockerfile just needed to use it properly.

## Evaluation notes (flywheel)

- Failure modes observed: Runtime error in HF Space due to incorrect Docker CMD
- Graders run and results (PASS/FAIL): N/A - manual verification on HF Space required
- Prompt variant (if applicable): N/A
- Next experiment (if needed): If still fails, check HF Space logs for exact error
