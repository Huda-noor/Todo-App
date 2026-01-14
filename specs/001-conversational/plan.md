# Implementation Plan: Phase III - Conversational AI Interface

**Branch**: `001-conversational` | **Date**: 2026-01-10 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-conversational/spec.md`

**Note**: This plan defines the stateless conversational architecture that layers natural language task management on top of the existing Phase II full-stack application.

---

## Summary

Phase III adds a conversational AI interface to the existing Todo application, enabling authenticated users to manage todos through natural language chat. The architecture consists of four stateless layers:

1. **Chat API Layer (FastAPI)**: HTTP endpoint receiving authenticated messages
2. **Agent Layer (OpenAI Agents SDK)**: Interprets intent and orchestrates tool calls
3. **MCP Server Layer**: Exposes five stateless tools for Todo operations
4. **Data Persistence Layer**: Neon PostgreSQL database for conversations and todos

All layers are completely stateless, with conversation history and task state persisted in the database and retrieved per request. The system strictly maintains phase isolation, reuses Phase II authentication, and enforces user data isolation.

---

## Introduction

This plan outlines the technical architecture and implementation approach for Phase III of the "Evolution of Todo" project. The purpose is to define HOW the conversational AI interface, stateless chat endpoint, OpenAI Agents SDK agent, and MCP tools will be implemented.

**Core Architectural Principles**:
- Complete statelessness of all layers (chat endpoint, agent, MCP tools)
- Database-only persistence for conversations and task state
- Strict layer separation: Chat API → Agent → MCP Tools → Database
- Reuse of Phase II authentication without modification
- No changes to existing Phase II frontend or REST API
- AI agents interact exclusively through MCP tools

---

## Overall Architecture Overview

### High-Level Flow

```
User Request (HTTP POST /api/chat)
        ↓
┌─────────────────────────────────────────────┐
│  Layer 1: Chat API (FastAPI)                │
│  - Validate authentication (Phase II)        │
│  - Extract user_id from session/token        │
│  - Load conversation thread from DB          │
│  - Prepare context for agent                 │
└─────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────┐
│  Layer 2: Agent (OpenAI Agents SDK)          │
│  - Receive message + conversation history   │
│  - Interpret natural language intent         │
│  - Call MCP tools for actions                │
│  - Generate natural language response       │
└─────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────┐
│  Layer 3: MCP Server & Tools                │
│  - Expose 5 stateless tools:                │
│    create_todo, list_todos, update_todo,    │
│    delete_todo, toggle_todo_complete         │
│  - Enforce user authorization                │
│  - Execute Todo operations via database      │
└─────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────┐
│  Layer 4: Database (Neon PostgreSQL)        │
│  - conversation_threads table               │
│  - conversation_messages table              │
│  - todos table (existing from Phase II)     │
│  - users table (existing from Phase II)     │
└─────────────────────────────────────────────┘
        ↓
