# Phase II - Feature Specification

**Phase**: II | **Status**: Implemented
**Constitution**: [phase-ii-constitution.md](../constitution/phase-ii-constitution.md)

---

## Overview

Phase II transforms the Evolution of Todo from a console application into a full-stack web application with:
- **Backend**: FastAPI REST API with SQLModel ORM and Neon PostgreSQL
- **Frontend**: Next.js (React + TypeScript) with Better Auth
- **Authentication**: Email/password with session-based auth
- **Persistence**: PostgreSQL database storage

---

## User Stories Summary

### Authentication (P1)
| Story | Priority | Goal |
|-------|----------|------|
| Signup | P1 | Create account with email/password |
| Signin | P1 | Access account with credentials |
| Signout | P2 | End session securely |

### Todo Operations (P1-P3)
| Story | Priority | Goal |
|-------|----------|------|
| Create Todo | P1 | Add new task to list |
| View Todos | P1 | See all tasks with status |
| Toggle Complete | P1 | Mark task done/undone |
| Update Todo | P2 | Edit task description |
| Delete Todo | P2 | Remove task from list |

---

## Data Models

### User
```typescript
interface User {
  id: string;           // UUID
  email: string;        // unique, validated
  password: string;     // hashed, never stored raw
  created_at: string;   // ISO timestamp
}
```

### Todo
```typescript
interface Todo {
  id: string;           // UUID
  user_id: string;      // FK to User
  description: string;  // 1-500 chars
  is_complete: boolean; // default false
  created_at: string;   // ISO timestamp
  updated_at: string;   // auto-updated
}
```

### Session (Better Auth)
```typescript
interface Session {
  id: string;           // UUID
  user_id: string;      // FK to User
  expires_at: string;   // expiration timestamp
  token: string;        // session token
}
```

---

## API Endpoints

### Authentication
```
POST /api/auth/signup    → Create account
POST /api/auth/signin    → Authenticate
POST /api/auth/signout   → End session
GET  /api/auth/me        → Get current user
```

### Todos
```
GET    /api/todos              → List all todos
POST   /api/todos              → Create todo
GET    /api/todos/{id}         → Get single todo
PUT    /api/todos/{id}         → Update todo
DELETE /api/todos/{id}         → Delete todo
PATCH  /api/todos/{id}/toggle  → Toggle status
```

---

## Frontend Pages

| Route | Page | Auth Required |
|-------|------|---------------|
| / | Landing | No (redirects) |
| /signup | Sign Up | No |
| /signin | Sign In | No |
| /todos | Todo List | Yes (protected) |

---

## Component Hierarchy

```
RootLayout (AuthProvider)
├── SignInPage
│   └── SignInForm
├── SignUpPage
│   └── SignUpForm
└── TodosPage (Protected)
    ├── Header (user email, logout)
    ├── TodoForm (create new)
    └── TodoList
        └── TodoItem (toggle, edit, delete)
```

---

## Success Criteria

| Metric | Target |
|--------|--------|
| Signup completion | < 60 seconds |
| Signin completion | < 30 seconds |
| Todo creation | < 10 seconds |
| Page load | < 3 seconds |
| API response | < 2 seconds |
| Data isolation | 100% (no cross-user access) |

---

## Files Reference

| Path | Purpose |
|------|---------|
| `source-code/backend/` | FastAPI backend application |
| `source-code/frontend/` | Next.js frontend application |
| `specs/full-spec.md` | Complete feature specification |
| `architecture/system-architecture.md` | High-level architecture |
| `user-flows/auth-flows.md` | Authentication flows |
| `user-flows/todo-flows.md` | Todo operation flows |
| `data-models/database-schema.md` | Database schema |
| `apis/rest-api-contract.md` | API documentation |
| `non-functional/requirements.md` | NFRs |
| `ui-ux/design-guide.md` | UI/UX design guide |

---

**Phase II Complete** — Ready for Phase III extension
