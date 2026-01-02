# Implementation Plan: Phase II Full-Stack Todo Web Application

**Branch**: `001-phase-ii-fullstack-todo` | **Date**: 2025-12-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-phase-ii-fullstack-todo/spec.md`

## Summary

Phase II transforms the Todo project from a console application (Phase I) into a full-stack web application with:
- **Backend**: FastAPI REST API with SQLModel ORM and Neon PostgreSQL
- **Frontend**: Next.js (React + TypeScript) with Better Auth for authentication
- **Architecture**: Separate frontend and backend with shared database for session validation

Key architectural decision: Better Auth runs on Next.js server-side, while FastAPI validates sessions by reading the session token cookie and querying the shared database.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript 5.x (frontend)
**Primary Dependencies**:
- Backend: FastAPI, SQLModel, psycopg2-binary, pydantic-settings, uvicorn
- Frontend: Next.js 14+, React 18+, Better Auth, TypeScript

**Storage**: Neon Serverless PostgreSQL (shared between frontend and backend)
**Testing**: pytest (backend), Jest/Vitest (frontend)
**Target Platform**: Web application (server: any platform, client: modern browsers)
**Project Type**: Web application (separate backend and frontend)
**Performance Goals**:
- API response < 2 seconds under normal load
- Page load < 3 seconds on standard connection
- UI feedback within 200ms of user action

**Constraints**:
- No Phase III+ technologies (Docker, Kubernetes, Kafka, Dapr)
- No AI, agents, background jobs, or WebSockets
- Email/password authentication only (no OAuth, SSO)
- No password reset or email verification

**Scale/Scope**: Single-user development, supports concurrent sessions

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| Spec-Driven Development | PASS | Implementation derives from spec.md |
| Phase Isolation | PASS | Only Phase II technologies used |
| Technology Constraints | PASS | FastAPI, SQLModel, Neon, Next.js, Better Auth |
| Clean Architecture | PASS | Separation of concerns in project structure |
| Full-Stack Separation | PASS | Independent backend API and frontend client |
| API Design | PASS | RESTful endpoints with consistent error format |
| Authentication Security | PASS | Hashed passwords, session expiration |
| No Feature Invention | PASS | Only specified features implemented |

**Post-Design Re-Check**: All gates pass. No constitutional violations.

## Project Structure

### Documentation (this feature)

```text
specs/001-phase-ii-fullstack-todo/
├── spec.md              # Feature specification (input)
├── plan.md              # This file (implementation plan)
├── research.md          # Technical research findings
├── data-model.md        # Database schema design
├── quickstart.md        # Development setup guide
├── contracts/           # API contracts
│   └── openapi.yaml     # OpenAPI 3.1 specification
├── checklists/          # Quality validation
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Task breakdown (created by /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Environment configuration (pydantic-settings)
│   ├── database.py          # Database connection and session management
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User model (read-only, Better Auth managed)
│   │   ├── session.py       # Session model (read-only, Better Auth managed)
│   │   └── todo.py          # Todo model (full CRUD)
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py          # User response schemas
│   │   └── todo.py          # Todo request/response schemas
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py          # Auth endpoints (/api/auth/me)
│   │   └── todos.py         # Todo CRUD endpoints
│   └── dependencies/
│       ├── __init__.py
│       └── auth.py          # Session validation dependency
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── test_auth.py         # Auth endpoint tests
│   └── test_todos.py        # Todo endpoint tests
├── alembic/
│   ├── env.py
│   └── versions/            # Migration files
├── alembic.ini
├── requirements.txt
├── .env.example
└── pytest.ini

frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx           # Root layout with auth provider
│   │   ├── page.tsx             # Landing page (redirect logic)
│   │   ├── signin/
│   │   │   └── page.tsx         # Sign in page
│   │   ├── signup/
│   │   │   └── page.tsx         # Sign up page
│   │   ├── todos/
│   │   │   └── page.tsx         # Protected todo list page
│   │   └── api/
│   │       └── auth/
│   │           └── [...all]/
│   │               └── route.ts # Better Auth route handler
│   ├── components/
│   │   ├── auth/
│   │   │   ├── SignInForm.tsx   # Sign in form component
│   │   │   ├── SignUpForm.tsx   # Sign up form component
│   │   │   └── AuthGuard.tsx    # Protected route wrapper
│   │   ├── todos/
│   │   │   ├── TodoList.tsx     # Todo list container
│   │   │   ├── TodoItem.tsx     # Individual todo item
│   │   │   ├── TodoForm.tsx     # Create/edit todo form
│   │   │   └── EmptyState.tsx   # No todos message
│   │   └── ui/
│   │       ├── Button.tsx       # Reusable button
│   │       ├── Input.tsx        # Form input
│   │       └── Loading.tsx      # Loading indicator
│   ├── lib/
│   │   ├── auth.ts              # Better Auth server config
│   │   ├── auth-client.ts       # Better Auth client instance
│   │   └── api-client.ts        # FastAPI client wrapper
│   └── types/
│       └── index.ts             # TypeScript type definitions
├── tests/
│   └── components/              # Component tests
├── package.json
├── tsconfig.json
├── next.config.js
├── tailwind.config.js           # If using Tailwind CSS
└── .env.example
```

**Structure Decision**: Web application with separate backend and frontend directories. This matches Phase II requirements for full-stack separation and allows independent development, testing, and deployment of each layer.

---

## Overall Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              CLIENT (Browser)                            │
├─────────────────────────────────────────────────────────────────────────┤
│  Next.js Frontend (localhost:3000)                                       │
│  ├── React Components (UI)                                               │
│  ├── Better Auth Client (auth state, signin/signup forms)                │
│  └── API Client (calls to FastAPI backend)                               │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
         ┌───────────────────────────┼───────────────────────────┐
         │                           │                           │
         ▼                           ▼                           │
┌─────────────────────┐   ┌─────────────────────┐               │
│ Next.js API Routes  │   │  FastAPI Backend    │               │
│ (Better Auth)       │   │  (localhost:8000)   │               │
│                     │   │                     │               │
│ /api/auth/*         │   │ /api/auth/me        │               │
│ - signup            │   │ /api/todos          │               │
│ - signin            │   │ /api/todos/{id}     │               │
│ - signout           │   │ /api/todos/{id}/toggle│             │
└─────────┬───────────┘   └─────────┬───────────┘               │
          │                         │                           │
          │    Session Cookie       │    Session Cookie         │
          │    (better-auth.        │    Validation             │
          │     session_token)      │                           │
          │                         │                           │
          └────────────┬────────────┘                           │
                       │                                        │
                       ▼                                        │
          ┌─────────────────────────┐                           │
          │   Neon PostgreSQL       │                           │
          │   (Shared Database)     │                           │
          │                         │                           │
          │ Tables:                 │                           │
          │ - user (Better Auth)    │                           │
          │ - session (Better Auth) │                           │
          │ - account (Better Auth) │                           │
          │ - todo (FastAPI)        │                           │
          └─────────────────────────┘                           │
                                                                │
          Session token cookie flows from browser ──────────────┘
```

### Separation of Concerns

| Layer | Responsibility | Technology |
|-------|----------------|------------|
| Presentation | UI rendering, user interactions | Next.js + React |
| Authentication | User signup/signin/signout | Better Auth (Next.js) |
| Session Validation | Verify authenticated requests | FastAPI (database query) |
| Business Logic | Todo CRUD operations | FastAPI routers |
| Data Access | Database queries | SQLModel + PostgreSQL |
| Persistence | Data storage | Neon PostgreSQL |

### Authentication Flow

```
1. SIGNUP FLOW
   Browser → Next.js /api/auth/signup → Better Auth
                                        ├── Create user in DB
                                        ├── Create account in DB
                                        ├── Create session in DB
                                        └── Set session cookie
   Browser ← Redirect to /todos

2. SIGNIN FLOW
   Browser → Next.js /api/auth/signin → Better Auth
                                        ├── Verify credentials
                                        ├── Create session in DB
                                        └── Set session cookie
   Browser ← Redirect to /todos

3. API REQUEST FLOW
   Browser → FastAPI /api/todos (with session cookie)
                     ├── Auth dependency extracts cookie
                     ├── Query session table in DB
                     ├── Verify not expired
                     ├── Get user_id from session
                     └── Execute todo operation
   Browser ← JSON response

4. SIGNOUT FLOW
   Browser → Next.js /api/auth/signout → Better Auth
                                         ├── Delete session from DB
                                         └── Clear session cookie
   Browser ← Redirect to /signin
```

---

## Backend Architecture (FastAPI)

### Project Structure

```
backend/app/
├── main.py          # App initialization, CORS, router mounting
├── config.py        # Settings from environment variables
├── database.py      # Engine, session factory, dependency
├── models/          # SQLModel table definitions
├── schemas/         # Pydantic request/response models
├── routers/         # API endpoint handlers
└── dependencies/    # Reusable dependencies (auth, etc.)
```

### Application Initialization (main.py)

- Create FastAPI app instance
- Configure CORS middleware (allow frontend origin, credentials)
- Mount routers with `/api` prefix
- Include exception handlers for consistent error responses

### Configuration (config.py)

Environment variables via pydantic-settings:
- `DATABASE_URL`: Neon PostgreSQL connection string
- `FRONTEND_URL`: Next.js frontend URL (for CORS)
- `CORS_ORIGINS`: Allowed origins list

### Database Connection (database.py)

- Create SQLModel engine with Neon connection string
- Session factory using `sessionmaker`
- `get_session` dependency for dependency injection
- Connection pooling appropriate for serverless

### Routing Strategy

| Router | Prefix | Endpoints |
|--------|--------|-----------|
| auth | /api/auth | GET /me |
| todos | /api/todos | GET, POST /, GET, PUT, DELETE /{id}, PATCH /{id}/toggle |

### Dependency Injection

**Database Session**:
```python
def get_session():
    with Session(engine) as session:
        yield session
```

**Current User (Auth)**:
```python
def get_current_user(
    request: Request,
    session: Session = Depends(get_session)
) -> User:
    # Extract session token from cookie
    # Query session table
    # Return user or raise 401
```

### User-to-Todo Ownership Enforcement

- All todo queries include `user_id = current_user.id` filter
- Prevents access to other users' todos
- Returns 404 (not 403) for unauthorized access attempts (no information leakage)

---

## Database Layer (SQLModel + Neon PostgreSQL)

### Models

See [data-model.md](./data-model.md) for complete definitions.

**Key Points**:
- User and Session models are read-only (Better Auth managed)
- Todo model is full CRUD (FastAPI managed)
- Foreign key from todo.user_id to user.id with CASCADE delete

### Migration Strategy

1. Better Auth generates its tables via CLI
2. Alembic manages the todo table migration
3. Order: Better Auth first, then Alembic

### Connection Handling

- Use SSL mode for Neon (`?sslmode=require`)
- Connection pooling via SQLModel/SQLAlchemy defaults
- Session-per-request pattern via dependency injection

---

## Frontend Architecture (Next.js + TypeScript)

### App Router Structure

```
src/app/
├── layout.tsx       # Root layout, auth provider wrapper
├── page.tsx         # / - Landing, redirects based on auth
├── signin/page.tsx  # /signin - Sign in form
├── signup/page.tsx  # /signup - Sign up form
├── todos/page.tsx   # /todos - Protected todo list
└── api/auth/[...all]/route.ts  # Better Auth handler
```

### Component Hierarchy

```
RootLayout (auth provider)
├── SignInPage
│   └── SignInForm
├── SignUpPage
│   └── SignUpForm
└── TodosPage (protected)
    ├── Header (user email, logout button)
    ├── TodoForm (create new)
    └── TodoList
        └── TodoItem (toggle, edit, delete)
```

### Authentication State Management

- Better Auth client provides hooks: `useSession`, `signIn`, `signUp`, `signOut`
- AuthGuard component checks session and redirects if unauthenticated
- Server components can access session via `auth.api.getSession`

### API Client Strategy

- Wrapper around `fetch` with base URL configuration
- Automatically includes credentials for cookies
- Handles error responses and transforms to user-friendly messages
- TypeScript types for request/response payloads

---

## API Integration & Communication

### Request/Response Flow

**Create Todo**:
1. User fills TodoForm, submits
2. Frontend validates (non-empty, ≤500 chars)
3. API client POSTs to `/api/todos`
4. FastAPI validates, inserts, returns todo
5. Frontend updates list state

**Toggle Todo**:
1. User clicks checkbox
2. API client PATCHes to `/api/todos/{id}/toggle`
3. FastAPI toggles, returns updated todo
4. Frontend updates item state

### Cookie Handling

- Better Auth sets `better-auth.session_token` HTTP-only cookie
- Frontend requests include `credentials: 'include'`
- FastAPI reads cookie from request headers
- Same-site deployment: `sameSite: 'lax'`

### Protected Routes

**Frontend**:
- AuthGuard component wraps protected pages
- Checks session, redirects to /signin if unauthenticated

**Backend**:
- `get_current_user` dependency on all /api/todos endpoints
- Returns 401 if session invalid or expired

### Error Handling Propagation

```
Backend Error → JSON Response → API Client → UI Component → User Message

Example:
400 {"error": "Todo description cannot be empty"}
    → apiClient catches 400
    → throws ApiError with message
    → TodoForm catches, shows inline error
```

---

## Error Handling & Validation Strategy

### Backend

**HTTP Status Codes**:
| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET, PUT, PATCH, DELETE |
| 201 | Created | Successful POST |
| 400 | Bad Request | Validation errors |
| 401 | Unauthorized | Missing or invalid session |
| 404 | Not Found | Todo not found (or unauthorized access) |
| 500 | Internal Error | Unexpected server errors |

**Error Response Format**:
```json
{"error": "Human-readable error message"}
```

**Input Validation**:
- Pydantic schemas validate request bodies
- SQLModel constraints enforce database rules
- Custom validators for business rules (description length)

### Frontend

**User-Friendly Messages**:
- Map API errors to display messages
- Show inline errors on forms
- Toast notifications for operations

**Loading States**:
- Show spinner during API calls
- Disable form buttons while submitting
- Optimistic updates for toggle (revert on error)

**Form Validation**:
- Client-side validation before submit
- Match backend rules (non-empty, ≤500 chars)
- Immediate feedback on invalid input

---

## Non-Functional Considerations

### Security

**Password Hashing**: Better Auth uses bcrypt (configurable)
**Protected Endpoints**: All /api/todos require valid session
**CORS Configuration**:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
**No Information Leakage**: Unauthorized todo access returns 404

### Responsiveness

- Mobile-first CSS approach
- Responsive breakpoints for form/list layouts
- Touch-friendly targets (checkboxes, buttons)
- CSS: Plain CSS or Tailwind (decision during implementation)

### Development Setup

**Environment Variables**:
- Backend: `.env` with DATABASE_URL, FRONTEND_URL
- Frontend: `.env.local` with BETTER_AUTH_SECRET, DATABASE_URL, NEXT_PUBLIC_API_URL

**Concurrent Running**:
- Backend: `uvicorn app.main:app --reload --port 8000`
- Frontend: `npm run dev` (port 3000)

**Local Neon Connection**: Use connection string from Neon dashboard with SSL

---

## Complexity Tracking

No constitutional violations requiring justification. Architecture follows all principles:
- Two projects (backend/frontend) is appropriate for full-stack separation
- No unnecessary abstractions or patterns
- Direct database access without Repository pattern
- Simple session validation without JWT complexity

---

## Artifacts Generated

| Artifact | Path | Purpose |
|----------|------|---------|
| Research | specs/001-phase-ii-fullstack-todo/research.md | Technical decisions and rationale |
| Data Model | specs/001-phase-ii-fullstack-todo/data-model.md | Database schema design |
| API Contract | specs/001-phase-ii-fullstack-todo/contracts/openapi.yaml | OpenAPI specification |
| Quickstart | specs/001-phase-ii-fullstack-todo/quickstart.md | Development setup guide |
| Plan | specs/001-phase-ii-fullstack-todo/plan.md | This document |

## Next Steps

1. **Run `/sp.tasks`** - Generate actionable implementation tasks
2. **Review ADR Suggestions** - Document architectural decisions if desired:
   - ADR-001: Session-Based Authentication with Shared Database
   - ADR-002: Separate Backend and Frontend Codebases
   - ADR-003: Better Auth for Authentication

## ADR Suggestions

The following architectural decisions were identified during planning:

**ADR-001: Session-Based Authentication with Shared Database**
> Better Auth on Next.js, session validation in FastAPI via database query
> Document reasoning and tradeoffs? Run `/sp.adr session-based-auth-shared-db`

**ADR-002: Separate Backend and Frontend Codebases**
> FastAPI backend, Next.js frontend as independent projects
> Document reasoning and tradeoffs? Run `/sp.adr separate-backend-frontend`

**ADR-003: Better Auth for Authentication**
> Using Better Auth library as specified in constitution
> Document reasoning and tradeoffs? Run `/sp.adr better-auth-selection`