Response (HTTP 200 with agent message)
```

### Layer Boundaries and Responsibilities

| Layer | Responsibility | State | Technology |
|-------|---------------|-------|------------|
| Chat API | HTTP handling, auth validation, context loading | Stateless | FastAPI |
| Agent | Intent interpretation, tool selection, response generation | Stateless | OpenAI Agents SDK |
| MCP Tools | Todo operations, user authorization, database interaction | Stateless | MCP SDK |
| Database | Persistence (conversations, todos, users) | Persistent | Neon PostgreSQL |

### Statelessness Guarantee

- **Chat API**: No in-memory state between requests. Each request loads conversation context from database.
- **Agent**: Created per request, no persistent memory, all context provided via conversation history.
- **MCP Tools**: Stateless operations, each tool call receives all necessary parameters, no side effects between calls.
- **Horizontal Scalability**: Multiple instances of any layer can run concurrently without data inconsistency.

---

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**:
- FastAPI (existing from Phase II)
- OpenAI Agents SDK (new for Phase III)
- Model Context Protocol (MCP) SDK (new for Phase III)
- SQLModel (existing from Phase II)

**Storage**: Neon PostgreSQL (existing from Phase II, extends with new tables)
**Testing**: pytest (existing from Phase II)
**Target Platform**: Linux server (Hugging Face Spaces deployment)
**Project Type**: Web application - backend extension
**Performance Goals**: <3 seconds for simple requests, <5 seconds for complex requests
**Constraints**: Complete statelessness, no in-memory agent state, deterministic tool execution
**Scale/Scope**: Single-user focused (can scale horizontally with stateless architecture)

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase III Authorization Verification

| Requirement | Status | Evidence |
|-------------|--------|----------|
| OpenAI Agents SDK authorized | ✅ PASS | Constitution v1.2.0 Section IV, Phase III |
| MCP SDK authorized | ✅ PASS | Constitution v1.2.0 Section IV, Phase III |
| Stateless chat endpoint | ✅ PASS | Constitution v1.2.0 Section V, Phase III AI & Tool Architecture |
| Conversation persistence in Neon DB | ✅ PASS | Constitution v1.2.0 Section IV, Phase III |
| No autonomous/background agents | ✅ PASS | Constitution v1.2.0 Section VII |

### Phase Isolation Verification

| Requirement | Status | Evidence |
|-------------|--------|----------|
| No Phase III tech in Phase I/II | ✅ PASS | Plan specifies new backend layer only |
| Phase III extends Phase II (not modifies) | ✅ PASS | No changes to existing REST API or frontend |
| AI agents interact via MCP only | ✅ PASS | Architecture shows exclusive MCP tool access |
| No direct database access from AI | ✅ PASS | All data operations through MCP tools |

### Agent Behavior Verification

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Deterministic executors only | ✅ PASS | Single-agent tool-calling pattern |
| No tool invention | ✅ PASS | Exactly 5 approved tools defined |
| Traceable to user intent | ✅ PASS | Conversation history preserved |
| No direct DB access | ✅ PASS | MCP tools as exclusive data access layer |

### Non-Functional Verification

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Stateless services | ✅ PASS | All layers designed stateless |
| Persistence in database | ✅ PASS | Conversation tables in Neon PostgreSQL |
| Separation of concerns | ✅ PASS | Clear layer boundaries defined |
| No multi-agent systems | ✅ PASS | Single-agent pattern only |

### Explicit Exclusions Verification

| Exclusion | Status | Evidence |
|-----------|--------|----------|
| No frontend chat UI | ✅ PASS | Backend-only capability in plan |
| No autonomous agents | ✅ PASS | Request-driven only |
| No multi-agent swarms | ✅ PASS | Single-agent pattern |
| No RAG/vector search | ✅ PASS | Not included in architecture |
| No model fine-tuning | ✅ PASS | Uses pre-trained OpenAI model |
| No real-time/WebSocket chat | ✅ PASS | HTTP POST only |
| No Phase IV-V tech | ✅ PASS | No Docker/Kubernetes/Kafka/Dapr |

**CONCLUSION**: All constitutional gates PASS. No violations detected.

---

## Chat API Layer (FastAPI)

### Endpoint Definition

| Attribute | Value |
|-----------|-------|
| Method | POST |
| Path | `/api/chat` |
| Authentication | Required (reuse Phase II Better Auth) |
| Content-Type | application/json |

### Request Parsing

**Request Body Schema**:
```json
{
  "message": "string (required, 1-1000 characters)",
  "thread_id": "string (optional, UUID format)"
}
```

**Validation Rules**:
- `message`: Required, non-empty, max 1000 characters
- `thread_id`: Optional, if provided must be valid UUID, must belong to authenticated user
- Return HTTP 400 for invalid requests

### Conversation Thread Retrieval

**When thread_id provided**:
1. Query `conversation_threads` table by `thread_id`
2. Verify `user_id` matches authenticated user
3. If thread not found or user mismatch, return HTTP 400
4. Load all messages from `conversation_messages` ordered by `created_at`

**When thread_id omitted**:
1. Create new thread in `conversation_threads` table:
   - Generate new UUID for `thread_id`
   - Set `user_id` from authentication context
   - Set `created_at` and `updated_at` to current timestamp
2. Return empty message list for context

### Agent Invocation Strategy

1. **Prepare Context**: Assemble conversation history as array of messages with role and content
2. **Create Agent Instance**: Instantiate OpenAI Agent with system prompt and available tools
3. **Invoke Agent**: Pass current user message + conversation history to agent
4. **Capture Response**: Receive agent's natural language response and any tool calls
5. **Handle Tool Calls**: If agent requests tool execution, invoke MCP tools synchronously

### Response Generation

**Response Format**:
```json
{
  "message": "string (natural language response from agent)",
  "thread_id": "string (UUID of conversation thread)",
  "actions_taken": [
    {
      "tool": "string (tool name)",
      "description": "string (human-readable description)"
    }
  ],
  "suggestions": [
    "string (optional follow-up suggestions)"
  ]
}
```

**HTTP Status Codes**:
- 200: Success
- 400: Invalid request (missing message, invalid thread_id)
- 401: Authentication required or failed
- 429: Rate limit exceeded
- 500: Internal server error

### Conversation Persistence

**Save User Message** (before agent invocation):
1. Insert into `conversation_messages`:
   - Generate new UUID for `id`
   - Set `thread_id` from request
   - Set `role = "user"`
   - Set `content` from request body
   - Set `created_at` to current timestamp

**Save Agent Response** (after agent invocation):
1. Insert into `conversation_messages`:
   - Generate new UUID for `id`
   - Set `thread_id` from request
   - Set `role = "assistant"`
   - Set `content` from agent response
   - Set `created_at` to current timestamp

2. Update `conversation_threads`:
   - Set `updated_at` to current timestamp

### Error Handling

| Error Type | HTTP Status | Response Body |
|------------|-------------|---------------|
| Authentication failed | 401 | `{"error": "Authentication required"}` |
| Invalid request (missing message) | 400 | `{"error": "Invalid request: 'message' is required"}` |
| Thread not found | 400 | `{"error": "Conversation thread not found"}` |
| Thread ownership violation | 403 | `{"error": "Access denied to conversation thread"}` |
| Rate limit exceeded | 429 | `{"error": "Rate limit exceeded, please try again later"}` |
| Internal error | 500 | `{"error": "Internal error processing request"}` |

---

## Agent Layer (OpenAI Agents SDK)

### Agent Configuration

**Model Choice**: Use OpenAI GPT-4o or equivalent for natural language understanding and generation.

**Configuration Parameters**:
- Model: `gpt-4o` or `gpt-4o-mini` (configurable)
- Temperature: `0.3` (lower for more deterministic behavior)
- Max Tokens: `500` (for response generation)
- Timeout: `30` seconds

### System Prompt

The agent's system prompt defines its behavior and boundaries:

```
You are a helpful AI assistant for managing todos through conversation.
Your role is to interpret natural language messages and manage todo tasks using the available tools.

