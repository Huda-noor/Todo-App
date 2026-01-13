# Evolution of Todo — Phase III Constitution

**Phase**: III | **Version**: 1.2.0 | **Status**: Active
**Extends**: Phase II Constitution (1.1.0)

---

## Vision

Add a conversational AI layer to the existing full-stack application, enabling authenticated users to manage their todos through natural language chat interactions. Phase III builds on Phase II by adding a stateless chat API endpoint that interprets user intent and executes operations via Model Context Protocol (MCP) tools, all powered by the OpenAI Agents SDK.

---

## Constitutional Foundation

### Extends Phase I & II Principles
All Phase I and Phase II principles apply, with additions for AI/agent operations.

### Phase Isolation (Strengthened for Phase III)

**Phase III Authorization**:
- ✅ **AI Logic**: OpenAI Agents SDK
- ✅ **Tooling**: Model Context Protocol (MCP)
- ✅ **MCP Server**: Stateless endpoint exposing task operations as tools
- ✅ **Conversational Interface**: Stateless chat API endpoint
- ✅ **State Management**: Conversation history in existing Neon PostgreSQL

**Phase III Prohibitions**:
- ❌ No direct database access from AI agents
- ❌ No autonomous/background agent execution
- ❌ No multi-agent systems
- ❌ No RAG or vector search
- ❌ No model fine-tuning
- ❌ No real-time/WebSocket chat
- ❌ No frontend chat UI (backend-only capability)

---

## Technology Stack (Phase III Additions)

### AI & Agent Layer (Authorized)
| Component | Technology | Purpose |
|-----------|------------|---------|
| AI Framework | OpenAI Agents SDK | Agent orchestration |
| Tool Protocol | Model Context Protocol (MCP) | Tool definitions |
| LLM | OpenAI model (GPT-4o-mini recommended) | Natural language understanding |
| State Persistence | Neon PostgreSQL (existing) | Conversation threads & messages |

