# Phase II - System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           CLIENT (Browser)                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Next.js Frontend (localhost:3000)                                      │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  React Components                                               │   │
│  │  ├── Pages: /, /signup, /signin, /todos                        │   │
│  │  ├── Auth: Better Auth Client                                  │   │
│  │  └── UI: TodoList, TodoItem, TodoForm, SignInForm, etc.       │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
           ┌────────────────────────┼────────────────────────┐
           │                        │                        │
           ▼                        ▼                        │
┌─────────────────────┐   ┌─────────────────────┐            │
│  Next.js API Routes │   │  FastAPI Backend    │            │
│  (Better Auth)      │   │  (localhost:8000)   │            │
│                     │   │                     │            │
│  /api/auth/signup   │   │  /api/auth/me      │            │
│  /api/auth/signin   │   │  /api/todos        │            │
│  /api/auth/signout  │   │  /api/todos/{id}   │            │
│                     │   │  /api/todos/{id}   │            │
│                     │   │  /toggle           │            │
└─────────┬───────────┘   └──────────┬──────────┘            │
          │                          │                        │
          │    Session Cookie        │    Session Cookie      │
          │    (better-auth.         │    Validation          │
          │     session_token)       │                        │
          │                          │                        │
          └──────────────┬───────────┘                        │
                         │                                    │
                         ▼                                    │
          ┌─────────────────────────┐                         │
          │   Neon PostgreSQL       │                         │
          │   (Shared Database)     │                         │
          │                         │                         │
          │ Tables:                 │                         │
          │ - user (Better Auth)    │                         │
          │ - session (Better Auth) │                         │
          │ - account (Better Auth) │                         │
          │ - todo (FastAPI)        │                         │
          └─────────────────────────┘                         │
                                                               │
          Session token cookie flows from browser ─────────────┘
```

---

## Component Architecture

### Frontend (Next.js)
```
src/
├── app/
│   ├── layout.tsx              # Root layout with auth provider
│   ├── page.tsx                # Landing (redirects based on auth)
│   ├── signin/page.tsx         # Sign in page
│   ├── signup/page.tsx         # Sign up page
│   ├── todos/page.tsx          # Protected todo list
│   └── api/auth/[...all]/      # Better Auth route handler
├── components/
│   ├── auth/
│   │   ├── SignInForm.tsx
│   │   ├── SignUpForm.tsx
│   │   └── AuthGuard.tsx       # Protected route wrapper
│   └── todos/
│       ├── TodoList.tsx
│       ├── TodoItem.tsx
│       ├── TodoForm.tsx
│       └── EmptyState.tsx
├── lib/
│   ├── auth.ts                 # Better Auth server config
│   ├── auth-client.ts          # Better Auth client instance
│   └── api-client.ts           # FastAPI client wrapper
└── types/
    └── index.ts                # TypeScript types
```

### Backend (FastAPI)
```
backend/app/
├── main.py                     # FastAPI app initialization
├── config.py                   # Environment configuration
├── database.py                 # SQLModel engine, session factory
├── models/
│   ├── __init__.py
│   ├── user.py                 # User model (read-only)
│   ├── session.py              # Session model (read-only)
│   └── todo.py                 # Todo model (full CRUD)
├── schemas/
│   ├── __init__.py
│   ├── user.py                 # User schemas
│   └── todo.py                 # Todo schemas (Pydantic)
├── routers/
│   ├── __init__.py
│   ├── auth.py                 # Auth endpoints
│   └── todos.py                # Todo CRUD endpoints
└── dependencies/
    ├── __init__.py
    └── auth.py                 # Session validation dependency
```

---

## Database Schema

### Entity Relationship
```
┌─────────────────┐       ┌─────────────────┐
│     user        │       │     session     │
├─────────────────┤       ├─────────────────┤
│ id (PK)         │◄──────┤ user_id (FK)    │
│ email           │       │ id (PK)         │
│ password        │       │ expires_at      │
│ created_at      │       │ token           │
└─────────────────┘       └─────────────────┘
       │                          │
       │                          │
       ▼                          │