Core Behaviors:
1. Interpret user intent from natural language messages
2. Use available tools to create, list, update, delete, or toggle todos
3. Ask for clarification when intent is ambiguous or parameters are missing
4. Request confirmation before destructive operations (delete)
5. Provide clear, helpful responses to the user
6. Maintain context across the conversation by referencing previous messages

Available Tools:
- create_todo: Create a new todo
- list_todos: List todos (optionally filtered by completion status)
- update_todo: Update an existing todo's title
- delete_todo: Delete an existing todo
- toggle_todo_complete: Toggle a todo's completion status

Important Constraints:
- Only use the provided tools for todo operations
- Do not make assumptions about unclear requests
- Do not invent tools or access data directly
- Be concise and helpful in responses
- Maintain professional, conversational tone

If a user asks for something outside your capabilities (e.g., weather, news, etc.), politely explain that you can only help with todo management.
```

### Single-Turn vs Multi-Turn Handling

**Single-Turn** (when no conversation history):
- Agent operates on current message only
- Cannot reference previous messages
- Requests clarification for ambiguous references

**Multi-Turn** (when conversation history exists):
- Agent receives array of previous messages (role + content)
- Can reference previous messages to understand context
- Can handle follow-up questions and refinements
- Maintains continuity across conversation

**Per-Request Processing**:
1. Receive: current_message + conversation_history (array)
2. Process: analyze context and current message together
3. Respond: generate response considering full conversation context
4. Terminate: agent instance destroyed after response, no persistent memory

### Tool-Calling Strategy

**Available Tools** (exactly five):

| Tool | Purpose | When Called |
|------|---------|-------------|
| create_todo | Create new todo | User expresses intent to add task |
| list_todos | List todos | User requests to see tasks |
| update_todo | Modify todo title | User requests to change task description |
| delete_todo | Remove todo | User requests to delete task |
| toggle_todo_complete | Mark done/undone | User reports task completion or wants to unmark |

**Tool Selection Process**:
1. Agent analyzes user message and conversation history
2. Determines required action(s)
3. Selects appropriate tool(s) based on intent
4. Constructs tool parameters from extracted information
5. Calls tool(s) synchronously
6. Incorporates tool results into response

**Clarification Pattern**:
- When intent ambiguous: ask specific question (e.g., "Which todo would you like to delete?")
- When parameters missing: request missing information (e.g., "What would you like the todo title to be?")
- Limit clarification questions to 2-3 maximum

### Confirmation for Destructive Actions

**Delete Operation Flow**:

1. **First User Message**: "Delete 'My important task'"
2. **Agent Response**: "Are you sure you want to delete 'My important task'? (yes/no)"
3. **Tool Calls**: None (waiting for confirmation)
4. **Second User Message**: "yes"
5. **Agent Response**: Calls `delete_todo` tool → "Deleted 'My important task'"

**Confirmation State Tracking**:
- Agent tracks pending confirmations via conversation context
- Confirmation stored implicitly in conversation history
- Next message evaluated against pending confirmation

**Cancel Flow**:
- User responds with "no" or similar
- Agent responds: "Cancelled. 'My important task' remains in your list."
- No tool execution

### Agent Lifecycle

**Creation**:
- New agent instance created for each incoming request
- Initialized with system prompt and available tools
- No persistent state between requests

**Execution**:
- Receives message + conversation history
- Processes and generates response
- Calls tools as needed (synchronous)
- Returns response to chat API layer

**Termination**:
- Agent instance destroyed after response
- All state persisted in database (conversation history)
- No in-memory state retention

**No Autonomous Execution**:
- Agent never initiates actions without user request
- No background processes or scheduled tasks
- Agent only responds to incoming HTTP requests

---

## MCP Server & Tools Layer

### MCP Server Responsibilities

1. **Expose Tools**: Register and expose exactly five stateless tools
2. **Tool Invocation**: Receive tool call requests from agent
3. **Parameter Validation**: Validate tool input parameters
4. **Authorization**: Enforce user authorization on all operations
5. **Database Interaction**: Execute Todo operations via database
6. **Error Handling**: Return structured error responses
7. **Result Formatting**: Format tool results for agent consumption

### Hosting Approach

The MCP server runs as a separate process/service within the same backend application:

- **Integration**: MCP server embedded in FastAPI application
- **Communication**: In-process method calls (agent invokes tools directly)
- **Statelessness**: Each tool call is independent, no server state
- **Synchronous**: Tool calls block until completion

### Tool Definitions

#### Tool 1: create_todo

**Purpose**: Creates a new todo for an authenticated user.

**Input Schema**:
```json
{
  "user_id": "string (UUID, required)",
  "title": "string (required, 1-500 characters)",
  "completed": "boolean (optional, default: false)"
}
```

**Output Schema**:
```json
{
  "success": true,
  "todo": {
    "id": 123,
    "user_id": "user-uuid",
    "title": "Buy milk",
    "completed": false,
    "created_at": "2026-01-10T10:30:00Z",
    "updated_at": "2026-01-10T10:30:00Z"
  }
}
```

**Error Schema**:
```json
{
  "success": false,
  "error": "Invalid title: cannot be empty"
}
```

**Validation Rules**:
- `user_id`: Required, valid UUID, must exist in users table
- `title`: Required, non-empty, max 500 characters
- `completed`: Optional, boolean type

**Database Interaction**:
1. Verify user exists in users table
2. Insert new row into todos table
3. Return created todo object

---

#### Tool 2: list_todos

**Purpose**: Retrieves todos for an authenticated user, optionally filtered by completion status.

**Input Schema**:
```json
{
  "user_id": "string (UUID, required)",
  "completed": "boolean (optional)"
}
```

**Output Schema**:
```json
{
  "success": true,
  "todos": [
    {
      "id": 123,
      "user_id": "user-uuid",
      "title": "Buy milk",
      "completed": false,
      "created_at": "2026-01-10T10:30:00Z",
      "updated_at": "2026-01-10T10:30:00Z"
    }
  ],
  "count": 1
}
```

**Error Schema**:
```json
{
  "success": false,
  "error": "User not found"
}
```

**Validation Rules**:
- `user_id`: Required, valid UUID, must exist in users table
- `completed`: Optional, boolean type (if provided)

**Database Interaction**:
1. Verify user exists in users table
2. Query todos table with filters:
   - `WHERE user_id = {user_id}`
   - `AND completed = {completed}` (if provided)
3. Return ordered by `created_at` DESC

---

#### Tool 3: update_todo

**Purpose**: Updates an existing todo's title.

**Input Schema**:
```json
{
  "user_id": "string (UUID, required)",
  "todo_id": "integer (required)",
  "title": "string (required, 1-500 characters)"
}
```

**Output Schema**:
```json
{
  "success": true,
  "todo": {
    "id": 123,
    "user_id": "user-uuid",
    "title": "Buy 2 gallons of milk",
    "completed": false,
    "created_at": "2026-01-10T10:30:00Z",
    "updated_at": "2026-01-10T11:00:00Z"
  }
}
```

**Error Schema**:
```json
{
  "success": false,
  "error": "Todo not found"
}
```

**Validation Rules**:
- `user_id`: Required, valid UUID
- `todo_id`: Required, positive integer
- `title`: Required, non-empty, max 500 characters

**Authorization Check**:
- Verify todo exists with matching `todo_id` AND `user_id`
- Return error if todo not found or owned by different user

**Database Interaction**:
1. Query todos table: `WHERE id = {todo_id} AND user_id = {user_id}`
2. If not found, return error
3. Update todo: `SET title = {title}, updated_at = NOW()`
4. Return updated todo object

---

#### Tool 4: delete_todo

**Purpose**: Deletes an existing todo for an authenticated user.

**Input Schema**:
```json
{
  "user_id": "string (UUID, required)",
  "todo_id": "integer (required)"
}
```

**Output Schema**:
```json
{
  "success": true,
  "deleted_id": 123
}
```

**Error Schema**:
```json
{
  "success": false,
  "error": "Todo not found"
}
```

**Validation Rules**:
- `user_id`: Required, valid UUID
- `todo_id`: Required, positive integer

**Authorization Check**:
- Verify todo exists with matching `todo_id` AND `user_id`
- Return error if todo not found or owned by different user (to prevent information leakage)

**Database Interaction**:
1. Query todos table: `WHERE id = {todo_id} AND user_id = {user_id}`
2. If not found, return error
3. Delete todo: `DELETE FROM todos WHERE id = {todo_id}`
4. Return deleted ID

---

#### Tool 5: toggle_todo_complete

**Purpose**: Toggles the completion status of an existing todo.

**Input Schema**:
```json
{
  "user_id": "string (UUID, required)",
  "todo_id": "integer (required)"
}
```

**Output Schema**:
```json
{
  "success": true,
  "todo": {
    "id": 123,
    "user_id": "user-uuid",
    "title": "Buy milk",
    "completed": true,
    "created_at": "2026-01-10T10:30:00Z",
    "updated_at": "2026-01-10T11:30:00Z"
  }
}
```

**Error Schema**:
```json
{
  "success": false,
  "error": "Todo not found"
}
```

**Validation Rules**:
- `user_id`: Required, valid UUID
- `todo_id`: Required, positive integer

**Authorization Check**:
- Verify todo exists with matching `todo_id` AND `user_id`
- Return error if todo not found or owned by different user

**Database Interaction**:
1. Query todos table: `WHERE id = {todo_id} AND user_id = {user_id}`
2. If not found, return error
3. Toggle: `UPDATE todos SET completed = NOT completed, updated_at = NOW() WHERE id = {todo_id}`
4. Return updated todo object

### Database Interaction Pattern

**Load Current State**:
- Query database for relevant entities
- Verify authorization (user ownership)
- Return error if not authorized

**Execute Operation**:
- Perform INSERT, UPDATE, DELETE, or SELECT
- Use database transactions for atomicity

**Save New State**:
- Changes persist immediately via database transaction
- No additional save step required (database handles persistence)

### User Context Enforcement

All tools enforce user authorization:

1. **Input Validation**: Validate `user_id` parameter
2. **Authorization Check**: Verify user owns the target data
3. **Data Isolation**: Never return data from other users
4. **Error Obfuscation**: Return generic "not found" errors for authorization failures

### Error Propagation

**Error Flow**:
1. Tool detects error (validation, authorization, database)
2. Returns structured error response: `{"success": false, "error": "message"}`
3. Chat API passes error to agent
4. Agent interprets error and formulates user-friendly response
5. User receives clear, actionable error message

**Error Categories**:
- **Validation Error**: Invalid input parameters
- **Authorization Error**: User not authorized
- **Not Found Error**: Target entity doesn't exist
- **Database Error**: Query/update failed

---

## Data Persistence Layer

### Conversation Thread Model

**Table**: `conversation_threads`

| Column | Type | Required | Description | Index |
|--------|------|----------|-------------|-------|
| id | UUID | Yes | Unique thread identifier (primary key) | PK |
| user_id | UUID | Yes | Reference to owning user | FK, IDX |
| created_at | timestamp | Yes | When thread was created | IDX |
| updated_at | timestamp | Yes | When thread was last updated | - |

**Relationships**:
- Foreign Key to `users` table on `user_id`
- One-to-many: `users` → `conversation_threads`
- One-to-many: `conversation_threads` → `conversation_messages`

**Indexes**:
- Primary key on `id`
- Index on `user_id` (for efficient user thread lookup)

### Conversation Message Model

**Table**: `conversation_messages`

| Column | Type | Required | Description | Index |
|--------|------|----------|-------------|-------|
| id | UUID | Yes | Unique message identifier (primary key) | PK |
| thread_id | UUID | Yes | Reference to thread | FK, IDX |
| role | enum | Yes | "user" or "assistant" | - |
| content | text | Yes | Message content (natural language) | - |
| created_at | timestamp | Yes | When message was created | IDX |

**Relationships**:
- Foreign Key to `conversation_threads` table on `thread_id`
- Many-to-one: `conversation_messages` → `conversation_threads`

**Indexes**:
- Primary key on `id`
- Index on `thread_id` (for efficient message retrieval)
- Index on `created_at` (for chronological ordering)

### Relationship with Existing Tables

```
users (existing Phase II)
  |
  | (1:many)
  |
  +--- conversation_threads (new Phase III)
        |
        | (1:many)
        |
        +--- conversation_messages (new Phase III)