### Architecture Pattern (Required)
```
┌─────────────────────────────────────────────────────────────┐
│                  CHAT API LAYER (FastAPI)                   │
│  POST /api/chat                                             │
│  - Auth validation                                          │
│  - Conversation loading                                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  AGENT LAYER (OpenAI SDK)                   │
│  - Natural language interpretation                          │
│  - Intent classification                                    │
│  - Tool orchestration                                       │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                 MCP SERVER LAYER                            │
│  Stateless tools for:                                       │
│  - create_todo(user_id, title)                             │
│  - list_todos(user_id, completed?)                         │
│  - update_todo(user_id, todo_id, title)                    │
│  - delete_todo(user_id, todo_id)                           │
│  - toggle_todo_complete(user_id, todo_id)                  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│               DATABASE LAYER (Neon PostgreSQL)              │
│  New tables:                                                │
│  - conversation_threads                                     │
│  - conversation_messages                                    │
│  Existing tables:                                           │
│  - users, sessions, todos                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Core Principles for Phase III

### 1. Stateless Services
- Chat endpoint: Completely stateless
- MCP tools: Completely stateless
- All state persisted in database
- No in-memory conversation state between requests

### 2. Deterministic Agent Behavior
- AI agents act as deterministic tool-callers
- No autonomous decision-making beyond tool selection
- All actions traceable to user intent
- Same user message → same agent behavior

### 3. Tool-Only Interaction
- AI agents **MUST** interact with system only through MCP tools
- No direct database access
- No direct backend API calls
- All data operations via approved tools

### 4. User Data Isolation
- All tool operations respect user authentication
- Conversation threads owned by authenticated users
- Users can only access their own conversations and todos
- 100% data isolation enforced at tool level

---

## AI Agent Constraints

### Agent Behavior Rules
| Rule | Description |
|------|-------------|
| Tool-Only | Agents use only approved MCP tools |
| Stateless | No in-memory state between requests |
| Traceable | All actions traceable to user intent |
| Deterministic | Same inputs produce same outputs |
| Idempotent | Safe to retry operations |

### Clarification Protocol
When user intent is ambiguous:
1. Ask targeted clarification question
2. Provide context from conversation
3. Limit to 2-3 questions per turn
4. Avoid asking for already-provided information

### Confirmation Protocol
For destructive operations (delete):
1. Present action to be performed
2. Request explicit confirmation
3. Execute only after confirmation
4. Confirm completion after execution

---

## MCP Tool Specifications

### Tool 1: create_todo
```typescript
create_todo = {
    parameters: {
        user_id: string,      // Required
        title: string,        // Required
        completed?: boolean   // Optional, default false
    },
    returns: {
        success: boolean,
        todo: Todo | null
    }
}
```

### Tool 2: list_todos
```typescript
list_todos = {
    parameters: {
        user_id: string,      // Required
        completed?: boolean   // Optional filter
    },
    returns: {
        success: boolean,
        todos: Todo[],
        count: number
    }
}
```

### Tool 3: update_todo
```typescript
update_todo = {
    parameters: {
        user_id: string,      // Required
        todo_id: number,      // Required
        title: string         // Required
    },
    returns: {
        success: boolean,
        todo: Todo | null
    }
}
```

### Tool 4: delete_todo
```typescript
delete_todo = {
    parameters: {
        user_id: string,      // Required
        todo_id: number       // Required
    },
    returns: {
        success: boolean,
        deleted_id: number | null
    }
}
```

### Tool 5: toggle_todo_complete
```typescript
toggle_todo_complete = {
    parameters: {
        user_id: string,      // Required
        todo_id: number       // Required
    },
    returns: {
        success: boolean,
        todo: Todo | null
    }
}
```

---

## Conversation Model

### Conversation Thread
| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary key |
| user_id | UUID | FK to user (owner) |
| created_at | timestamp | Thread creation time |
| updated_at | timestamp | Last message time |

### Conversation Message
| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary key |
| thread_id | UUID | FK to conversation_thread |
| role | enum | "user" or "assistant" |
| content | text | Message content |
| created_at | timestamp | Message timestamp |

---

## API Endpoint

### POST /api/chat
Conversational interface for todo management.

**Request**:
```json
{
  "message": "Add a task to buy groceries",
  "thread_id": "optional-existing-thread-uuid"
}
```

**Authentication**: Required (session cookie)

**Success Response** (200 OK):
```json
{
  "message": "I've created a new todo: 'Buy groceries'",
  "thread_id": "uuid-of-conversation-thread",
  "actions_taken": [
    {
      "tool": "create_todo",
      "description": "Created todo with title 'Buy groceries'"
    }
  ],
  "suggestions": [
    "Would you like to add more todos?"
  ]
}
```

---

## Phase III Scope

### Features (In Scope)
| Feature | Description |
|---------|-------------|
| Natural language todo creation | "Add a task to buy milk" |
| Natural language listing | "Show me my todos" |
| Natural language completion | "Mark task as done" |
| Natural language update | "Change task title" |
| Natural language deletion | "Delete old task" |
| Multi-turn conversations | Context-aware follow-ups |
| Conversation history | Persisted in database |

### Features (Explicitly Out of Scope)
| Feature | Reason |
|---------|--------|
| Frontend chat UI | Backend-only in Phase III |
| Autonomous agents | Only tool-calling pattern |
| Multi-agent systems | Single agent only |
| RAG/vector search | Not specified |
| Model fine-tuning | Not specified |
| WebSocket chat | Request/response only |
| Background jobs | Stateless design |

---

## Intent Detection

The AI agent must classify user messages into intents:

| Intent | Example Messages |
|--------|------------------|
| create_todo | "Add a task...", "Create a new todo...", "Remind me to..." |
| list_todos | "Show me my todos", "What tasks do I have?", "List tasks" |
| update_todo | "Change task...", "Update the todo...", "Rename..." |
| delete_todo | "Delete task...", "Remove the todo...", "Get rid of..." |
| toggle_complete | "Mark as done", "Complete the task", "I'm finished with..." |
| clarification | Ambiguous requests (agent asks questions) |
| conversation | Greetings, thanks, general chat |

---

## Execution Contract

For every Phase III request:

1. **Confirm** surface (backend API) and success criteria
2. **List** constraints (stateless, tool-only, authenticated)
3. **Produce** artifact with MCP tool compliance checks
4. **Add** follow-ups and risks
5. **Create** PHR in `history/prompts/phase-three/`

---

## Quality Requirements

### Performance
| Metric | Target |
|--------|--------|
| Chat response | < 5 seconds |
| Tool execution | < 2 seconds |
| Context loading | < 500ms |

### Reliability
| Metric | Target |
|--------|--------|
| Tool success rate | 99%+ |
| Data isolation | 100% |
| Error recovery | Graceful with user messages |

### Security
| Requirement | Implementation |
|-------------|----------------|
| Auth validation | Every request |
| Tool authorization | User ID passed to tools |
| No prompt injection | Input sanitization |
| No internal exposure | User-friendly errors only |

---

## Phase Transition

### From Phase II → Phase III
- Phase II code remains unchanged
- New chat endpoint added at `/api/chat`
- New tables for conversation storage
- MCP tools wrap existing todo operations
- Frontend unchanged (Phase III is backend-only)

### To Phase IV (Future)
- Phase IV adds infrastructure (Docker, etc.)
- Core chat API remains unchanged
- Additional features built on Phase III foundation

---

## Amendment Procedure

Constitutional changes require:
1. Formal proposal with Phase III impact analysis
2. User approval
3. Version increment (1.2.0 → 1.3.0)

**Version**: 1.2.0 | **Ratified**: 2025-12-27 | **Extends**: Phase I 1.0.0, Phase II 1.1.0
