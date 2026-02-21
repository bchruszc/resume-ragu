# Resume Builder Assistant — Project Plan

## Overview

A full-stack application for managing career data and generating tailored resume content with AI assistance. The app stores structured career history (jobs, skills, projects, accomplishments) and uses a conversational AI interface to generate polished resume content in markdown format.

This project demonstrates: full-stack development, AI integration and prompt engineering, thoughtful data modeling, and building practical developer tools.

---

## Engineering Principles

This project is intended to reflect senior-level software engineering practices. Every contributor (human or AI) should keep the following principles in mind:

**Clear module boundaries.** Each layer (API routes, services, storage, AI integration) should be independently understandable. A reader should be able to look at any single module and understand its responsibility without reading the rest of the codebase. Modules communicate through well-defined interfaces, not by reaching into each other's internals.

**Separation of concerns.** Routes handle HTTP. Services handle business logic. Storage handles persistence. The AI layer handles prompt construction and API communication. No layer should take on responsibilities that belong to another. For example, a route handler should never construct a prompt, and the AI service should never read files directly from disk.

**Real error handling.** No bare `except: pass`. Errors should be caught at appropriate levels, logged with context, and surfaced to the user as meaningful messages. The AI layer in particular needs robust handling — API timeouts, rate limits, malformed responses, and content filter rejections should all be handled gracefully, not silently swallowed.

**Config management.** All environment-specific values (API keys, model names, file paths, feature flags) live in configuration, never hardcoded. Use a validated config module that fails fast on startup if required values are missing, rather than failing at runtime when a code path is first hit.

**AI safety guardrails.** The system prompt and chat endpoint should include guardrails to keep the AI scoped to its intended purpose (resume building). This means instructing the model to decline off-topic requests, sanitizing or validating user input before it reaches the AI, and ensuring the AI cannot be trivially jailbroken into producing unrelated or harmful content. Think of this as defense in depth — the prompt constrains intent, and the code constrains behavior.

**Quality README.** The repository README should be comprehensive enough that a reviewer can understand the project's purpose, architecture, and how to run it without reading the source code. It should reflect the same care as the code itself.

**Logging and observability.** Structured logging with context (request IDs, user IDs, operation being performed), not ad-hoc `print()` statements. AI interactions in particular should log what prompt was sent, response time, and token usage. Even in a local-only app, good logging makes debugging faster and signals production-mindedness. Use Python's `logging` module with a consistent format across all modules.

**Testing strategy.** A deliberate, layered approach: unit tests for services and storage, integration tests for API endpoints, and a mock/stub AI client that returns canned responses so orchestration logic can be tested without hitting the API. Testability should be a design consideration when building modules (e.g., the AI client interface should be easy to swap with a fake), not an afterthought.

**Type safety end-to-end.** Pydantic models define the data contracts on the backend. On the frontend, use TypeScript so the profile schema and API response shapes are explicit and compiler-checked. The goal is that a data structure change is caught at build time on both sides, not at runtime in a user's browser.

**API design consistency.** All endpoints should follow the same conventions: consistent response envelopes, predictable error shapes, and correct HTTP status codes. A consumer of the API should never have to guess how a particular endpoint formats its responses or errors. FastAPI's response models and exception handlers make this straightforward to enforce.

---

## Tech Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Frontend | React (Vite) + TypeScript | Fast dev experience, strong ecosystem, type-safe data contracts |
| Backend | Python + FastAPI | Clean async API, pairs well with AI SDKs |
| AI | Anthropic Claude API (via SDK) | Primary AI provider, abstracted for flexibility |
| Data Storage | JSON files (one per user) | Zero setup, easy to iterate on structure, trivially injected into AI context |
| Dev Environment | Two local processes (frontend + backend) | Simple to start; Docker can be added later |

### Configuration

All environment-specific values live in a validated config module. The app uses a `.env` file for local development, with a startup validation step that fails fast if required values are missing.

Required:
- `ANTHROPIC_API_KEY` — API key for Claude

Optional (with sensible defaults):
- `DATA_DIR` — path to JSON data directory (default: `./data`)
- `MODEL_NAME` — model identifier (default: `claude-sonnet-4-20250514`)
- `MAX_CONVERSATION_TURNS` — safety limit on chat history length (default: `20`)
- `LOG_LEVEL` — logging verbosity (default: `INFO`)

The backend should expose a `/health` endpoint that confirms the app is configured correctly and can reach its dependencies.

---

## Data Model

A single JSON file per user at `data/{userId}/profile.json`. The entire file can be loaded and injected into AI context for resume generation.

