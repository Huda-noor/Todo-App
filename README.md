# Evolution of Todo

A multi-phase todo management application demonstrating Spec-Driven Development (SDD) through progressive capability enhancement.

## Project Phases

This project is organized into three clearly separated phases:

### Phase 1: In-Memory CLI
**Location**: `/phase-1`

A simple, single-user console application with no persistence.

| Aspect | Details |
|--------|---------|
| Stack | Python (stdlib only) |
| Interface | Console (CLI) |
| Storage | In-memory |
| Features | Add, View, Update, Delete, Toggle |

**Status**: Complete

---

### Phase 2: Full-Stack Web Application
**Location**: `/phase-2`

Persistent web application with authentication and modern UI.

| Aspect | Details |
|--------|---------|
| Stack | FastAPI + Next.js + PostgreSQL |
| Interface | Web (responsive) |
| Storage | Neon PostgreSQL |
| Features | Auth, CRUD, User scoping |

**Status**: Complete

**UI/UX**: [View Design Guide](./phase-2/ui-ux/design-guide.md)

---

### Phase 3: Conversational AI
**Location**: `/phase-3`

Natural language interface powered by AI agents.

| Aspect | Details |
|--------|---------|
| Stack | OpenAI Agents SDK + MCP |
| Interface | Chat API (backend) |
| Storage | PostgreSQL (conversations) |
| Features | NLP todo management, Multi-turn |

**Status**: Planning

**UI/UX**: [View Design Guide](./phase-3/ui-ux/chat-interface-design.md)

---

## Quick Navigation

- **Project Overview**: [README.md](./README.md)
- **Document Index**: [NAVIGATION.md](./NAVIGATION.md)
- **Phase 1**: [phase-1/](./phase-1/)
- **Phase 2**: [phase-2/](./phase-2/)
- **Phase 3**: [phase-3/](./phase-3/)

---

## Project Structure

```
evolution-of-todo/
├── phase-1/                      # In-memory CLI
│   ├── constitution/             # Phase I governance
│   │   └── phase-i-constitution.md
│   ├── specs/                    # Feature specs
│   │   └── feature-summary.md
│   ├── user-flows/               # Interaction flows
│   │   └── cli-interaction-flows.md
│   ├── architecture/             # Design docs
│   │   └── clean-architecture.md
│   ├── data-models/              # Data structures
│   │   └── task-model.md
│   ├── non-functional/           # NFRs
│   │   └── requirements.md
│   └── source-code/              # Implementation
│       └── todo_phase1.py
│
├── phase-2/                      # Full-stack web
│   ├── constitution/             # Phase II amendments
│   │   └── phase-ii-constitution.md
│   ├── specs/                    # Feature specs
│   │   └── feature-summary.md
│   ├── user-flows/               # Auth & todo flows
│   │   ├── authentication-flows.md
│   │   └── todo-flows.md
│   ├── architecture/             # System design
│   │   └── system-architecture.md
│   ├── data-models/              # Database schema
│   │   └── database-schema.md
│   ├── apis/                     # REST API contract
│   │   └── rest-api-contract.md
│   ├── non-functional/           # NFRs
│   │   └── requirements.md
│   ├── source-code/              # Backend & frontend
│   │   ├── backend/
│   │   └── frontend/
│   └── ui-ux/                    # Design guide
│       └── design-guide.md       # MODERN UI/UX
│
├── phase-3/                      # Conversational AI
│   ├── constitution/             # Phase III amendments
│   │   └── phase-iii-constitution.md
│   ├── specs/                    # Feature specs
│   │   └── feature-summary.md
│   ├── user-flows/               # Chat flows
│   │   └── chat-flows.md
│   ├── architecture/             # Agent design
│   │   └── agent-architecture.md
│   ├── data-models/              # Conversation models
│   │   └── conversation-model.md
│   ├── apis/                     # Chat API
│   │   └── chat-api.md
│   ├── non-functional/           # NFRs
│   │   └── requirements.md
│   ├── source-code/              # Backend implementation
│   └── ui-ux/                    # Chat design
│       └── chat-interface-design.md  # MODERN UI/UX
│
├── history/                      # Prompt History Records
├── specs/                        # Original spec documents
└── README.md                     # This file
```

---

## Documentation by Phase

### Phase 1 Documents
| Document | Path |
|----------|------|
| Constitution | [phase-1/constitution/phase-i-constitution.md](./phase-1/constitution/phase-i-constitution.md) |
| Feature Summary | [phase-1/specs/feature-summary.md](./phase-1/specs/feature-summary.md) |
| User Flows | [phase-1/user-flows/cli-interaction-flows.md](./phase-1/user-flows/cli-interaction-flows.md) |
| Architecture | [phase-1/architecture/clean-architecture.md](./phase-1/architecture/clean-architecture.md) |
| Data Model | [phase-1/data-models/task-model.md](./phase-1/data-models/task-model.md) |
| NFRs | [phase-1/non-functional/requirements.md](./phase-1/non-functional/requirements.md) |

