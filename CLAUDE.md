# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Resume Ragu is a full-stack application for managing career data (jobs, skills, projects, accomplishments) and generating tailored resume content via a conversational AI interface. Output is markdown format. See `plan.md` for the full specification.

## Tech Stack

- **Frontend:** React + TypeScript (Vite)
- **Backend:** Python + FastAPI
- **AI:** Anthropic Claude API (via SDK)
- **Storage:** JSON files per user (in `data/` directory)

## Development Commands

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Testing
```bash
# Backend tests
cd backend
pytest
pytest tests/test_profile_service.py  # single test file
pytest tests/test_profile_service.py::test_name -v  # single test

# Frontend tests (if configured)
cd frontend
npm test
```

## Architecture

The app follows a strict layered architecture with clear separation of concerns:

```
Routes (HTTP) → Services (business logic) → Storage / AI (persistence & Claude API)
```

- **`backend/app/routes/`** — HTTP handlers only, no business logic
- **`backend/app/services/`** — Business logic (profile_service, chat_service)
- **`backend/app/storage/`** — JSON file persistence (`json_store.py`)
- **`backend/app/ai/`** — Claude API wrapper, prompt construction, guardrails
- **`backend/app/models.py`** — Pydantic data models (source of truth for data shapes)
- **`frontend/src/services/api.ts`** — Single API client, sole contact point with backend
- **`frontend/src/hooks/`** — Custom React hooks for state (useChat, useProfile)
- **`frontend/src/types/`** — TypeScript interfaces mirroring backend Pydantic models

### Key Design Decisions

- **No cross-layer access:** Routes never construct prompts; AI service never reads files directly.
- **Stateless backend for chat:** Frontend maintains full conversation history and sends complete message array with each request.
- **User profile as single JSON file:** Entire profile fits in Claude's context window, no retrieval/chunking needed.
- **System prompt lives in `backend/app/prompts/resume_system.txt`**, iterable without code changes.
- **AI client is provider-agnostic interface** to allow swapping providers.

### Data Model

User data stored at `data/{userId}/profile.json` with linked entities: user info, jobs, skills, projects, and accomplishments (the core unit for resume content). All entities cross-reference by ID.

## Configuration

Environment variables via `.env` file (see `.env.example`):
- `ANTHROPIC_API_KEY` (required)
- `DATA_DIR` (default: `./data`)
- `MODEL_NAME` (default: `claude-sonnet-4-20250514`)
- `MAX_CONVERSATION_TURNS` (default: `20`)
- `LOG_LEVEL` (default: `INFO`)

Config is validated at startup — app fails fast on missing required values.

## Engineering Conventions

- Use Python's `logging` module with structured context (request IDs, user IDs), never `print()`
- Pydantic models define backend data contracts; TypeScript interfaces mirror them on frontend
- AI guardrails are defense-in-depth: prompt-level constraints, input validation in `guardrails.py`, output validation
- Tests use a mock AI client (no real API calls); shared fixtures in `conftest.py`
- Consistent API response envelopes and error shapes across all endpoints
