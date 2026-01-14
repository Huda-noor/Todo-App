# Feature Specification: Phase III - Conversational AI Interface

**Feature Branch**: `001-conversational`
**Created**: 2026-01-10
**Status**: Draft
**Input**: Phase III conversational interface for Todo management with AI agents and MCP tools

---

## Introduction

Phase III of the "Evolution of Todo" project delivers a natural language conversational layer on top of the existing Phase II full-stack application. This enables authenticated users to manage their todos through text-based chat interactions, powered by AI agents that interpret intent and execute actions via Model Context Protocol (MCP) tools.

### Objectives

- Add a stateless conversational interface that allows users to manage todos using natural language
- Provide all five basic Todo operations (create, read, update, delete, toggle complete) through chat
- Maintain strict phase isolation by building on Phase II without modifying existing REST API or frontend
- Ensure all task management actions occur exclusively through MCP tools called by AI agents
- Persist conversation history and intermediate state in the existing database

### Constitutional Alignment

This specification strictly adheres to the amended Global Constitution (v1.2.0):

- **Phase III Authorization**: Uses only Phase III-authorized technologies (OpenAI Agents SDK, MCP)
- **Phase Isolation**: No leakage of Phase III technologies into Phase I or II; extends Phase II as an additional layer
- **Agent Behavior**: AI agents act as deterministic tool-callers, not autonomous actors
- **Stateless Services**: Both chat endpoint and MCP tools are completely stateless
- **Data Isolation**: All operations respect existing user-todo isolation from Phase II

### Governance Statement

Phase III delivers a conversational capability as an additional stateless backend endpoint. The existing Phase II frontend UI and core REST API remain unchanged. No preparation, scaffolding, or references to Phase IV-V technologies (Docker, Kubernetes, Kafka, Dapr) are introduced.

---

## User Scenarios & Testing

### User Story 1 - Create Todo via Chat (Priority: P1)

As an authenticated user, I want to create a new todo by sending a natural language message, so that I can add tasks without navigating through a UI.

**Why this priority**: This is the most fundamental operation and enables users to build their todo list entirely through conversation.

**Independent Test**: Can be fully tested by sending a chat message requesting to create a todo and verifying the todo is created in the user's database.

**Acceptance Scenarios**:

1. **Given** an authenticated user with no todos, **When** the user sends "Add a task to buy groceries", **Then** a new todo with title "Buy groceries" is created for that user
2. **Given** an authenticated user with existing todos, **When** the user sends "Create a todo: Schedule dentist appointment for next Friday", **Then** a new todo with the specified title is created and appears in the user's list
3. **Given** an authenticated user, **When** the user sends an ambiguous message like "Add something for later", **Then** the agent asks for clarification about the todo title
4. **Given** an authenticated user, **When** the user sends "Remind me to call mom tomorrow at 5pm", **Then** the agent interprets this as creating a todo with the appropriate title

---

### User Story 2 - List Todos via Chat (Priority: P1)

As an authenticated user, I want to view all my todos by sending a simple message, so that I can quickly see what tasks I have pending.

**Why this priority**: Users need to see their existing tasks to manage them effectively; this is foundational for all other operations.

**Independent Test**: Can be fully tested by sending a chat message requesting to view todos and verifying the returned list matches the user's stored todos.

**Acceptance Scenarios**:

1. **Given** an authenticated user with 3 todos, **When** the user sends "Show me my todos", **Then** the system returns all 3 todos in a human-readable format
2. **Given** an authenticated user with no todos, **When** the user sends "What are my tasks?", **Then** the system responds that the user has no pending todos
3. **Given** an authenticated user with completed and incomplete todos, **When** the user sends "List my pending tasks", **Then** the system returns only incomplete todos
4. **Given** an authenticated user, **When** the user sends "What do I need to do?", **Then** the system returns all todos with appropriate formatting

---

### User Story 3 - Mark Todo Complete via Chat (Priority: P1)

As an authenticated user, I want to mark a todo as completed by sending a natural language message, so that I can track my progress without manual checkbox clicks.

