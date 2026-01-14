# Evolution of Todo — Phase II Constitution

**Phase**: II | **Version**: 1.1.0 | **Status**: Active
**Extends**: Phase I Constitution

---

## Vision

Transform the in-memory console application into a full-stack web application with persistent storage, user authentication, and a modern responsive UI. Phase II builds incrementally on Phase I concepts, adding database persistence, RESTful API, web frontend, and user management while maintaining clean architecture and separation of concerns.

---

## Constitutional Foundation

### Extends Phase I Principles
All Phase I principles apply, with these additions and modifications for Phase II scope.

### Phase Isolation (Strengthened)

**Phase II is strictly isolated:**
- ✅ **Authorized**: FastAPI, SQLModel, Neon PostgreSQL, Next.js, Better Auth
- ❌ **Prohibited**: OpenAI Agents SDK, MCP, Docker, Kubernetes, Kafka, Dapr (Phase III+)

**No Back-Porting**:
- Phase I remains pure in-memory Python console application
- Phase II codebases (backend/frontend) cannot be imported into Phase I
- No database connection code in Phase I
- No web/API scaffolding in Phase I

---

## Technology Stack

### Backend (Authorized)
| Component | Technology | Purpose |
|-----------|------------|---------|
| Language | Python 3.11+ | API development |
| Framework | FastAPI | REST API server |
| ORM | SQLModel | Database ORM with Pydantic |
| Database | Neon PostgreSQL | Persistent storage |
| Auth | Better Auth | Session management (managed by frontend) |

### Frontend (Authorized)
| Component | Technology | Purpose |
|-----------|------------|---------|
| Framework | Next.js 14+ | React framework |
| Language | TypeScript 5.x | Type-safe frontend |
| Auth | Better Auth | Client-side authentication |
| Styling | Tailwind CSS | Utility-first styling |

### Explicitly Prohibited in Phase II
- OpenAI Agents SDK
- Model Context Protocol (MCP)
- AI/ML libraries
- Chat endpoints
- Docker/Kubernetes/Kafka/Dapr (Phase IV-V)

---

## Phase II Scope

### Features (In Scope)
| Category | Features |
|----------|----------|
| Authentication | User signup, signin, signout, session management |
| Todo CRUD | Create, Read, Update, Delete, Toggle completion |
| Persistence | PostgreSQL database storage |
| API | RESTful backend endpoints |
| Web UI | Modern responsive frontend |
| User Scoping | Data isolation per authenticated user |

### Features (Explicitly Out of Scope)
| Category | Excluded |
|----------|----------|
| Password Reset | Email verification, password recovery |
| Social Login | OAuth, Google, GitHub, SSO |
| Advanced Auth | Roles, admin functionality, 2FA |
| Real-time | WebSockets, Server-Sent Events |
| Advanced Features | Categories, tags, due dates, reminders |
| Sharing | Shared todos, collaboration |
| AI Features | Chat interface, agent tools (Phase III) |
| Infrastructure | Docker, Kubernetes, containers (Phase IV-V) |

---

## Architecture Principles