```json
{
  "user": {
    "id": "user-1",
    "name": "Jane Doe",
    "contact": {
      "email": "jane@example.com",
      "phone": "555-123-4567",
      "location": "Toronto, ON",
      "linkedin": "linkedin.com/in/janedoe",
      "github": "github.com/janedoe"
    },
    "summary": "Optional high-level professional summary the user maintains."
  },

  "jobs": [
    {
      "id": "job-1",
      "company": "Acme Corp",
      "title": "Senior Software Engineer",
      "startDate": "2020-01",
      "endDate": "2024-06",
      "description": "Optional brief description of the role.",
      "highlights": ["Led platform team", "Drove cloud migration"]
    }
  ],

  "skills": [
    {
      "id": "skill-1",
      "name": "Python",
      "category": "Languages",
      "proficiency": "expert",
      "yearsOfExperience": 10
    }
  ],

  "projects": [
    {
      "id": "proj-1",
      "name": "Cloud Migration",
      "description": "Migrated monolith to microservices on AWS.",
      "jobIds": ["job-1"],
      "skillIds": ["skill-1", "skill-3"],
      "outcome": "Reduced deployment time by 80%."
    }
  ],

  "accomplishments": [
    {
      "id": "acc-1",
      "statement": "Led migration of monolithic application to microservices architecture, reducing deployment time from 2 hours to 15 minutes.",
      "context": "The legacy system had become a bottleneck for the team. I proposed and led the migration effort over 6 months.",
      "impact": "80% reduction in deployment time, 50% fewer production incidents.",
      "jobIds": ["job-1"],
      "projectIds": ["proj-1"],
      "skillIds": ["skill-1", "skill-3"],
      "tags": ["leadership", "architecture", "cloud"]
    }
  ]
}
```

### Design Notes

- **Accomplishments are the core building block.** They carry the raw material the AI needs: what was done, the context, and the measurable impact. Links to jobs, skills, and projects let the AI place them in the right resume sections.
- **Everything is linked by ID.** This allows the AI (and the UI) to filter and group accomplishments by job, skill, or project.
- **The whole file is AI-context-friendly.** At typical career lengths, the full JSON is well within context window limits. No need for retrieval or chunking.

---

## Application Architecture

```
┌─────────────────────┐     ┌─────────────────────────────┐
│   React Frontend    │────▶│   FastAPI Backend            │
│                     │     │                               │
│  - Data entry forms │     │  /api/profile      (CRUD)    │
│  - Chat interface   │     │  /api/chat         (AI)      │
│                     │     │                               │
└─────────────────────┘     │                               │
                            │  ┌───────────────────────┐   │
                            │  │  AI Service Layer      │   │
                            │  │  - System prompt       │   │
                            │  │  - Context injection   │   │
                            │  │  - Conversation mgmt   │   │
                            │  └───────────────────────┘   │
                            │                               │
                            │  ┌───────────────────────┐   │
                            │  │  JSON File Storage     │   │
                            │  │  data/{userId}/        │   │
                            │  │    profile.json        │   │
                            │  └───────────────────────┘   │
                            └─────────────────────────────┘
```

### API Endpoints (v1)

**Profile Data (CRUD)**
- `GET /api/profile/{userId}` — full profile
- `PUT /api/profile/{userId}` — update full profile
- `POST /api/profile/{userId}/jobs` — add a job
- `PUT /api/profile/{userId}/jobs/{jobId}` — update a job
- `DELETE /api/profile/{userId}/jobs/{jobId}` — delete a job
- *(Same pattern for skills, projects, accomplishments)*

**Resume Generation (AI)**
- `POST /api/chat` — single endpoint for both initial generation and conversational iteration

The frontend maintains conversation history in state and sends the full message array with each request. The backend is stateless — it loads the user's profile, prepends the system prompt and profile context, and forwards the messages to Claude.

```json
POST /api/chat
{
  "userId": "user-1",
  "messages": [
    {"role": "user", "content": "Create a resume focusing on leadership"},
    {"role": "assistant", "content": "# Jane Doe\n\n..."},
    {"role": "user", "content": "Make the cloud section more prominent"}
  ]
}
```

The first message in a conversation is the initial generation. Every subsequent message is iteration. From the API's perspective, the operation is identical: system prompt + profile data + conversation history + new message → Claude → response. Keeping the full history enables the user to reference and revisit earlier drafts during refinement.

---

## AI Integration Design

### System Prompt Strategy

The resume generation is driven by a system prompt that lives in a dedicated file (e.g., `prompts/resume_system.txt`) so it can be iterated on independently of the code. The system prompt includes:

1. **Role definition** — "You are a resume writing assistant..."
2. **Resume best practices** — focus on recent/relevant experience, use strong action verbs, quantify impact, tailor to audience
3. **Output format** — produce clean markdown with standard resume sections
4. **Context handling** — instructions for how to interpret the injected career data

### Context Injection

When generating a resume, the backend:

1. Loads the user's full `profile.json`
2. Serializes it into the system prompt (or as a user message prefix)
3. Appends the user's generation instructions (or defaults to "Create a well-rounded resume")
4. Sends to Claude API

