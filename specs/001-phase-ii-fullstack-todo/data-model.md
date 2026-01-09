# Data Model: Phase II Full-Stack Todo Web Application

**Feature**: 001-phase-ii-fullstack-todo
**Date**: 2025-12-28
**Source**: spec.md, research.md

## Overview

Phase II uses a shared Neon PostgreSQL database accessed by both:
- **Better Auth (Next.js)**: Manages `user`, `session`, `account` tables
- **FastAPI Backend**: Manages `todo` table, reads `user`/`session` for validation

## Entity Relationship Diagram (Text)

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│      user       │       │     session     │       │     account     │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id (PK)         │◄──────│ user_id (FK)    │       │ id (PK)         │
│ email           │       │ id (PK)         │       │ user_id (FK)    │──►
│ email_verified  │       │ token           │       │ account_id      │
│ name            │       │ expires_at      │       │ provider_id     │
│ image           │       │ ip_address      │       │ password        │
│ created_at      │       │ user_agent      │       │ ...             │
│ updated_at      │       │ created_at      │       └─────────────────┘
└─────────────────┘       │ updated_at      │
        │                 └─────────────────┘
        │
        │ 1:N
        ▼
┌─────────────────┐
│      todo       │
├─────────────────┤
│ id (PK)         │
│ user_id (FK)    │
│ description     │
│ is_complete     │
│ created_at      │
│ updated_at      │
└─────────────────┘
```

## Entities

### User (Better Auth Managed)

**Table**: `user`
**Owner**: Better Auth (auto-generated)
**FastAPI Access**: Read-only (for user info display)

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | TEXT | PRIMARY KEY | Better Auth generated ID |
| email | TEXT | UNIQUE, NOT NULL | User's email address |
| email_verified | BOOLEAN | DEFAULT FALSE | Email verification status |
| name | TEXT | NULLABLE | User's display name |
| image | TEXT | NULLABLE | Profile image URL |
| created_at | TIMESTAMP | DEFAULT NOW() | Account creation time |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update time |

**Notes**:
- Better Auth uses TEXT for IDs (not UUID)
- Email is case-insensitive for uniqueness (handled by Better Auth)
- FastAPI should NOT write to this table

---

### Session (Better Auth Managed)

**Table**: `session`
**Owner**: Better Auth (auto-generated)
**FastAPI Access**: Read-only (for session validation)

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | TEXT | PRIMARY KEY | Session ID |
| token | TEXT | UNIQUE, NOT NULL | Session token (in cookie) |
| user_id | TEXT | FOREIGN KEY → user(id) | Associated user |
| expires_at | TIMESTAMP | NOT NULL | Session expiration time |
| ip_address | TEXT | NULLABLE | Client IP address |
| user_agent | TEXT | NULLABLE | Client user agent |
| created_at | TIMESTAMP | DEFAULT NOW() | Session creation time |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update time |

**Session Validation Query**:
```sql
SELECT user_id FROM session
WHERE token = :session_token
AND expires_at > NOW();
```

---

### Account (Better Auth Managed)

**Table**: `account`
**Owner**: Better Auth (auto-generated)
**FastAPI Access**: None (authentication only)

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | TEXT | PRIMARY KEY | Account ID |
| user_id | TEXT | FOREIGN KEY → user(id) | Associated user |
| account_id | TEXT | NOT NULL | Provider account ID |
| provider_id | TEXT | NOT NULL | Auth provider (e.g., "credential") |
| password | TEXT | NULLABLE | Hashed password |
| access_token | TEXT | NULLABLE | OAuth access token |
| refresh_token | TEXT | NULLABLE | OAuth refresh token |
| expires_at | TIMESTAMP | NULLABLE | Token expiration |

**Notes**:
- For email/password auth, `provider_id = "credential"`
- Password is hashed by Better Auth (bcrypt)
- FastAPI should NOT access this table

---

### Todo (FastAPI Managed)

**Table**: `todo`
**Owner**: FastAPI backend
**FastAPI Access**: Full CRUD

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Todo unique ID |
| user_id | TEXT | FOREIGN KEY → user(id), ON DELETE CASCADE | Owner user |
| description | TEXT | NOT NULL, LENGTH 1-500 | Todo content |
| is_complete | BOOLEAN | DEFAULT FALSE | Completion status |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | DEFAULT NOW(), ON UPDATE | Last modification |

**Validation Rules**:
- `description`: Required, 1-500 characters, non-whitespace-only
- `user_id`: Must reference existing user
- `is_complete`: Defaults to false on creation

**Business Rules**:
- User can only access their own todos
- Deleting user cascades to delete all their todos
- `updated_at` auto-updates on any modification

---

## SQLModel Definitions (FastAPI)

### Session Model (Read-Only)

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Session(SQLModel, table=True):
    """Better Auth session table - READ ONLY"""
    __tablename__ = "session"

    id: str = Field(primary_key=True)
    token: str = Field(unique=True, index=True)
    user_id: str = Field(foreign_key="user.id")
    expires_at: datetime
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### User Model (Read-Only)

```python
class User(SQLModel, table=True):
    """Better Auth user table - READ ONLY"""
    __tablename__ = "user"

    id: str = Field(primary_key=True)
    email: str = Field(unique=True, index=True)
    email_verified: bool = Field(default=False)
    name: Optional[str] = None
    image: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Todo Model (Full CRUD)

