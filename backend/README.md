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