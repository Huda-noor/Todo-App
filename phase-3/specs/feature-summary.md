# Phase III - Conversational AI Feature Specification

**Phase**: III | **Status**: Draft
**Constitution**: [phase-iii-constitution.md](../constitution/phase-iii-constitution.md)

---

## Overview

Phase III adds a conversational AI layer to the existing Phase II full-stack application. Authenticated users can manage their todos through natural language chat interactions powered by OpenAI Agents SDK and Model Context Protocol (MCP) tools.

### Key Characteristics
- **Backend-only**: No frontend changes in Phase III
- **Stateless**: All state persisted in database
- **Tool-based**: AI agents use MCP tools only (no direct DB access)
- **Extends Phase II**: Builds on existing REST API and authentication

---

## User Stories

### Story 1: Create Todo via Chat (P1)
As an authenticated user, I want to create a todo by sending a natural language message so that I can add tasks without using forms.

**Examples**:
- "Add a task to buy groceries"
- "Create a todo: Schedule dentist appointment"
- "Remind me to call mom tomorrow"

**Acceptance**:
- Todo created with parsed title
- User sees confirmation message
- Todo appears in their list

---

### Story 2: List Todos via Chat (P1)
As an authenticated user, I want to view my todos by sending a simple message so that I can quickly see my tasks.

**Examples**:
- "Show me my todos"
- "What tasks do I have?"
- "List my pending tasks"

**Acceptance**:
- Returns all user's todos
- Clear formatting
- Empty state handled

---

### Story 3: Toggle Complete via Chat (P1)
As an authenticated user, I want to mark a todo complete by sending a natural language message so that I can track progress conversationally.

**Examples**:
- "I finished buying milk"
- "Mark task 'call client' as done"
- "Complete the first task"

**Acceptance**:
- Correct todo identified and toggled
- Confirmation message
- Idempotent (can toggle again)

---

### Story 4: Update Todo via Chat (P2)
As an authenticated user, I want to modify a todo's title by sending a natural language message so that I can refine task descriptions.

**Examples**:
- "Change 'Buy milk' to 'Buy 2 gallons of milk'"
- "Update the first task to include phone number"
- "Rename todo #3 to 'Email boss'"

**Acceptance**:
- Correct todo identified
- Title updated
- Confirmation message

---

### Story 5: Delete Todo via Chat (P2)
As an authenticated user, I want to remove a todo by sending a natural language message so that I can clean up my task list.

**Examples**:
- "Delete 'Old task'"
- "Remove the task about groceries"
- "Get rid of that task I just added"

**Acceptance**:
- Correct todo identified
- Confirmation before deletion
- Deletion confirmed

---

### Story 6: Multi-Turn Conversation (P2)
As an authenticated user, I want to have a back-and-forth conversation so that I can refine my requests.

**Example**:
```
User: "Add a task"
Agent: "What would you like the task to be?"
User: "Buy groceries"
Agent: "I've created a new todo: 'Buy groceries'. Anything else?"
```

**Acceptance**:
- Context maintained across messages
- Clarification requests work
- Natural conversation flow

---

## Data Models

### Conversation Thread
```typescript
interface ConversationThread {
    id: UUID;           // Primary key
    user_id: UUID;      // FK to user (owner)
    created_at: Date;   // Thread creation
    updated_at: Date;   // Last activity
}
```

### Conversation Message
```typescript
interface ConversationMessage {
    id: UUID;           // Primary key
    thread_id: UUID;    // FK to thread
    role: "user" | "assistant";
    content: string;    // Message text
    created_at: Date;   // Message timestamp
}
```

---

## Intent Detection

The agent classifies messages into these intents:

| Intent | Trigger Examples |
|--------|------------------|
| `create_todo` | "Add", "Create", "Remind me", "New task" |
| `list_todos` | "Show", "List", "What do I have", "View" |
| `update_todo` | "Change", "Update", "Rename", "Modify" |
| `delete_todo` | "Delete", "Remove", "Get rid of", "Cancel" |
| `toggle_complete` | "Complete", "Done", "Finished", "Mark as done" |
| `clarification` | Ambiguous requests requiring more info |
| `conversation` | Greetings, thanks, general chat |

---

## MCP Tools

### Tool Signatures

```typescript
// Tool 1: Create todo
create_todo(user_id: string, title: string, completed?: boolean): {
    success: boolean;
    todo: Todo | null;
}

// Tool 2: List todos
list_todos(user_id: string, completed?: boolean): {
    success: boolean;
    todos: Todo[];
    count: number;
}

// Tool 3: Update todo
update_todo(user_id: string, todo_id: number, title: string): {
    success: boolean;
    todo: Todo | null;
}

// Tool 4: Delete todo
delete_todo(user_id: string, todo_id: number): {
    success: boolean;
    deleted_id: number | null;
}

// Tool 5: Toggle complete
toggle_todo_complete(user_id: string, todo_id: number): {
    success: boolean;
    todo: Todo | null;
}
```

---

## API Endpoint

### POST /api/chat

**Request**:
```json
{
  "message": "Add a task to buy milk",
  "thread_id": "optional-uuid"  // Omit for new conversation
}
```

**Response**:
```json
{
  "message": "I've created a new todo: 'Buy milk'",
  "thread_id": "new-or-existing-uuid",
  "actions_taken": [
    {
      "tool": "create_todo",
      "description": "Created todo with title 'Buy milk'"
    }
  ],
  "suggestions": [
    "Would you like to add more todos?"
  ]
}
```

---

## Architecture

```
User Message
    │
    ▼
┌─────────────────────────────────────┐
│  Chat API Endpoint (/api/chat)      │
│  - Validate authentication          │
│  - Load conversation context        │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│  OpenAI Agents SDK                  │
│  - Interpret intent                 │
│  - Extract parameters               │
│  - Decide which tools to call       │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│  MCP Server (5 Tools)               │
│  - create_todo                      │
│  - list_todos                       │
│  - update_todo                      │
│  - delete_todo                      │
│  - toggle_todo_complete             │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│  Database (Neon PostgreSQL)         │
│  - CRUD todos (existing tables)     │
│  - Store conversation threads       │
│  - Store conversation messages      │
└─────────────────────────────────────┘
```

---

## Success Criteria

| Criterion | Target |
|-----------|--------|
| Intent accuracy | 90%+ for common phrasings |
| Response time | < 5 seconds |
| Multi-turn context | 10+ messages |
| Clarification success | 85%+ resolution |
| Data isolation | 100% (no cross-user access) |
| Tool success rate | 99%+ |

---

## Files Reference

| Path | Purpose |
|------|---------|
| `constitution/phase-iii-constitution.md` | Phase III constitution |
| `specs/feature-summary.md` | This file |
| `architecture/agent-architecture.md` | Detailed agent design |
| `user-flows/chat-flows.md` | Conversation flows |
| `data-models/conversation-model.md` | Conversation data models |
| `apis/chat-api.md` | API specification |
| `non-functional/requirements.md` | NFRs |
| `ui-ux/chat-interface-design.md` | Future frontend design |

---

**Phase III Ready for Planning**