### Full-Stack Separation
```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (Next.js)                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ SignIn/Up   │  │ Todo List   │  │ API Client          │ │
│  │ Forms       │  │ Components  │  │ (calls backend)     │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTP REST API
┌────────────────────────────▼────────────────────────────────┐
│                    BACKEND (FastAPI)                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ Auth Router │  │ Todo Router │  │ Database Layer      │ │
│  │ (/api/auth) │  │ (/api/todos)│  │ (SQLModel + SQL)    │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└────────────────────────────┬────────────────────────────────┘
                             │ SQL
┌────────────────────────────▼────────────────────────────────┐
│                  DATABASE (Neon PostgreSQL)                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ Users       │  │ Sessions    │  │ Todos               │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Clean Architecture Layers

| Layer | Responsibility | Phase II Implementation |
|-------|----------------|------------------------|
| Presentation | UI rendering | Next.js React components |
| API | HTTP handling | FastAPI routers |
| Business Logic | Todo operations | FastAPI routers + services |
| Data Access | Persistence | SQLModel models + sessions |

---

## User Scenarios (Phase II)

### Authentication Stories

#### Story 1: User Signup
As a new visitor, I want to create an account with email and password so that I can start managing my personal todos.

**Acceptance:**
- Valid email + 8+ char password → Account created
- Duplicate email → Clear error message
- Invalid email format → Validation error
- Empty fields → Inline validation errors

#### Story 2: User Signin
As a returning user, I want to sign in with my credentials so that I can access my todos.

**Acceptance:**
- Correct credentials → Redirect to todo list
- Wrong credentials → "Invalid email or password"
- Empty fields → Validation errors
- Unauthenticated access → Redirect to signin

#### Story 3: User Signout
As a signed-in user, I want to log out so that I can securely end my session.

**Acceptance:**
- Click logout → Session terminated
- Redirected to signin page
- Cannot access protected pages after logout

### Todo Stories

#### Story 4: Create Todo
As an authenticated user, I want to create a new todo so that I can track tasks.

**Acceptance:**
- Non-empty description → Todo created
- Empty description → Validation error
- Data persists across sessions

#### Story 5: View Todos
As an authenticated user, I want to view all my todos so that I can see my tasks.

**Acceptance:**
- All own todos displayed with status
- Empty list shows encouraging message
- Cannot see other users' todos

#### Story 6: Toggle Completion
As an authenticated user, I want to mark todos complete/incomplete so that I can track progress.

**Acceptance:**
- Single click toggles status
- Visual feedback (strikethrough/color)
- Changes persist

#### Story 7: Update Todo
As an authenticated user, I want to edit a todo description so that I can refine tasks.

**Acceptance:**
- Edit mode with inline editing
- Save/cancel options
- Validation on save

#### Story 8: Delete Todo
As an authenticated user, I want to delete a todo so that I can remove completed tasks.

**Acceptance:**
- Delete button on each todo
- Confirmation before deletion
- Removed from list immediately

---

## Data Models

### User Entity
| Field | Type | Constraints |
|-------|------|-------------|
| id | UUID | Primary key, system-generated |
| email | string | Required, unique, valid email, max 255 |
| password | string | Required, min 8 chars, hashed |
| created_at | timestamp | System-generated |

### Todo Entity
| Field | Type | Constraints |
|-------|------|-------------|
| id | UUID | Primary key, system-generated |
| user_id | UUID | Foreign key to User |
| description | string | Required, 1-500 chars |
| is_complete | boolean | Default: false |
| created_at | timestamp | System-generated |
| updated_at | timestamp | Auto-updated |

### Session Entity (Managed by Better Auth)
| Field | Type | Constraints |
|-------|------|-------------|
| id | UUID | Primary key |
| user_id | UUID | Foreign key to User |
| expires_at | timestamp | Session expiration |
| token | string | Session token |

---

## API Contracts

### Authentication Endpoints
| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| POST | /api/auth/signup | No | Create account |
| POST | /api/auth/signin | No | Authenticate |
| POST | /api/auth/signout | Yes | End session |
| GET | /api/auth/me | Yes | Get current user |

### Todo Endpoints
| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| GET | /api/todos | Yes | List todos |
| POST | /api/todos | Yes | Create todo |
| GET | /api/todos/{id} | Yes | Get single todo |
| PUT | /api/todos/{id} | Yes | Update todo |
| DELETE | /api/todos/{id} | Yes | Delete todo |
| PATCH | /api/todos/{id}/toggle | Yes | Toggle status |

---

## Security Requirements

### Password Security
- **Must** be hashed before storage (bcrypt)
- **Never** stored in plaintext
- Minimum 8 characters

### Session Security
- **Must** have expiration
- **Must** be HTTP-only cookies
- **Must** validate on every API request

### Data Isolation
- Users **can only** access their own todos
- Attempting to access other users' todos returns 404 (not 403)
- No information leakage in error messages

---

## Quality Standards

### Performance
| Metric | Target |
|--------|--------|
| Page load | < 3 seconds |
| API response | < 2 seconds |
| UI feedback | < 200ms |

### Usability
- Responsive design (320px to 1920px)
- Accessible (keyboard navigation, form labels)
- Clear error messages
- Loading states for async operations

### Code Quality
- TypeScript for frontend (no any types)
- Pydantic models for backend validation
- Separation of concerns (routers, schemas, models)
- Environment-based configuration

---

## Execution Contract

For every Phase II request:

1. **Confirm** surface and success criteria
2. **List** constraints (backend/frontend separation)
3. **Produce** artifact with phase-specific checks
4. **Add** follow-ups and risks
5. **Create** PHR in `history/prompts/phase-two/`

---

## Phase Transition

### From Phase I → Phase II
- Phase I remains unchanged at `phase-1/`
- New Phase II code at `phase-2/`
- No migration of Phase I code (different architecture)
- Phase I can still be run independently

### To Phase III (Future)
- Phase III builds on Phase II (adds conversational layer)
- Core REST API and frontend remain unchanged
- Only chat endpoint added (no modifications to existing)

---

## Amendment Procedure

Constitutional changes require:
1. Formal proposal with Phase II impact analysis
2. User approval
3. Version increment (1.1.0 → 1.2.0)

**Version**: 1.1.0 | **Ratified**: 2025-12-28 | **Extends**: Phase I 1.0.0