**Why this priority**: Task completion is the core feedback loop for todo management; users need to mark progress through conversation.

**Independent Test**: Can be fully tested by sending a chat message to complete a todo and verifying the todo's completion status is updated.

**Acceptance Scenarios**:

1. **Given** an authenticated user with an incomplete todo "Buy milk", **When** the user sends "I finished buying milk", **Then** the todo is marked as completed
2. **Given** an authenticated user with multiple todos, **When** the user sends "Mark task 'call client' as done", **Then** the specified todo is marked as completed
3. **Given** an authenticated user with a completed todo, **When** the user sends "Mark 'Buy milk' as done again", **Then** the system confirms it's already completed (no error)
4. **Given** an authenticated user, **When** the user sends an ambiguous message like "I'm done with that", **Then** the agent asks for clarification about which todo to complete

---

### User Story 4 - Update Todo via Chat (Priority: P2)

As an authenticated user, I want to modify an existing todo's title by sending a natural language message, so that I can correct mistakes or refine task descriptions.

**Why this priority**: Users often need to refine task descriptions; this enables corrections without navigating to an edit screen.

**Independent Test**: Can be fully tested by sending a chat message to update a todo and verifying the title change is persisted.

**Acceptance Scenarios**:

1. **Given** an authenticated user with a todo "Buy milk", **When** the user sends "Change 'Buy milk' to 'Buy 2 gallons of milk'", **Then** the todo title is updated to "Buy 2 gallons of milk"
2. **Given** an authenticated user with multiple similar todos, **When** the user sends "Update the first 'call client' task to include phone number", **Then** the agent asks for clarification about which todo to update
3. **Given** an authenticated user, **When** the user sends "Fix that task I just added", **Then** the agent asks for clarification about which task and what changes to make
4. **Given** an authenticated user, **When** the user sends "Rename todo #3 to 'Email boss'", **Then** the agent interprets this and updates the third todo appropriately

---

### User Story 5 - Delete Todo via Chat (Priority: P2)

As an authenticated user, I want to remove a todo by sending a natural language message, so that I can clean up my task list when tasks are no longer relevant.

**Why this priority**: Task deletion maintains list hygiene; users need to remove irrelevant tasks to keep their list focused.

**Independent Test**: Can be fully tested by sending a chat message to delete a todo and verifying the todo is removed from the user's database.

**Acceptance Scenarios**:

1. **Given** an authenticated user with a todo "Old task", **When** the user sends "Delete 'Old task'", **Then** the system confirms deletion and the todo is removed
2. **Given** an authenticated user, **When** the user sends "Remove the task about groceries", **Then** the system identifies the matching todo and deletes it
3. **Given** an authenticated user attempting to delete a todo, **When** the user sends "Delete 'My important task'", **Then** the system requires confirmation before deletion
4. **Given** an authenticated user with no matching todo, **When** the user sends "Delete non-existent task", **Then** the system informs the user that no matching todo was found

---

### User Story 6 - General Conversation (Priority: P3)

As an authenticated user, I want to engage in casual conversation about my todos, so that the interface feels natural and helpful rather than robotic.

**Why this priority**: Conversational polish improves user experience and makes the system more approachable.

**Independent Test**: Can be fully tested by sending conversational messages and verifying helpful, context-aware responses.

**Acceptance Scenarios**:

1. **Given** an authenticated user with todos, **When** the user sends "How many tasks do I have?", **Then** the system responds with the count and optionally lists them
2. **Given** an authenticated user, **When** the user sends "What should I do first?", **Then** the system suggests prioritizing based on task order or asks for preferences
3. **Given** an authenticated user, **When** the user sends "I feel overwhelmed by all my tasks", **Then** the system provides a supportive message and offers to help organize or prioritize
4. **Given** an authenticated user, **When** the user sends a greeting like "Hello", **Then** the system responds helpfully and offers to help manage todos

---

### Edge Cases