users (existing Phase II)
  |
  | (1:many)
  |
  +--- todos (existing Phase II)
```

### Storage Strategy

**Append-Only Message History**:
- Messages are never modified after creation
- New messages appended to conversation
- Chronological ordering via `created_at` timestamp

**Conversation Thread Updates**:
- `updated_at` timestamp updated on each new message
- Thread persists indefinitely (no expiration in Phase III)

### Schema Additions and Migration Approach

**New Tables** (Phase III):
- `conversation_threads`
- `conversation_messages`

**Migration Approach**:
1. Create migration script using existing Phase II migration framework
2. Add both new tables with proper constraints and indexes
3. Add foreign key relationships to existing `users` table
4. Run migration as part of Phase III deployment
5. No modifications to existing `users` or `todos` tables

**Migration SQL** (pseudo):
```sql
-- Create conversation_threads table
CREATE TABLE conversation_threads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Create index on user_id
CREATE INDEX idx_conversation_threads_user_id ON conversation_threads(user_id);
CREATE INDEX idx_conversation_threads_created_at ON conversation_threads(created_at);

-- Create conversation_messages table
CREATE TABLE conversation_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  thread_id UUID NOT NULL REFERENCES conversation_threads(id) ON DELETE CASCADE,
  role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
  content TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_conversation_messages_thread_id ON conversation_messages(thread_id);