┌─────────────────┐
│      todo       │
├─────────────────┤
│ id (PK)         │
│ user_id (FK)    │────────► user.id
│ description     │
│ is_complete     │
│ created_at      │
│ updated_at      │
└─────────────────┘
```

### Table Definitions

**user table** (Better Auth managed)
```sql
CREATE TABLE user (
    id UUID PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL
);
```

**session table** (Better Auth managed)
```sql
CREATE TABLE session (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES user(id),
    expires_at TIMESTAMP NOT NULL,
    token VARCHAR(255) NOT NULL UNIQUE
);
```

**account table** (Better Auth managed)
```sql
CREATE TABLE account (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES user(id),
    account_id VARCHAR(255) NOT NULL,
    provider_id VARCHAR(255) NOT NULL,
    access_token VARCHAR(255),
    refresh_token VARCHAR(255),
    expires_at TIMESTAMP,
    password VARCHAR(255),
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
```

**todo table** (FastAPI managed)
```sql
CREATE TABLE todo (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES user(id) ON DELETE CASCADE,
    description VARCHAR(500) NOT NULL,
    is_complete BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE INDEX idx_todo_user_id ON todo(user_id);
```

---

## Authentication Flow

### Signup Flow
```
Browser                    Next.js                   Database
   │                          │                          │
   │── POST /api/auth/signup  │                          │
   │   {email, password}      │                          │
   │                          │── Create user            │
   │                          │   Create account         │
   │                          │   Create session         │
   │                          │                          │
   │                          │◄── Session created       │
   │◄── Set-Cookie: session   │                          │
   │                          │                          │
   │── Redirect /todos        │                          │
```

### Signin Flow
```
Browser                    Next.js                   Database
   │                          │                          │
   │── POST /api/auth/signin  │                          │
   │   {email, password}      │                          │
   │                          │── Verify credentials     │
   │                          │── Create session         │
   │                          │                          │
   │                          │◄── Session created       │
   │◄── Set-Cookie: session   │                          │
   │                          │                          │
   │── Redirect /todos        │                          │
```

### API Request Flow
```
Browser                                          FastAPI               Database
   │                                                │                    │
   │── GET /api/todos                               │                    │
   │   Cookie: better-auth.session_token=xxx        │                    │
   │                                                │                    │
   │                                                │── Extract cookie   │
   │                                                │── Query session    │
   │                                                │                    │
   │                                                │◄── Session valid   │
   │                                                │── Get user_id      │
   │                                                │── Query todos      │
   │                                                │   WHERE user_id = ?│
   │                                                │                    │
   │◄── {todos: [...]}                             │                    │
```

---

## API Layer Architecture

### Request/Response Pattern

```
┌─────────────────────────────────────────────────────────────────┐
│                        API Request                              │
│  Method: POST/PUT/PATCH/DELETE                                  │
│  Path: /api/todos or /api/todos/{id}                           │
│  Headers: Cookie, Content-Type                                  │
│  Body: (for POST/PUT) {description?}                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FastAPI Router                              │
│  - Route matching                                               │
│  - Method validation                                            │
│  - Dependency injection (get_session, get_current_user)         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Validation (Pydantic)                          │
│  - Request body schema validation                               │
│  - Path parameter validation                                    │
│  - Query parameter validation                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Business Logic                              │
│  - Todo CRUD operations                                         │
│  - User ownership enforcement                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Data Access (SQLModel)                        │
│  - Database session                                             │
│  - Query execution                                              │
│  - Result mapping                                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Response Builder                            │
│  - Status code                                                 │
│  - Response body (JSON)                                         │
│  - Error handling                                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Error Handling Architecture

### HTTP Status Codes
| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET, PUT, PATCH, DELETE |
| 201 | Created | Successful POST |
| 400 | Bad Request | Validation errors |
| 401 | Unauthorized | Missing/invalid session |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Pydantic validation errors |
| 500 | Internal Error | Unexpected server errors |

### Error Response Format
```json
{
  "error": "Human-readable error message"
}
```

### Error Handling Flow
```
Request
    │
    ▼
┌──────────────┐
│ Route Match  │── No ──► 404 Not Found
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Auth Check   │── Fail ──► 401 Unauthorized
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Validation   │── Fail ──► 400/422 Bad Request
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Execute      │── Error ──► 500 Internal Error
└──────┬───────┘
       │
       ▼
    Response
```

---

## Security Architecture

### CORS Configuration
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],  # Only Next.js origin
    allow_credentials=True,                  # Allow cookies
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Session Validation
```python
async def get_current_user(
    request: Request,
    session: Session = Depends(get_session)
) -> User:
    # Extract session token from cookie
    token = request.cookies.get("better-auth.session_token")

    # Query session from database
    db_session = session.query(Session).filter(
        Session.token == token,
        Session.expires_at > func.now()
    ).first()

    if not db_session:
        raise HTTPException(status_code=401)

    # Get associated user
    user = session.query(User).get(db_session.user_id)
    return user
```

### User Data Isolation
```python
@router.get("/todos")
def list_todos(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TodoListResponse:
    # Always filter by current user
    todos = session.query(Todo).filter(
        Todo.user_id == current_user.id
    ).all()

    return TodoListResponse(todos=todos, count=len(todos))
```

---

## Performance Considerations

### Database Connection
- SQLModel with connection pooling
- Session-per-request pattern
- SSL mode for Neon

### Query Optimization
- Indexed foreign keys
- Pagination for large lists (future)
- SELECT only needed columns

### Frontend Optimization
- Optimistic UI updates
- Debounced input
- Code splitting (Next.js automatic)
- Static generation where possible