- What happens when a user sends a message that doesn't match any intent?
- How does the system handle messages with typos or unclear phrasing?
- What happens when the user references a todo that doesn't exist?
- How does the system handle concurrent chat requests from the same user?
- What happens when the MCP tool execution fails during a chat interaction?
- How does the system handle rate limiting or quota exhaustion for the AI model?
- What happens when a user's authentication session expires mid-conversation?
- How does the system handle extremely long messages or rapid successive inputs?

---

## Requirements

### Functional Requirements

- **FR-001**: System MUST accept authenticated POST requests to `/api/chat` with natural language messages
- **FR-002**: System MUST interpret natural language messages to detect todo operation intents (create, read, update, delete, toggle complete)
- **FR-003**: System MUST execute todo operations exclusively through MCP tools (no direct database access)
- **FR-004**: System MUST expose exactly five MCP tools corresponding to basic Todo operations
- **FR-005**: System MUST maintain conversation history in the database per user
- **FR-006**: System MUST associate conversation threads with authenticated users via user_id
- **FR-007**: System MUST return natural language responses from the AI agent
- **FR-008**: System MUST request clarification when user intent is ambiguous
- **FR-009**: System MUST require confirmation before destructive operations (delete)
- **FR-010**: System MUST persist both user messages and agent responses in the database
- **FR-011**: System MUST load conversation history from the database on every request
- **FR-012**: System MUST support multi-turn conversations with context awareness
- **FR-013**: System MUST enforce user data isolation (users access only their own data)
- **FR-014**: System MUST handle errors gracefully with user-friendly messages
- **FR-015**: System MUST be completely stateless (chat endpoint and all MCP tools)
- **FR-016**: System MUST reuse Phase II authentication without modification
- **FR-017**: System MUST NOT modify Phase II REST API endpoints
- **FR-018**: System MUST NOT modify Phase II frontend
- **FR-019**: System MUST NOT introduce Phase IV-V technologies
- **FR-020**: System MUST NOT include autonomous or background agent execution
- **FR-021**: System MUST NOT include multi-agent systems
- **FR-022**: System MUST NOT include RAG or vector search
- **FR-023**: System MUST NOT include model fine-tuning
- **FR-024**: System MUST NOT include real-time/WebSocket chat
- **FR-025**: System MUST NOT include a frontend chat UI

---

### Key Entities

- **Conversation Thread**: A container for messages exchanged between a user and the AI agent. Has a unique ID, is owned by a user, and contains a chronologically ordered list of messages.
- **Conversation Message**: A single message in a conversation thread. Has a role (user or assistant), content text, and timestamp.
- **Todo**: (existing from Phase II) A task item with title, completion status, and ownership by a user.
- **User**: (existing from Phase II) An authenticated user with unique ID, credentials, and associated todos.

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can successfully create a todo via natural language chat in under 5 seconds from message submission to confirmation
- **SC-002**: Users can retrieve their complete todo list via natural language chat with 100% accuracy (all todos returned)
- **SC-003**: The system correctly interprets user intent for all five basic operations with at least 90% accuracy across common phrasing variations
- **SC-004**: Conversation history is reliably persisted such that multi-turn conversations maintain context across 10+ message exchanges
- **SC-005**: The system handles clarification requests appropriately, achieving a successful resolution rate of at least 85% on ambiguous inputs
- **SC-006**: User data isolation is maintained such that users cannot access or modify todos or conversations belonging to other users (100% isolation)
- **SC-007**: The chat endpoint remains stateless, capable of handling concurrent requests from multiple users without data inconsistency
- **SC-008**: All MCP tools execute successfully within 2 seconds for simple operations
- **SC-009**: Error messages are user-friendly and actionable, with users able to self-correct their input in at least 80% of error cases
- **SC-010**: Destructive operations (delete) always require explicit confirmation before execution, preventing accidental data loss

---

## Detailed Specifications (Phase III-Specific)

The following sections provide detailed specifications for Phase III-specific components. These are implementation-focused and should be used during the planning phase.

### Agent Behavior Expectations

#### Intent Interpretation

The AI agent MUST:

- Analyze incoming natural language messages to determine the user's intent (create, read, update, delete, toggle complete, or general conversation)
- Extract relevant parameters from the message (todo title, identifiers, completion status, etc.)
- Apply reasonable interpretation for common phrasing variations
- Request clarification when intent is ambiguous or parameters are missing
- Avoid making assumptions about unclear user requests

**Examples of Intent Detection**:

| User Message | Detected Intent | Parameters |
|-------------|----------------|------------|
| "Add a task to buy milk" | Create Todo | title: "Buy milk" |
| "Show me my tasks" | List Todos | (none) |
| "I'm done with that" | Toggle Complete | Requires clarification: which todo? |
| "Change task 1 to new title" | Update Todo | identifier: 1, new_title: "new title" |
| "Remove the grocery task" | Delete Todo | title_pattern: "grocery" |

#### Clarification Handling

When intent or parameters are ambiguous, the agent MUST:

- Ask targeted clarification questions to resolve ambiguity
- Provide context from previous messages when relevant
- Limit clarification requests to 2-3 questions maximum per turn
- Avoid asking about information already provided in conversation history

#### Confirmation for Destructive Actions

For destructive operations (delete), the agent MUST:

- Present the action to be performed clearly
- Request explicit confirmation before executing
- Confirm completion after execution
- Cancel if user rejects confirmation

#### Multi-Turn Conversation Handling

The agent MUST:

- Maintain conversation context across multiple turns by retrieving conversation history from the database
- Reference previous messages when interpreting new messages
- Support follow-up questions and refinements
- Allow users to provide information incrementally
- Handle corrections to previous actions

#### Error Recovery

When tool execution fails, the agent MUST:

- Inform the user in clear, non-technical language
- Suggest alternative approaches if possible
- Allow the user to retry or modify their request
- Avoid exposing internal error details or stack traces

---

### MCP Tool Definitions

The MCP server exposes exactly five stateless tools corresponding to basic Todo operations.

#### Tool 1: create_todo

**Purpose**: Creates a new todo for an authenticated user.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | string | Yes | Unique identifier of the authenticated user |
| title | string | Yes | Title/description of the todo |
| completed | boolean | No | Initial completion status (default: false) |

**Expected Output Shape**:

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

#### Tool 2: list_todos

**Purpose**: Retrieves todos for an authenticated user, optionally filtered by completion status.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | string | Yes | Unique identifier of the authenticated user |
| completed | boolean | No | Filter by completion status (if provided) |

**Expected Output Shape**:

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

#### Tool 3: update_todo

**Purpose**: Updates an existing todo's title.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | string | Yes | Unique identifier of the authenticated user |
| todo_id | integer | Yes | Unique identifier of the todo to update |
| title | string | Yes | New title for the todo |

**Expected Output Shape**:

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

#### Tool 4: delete_todo

**Purpose**: Deletes an existing todo for an authenticated user.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | string | Yes | Unique identifier of the authenticated user |
| todo_id | integer | Yes | Unique identifier of the todo to delete |

**Expected Output Shape**:

```json
{
  "success": true,
  "deleted_id": 123
}
```

#### Tool 5: toggle_todo_complete

**Purpose**: Toggles the completion status of an existing todo.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | string | Yes | Unique identifier of the authenticated user |
| todo_id | integer | Yes | Unique identifier of the todo to toggle |

**Expected Output Shape**:

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

---

### Conversation & State Lifecycle

#### Conversation Thread Creation

1. **Initial Request**: When an authenticated user sends the first message:
   - System validates authentication (reuses Phase II session/token)
   - Extracts user_id from authentication context
   - Creates a new conversation thread in the database
   - Thread is associated with the user via user_id
   - Thread receives a unique thread_id

#### Context Retrieval

On every incoming chat request:

1. **Load Thread**: System retrieves the conversation thread by thread_id
2. **Load Messages**: All messages in the thread are loaded in chronological order
3. **Authentication Verify**: System verifies user owns the thread
4. **Context Assembly**: Message history is assembled and passed to the AI agent

#### Message Processing Flow