CREATE INDEX idx_conversation_messages_created_at ON conversation_messages(created_at);
```

---

## Integration & Flow Details

### End-to-End Request Lifecycle

**Step 1: HTTP Request Received**
- Client sends POST `/api/chat` with authentication header
- FastAPI validates authentication using Phase II middleware
- Extracts `user_id` from authentication context

**Step 2: Request Parsing**
- Parse JSON request body
- Validate required fields (`message`)
- Extract `thread_id` if provided

**Step 3: Context Loading**
- Query `conversation_threads` by `thread_id` (or create new)
- Verify user owns thread (`user_id` matches)
- Query `conversation_messages` ordered by `created_at`
- Assemble conversation history as array of messages

**Step 4: Agent Invocation**
- Create new OpenAI Agent instance with system prompt
- Pass current message + conversation history to agent
- Agent analyzes intent and determines action(s)

**Step 5: Tool Execution (if needed)**
- Agent calls MCP tool(s) with parameters
- MCP tool validates input and authorization
- Tool executes database operation
- Tool returns result to agent

**Step 6: Response Generation**
- Agent generates natural language response
- Agent may call additional tools based on results
- Final response formatted with action descriptions

**Step 7: Conversation Persistence**
- Insert user message into `conversation_messages`
- Insert agent response into `conversation_messages`
- Update `conversation_threads.updated_at`

**Step 8: HTTP Response**
- Format response JSON with message, thread_id, actions, suggestions
- Return HTTP 200 to client

### Authentication Propagation

**Phase II Authentication**:
- Better Auth middleware validates session/token
- Extracts `user_id` from authentication context
- Makes `user_id` available to request handler

**Propagation to Agent**:
- `user_id` included in tool parameters
- Agent doesn't handle authentication directly
- All tools receive `user_id` for authorization

**Propagation to MCP Tools**:
- Each tool call includes `user_id` parameter
- Tools verify user ownership before operations
- No access to other users' data

### Tool Failure Handling

**Tool Execution Failure**:
1. Tool detects error (validation, database, authorization)
2. Returns structured error: `{"success": false, "error": "..."}`
3. Agent receives error result
4. Agent formulates user-friendly response explaining the issue
5. Chat API returns HTTP 200 (tool failure is operational, not API error)

**User-Facing Error Messages**:
- "I couldn't find that todo. Would you like me to list your tasks?"
- "There was an error saving your task. Please try again."
- "I need more information to help you with that."

### Thread Management

**New Thread Creation**:
- Triggered when `thread_id` omitted from request
- Generates new UUID for `thread_id`
- Associates with authenticated `user_id`
- Returns empty message history to agent

**Existing Thread Continuation**:
- Triggered when valid `thread_id` provided
- Loads existing conversation history
- Verifies user ownership
- Appends new messages to thread

**Thread Ownership Enforcement**:
- User cannot access threads belonging to other users
- HTTP 403 returned for ownership violations
- Generic error message to prevent information leakage

---

## Error Handling & Resilience Strategy

### Handling Ambiguous Intent

**Detection**:
- Agent detects ambiguous intent from user message
- Example: "I'm done with that" (unclear which todo)

**Handling Flow**:
1. Agent identifies ambiguity
2. Agent requests clarification (no tool call)
3. Response: "Which todo would you like to mark as done?"
4. User provides clarification in next message
5. Agent processes with new context

**Clarification Best Practices**:
- Limit to 2-3 questions maximum
- Provide context from conversation history
- Avoid asking about already-provided information
- Present multiple-choice options when helpful

### Tool Execution Failures

**Failure Types**:
- **Validation Error**: Invalid input parameters
- **Authorization Error**: User not authorized
- **Database Error**: Query/update failed
- **Not Found Error**: Target entity doesn't exist

**Handling Flow**:
1. Tool returns error response to agent
2. Agent interprets error message
3. Agent formulates user-friendly explanation
4. Agent suggests retry or alternative action
5. Chat API returns HTTP 200 with explanation

**Example**:
- Tool: `{"success": false, "error": "Todo not found"}`
- Agent: "I couldn't find that todo. Would you like me to list your tasks?"
- User can retry with correct information

### Authentication/Authorization Failures

**Authentication Failure** (401):
- No valid session/token
- Expired session
- Invalid credentials

**Response**:
```json
{"error": "Authentication required"}
```

**Authorization Failure** (403):
- User tries to access another user's thread
- User tries to modify another user's todo

**Response**:
```json
{"error": "Access denied"}
```

### Rate Limiting & Quota Considerations

**Rate Limiting**:
- Limit requests per user per minute (e.g., 30 requests/minute)
- Track using sliding window algorithm
- Use `user_id` as rate limit key

**Quota Considerations**:
- OpenAI API quota per model
- Track token usage per request
- Log quota exhaustion for monitoring

**Rate Limit Response** (429):
```json
{
  "error": "Rate limit exceeded, please try again later"
}
```

**Headers**:
- `Retry-After`: Seconds before next allowed request

### User-Friendly Error Messages

| Error | Technical | User-Friendly |
|-------|-----------|---------------|
| Invalid title | "Title cannot be empty" | "Please provide a task title" |
| Todo not found | "Todo with id 999 not found" | "I couldn't find that todo" |
| User not found | "User uuid not found in database" | "Authentication error" |
| Database error | "Connection timeout" | "There was an error processing your request" |
| Rate limit | "Rate limit exceeded" | "You're sending messages too quickly, please wait" |

---

## Non-Functional Considerations

### Complete Statelessness

**Chat Endpoint**:
- No in-memory state between requests
- Each request loads conversation context from database
- Multiple instances can run concurrently

**Agent**:
- Created per request, destroyed after response
- No persistent memory
- All context provided via conversation history

**MCP Tools**:
- Stateless operations
- Each call receives all necessary parameters
- No side effects between calls

**Horizontal Scalability**:
- Multiple FastAPI instances can run behind load balancer
- Multiple MCP server instances (if deployed separately)
- No shared state required between instances

### Deterministic Behavior

**Agent Behavior**:
- Low temperature setting (0.3) for consistent responses
- Same input produces similar output
- System prompt provides clear guidelines

**Tool Execution**:
- Idempotent where possible (e.g., marking completed task as complete again)
- Deterministic database operations
- No randomness in tool logic

**Conversation Handling**:
- Deterministic context assembly (ordered by timestamp)
- Predictable tool selection based on intent
- No hidden state affecting behavior

### Reasonable Latency Expectations

**Response Time Targets**:
- **Simple requests** (no tool calls): <3 seconds
- **Tool calls**: +1-2 seconds per tool
- **Complex requests** (multiple tools): <5 seconds
- **Maximum**: <10 seconds for any request

**Latency Breakdown**:
- Authentication: 10-50ms
- Context loading: 50-200ms
- Agent processing: 500-2000ms
- Tool execution: 100-500ms per tool
- Response persistence: 50-200ms

### Security: Data Isolation

**User Data Isolation**:
- Each user isolated by `user_id`
- Tools enforce ownership on all operations
- No cross-user data leakage possible

**Authorization Checks**:
- Verify user owns conversation thread
- Verify user owns todo before operations
- Generic "not found" errors to prevent information leakage

**Authentication**:
- Reuse Phase II Better Auth
- Session/token validation on every request
- Secure session management

### Logging and Observability

**Logging Points**:
- Incoming request: user_id, thread_id, message preview
- Agent tool calls: tool name, parameters, result
- Tool execution: success/failure, duration
- Errors: error type, message, stack trace (server-side only)

**Observability Metrics**:
- Request latency (p50, p95, p99)
- Error rate by type
- Tool execution duration
- Token usage (OpenAI API)
- Rate limit violations

**Log Levels**:
- INFO: Normal operations
- WARN: Expected errors (validation, not found)
- ERROR: Unexpected errors (database failures)

---

## Strict Constraints (Explicitly Acknowledged)

This plan explicitly acknowledges and adheres to the following strict constraints:

### Phase Isolation Constraints

- ✅ No changes to existing Phase II frontend, REST API, or UI
- ✅ No autonomous/background agents
- ✅ No in-memory state anywhere (all state in Neon PostgreSQL)
- ✅ No multi-agent orchestration or swarms
- ✅ No RAG, vector search, fine-tuning, or external knowledge bases
- ✅ No real-time/WebSocket chat
- ✅ Use only Phase III authorized technologies: OpenAI Agents SDK + Official MCP SDK
- ✅ No Docker/Kubernetes/Kafka/Dapr or any later-phase infrastructure
- ✅ No additional features beyond the five basic todo operations via conversation

### Constitutional Compliance

This plan ensures 100% compliance with the amended Global Constitution (v1.2.0):

- **Phase III Authorization**: Uses only OpenAI Agents SDK and MCP SDK
- **Phase Isolation**: No leakage to earlier phases, extends Phase II as additional layer
- **Agent Behavior**: Deterministic tool-callers, no autonomous execution
- **Stateless Services**: All layers completely stateless
- **Data Isolation**: 100% user data isolation enforced
- **No Direct DB Access**: AI agents interact exclusively through MCP tools

---

## Project Structure

### Documentation (this feature)

```text
specs/001-conversational/
├── spec.md              # Feature specification (created)
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0 output (to be created)
├── data-model.md        # Phase 1 output (to be created)
├── quickstart.md        # Phase 1 output (to be created)
├── contracts/           # Phase 1 output (to be created)
└── tasks.md             # Phase 2 output (NOT created by /sp.plan)
```

### Source Code (extends existing Phase II backend)

```text
backend/
├── src/
│   ├── models/
│   │   ├── user.py (existing)
│   │   ├── todo.py (existing)
│   │   ├── conversation_thread.py (new)
│   │   └── conversation_message.py (new)
│   ├── services/
│   │   ├── auth_service.py (existing)
│   │   ├── todo_service.py (existing)
│   │   ├── chat_service.py (new)
│   │   └── mcp_tool_service.py (new)
│   ├── api/
│   │   ├── auth.py (existing)
│   │   ├── todos.py (existing)
│   │   └── chat.py (new)
│   ├── mcp/
│   │   ├── server.py (new)
│   │   └── tools.py (new)
│   └── agent/
│       └── chat_agent.py (new)
├── tests/
│   ├── contract/
│   ├── integration/
│   └── unit/
└── migrations/
    └── add_conversation_tables.py (new)
```

**Structure Decision**: Extends existing Phase II backend with new modules. No modifications to frontend or existing REST API endpoints.

---

## Complexity Tracking

> **No constitutional violations** - All gates passed, no complexity tracking required.

---

## Constitution Check (Post-Design Re-evaluation)

*GATE: Re-verified after Phase 1 design completion*

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Phase III technologies only | ✅ PASS | OpenAI Agents SDK + MCP SDK only |
| Stateless architecture | ✅ PASS | All layers designed stateless |
| No direct DB access from AI | ✅ PASS | MCP tools as exclusive access layer |
| Agent deterministic behavior | ✅ PASS | Single-agent pattern, low temperature |
| User data isolation | ✅ PASS | Authorization checks in all tools |
| No Phase II modifications | ✅ PASS | New modules only, no changes to existing code |
| No multi-agent systems | ✅ PASS | Single agent per request |
| No autonomous execution | ✅ PASS | Request-driven only |

**FINAL CONCLUSION**: All constitutional gates PASS. Plan is ready for task breakdown via `/sp.tasks`.

---

**Status**: Ready for Phase 0 (research.md generation)
