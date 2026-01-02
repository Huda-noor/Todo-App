# Research: Phase II Full-Stack Todo Web Application

**Feature**: 001-phase-ii-fullstack-todo
**Date**: 2025-12-28
**Status**: Complete

## Research Questions

### RQ-1: Better Auth Integration with FastAPI Backend

**Question**: How does Better Auth (TypeScript library) integrate with a separate FastAPI (Python) backend?

**Decision**: Better Auth runs on Next.js server-side (API routes), with FastAPI validating sessions by reading the session token cookie and querying the shared database.

**Rationale**:
- Better Auth is a TypeScript-only library that cannot run in Python
- Next.js is a full-stack framework with API routes capability
- Better Auth uses the session database table as the source of truth
- FastAPI can validate sessions by:
  1. Reading the `better-auth.session_token` cookie from requests
  2. Querying the `session` table in the shared PostgreSQL database
  3. Verifying the session is valid and not expired
  4. Extracting the user ID from the session record

**Alternatives Considered**:
1. JWT Plugin approach - Adds complexity, requires JWT verification in Python
2. Proxy all requests through Next.js - Creates unnecessary bottleneck
3. Use FastAPI-Users instead - Different library, doesn't match constitution requirement

**Sources**:
- [Better Auth Installation](https://www.better-auth.com/docs/installation)
- [Better Auth Discussion #5578](https://github.com/better-auth/better-auth/discussions/5578)

---

### RQ-2: FastAPI + SQLModel Project Structure

**Question**: What is the recommended project structure for FastAPI with SQLModel and PostgreSQL?

**Decision**: Use a modular structure with separate folders for routers, models, schemas, and dependencies.

**Rationale**:
- Official FastAPI best practices recommend separation of concerns
- SQLModel combines Pydantic validation with SQLAlchemy ORM
- Dependency injection pattern for database sessions is idiomatic FastAPI

**Recommended Structure**:
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── config.py            # Environment configuration
│   ├── database.py          # Database connection and session
│   ├── models/              # SQLModel table definitions
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── todo.py
│   ├── schemas/             # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── todo.py
│   ├── routers/             # API route handlers
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── todos.py
│   └── dependencies/        # Dependency injection functions
│       ├── __init__.py
│       └── auth.py          # Session validation dependency
└── tests/
```

**Alternatives Considered**:
1. Single-file structure - Not scalable, harder to maintain
2. Feature-based folders - Overkill for Phase II scope
3. Full-stack template with Docker - Phase III+ technology, not allowed

**Sources**:
- [FastAPI SQL Databases Tutorial](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)

---

### RQ-3: Session Validation Architecture

**Question**: How should FastAPI validate Better Auth sessions without running Better Auth?

**Decision**: FastAPI reads the session token cookie and queries the session table directly in the shared Neon PostgreSQL database.

**Rationale**:
- Better Auth stores sessions in a `session` table with token, user_id, and expires_at
- FastAPI can query this table to validate sessions
- No cryptographic verification needed if using session-based auth (not JWT)
- Same database used by both Next.js (Better Auth) and FastAPI

**Session Validation Flow**:
1. Client sends request with `better-auth.session_token` cookie
2. FastAPI dependency extracts cookie value
3. Query `session` table: `WHERE token = ? AND expires_at > NOW()`
4. If valid, attach user_id to request context
5. If invalid/expired, return 401 Unauthorized

**Alternatives Considered**:
1. JWT validation - Requires cryptographic verification, more complex
2. Call Better Auth API to validate - Adds network hop, latency
3. Forward auth via reverse proxy - Adds infrastructure complexity

---

### RQ-4: Next.js App Router Structure

**Question**: What is the recommended Next.js structure for authentication with Better Auth?

**Decision**: Use Next.js App Router with dedicated auth routes and protected todo pages.

**Rationale**:
- App Router is the modern Next.js standard (Next.js 13+)
- Server Components allow server-side session checks
- Better Auth provides native Next.js integration with `toNextJsHandler`

**Recommended Structure**:
```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx           # Root layout with auth provider
│   │   ├── page.tsx             # Landing/redirect page
│   │   ├── signin/
│   │   │   └── page.tsx         # Sign in page
│   │   ├── signup/
│   │   │   └── page.tsx         # Sign up page
│   │   ├── todos/
│   │   │   └── page.tsx         # Protected todo list page
│   │   └── api/
│   │       └── auth/
│   │           └── [...all]/
│   │               └── route.ts # Better Auth handler
│   ├── components/
│   │   ├── auth/                # Auth-related components
│   │   └── todos/               # Todo-related components
│   ├── lib/
│   │   ├── auth.ts              # Better Auth client config
│   │   ├── auth-client.ts       # Client-side auth utilities
│   │   └── api-client.ts        # FastAPI client wrapper
│   └── types/
│       └── index.ts             # TypeScript types
└── tests/
```

**Sources**:
- [Better Auth Next.js Integration](https://www.better-auth.com/docs/integrations/next)
- [Next.js Example](https://www.better-auth.com/docs/examples/next-js)

---

### RQ-5: Cross-Origin Cookie Configuration

**Question**: How to handle cookies between Next.js frontend and FastAPI backend?

**Decision**: Use same-origin deployment or configure CORS with credentials.

**Rationale**:
- Better Auth sets HTTP-only cookies for session management
- FastAPI must receive these cookies to validate sessions
- Development: Run both on localhost with different ports
- Production: Deploy under same domain or configure cross-origin

**Configuration Requirements**:

**Better Auth (Next.js)**:
- Set `trustedOrigins` to include FastAPI backend URL
- Configure `sameSite: 'lax'` for same-site, `'none'` for cross-origin
- Set `secure: true` for production (HTTPS)

**FastAPI**:
- Configure CORS middleware with `allow_credentials=True`
- Set `allow_origins` to Next.js frontend URL
- Read cookies from request headers

**Development Setup**:
- Next.js: `http://localhost:3000`
- FastAPI: `http://localhost:8000`
- Cookies work with `sameSite: 'lax'` on localhost

---

### RQ-6: Database Schema for Better Auth

**Question**: What database tables does Better Auth require?

**Decision**: Better Auth auto-generates user and session tables; we add a custom todo table.

**Rationale**:
- Better Auth CLI generates required tables via migration
- Tables include: `user`, `session`, `account`, `verification`
- Our `todo` table references the Better Auth `user` table
- SQLModel models in FastAPI must match Better Auth schema

**Better Auth Tables** (auto-generated):
```sql
-- user table (Better Auth)
CREATE TABLE "user" (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    name TEXT,
    image TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- session table (Better Auth)
CREATE TABLE "session" (
    id TEXT PRIMARY KEY,
    token TEXT UNIQUE NOT NULL,
    user_id TEXT REFERENCES "user"(id),
    expires_at TIMESTAMP NOT NULL,
    ip_address TEXT,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- account table (Better Auth - for credentials)
CREATE TABLE "account" (
    id TEXT PRIMARY KEY,
    user_id TEXT REFERENCES "user"(id),
    account_id TEXT NOT NULL,
    provider_id TEXT NOT NULL,
    access_token TEXT,
    refresh_token TEXT,
    expires_at TIMESTAMP,
    password TEXT  -- hashed password for email/password auth
);
```

**Custom Todo Table**:
```sql
CREATE TABLE "todo" (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT REFERENCES "user"(id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    is_complete BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

---

## Resolved Clarifications

All technical unknowns have been resolved through research:

| Unknown | Resolution |
|---------|------------|
| Better Auth + FastAPI integration | Session validation via shared database |
| Project structure | Modular FastAPI + App Router Next.js |
| Session validation | Direct database query of session table |
| Cookie handling | CORS with credentials, same-site cookies |
| Database schema | Better Auth auto-generated + custom todo |

## Architecture Decisions Identified

The following decisions warrant ADR documentation:

1. **ADR-001: Session-Based Authentication with Shared Database**
   - Better Auth on Next.js, session validation in FastAPI via database
   - Impact: Cross-service authentication architecture

2. **ADR-002: Separate Backend and Frontend Codebases**
   - FastAPI backend, Next.js frontend as independent projects
   - Impact: Deployment, development workflow, team structure

3. **ADR-003: Better Auth for Authentication**
   - Using Better Auth library as specified in constitution
   - Impact: Session management, user table schema, cookie handling