1. **Receive Request**: Chat endpoint receives authenticated message
2. **Load Context**: Retrieve conversation history from database
3. **AI Processing**: Agent analyzes message + context to determine intent
4. **Tool Execution**: Agent calls MCP tools if action required
5. **Response Generation**: Agent formulates natural language response
6. **Persistence**: User message and agent response are saved to database
7. **Return Response**: Response is returned to user

---

### Data Models for Persistence

#### Conversation Thread Model

**Table**: `conversation_threads`

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| id | UUID | Yes | Unique thread identifier (primary key) |
| user_id | UUID | Yes | Reference to the owning user |
| created_at | timestamp | Yes | When the thread was created |
| updated_at | timestamp | Yes | When the thread was last updated |

#### Conversation Message Model

**Table**: `conversation_messages`

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| id | UUID | Yes | Unique message identifier (primary key) |
| thread_id | UUID | Yes | Reference to the thread |
| role | enum | Yes | "user" or "assistant" |
| content | text | Yes | Message content (natural language) |
| created_at | timestamp | Yes | When the message was created |

---

### API Endpoint Specification

#### Chat Endpoint

**Method**: `POST`

**Path**: `/api/chat`

**Authentication Required**: Yes (reuses Phase II authentication)

**Request Body**:

```json
{
  "message": "Add a task to buy milk",
  "thread_id": "optional-existing-thread-uuid"
}
```

**Success Response** (HTTP 200):

```json
{
  "message": "I've created a new todo: 'Buy milk'",
  "thread_id": "uuid-of-conversation-thread",
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

### Acceptance Criteria (Detailed)

#### AC-1: Successful Todo Creation via Chat

**Given** an authenticated user with an active session,
**When** the user sends a POST request to `/api/chat` with message "Add a task to buy milk",
**Then** the system MUST:
- Authenticate the user successfully
- Create a new conversation thread (if none provided)
- Interpret the intent as "create_todo"
- Call the `create_todo` MCP tool with appropriate parameters
- Persist the user message and agent response in the database
- Return HTTP 200 with a confirmation message
- Return the new thread_id for context persistence
- The todo must be stored in the database associated with the user

#### AC-2 through AC-8: Similar detailed acceptance criteria for list, update, delete, clarification, multi-turn, and error recovery scenarios.

---

### Error & Edge Cases

- **EC-1**: Invalid Authentication - Return HTTP 401
- **EC-2**: Unrecognized Intent - Return HTTP 200 with polite rejection
- **EC-3**: Tool Execution Failure - Return HTTP 200 with user-friendly error
- **EC-4**: Ambiguous Command - Request clarification
- **EC-5**: Destructive Action - Require confirmation
- **EC-6**: Rate Limiting - Return HTTP 429
- **EC-7**: Todo Not Found - Return HTTP 200 with "Todo not found"
- **EC-8**: Empty/Invalid Message - Return HTTP 400

---

### Non-Functional Requirements

- **NFR-1**: Stateless Services - No in-memory state between requests
- **NFR-2**: Deterministic Behavior - Similar inputs produce similar outputs
- **NFR-3**: User Data Isolation - 100% data isolation between users
- **NFR-4**: Response Time - Under 3 seconds for simple requests, under 5 seconds for complex requests
- **NFR-5**: No Persistent In-Memory Agent State - All state persisted in database
- **NFR-6**: Persistence Reliability - All messages saved before response

---

### Assumptions & Explicit Exclusions

#### Assumptions

1. Phase II provides reliable authentication with session/token management
2. Phase II's Neon PostgreSQL database is accessible and accepts new tables
3. Phase II's user model provides stable user_id for conversation thread association
4. Valid API key for OpenAI model is available and configured
5. Official MCP SDK is compatible with the project's Python environment
6. OpenAI Agents SDK is available and compatible with the project

#### Explicit Exclusions

1. No frontend chat UI (backend-only capability)
2. No autonomous/background agent execution
3. No multi-agent systems
4. No RAG/vector search
5. No model fine-tuning
6. No real-time/WebSocket chat
7. No new authentication mechanisms
8. No modifications to Phase II REST API
9. No modifications to Phase II frontend
10. No preparation for Phase IV-V technologies

---

**Status**: Ready for planning