### Conversation Flow

The frontend manages conversation state. Each request sends the full message history, making the backend stateless.

```
User: "Create a resume focusing on leadership and cloud architecture"
  ↓
Frontend sends: { messages: [user message] }
  ↓
Backend: [system prompt + full profile JSON + messages] → Claude API
  ↓
Claude: [markdown resume draft]
  ↓
User: "Make the AWS section more prominent and drop anything before 2018"
  ↓
Frontend sends: { messages: [user msg, assistant msg, new user msg] }
  ↓
Backend: [system prompt + profile JSON + full message history] → Claude API
  ↓
Claude: [revised markdown resume]
```

The user can start a new conversation at any time to begin a fresh generation.

### AI Guardrails

Defense in depth to keep the AI scoped to its intended purpose:

**Prompt-level constraints.** The system prompt explicitly instructs the model that it is a resume writing assistant and should decline requests unrelated to resume content. It should not act as a general-purpose chatbot, produce content unrelated to the user's career data, or follow instructions that attempt to override its role.

**Input validation (`guardrails.py`).** User messages are validated before reaching the AI. This includes enforcing a maximum message length, limiting conversation history depth (configurable via `MAX_CONVERSATION_TURNS`), and basic sanitization to strip prompt injection patterns (e.g., "ignore all previous instructions").

**Output validation.** AI responses are checked before being returned to the frontend. If the model's response appears to have deviated from resume content (e.g., it contains code blocks unrelated to resume formatting, or disclaimers suggesting it was manipulated), the response is flagged or replaced with a safe fallback.

**Rate limiting and cost awareness.** The chat endpoint should enforce sensible limits on request frequency and conversation length to prevent runaway API costs, whether from a bug or misuse.

---

## Phased Build Plan

### Phase 1: Foundation (Tracer Bullet)

**Goal:** End-to-end flow working — enter one job and one accomplishment, generate a basic resume via AI. Establish the module structure and engineering patterns that all future work builds on.

Steps:
1. Initialize monorepo structure with the full directory layout (routes, services, ai, storage)
2. Implement `config.py` with environment validation — the app should refuse to start if `ANTHROPIC_API_KEY` is missing
3. Set up `logging_setup.py` with structured logging and request context (request ID, user ID)
4. Define standard API response envelope and error shapes in `errors.py`
5. Set up FastAPI with health check, CORS middleware, and centralized error handling
6. Implement JSON file storage utility (read/write profile) in `storage/json_store.py`
7. Define Pydantic models for the profile data structures
8. Build profile CRUD endpoints for jobs + accomplishments, routed through the service layer
9. Set up React app with Vite + TypeScript, install dependencies, create the API client service
10. Define TypeScript interfaces mirroring the backend Pydantic models
11. Build a minimal data entry form for adding a job and an accomplishment
12. Integrate Anthropic SDK in `ai/client.py` behind a provider-agnostic interface, create initial system prompt, implement basic input guardrails
13. Create a mock AI client for testing that returns canned responses
14. Build the `/api/chat` route → `chat_service` → AI layer pipeline
15. Build a simple chat UI that sends messages and renders the AI's markdown response
16. Wire it all together — enter data, generate resume via chat, see output
17. Write initial unit tests for storage and profile service layers
18. Write the initial README covering project purpose, architecture overview, and setup instructions

### Phase 2: Full Data Entry

**Goal:** Complete the data model with full CRUD for all entity types.

Steps:
1. Add skills and projects CRUD endpoints
2. Build form components for skills, projects, and additional accomplishments
3. Add linking UI (associate accomplishments with jobs, skills, projects)
4. Add a profile overview/dashboard showing all entered data
5. Data validation on both frontend and backend

### Phase 3: Chat Refinement & UX

**Goal:** Polish the conversational resume iteration experience.

Steps:
1. Add visual distinction between user messages and AI responses in the chat UI
2. Render the latest AI response in a dedicated markdown preview pane (split view)
3. Add "copy to clipboard" for the current resume draft
4. Add "new conversation" to start a fresh generation
5. Iterate on the system prompt based on output quality

### Phase 4: Hardening & Polish

**Goal:** Make the AI output genuinely good, the error handling robust, and the project presentation-ready.

Steps:
1. Refine system prompt with resume best practices and formatting rules
2. Add preset generation options ("leadership-focused", "technical deep-dive", etc.)
3. Harden error handling: structured error responses for all failure modes (AI timeout, rate limit, invalid input, storage errors)
4. Harden AI guardrails: test with adversarial prompts, refine input sanitization and output validation
5. Add ability to save/name generated resume versions (store as markdown files)
6. Frontend loading states, error toasts, and graceful degradation
7. Finalize the README: architecture diagram, setup guide, design decisions, screenshots

