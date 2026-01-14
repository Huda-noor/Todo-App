---
id: 1
title: ai-conversational-todo-plan
stage: plan
date: 2026-01-14
surface: agent
model: Qwen
feature: ai-conversational-todo
branch: 001-ai-conversational-todo
user: User
command: sp.plan
labels: ["plan", "ai", "conversational", "todo", "mcp", "openai-agents", "fastapi"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-ai-conversational-todo/plan.md
  - specs/001-ai-conversational-todo/research.md
  - specs/001-ai-conversational-todo/data-model.md
  - specs/001-ai-conversational-todo/quickstart.md
  - specs/001-ai-conversational-todo/contracts/chat-api-openapi.yaml
tests: []
outcome: Successfully created comprehensive implementation plan for AI conversational todo interface
evaluation: Plan includes all required sections and meets constitutional requirements
---

# Prompt

Create the Phase III technical architecture and implementation plan for the "Evolution of Todo" project.

This plan must derive **exclusively** from the approved Phase III specification and the amended global constitution.  
It defines **HOW** the conversational AI interface, stateless chat endpoint, OpenAI Agents SDK agent, and MCP tools will be implemented — without introducing any new features, UI changes, or future-phase technologies.

Required Sections (structured in clean markdown):

- **Introduction**  
  Purpose of the plan: outline the stateless, database-persisted conversational architecture that layers natural language task management on top of the existing Phase II full-stack application.

- **Overall Architecture Overview**  
  - Textual high-level flow diagram description  
  - Boundaries between: Chat API → OpenAI Agent → MCP Tools → Existing Backend Database  
  - Emphasis on complete statelessness of every layer

- **Chat API Layer (FastAPI)**  
  - Endpoint definition (path, method, authentication)  
  - Request parsing (user message + optional thread_id)  
  - Conversation thread retrieval from database  
  - Agent invocation strategy  
  - Response generation and conversation persistence  
  - Error handling and response format

- **Agent Layer (OpenAI Agents SDK)**  
  - Agent configuration and model choice  
  - System prompt and behavior guidelines  
  - Single-turn vs multi-turn handling per request  
  - Tool-calling strategy (only allowed tools: the five todo operations)  
  - Clarification and confirmation patterns  
  - Agent lifecycle: created per request, no persistent memory

- **MCP Server & Tools Layer**  
  - MCP server responsibilities and hosting approach  
  - Definition of exactly five stateless MCP tools:  
    – create_todo  
    – list_todos  
    – update_todo  
    – delete_todo  
    – toggle_todo_completion  
  - Tool input/output schemas (parameters & return types)  
  - Database interaction pattern (load current state → execute → save new state)  
  - User context enforcement (all operations scoped to authenticated user)  
  - Error propagation mechanism back to agent

- **Data Persistence Layer**  
  - Conversation model (thread per user, ordered messages, timestamps)  
  - Storage strategy (append-only message history)  
  - Relationship with existing User and Todo tables  
  - Schema additions and migration approach

- **Integration & Flow Details**  
  - End-to-end request lifecycle (from HTTP request → agent → tools → DB → response)  
  - Authentication propagation from chat request to all layers  
  - How tool failures are surfaced to the user  
  - Thread management (new vs continuing existing conversation)

- **Error Handling & Resilience Strategy**  
  - Handling ambiguous intent  
  - Tool execution failures  
  - Authentication/authorization failures  
  - Rate limiting & quota considerations  
  - User-friendly error messages

- **Non-Functional Considerations**  
  - Complete statelessness of chat endpoint, agent, and tools  
  - Deterministic behavior where possible  
  - Reasonable latency expectations  
  - Security: no leakage of user data between conversations  
  - Logging and observability points

Strict Constraints (explicitly acknowledge):
- No changes to existing Phase II frontend, REST API, or UI
- No autonomous/background agents
- No in-memory state anywhere (all state in Neon PostgreSQL)
- No multi-agent orchestration or swarms
- No RAG, vector search, fine-tuning, or external knowledge bases
- No real-time/WebSocket chat
- Use only Phase III authorized technologies: OpenAI Agents SDK + Official MCP SDK
- No Docker/Kubernetes/Kafka/Dapr or any later-phase infrastructure
- No additional features beyond the five basic todo operations via conversation

The plan must remain purely architectural/descriptive — use textual flows, pseudo-JSON schemas, and clear language, **no actual code**.  
It must enable precise, deterministic task breakdown while guaranteeing 100% compliance with the amended global constitution.

Output the complete plan in well-structured markdown with headings, subheadings, bullet points, tables (especially for tool schemas), and numbered flows for maximum readability and traceability.

# Response

# Implementation Plan: AI Conversational Todo Interface (Phase III)

**Branch**: `001-ai-conversational-todo` | **Date**: 2026-01-14 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-ai-conversational-todo/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan outlines the technical architecture for implementing a stateless, database-persisted conversational interface that layers natural language task management on top of the existing Phase II full-stack application. The implementation uses OpenAI Agents SDK to interpret user intent and MCP tools to perform the five basic todo operations (create, read, update, delete, toggle complete) while maintaining complete statelessness across all layers.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, OpenAI Agents SDK, Official MCP SDK, SQLAlchemy, Neon PostgreSQL driver
**Storage**: Neon PostgreSQL (existing Phase II database with new conversation tables)
**Testing**: pytest with integration and unit tests
**Target Platform**: Linux server (backend service)
**Project Type**: Web application (backend service extension to existing Phase II)
**Performance Goals**: <5 seconds response time for 90% of interactions, <2 seconds for tool execution
**Constraints**: Complete statelessness (no in-memory state), 100% user data isolation, deterministic behavior
**Scale/Scope**: Up to 1000 concurrent users, conversation history retention for 1 year

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Statelessness**: All components (chat endpoint, agent, MCP tools) must be completely stateless
- **No Direct DB Access**: AI agent must only interact through MCP tools
- **User Data Isolation**: Strict enforcement that users can only access their own data
- **Phase III Authorization**: Only using OpenAI Agents SDK and MCP SDK as authorized
- **No Autonomous Execution**: Agent operates only in response to user requests
- **No Memory State**: No persistent in-memory state between requests
- **Re-use Phase II**: Must reuse existing authentication and database infrastructure

## Overall Architecture Overview

The architecture consists of four distinct layers with clear boundaries:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        CLIENT (Browser)                               │
├─────────────────────────────────────────────────────────────────────────┤
│  Next.js Frontend (existing Phase II)                                 │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Todo List Page + Chat Interface (Phase III)                  │   │
│  │  - Chat message input                                         │   │
│  │  - Message history display                                    │   │
│  │  - Quick reply suggestions                                    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  API Calls:                                                            │
│  - GET/POST /api/todos (existing)                                     │
│  - POST /api/v1/chat/converse (NEW - Phase III)                       │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Existing Phase II Endpoints                                    │   │
│  │  - /api/auth/* (Better Auth)                                   │   │
│  │  - /api/todos/* (Todo CRUD)                                    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  NEW Phase III Endpoints                                       │   │
│  │  - POST /api/v1/chat/converse (Conversational AI)             │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                   PHASE III COMPONENTS                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Chat Endpoint Layer                                            │   │
│  │  /app/routers/chat.py                                          │   │
│  │  ├── Validate authentication (reuses Phase II)                 │   │
│  │  ├── Load conversation thread + messages                       │   │
│  │  ├── Call agent with user message + context                    │   │
│  │  ├── Save user message to database                             │   │
│  │  ├── Save AI response to database                              │   │
│  │  └── Return response to client                                 │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                   │                                     │
│                                   ▼                                     │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Agent Layer (OpenAI Agents SDK)                              │   │
│  │  /app/agents/todo_agent.py                                     │   │
│  │  ├── Receive user message + conversation history               │   │
│  │  ├── Analyze intent (create/list/update/delete/toggle)         │   │
│  │  ├── Extract parameters from natural language                  │   │
│  │  ├── Decide which tools to call                                │   │
│  │  ├── Execute tool calls via MCP                                │   │
│  │  ├── Formulate natural language response                       │   │
│  │  └── Return: message + actions_taken + suggestions           │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                   │                                     │
│                                   ▼                                     │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  MCP Server Layer                                              │   │
│  │  /app/mcp/tools.py                                             │   │
│  │  ├── create_todo(user_id, title, completed?, due_date?)        │   │
│  │  ├── list_todos(user_id, filter?)                             │   │
│  │  ├── update_todo(user_id, todo_id, title?, completed?)        │   │
│  │  ├── delete_todo(user_id, todo_id)                            │   │
│  │  └── toggle_todo_completion(user_id, todo_id, completed?)    │   │
│  │                                                                   │   │
│  │  Each tool:                                                     │   │
│  │  - Stateless (no in-memory state)                               │   │
│  │  - Authenticates user_id                                        │   │
│  │  - Queries/updates database                                     │   │
│  │  - Returns structured result                                    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    DATABASE (Neon PostgreSQL)                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Existing Tables (Phase II):                                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐         │
│  │ user            │  │ session         │  │ todo            │         │
│  ├─────────────────┤  ├─────────────────┤  ├─────────────────┤         │
│  │ id (PK)         │  │ id (PK)         │  │ id (PK)         │         │
│  │ email           │  │ user_id (FK)    │  │ user_id (FK)    │         │
│  │ password        │  │ expires_at      │  │ description     │         │
│  │ created_at      │  │ token           │  │ is_complete     │         │
│  └─────────────────┘  └─────────────────┘  │ created_at      │         │
│                                            │ updated_at      │         │
│  NEW Tables (Phase III):                    └─────────────────┘         │
│  ┌─────────────────────────┐                                        │
│  │ conversation_thread     │                                        │
│  ├─────────────────────────┤                                        │
│  │ id (PK, UUID)           │                                        │
│  │ user_id (FK)            │                                        │
│  │ created_at              │                                        │
│  │ updated_at              │                                        │
│  └─────────────────────────┘                                        │
│                                                                         │
│  ┌─────────────────────────┐                                        │
│  │ conversation_message    │                                        │
│  ├─────────────────────────┤                                        │
│  │ id (PK, UUID)           │                                        │
│  │ thread_id (FK)          │                                        │
│  │ role (user/assistant)   │                                        │
│  │ content (text)          │                                        │
│  │ created_at              │                                        │
│  └─────────────────────────┘                                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Chat API Layer (FastAPI)

The chat API endpoint serves as the entry point for all conversational interactions:

### Endpoint Definition
- **Method**: POST
- **Path**: `/api/v1/chat/converse`
- **Authentication**: Bearer token (reusing Phase II authentication)

### Request Processing Flow
1. **Authentication Validation**: Extract and validate user session from bearer token
2. **Conversation Context Loading**: Load conversation thread and message history from database
3. **Agent Invocation**: Pass user message and context to OpenAI agent
4. **Response Generation**: Format agent response for client
5. **Persistence**: Save both user message and agent response to database
6. **Response Return**: Return formatted response to client

### Request Format
```json
{
  "message": "string",
  "thread_id": "string (optional)"
}
```

### Response Format
```json
{
  "response": "string",
  "thread_id": "string",
  "actions_taken": "array of operations performed"
}
```

### Error Handling
- **401 Unauthorized**: Invalid or expired authentication token
- **422 Validation Error**: Invalid request format
- **500 Internal Error**: Tool execution or agent processing failures

## Agent Layer (OpenAI Agents SDK)

The agent layer processes natural language input and orchestrates tool calls:

### Configuration
- **Model**: OpenAI GPT-4o-mini (recommended for cost/performance balance)
- **System Prompt**: Defines agent behavior and constraints for todo operations
- **Tool Integration**: MCP tools registered for agent to call

### Agent Behavior Guidelines
- **Intent Classification**: Accurately identify user intent (create, read, update, delete, toggle complete)
- **Parameter Extraction**: Parse relevant parameters from natural language
- **Tool Selection**: Choose appropriate MCP tool based on intent
- **Context Awareness**: Maintain conversation context across turns
- **Clarification Handling**: Request clarification for ambiguous requests
- **Confirmation Enforcement**: Require confirmation for destructive operations

### Agent Lifecycle
- **Per-Request Creation**: Agent instantiated for each request, no persistent state
- **Tool Calling**: Execute only approved MCP tools (no direct database access)
- **Response Generation**: Formulate natural language response based on tool results

## MCP Server & Tools Layer

The MCP server exposes exactly five stateless tools for todo operations:

### Tool Definitions

#### 1. create_todo
```python
def create_todo(
    user_id: str,
    title: str,
    description: str = "",
    due_date: str = None  # ISO 8601 datetime (optional)
) -> dict:
    """
    Creates a new todo item for the authenticated user.
    
    Args:
        user_id: Unique identifier of the authenticated user
        title: Title/description of the todo
        description: Additional details (optional)
        due_date: Due date in ISO 8601 format (optional)
        
    Returns:
        {
            "success": bool,
            "todo_id": str,
            "message": str
        }
    """
```

#### 2. list_todos
```python
def list_todos(
    user_id: str,
    filter: str = "all"  # all, completed, pending, overdue, today, etc.
) -> dict:
    """
    Retrieves todo items for the authenticated user.
    
    Args:
        user_id: Unique identifier of the authenticated user
        filter: Filter criteria for todo list (optional)
        
    Returns:
        {
            "success": bool,
            "todos": list of todo objects,
            "count": int
        }
    """
```

#### 3. update_todo
```python
def update_todo(
    user_id: str,
    todo_id: str,
    title: str = None,
    description: str = None,
    due_date: str = None,
    completed: bool = None
) -> dict:
    """
    Updates an existing todo item for the authenticated user.
    
    Args:
        user_id: Unique identifier of the authenticated user
        todo_id: Unique identifier of the todo to update
        title: New title for the todo (optional)
        description: New description for the todo (optional)
        due_date: New due date in ISO 8601 format (optional)
        completed: New completion status (optional)
        
    Returns:
        {
            "success": bool,
            "message": str
        }
    """
```

#### 4. delete_todo
```python
def delete_todo(
    user_id: str,
    todo_id: str
) -> dict:
    """
    Deletes an existing todo item for the authenticated user.
    
    Args:
        user_id: Unique identifier of the authenticated user
        todo_id: Unique identifier of the todo to delete
        
    Returns:
        {
            "success": bool,
            "message": str
        }
    """
```

#### 5. toggle_todo_completion
```python
def toggle_todo_completion(
    user_id: str,
    todo_id: str,
    completed: bool
) -> dict:
    """
    Marks an existing todo as complete/incomplete for the authenticated user.
    
    Args:
        user_id: Unique identifier of the authenticated user
        todo_id: Unique identifier of the todo to update
        completed: New completion status
        
    Returns:
        {
            "success": bool,
            "message": str
        }
    """
```

### MCP Server Characteristics
- **Statelessness**: Each tool call is independent with no shared state
- **User Authentication**: Validates user_id for all operations
- **Database Interaction**: Performs CRUD operations on todo and conversation tables
- **Error Propagation**: Returns structured error responses to agent

## Data Persistence Layer

### Conversation Model
The conversation model stores all chat interactions:

#### Conversation Thread
- `thread_id`: UUID primary key for conversation thread
- `user_id`: Foreign key linking to authenticated user
- `created_at`: Timestamp of thread creation
- `updated_at`: Timestamp of last activity in thread
- `active`: Boolean indicating if thread is currently active

#### Conversation Message
- `id`: UUID primary key for message
- `thread_id`: Foreign key linking to conversation thread
- `role`: Enum ("user" or "assistant")
- `content`: Text content of the message
- `timestamp`: ISO 8601 timestamp of when message was sent

### Database Schema
```sql
-- Conversation thread table
CREATE TABLE conversation_thread (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    active BOOLEAN DEFAULT TRUE,

    CONSTRAINT fk_conversation_thread_user
        FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

-- Conversation message table
CREATE TABLE conversation_message (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    thread_id UUID NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_conversation_message_thread
        FOREIGN KEY (thread_id) REFERENCES conversation_thread(id) ON DELETE CASCADE
);
```

### Data Relationships
- `conversation_thread.user_id` → `user.id` (CASCADE delete)
- `conversation_message.thread_id` → `conversation_thread.id` (CASCADE delete)

## Integration & Flow Details

### End-to-End Request Lifecycle
1. **Client Request**: User sends message to `/api/v1/chat/converse`
2. **Authentication**: Chat endpoint validates user session token
3. **Context Loading**: Load conversation thread and message history from database
4. **Agent Processing**: Pass message and context to OpenAI agent
5. **Intent Analysis**: Agent determines user intent and extracts parameters
6. **Tool Execution**: Agent calls appropriate MCP tool(s)
7. **Database Operations**: MCP tool performs database CRUD operation
8. **Response Generation**: Agent formulates natural language response
9. **Persistence**: Save user message and agent response to database
10. **Response Return**: Return formatted response to client

### Authentication Propagation
- **Token Validation**: Chat endpoint validates bearer token from Phase II auth system
- **User Context**: User ID extracted and passed to all MCP tools
- **Authorization**: All database operations scoped to authenticated user

### Thread Management
- **New Conversation**: If no thread_id provided, create new conversation thread
- **Existing Conversation**: If thread_id provided, load existing thread and history
- **Context Preservation**: All previous messages available to agent for context

## Error Handling & Resilience Strategy

### Ambiguous Intent Handling
- **Detection**: Agent identifies when user intent is unclear
- **Clarification**: Agent asks targeted questions to resolve ambiguity
- **Context**: Reference previous messages when asking for clarification

### Tool Execution Failures
- **Error Capture**: MCP tools return structured error responses
- **User Notification**: Agent communicates failure in user-friendly terms
- **Retry Suggestion**: Suggest user try again or rephrase request

### Authentication Failures
- **Validation**: Chat endpoint validates authentication on every request
- **Response**: Return 401 Unauthorized with appropriate message
- **No Information Leakage**: Don't reveal internal system details

### Rate Limiting
- **Quota Management**: Implement rate limiting to prevent abuse
- **Response**: Return 429 Too Many Requests with retry-after header
- **User Messaging**: Friendly message suggesting they slow down

## Non-Functional Considerations

### Statelessness
- **Complete Statelessness**: No in-memory state in chat endpoint, agent, or tools
- **Database-Only State**: All state persisted in Neon PostgreSQL
- **Horizontal Scaling**: Ability to scale backend instances without shared state

### Deterministic Behavior
- **Consistent Responses**: Same input produces same output (given same model)
- **Predictable Tooling**: MCP tools behave consistently for same inputs
- **Traceable Actions**: All operations traceable to user intent

### Latency Expectations
- **Response Time**: <5 seconds for 90% of interactions
- **Tool Execution**: <2 seconds for individual tool calls
- **Context Loading**: <500ms for conversation history retrieval

### Security
- **Data Isolation**: Users can only access their own conversations and todos
- **No Direct Access**: Agent restricted to MCP tools only
- **Input Sanitization**: Validate and sanitize all user inputs

### Observability
- **Logging**: Structured logging for debugging and monitoring
- **Metrics**: Track response times, error rates, and usage patterns
- **Tracing**: Request tracing across all layers for debugging

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-conversational-todo/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── todo.py
│   │   ├── user.py
│   │   ├── conversation_thread.py
│   │   └── conversation_message.py
│   ├── services/
│   │   ├── auth_service.py
│   │   └── todo_service.py
│   ├── mcp/
│   │   ├── tools.py
│   │   └── server.py
│   ├── agents/
│   │   └── todo_agent.py
│   ├── routers/
│   │   └── chat.py
│   └── main.py
└── tests/
    ├── unit/
    ├── integration/
    └── contract/
```

**Structure Decision**: Web application with backend service extension to existing Phase II. The new conversational features are added as an extension to the existing backend, with new models for conversation persistence and new endpoints for chat functionality.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| (None) | (None) | (None) |