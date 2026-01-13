# Navigation Guide

Quick reference for finding documents across all phases.

## By Document Type

### Constitutions
| Phase | Path |
|-------|------|
| Phase 1 | [phase-1/constitution/phase-i-constitution.md](./phase-1/constitution/phase-i-constitution.md) |
| Phase 2 | [phase-2/constitution/phase-ii-constitution.md](./phase-2/constitution/phase-ii-constitution.md) |
| Phase 3 | [phase-3/constitution/phase-iii-constitution.md](./phase-3/constitution/phase-iii-constitution.md) |

### Feature Specifications
| Phase | Path |
|-------|------|
| Phase 1 | [phase-1/specs/feature-summary.md](./phase-1/specs/feature-summary.md) |
| Phase 2 | [phase-2/specs/feature-summary.md](./phase-2/specs/feature-summary.md) |
| Phase 3 | [phase-3/specs/feature-summary.md](./phase-3/specs/feature-summary.md) |

### User Flows
| Phase | Topic | Path |
|-------|-------|------|
| Phase 1 | CLI Flows | [phase-1/user-flows/cli-interaction-flows.md](./phase-1/user-flows/cli-interaction-flows.md) |
| Phase 2 | Authentication | [phase-2/user-flows/authentication-flows.md](./phase-2/user-flows/authentication-flows.md) |
| Phase 2 | Todo Operations | [phase-2/user-flows/todo-flows.md](./phase-2/user-flows/todo-flows.md) |
| Phase 3 | Chat Flows | [phase-3/user-flows/chat-flows.md](./phase-3/user-flows/chat-flows.md) |

### Architecture
| Phase | Path |
|-------|------|
| Phase 1 | [phase-1/architecture/clean-architecture.md](./phase-1/architecture/clean-architecture.md) |
| Phase 2 | [phase-2/architecture/system-architecture.md](./phase-2/architecture/system-architecture.md) |
| Phase 3 | [phase-3/architecture/agent-architecture.md](./phase-3/architecture/agent-architecture.md) |

### Data Models
| Phase | Path |
|-------|------|
| Phase 1 | [phase-1/data-models/task-model.md](./phase-1/data-models/task-model.md) |
| Phase 2 | [phase-2/data-models/database-schema.md](./phase-2/data-models/database-schema.md) |
| Phase 3 | [phase-3/data-models/conversation-model.md](./phase-3/data-models/conversation-model.md) |

### APIs
| Phase | Path |
|-------|------|
| Phase 2 | [phase-2/apis/rest-api-contract.md](./phase-2/apis/rest-api-contract.md) |
| Phase 3 | [phase-3/apis/chat-api.md](./phase-3/apis/chat-api.md) |

### Non-Functional Requirements
| Phase | Path |
|-------|------|
| Phase 1 | [phase-1/non-functional/requirements.md](./phase-1/non-functional/requirements.md) |
| Phase 2 | [phase-2/non-functional/requirements.md](./phase-2/non-functional/requirements.md) |
| Phase 3 | [phase-3/non-functional/requirements.md](./phase-3/non-functional/requirements.md) |

### UI/UX Design (Phases 2-3 only)
| Phase | Path |
|-------|------|
| Phase 2 | [phase-2/ui-ux/design-guide.md](./phase-2/ui-ux/design-guide.md) |
| Phase 3 | [phase-3/ui-ux/chat-interface-design.md](./phase-3/ui-ux/chat-interface-design.md) |

### Source Code
| Phase | Path |
|-------|------|
| Phase 1 | [phase-1/source-code/todo_phase1.py](./phase-1/source-code/todo_phase1.py) |
| Phase 2 Backend | `phase-2/source-code/backend/` |
| Phase 2 Frontend | `phase-2/source-code/frontend/` |
| Phase 3 | `phase-3/source-code/` |

---

## By Task

### I want to understand the project principles
→ [Phase 1 Constitution](./phase-1/constitution/phase-i-constitution.md)

### I want to build Phase 1
→ [Feature Summary](./phase-1/specs/feature-summary.md) + [Source Code](./phase-1/source-code/todo_phase1.py)

### I want to build Phase 2
→ [Feature Summary](./phase-2/specs/feature-summary.md) + [Architecture](./phase-2/architecture/system-architecture.md)

### I want to design Phase 2 UI
→ [UI/UX Design Guide](./phase-2/ui-ux/design-guide.md)

### I want to build Phase 3
→ [Feature Summary](./phase-3/specs/feature-summary.md) + [Agent Architecture](./phase-3/architecture/agent-architecture.md)

### I want to design Phase 3 chat UI
→ [Chat Interface Design](./phase-3/ui-ux/chat-interface-design.md)

### I want to understand how phases are separated
→ [Project README](../README.md#phase-isolation)

### I want to see API contracts
→ [Phase 2 REST API](./phase-2/apis/rest-api-contract.md) or [Phase 3 Chat API](./phase-3/apis/chat-api.md)

---

## Document Relationships

```
CONSTITUTION (principles)
    │
    ├──► SPECS (what to build)
    │       │
    │       ├──► USER FLOWS (how it works)
    │       │
    │       ├──► ARCHITECTURE (how it's structured)
    │       │
    │       ├──► DATA MODELS (what data)
    │       │
    │       ├──► APIs (interfaces)
    │       │
    │       ├──► NFRs (quality requirements)
    │       │
    │       └──► UI/UX (visual design) [Phases 2-3]
    │
    └──► SOURCE CODE (implementation)
```

---

## Phase Comparison

| Aspect | Phase 1 | Phase 2 | Phase 3 |
|--------|---------|---------|---------|
| Code | `phase-1/source-code/` | `phase-2/source-code/` | `phase-3/source-code/` |
| Specs | `phase-1/specs/` | `phase-2/specs/` | `phase-3/specs/` |
| Docs | `phase-1/*/*.md` | `phase-2/*/*.md` | `phase-3/*/*.md` |
| UI/UX | ❌ | `phase-2/ui-ux/` | `phase-3/ui-ux/` |