### Phase 5: Tailored Resume Generation (Stretch)

**Goal:** Paste a job description and get a resume tailored to it.

Steps:
1. Add job description input (paste or URL)
2. Build a tailoring prompt that analyzes the JD and maps it to the user's experience
3. Extend the chat interface to support tailoring context
4. Consider adding an "analysis" step that shows which accomplishments are most relevant before generating

---

## Project Structure

```
resume-builder/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── DataEntry/        # Forms for jobs, skills, projects, accomplishments
│   │   │   ├── Chat/             # Chat interface for resume generation
│   │   │   ├── ResumePreview/    # Markdown preview pane
│   │   │   └── Layout/           # Navigation, layout components
│   │   ├── hooks/                # Custom hooks (useChat, useProfile, etc.)
│   │   ├── types/                # TypeScript interfaces mirroring backend Pydantic models
│   │   ├── services/
│   │   │   └── api.ts            # API client — single point of contact with backend
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── backend/
│   ├── app/
│   │   ├── main.py               # FastAPI app bootstrap and middleware
│   │   ├── config.py             # Validated configuration (fails fast on missing values)
│   │   ├── logging_setup.py      # Structured logging configuration
│   │   ├── routes/
│   │   │   ├── profile.py        # Profile CRUD route handlers
│   │   │   └── chat.py           # Chat/generation route handler
│   │   ├── services/
│   │   │   ├── profile_service.py  # Business logic for profile operations
│   │   │   └── chat_service.py     # Orchestrates AI calls with profile context
│   │   ├── ai/
│   │   │   ├── client.py         # Claude API client wrapper (provider-agnostic interface)
│   │   │   ├── prompts.py        # Prompt construction and context injection
│   │   │   └── guardrails.py     # Input validation and output safety checks
│   │   ├── storage/
│   │   │   └── json_store.py     # JSON file persistence (isolated from business logic)
│   │   ├── models.py             # Pydantic models (shared data contracts)
│   │   ├── errors.py             # Custom exception types and error response formatting
│   │   └── prompts/
│   │       └── resume_system.txt # System prompt (iterable, outside of code)
│   ├── tests/
│   │   ├── conftest.py           # Shared fixtures (mock AI client, temp storage, etc.)
│   │   ├── test_profile_service.py
│   │   ├── test_chat_service.py
│   │   ├── test_json_store.py
│   │   └── test_routes/          # Integration tests against the FastAPI test client
│   ├── requirements.txt
│   └── .env.example
├── data/
│   └── {userId}/
│       └── profile.json
├── README.md
└── plan.md                       # This file
```

### Module Responsibilities

The backend structure enforces clear boundaries:

- **`routes/`** — HTTP concerns only. Parse requests, call services, return responses. No business logic, no direct AI or storage access.
- **`services/`** — Business logic and orchestration. The `chat_service` loads the profile, calls the AI layer, and returns results. The `profile_service` validates and coordinates CRUD operations.
- **`ai/`** — Everything AI-related. The `client` wraps the Anthropic SDK behind an interface. `prompts` handles construction and context injection. `guardrails` validates that inputs are safe to send and outputs are scoped to resume content.
- **`storage/`** — Persistence only. Reads and writes JSON. Knows nothing about what the data means.
- **`models.py`** — Shared Pydantic models that define the data contracts between layers.
- **`errors.py`** — Centralized error types. Routes catch service/AI exceptions and map them to appropriate HTTP responses.

---

## Getting Started (Quick Reference)

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn anthropic pydantic python-dotenv
cp .env.example .env  # Add your ANTHROPIC_API_KEY
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm create vite@latest . -- --template react-ts
npm install
npm run dev
```

---

## Key Decisions & Tradeoffs

| Decision | Rationale | Revisit When... |
|----------|-----------|-----------------|
| JSON file storage | Zero setup, AI-context-friendly, easy to iterate | Multi-user, concurrent access, or data > a few MB |
| Single file per user | Simplifies context injection — load one file, send to AI | Profile data grows very large |
| System prompt in a file | Iterate on prompt without code changes | Need dynamic/conditional prompting |
| Frontend-managed chat history | Backend stays stateless; frontend sends full history each request | Want to save/resume conversations across sessions |
| Markdown output only | Fast to implement, easy to copy/paste | Want PDF/DOCX export |
| Monorepo | Everything in one place for a portfolio project | Team scales or deploys separately |

---

## Future Ideas (Backlog)

- AI-assisted data intake ("paste your LinkedIn, I'll structure it")
- PDF/DOCX export from generated markdown
- Multiple resume versions saved and named
- Side-by-side diff when iterating on a resume
- Job description URL scraping for the tailoring feature
- Skills gap analysis (compare your profile to a job description)
- Interview prep mode (generate likely questions based on your resume + a JD)
