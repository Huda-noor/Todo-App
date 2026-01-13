# Phase III - Agent Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          CLIENT (Browser)                               │
├─────────────────────────────────────────────────────────────────────────┤
│  Next.js Frontend (existing Phase II)                                   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Todo List Page + New Chat UI (Phase III)                      │   │
│  │  - Chat message input                                           │   │
│  │  - Message history display                                      │   │
│  │  - Quick reply suggestions                                      │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                           │
│  API Calls:                                                              │
│  - GET/POST /api/todos (existing)                                       │
│  - POST /api/chat (NEW - Phase III)                                     │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Existing Phase II Endpoints                                    │   │
│  │  - /api/auth/* (Better Auth)                                   │   │
│  │  - /api/todos/* (Todo CRUD)                                    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  NEW Phase III Endpoints                                       │   │
│  │  - POST /api/chat (Conversational AI)                          │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                   PHASE III COMPONENTS                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Chat Endpoint Layer                                            │   │
│  │  /app/routers/chat.py                                           │   │
│  │  ├── Validate authentication (reuses Phase II)                  │   │
│  │  ├── Load conversation thread + messages                        │   │
│  │  ├── Call agent with user message + context                     │   │
│  │  ├── Save user message to database                              │   │
│  │  ├── Save AI response to database                               │   │
│  │  └── Return response to client                                  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                   │                                     │
│                                   ▼                                     │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Agent Layer (OpenAI Agents SDK)                               │   │
│  │  /app/agents/todo_agent.py                                      │   │
│  │  ├── Receive user message + conversation history                │   │
│  │  ├── Analyze intent (create/list/update/delete/toggle)          │   │
│  │  ├── Extract parameters from natural language                   │   │
│  │  ├── Decide which tools to call                                 │   │
│  │  ├── Execute tool calls via MCP                                 │   │
│  │  ├── Formulate natural language response                        │   │
│  │  └── Return: message + actions_taken + suggestions              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                   │                                     │
│                                   ▼                                     │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  MCP Server Layer                                              │   │
│  │  /app/mcp/tools.py                                             │   │
│  │  ├── create_todo(user_id, title, completed?)                   │   │
│  │  ├── list_todos(user_id, completed?)                           │   │
│  │  ├── update_todo(user_id, todo_id, title)                      │   │
│  │  ├── delete_todo(user_id, todo_id)                             │   │
│  │  └── toggle_todo_complete(user_id, todo_id)                    │   │
│  │                                                                   │   │
│  │  Each tool:                                                     │   │
│  │  - Stateless (no in-memory state)                               │   │
│  │  - Authenticates user_id                                        │   │
│  │  - Queries/updates database                                     │   │
│  │  - Returns structured result                                    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    DATABASE (Neon PostgreSQL)                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Existing Tables (Phase II):                                            │
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
│                                                                           │
│  ┌─────────────────────────┐                                        │
│  │ conversation_message    │                                        │
│  ├─────────────────────────┤                                        │
│  │ id (PK, UUID)           │                                        │
│  │ thread_id (FK)          │                                        │
│  │ role (user/assistant)   │                                        │
│  │ content (text)          │                                        │
│  │ created_at              │                                        │
│  └─────────────────────────┘                                        │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Component Details

### Chat Endpoint (`/app/routers/chat.py`)

```python
from fastapi import APIRouter, Depends, Request
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/api", tags=["chat"])

@router.post("/chat")
async def chat_endpoint(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
) -> ChatResponse:
    """
    Handle conversational AI requests.

    1. Load or create conversation thread
    2. Load conversation history
    3. Call agent with message + history
    4. Save messages to database
    5. Return response
    """
    # Load thread
    thread = get_or_create_thread(db, current_user.id, request.thread_id)

    # Load message history
    messages = load_thread_messages(db, thread.id)

    # Add user message to history
    messages.append({"role": "user", "content": request.message})

    # Call agent
    result = await agent.run(messages)

    # Save messages
    save_message(db, thread.id, "user", request.message)
    save_message(db, thread.id, "assistant", result.message)

    return ChatResponse(
        message=result.message,
        thread_id=str(thread.id),
        actions_taken=result.actions_taken,
        suggestions=result.suggestions
    )
```

### Agent Layer (`/app/agents/todo_agent.py`)

```python
from agents import Agent, function_tool
from app.mcp.tools import (
    create_todo,
    list_todos,
    update_todo,
    delete_todo,
    toggle_todo_complete
)

todo_agent = Agent(
    name="Todo Assistant",
    instructions="""You are a helpful todo assistant. You help users
    manage their todo list through natural conversation. Use tools
    to perform actions. Always be clear and helpful. Ask for
    clarification when user intent is ambiguous.""",
    tools=[
        create_todo,
        list_todos,
        update_todo,
        delete_todo,
        toggle_todo_complete
    ]
)
```

### MCP Tools (`/app/mcp/tools.py`)

```python
from mcp import Tool
from app.models.todo import Todo
from sqlalchemy.orm import Session

@function_tool
def create_todo(
    user_id: str,
    title: str,
    completed: bool = False
) -> dict:
    """Create a new todo for the authenticated user."""
    db = get_db_session()
    todo = Todo(
        user_id=user_id,
        description=title,
        is_complete=completed
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return {"success": True, "todo": todo}

@function_tool
def list_todos(
    user_id: str,
    completed: bool | None = None
) -> dict:
    """List todos for the authenticated user, optionally filtered."""
    db = get_db_session()
    query = db.query(Todo).filter(Todo.user_id == user_id)
    if completed is not None:
        query = query.filter(Todo.is_complete == completed)
    todos = query.order_by(Todo.created_at.desc()).all()
    return {"success": True, "todos": todos, "count": len(todos)}

# ... similar for update_todo, delete_todo, toggle_todo_complete
```

---

## Data Flow Sequence

```
1. User sends message
   POST /api/chat
   { "message": "Add a task to buy milk", "thread_id": null }

2. Validate authentication
   - Extract session cookie
   - Query session table
   - Get user_id

3. Load conversation context
   - If thread_id provided: load existing thread
   - Else: create new thread
   - Load all messages for thread

4. Call agent with context
   Agent receives:
   - User message
   - Full conversation history
   - List of available tools

5. Agent analyzes intent
   - Classify intent (create/list/update/delete/toggle)
   - Extract parameters from message
   - Decide which tools to call

6. Execute tool calls (via MCP)
   Each tool:
   - Receives user_id + parameters
   - Validates user authorization
   - Performs database operation
   - Returns structured result

7. Agent formulates response
   - Based on tool results
   - Natural language message
   - Suggestions for follow-up

8. Save to database
   - Insert user message
   - Insert AI response
   - Update thread timestamp

9. Return response
   {
     "message": "I've created: 'Buy milk'",
     "thread_id": "uuid",
     "actions_taken": [...],
     "suggestions": [...]
   }
```

---

## Stateless Design

### What is Stateless
- Chat endpoint: No in-memory state between requests
- MCP tools: No shared state, each call is independent
- All state persisted in database

### State Persistence
```
Request 1: "Add a task"
  → Load thread + messages from DB
  → Process with agent
  → Save messages to DB
  → Return response

Request 2: "Add another task"
  → Load thread + messages from DB (includes Request 1)
  → Process with agent (has context)
  → Save messages to DB
  → Return response
```

### No In-Memory State
```python
# WRONG - Stateful design (not allowed)
class ChatSession:
    def __init__(self):
        self.messages = []  # In-memory state!
        self.context = {}

# CORRECT - Stateless design
@router.post("/chat")
async def chat(request: ChatRequest):
    # Load state from DB on every request
    messages = load_from_db(request.thread_id)

    # Process
    result = agent.run(messages)

    # Save state to DB
    save_to_db(result)

    return result
```

---

## Error Handling

### Error Categories & Responses

| Error Type | Handling | User Message |
|------------|----------|--------------|
| Authentication error | 401 response | "Please sign in" |
| Invalid thread | Create new thread | (automatic) |
| Tool execution error | Return error in response | "I had trouble..." |
| LLM timeout | Return timeout message | "Taking too long..." |
| Rate limit | Return 429 | "Please wait a moment" |
| Malicious input | Sanitize, then process | (clean input) |

### Tool Error Handling
```python
@function_tool
def create_todo(user_id: str, title: str) -> dict:
    try:
        # Database operation
        todo = create_todo_db(user_id, title)
        return {"success": True, "todo": todo}
    except Exception as e:
        # Log error
        logger.error(f"Tool error: {e}")
        return {"success": False, "error": str(e)}
```