### Phase 2 Documents (with UI/UX)
| Document | Path |
|----------|------|
| Constitution | [phase-2/constitution/phase-ii-constitution.md](./phase-2/constitution/phase-ii-constitution.md) |
| Feature Summary | [phase-2/specs/feature-summary.md](./phase-2/specs/feature-summary.md) |
| Auth Flows | [phase-2/user-flows/authentication-flows.md](./phase-2/user-flows/authentication-flows.md) |
| Todo Flows | [phase-2/user-flows/todo-flows.md](./phase-2/user-flows/todo-flows.md) |
| Architecture | [phase-2/architecture/system-architecture.md](./phase-2/architecture/system-architecture.md) |
| Database Schema | [phase-2/data-models/database-schema.md](./phase-2/data-models/database-schema.md) |
| API Contract | [phase-2/apis/rest-api-contract.md](./phase-2/apis/rest-api-contract.md) |
| NFRs | [phase-2/non-functional/requirements.md](./phase-2/non-functional/requirements.md) |
| **UI/UX Design** | [phase-2/ui-ux/design-guide.md](./phase-2/ui-ux/design-guide.md) |

### Phase 3 Documents (with UI/UX)
| Document | Path |
|----------|------|
| Constitution | [phase-3/constitution/phase-iii-constitution.md](./phase-3/constitution/phase-iii-constitution.md) |
| Feature Summary | [phase-3/specs/feature-summary.md](./phase-3/specs/feature-summary.md) |
| Chat Flows | [phase-3/user-flows/chat-flows.md](./phase-3/user-flows/chat-flows.md) |
| Agent Architecture | [phase-3/architecture/agent-architecture.md](./phase-3/architecture/agent-architecture.md) |
| Conversation Model | [phase-3/data-models/conversation-model.md](./phase-3/data-models/conversation-model.md) |
| Chat API | [phase-3/apis/chat-api.md](./phase-3/apis/chat-api.md) |
| NFRs | [phase-3/non-functional/requirements.md](./phase-3/non-functional/requirements.md) |
| **UI/UX Design** | [phase-3/ui-ux/chat-interface-design.md](./phase-3/ui-ux/chat-interface-design.md) |

---

## Technology Evolution

| Layer | Phase 1 | Phase 2 | Phase 3 |
|-------|---------|---------|---------|
| Backend | Python CLI | FastAPI | FastAPI + OpenAI SDK |
| Frontend | None | Next.js | Next.js (unchanged) |
| Database | None | PostgreSQL | PostgreSQL + Conversations |
| Auth | None | Better Auth | Better Auth (unchanged) |
| AI | None | None | OpenAI Agents + MCP |
| UI | Console | Web + Tailwind | Web + Chat UI |

---

## Phase Isolation

Each phase is strictly isolated:

- **Phase 1** has no knowledge of Phases 2-3
- **Phase 2** builds on Phase 1 concepts but different codebase
- **Phase 3** extends Phase 2 without modifying core APIs

This ensures:
- Clear separation of concerns
- No technology bleeding between phases
- Independent testing and deployment
- Clean evolution path

---

## Spec-Driven Development

This project follows Spec-Driven Development:

```
Constitution → Specifications → Plan → Tasks → Implementation
```

All phases include:
- Constitution documents defining principles
- Feature specifications (WHAT)
- Architecture plans (HOW)
- Task breakdowns (WHAT to build)
- Implementation (the code)

---

## Quick Start

### Phase 1 (CLI)
```bash
python phase-1/source-code/todo_phase1.py
```

### Phase 2 (Web)
```bash
# Backend
cd phase-2/source-code/backend
uvicorn app.main:app --reload

# Frontend (separate terminal)
cd phase-2/source-code/frontend
npm run dev
```

### Phase 3 (AI Chat)
```bash
cd phase-3/source-code/backend
uvicorn app.main:app --reload
# Chat endpoint: POST /api/chat
```

---

## Version History

| Version | Date | Phase | Changes |
|---------|------|-------|---------|
| 1.0.0 | 2025-12-27 | I | Initial constitution |
| 1.1.0 | 2025-12-28 | II | Full-stack amendments |
| 1.2.0 | 2026-01-10 | III | AI/conversational amendments |

---

## Navigation

For quick access to specific documents, see [NAVIGATION.md](./NAVIGATION.md).

---

## License

This is a demonstration project for Spec-Driven Development practices.
