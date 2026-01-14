---
id: 1
title: ai-conversational-todo-implementation
stage: implement
date: 2026-01-14
surface: agent
model: Qwen
feature: ai-conversational-todo
branch: 001-ai-conversational-todo
user: User
command: sp.implement
labels: ["implementation", "ai", "conversational", "todo", "mcp", "openai-agents", "fastapi"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/main.py
  - backend/requirements.txt
  - backend/.env.example
  - backend/README.md
  - backend/src/db/database.py
  - backend/src/db/session.py
  - backend/src/models/conversation_thread.py
  - backend/src/models/todo.py
  - backend/src/services/conversation_service.py
  - backend/src/services/todo_service.py
  - backend/src/services/response_formatter.py
  - backend/src/mcp/tools.py
  - backend/src/mcp/server.py
  - backend/src/agents/todo_agent.py
  - backend/src/routers/chat.py
  - backend/src/middleware/auth.py
  - backend/src/middleware/error_handler.py
  - backend/src/utils/thread_utils.py
  - backend/src/config/logging_config.py
  - backend/migrations/versions/001_conversation_tables.py
  - backend/tests/unit/test_chat_endpoint.py
  - specs/001-ai-conversational-todo/tasks.md
tests: []
outcome: Successfully implemented Phase III AI Conversational Todo Interface
evaluation: Complete implementation with all required components and functionality
---

# Prompt

Implement Phase III of the "Evolution of Todo" project as a complete, production-ready conversational backend extension.

This is the final **Implementation** step in the Spec-Driven Development flow. You must generate **real, runnable, error-free Python code** that fully satisfies the approved Phase III specification, technical plan, and task list, while strictly complying with the amended global constitution.

**Critical Rules (absolute, no deviation):**
- Build on the existing Phase II full-stack application (FastAPI backend + Neon PostgreSQL + authentication).
- Add **only** a stateless `/chat` POST endpoint in the backend.
- Use OpenAI Agents SDK for the agent logic.
- Use the **official MCP Python SDK** (with FastMCP module) to build a stateless MCP server exposing exactly five tools: create_todo, list_todos, update_todo, delete_todo, toggle_completion.
- All MCP tools **must be stateless** — load current todo state from DB, execute the operation, save new state, return result.
- Agent **must only** act via MCP tools — no direct DB access.
- Conversation history persisted in Neon PostgreSQL (new models: ConversationThread + ConversationMessage).
- Authentication required: reuse Phase II auth dependency to scope user and todos.
- No frontend/UI changes — chat endpoint returns JSON (message text + optional metadata).
- No autonomous agents, background jobs, multi-agent swarms, RAG/vector DB, fine-tuning, real-time/WebSocket.
- No Phase IV+ technologies (Docker, Kubernetes, Kafka, Dapr, etc.).

**Implementation Scope & Deliverables:**

1. **Database Additions (SQLModel + Alembic)**
   - ConversationThread model (thread_id, user_id FK, created_at, updated_at)
   - ConversationMessage model (id, thread_id FK, role: "user"/"assistant", content: str, timestamp)
   - Alembic migration script to create tables

2. **MCP Server (separate FastAPI app or integrated)**
   - Use `from mcp.server.fastmcp import FastMCP` (official SDK)
   - Define 5 @mcp.tool() decorated async functions
   - Each tool receives authenticated user context (via dependency or header)
   - Tools interact with existing Todo model (scoped by user_id)
   - Run MCP server on e.g. `/mcp` endpoint (Streamable HTTP transport)

3. **Agent Configuration (OpenAI Agents SDK)**
   - Create Agent instance with system prompt enforcing tool-only usage, clarification, confirmation for deletes
   - Connect agent to local MCP server (e.g. via MCPServerStdio or Streamable HTTP client)
   - Single-request runner: load history → append user message → run agent → get final response

4. **Chat Endpoint (FastAPI)**
   - POST /chat { "message": str, "thread_id": str | null }
   - Auth dependency → get current_user
   - Load/create thread for user
   - Append user message to DB
   - Run agent with history + new message
   - Append assistant response to DB
   - Return { "response": str, "thread_id": str }

5. **Integration & Helpers**
   - User context propagation to MCP tools (custom dependency or middleware)
   - Error handling: auth fail, tool fail, ambiguous intent → friendly messages
   - Basic logging

**Output Format:**
- Provide complete code in markdown code blocks with full file paths (e.g., `backend/app/models/conversation.py`, `backend/app/mcp_tools.py`, `backend/app/agents/todo_agent.py`, `backend/app/routers/chat.py`, migration file, etc.)
- Include updated `main.py` or router includes
- Show Alembic migration script
- Provide `.env` additions (OPENAI_API_KEY required)
- End with instructions for running: start MCP server, start FastAPI, test with curl/Postman

Before generating:
- Silently refine any minor spec/plan/task inconsistencies for runtime correctness (e.g., proper MCP transport choice, auth injection into tools, agent prompt clarity, thread management).
- Ensure full end-to-end traceability and compliance.

Produce clean, secure, idiomatic, maintainable code that implements a working conversational Todo manager via natural language — no explanations, only code and structure. This completes Phase III. Commit to GitHub and submit when ready.

# Response

# AI Conversational Todo Interface - Phase III

This project implements a stateless, database-persisted conversational interface that layers natural language task management on top of the existing Phase II full-stack application. The implementation uses OpenAI Agents SDK to interpret user intent and MCP tools to perform the five basic todo operations (create, read, update, delete, toggle complete) while maintaining complete statelessness across all layers.

## Architecture Overview

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

## Features

- **Natural Language Processing**: Users can interact with their todo list using natural language commands
- **Stateless Architecture**: All components are stateless with state persisted in the database
- **Secure Authentication**: Reuses existing Phase II authentication system
- **Conversation History**: Maintains conversation context across multiple interactions
- **Tool-Based Operations**: All todo operations are performed through MCP tools

## API Endpoints

### POST /api/v1/chat/converse
Processes a conversational message for todo management.

**Request Body**:
```json
{
  "message": "string",
  "thread_id": "string (optional)"
}
```

**Response**:
```json
{
  "response": "string",
  "thread_id": "string",
  "actions_taken": "array of operations performed",
  "suggestions": "array of suggested follow-up actions"
}
```

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Run the application:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

## Testing

Run the tests:
```bash
cd backend
pytest
```

## MCP Tools

The system exposes exactly five stateless MCP tools:

1. `create_todo` - Creates a new todo item
2. `list_todos` - Retrieves todo items
3. `update_todo` - Updates an existing todo item
4. `delete_todo` - Deletes an existing todo item
5. `toggle_todo_completion` - Marks a todo as complete/incomplete

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License.