```python
from uuid import UUID, uuid4

class Todo(SQLModel, table=True):
    """Todo table - managed by FastAPI"""
    __tablename__ = "todo"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    description: str = Field(min_length=1, max_length=500)
    is_complete: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

---

## Relationships

### User → Todo (One-to-Many)

- One user can have many todos
- Each todo belongs to exactly one user
- Cascade delete: when user is deleted, all their todos are deleted

### User → Session (One-to-Many)

- One user can have multiple active sessions
- Managed entirely by Better Auth
- FastAPI reads sessions for authentication validation

---

## Migration Strategy

### Phase 1: Better Auth Tables

Better Auth CLI generates initial migration:
```bash
npx @better-auth/cli generate
npx @better-auth/cli migrate
```

This creates: `user`, `session`, `account`, `verification` tables.

### Phase 2: Todo Table

After Better Auth tables exist, create todo table:

**Option A**: Alembic migration (recommended)
```bash
alembic revision --autogenerate -m "add_todo_table"
alembic upgrade head
```

**Option B**: Manual SQL
```sql
CREATE TABLE IF NOT EXISTS "todo" (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    description TEXT NOT NULL CHECK (length(description) >= 1 AND length(description) <= 500),
    is_complete BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_todo_user_id ON todo(user_id);
```

---

## Data Access Patterns

### FastAPI Queries

**Get User's Todos**:
```sql
SELECT * FROM todo WHERE user_id = :user_id ORDER BY created_at DESC;
```

**Create Todo**:
```sql
INSERT INTO todo (user_id, description) VALUES (:user_id, :description) RETURNING *;
```

**Update Todo**:
```sql
UPDATE todo SET description = :description, updated_at = NOW()
WHERE id = :id AND user_id = :user_id RETURNING *;
```

**Toggle Complete**:
```sql
UPDATE todo SET is_complete = NOT is_complete, updated_at = NOW()
WHERE id = :id AND user_id = :user_id RETURNING *;
```

**Delete Todo**:
```sql
DELETE FROM todo WHERE id = :id AND user_id = :user_id;
```

### Session Validation

```sql
SELECT s.user_id, u.email
FROM session s
JOIN "user" u ON s.user_id = u.id
WHERE s.token = :session_token AND s.expires_at > NOW();
```

---

## Indexes

| Table | Index | Columns | Purpose |
|-------|-------|---------|---------|
| user | PRIMARY | id | Primary key lookup |
| user | UNIQUE | email | Email uniqueness, login lookup |
| session | PRIMARY | id | Primary key lookup |
| session | UNIQUE | token | Session validation |
| todo | PRIMARY | id | Primary key lookup |
| todo | INDEX | user_id | User's todos query |
