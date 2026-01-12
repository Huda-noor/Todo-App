# Phase III - Chat API Specification

## Endpoint

### POST /api/chat

Conversational interface for todo management via natural language.

**Base URL**: Same as backend (`http://localhost:8000` or production)

**Authentication**: Required (session cookie)

---

## Request

### Headers
```
Content-Type: application/json
Cookie: better-auth.session_token={session_token}
```

### Body
```json
{
  "message": "Add a task to buy milk",
  "thread_id": "770e8400-e29b-41d4-a716-446655440000"  // Optional
}
```

**Parameters**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | string | Yes | User's natural language message (1-10000 chars) |
| `thread_id` | UUID | No | Existing conversation thread. Omit for new conversation |

---

## Response

### Success (200 OK)
```json
{
  "message": "I've created a new todo: 'Buy groceries'",
  "thread_id": "770e8400-e29b-41d4-a716-446655440000",
  "actions_taken": [
    {
      "tool": "create_todo",
      "description": "Created todo with title 'Buy groceries'",
      "result": {
        "success": true,
        "todo": {
          "id": "660e8400-e29b-41d4-a716-446655440001",
          "user_id": "550e8400-e29b-41d4-a716-446655440000",
          "description": "Buy groceries",
          "is_complete": false,
          "created_at": "2025-12-28T10:00:00Z",
          "updated_at": "2025-12-28T10:00:00Z"
        }
      }
    }
  ],
  "suggestions": [
    "Would you like to add more todos?",
    "Show me all your tasks"
  ]
}
```

**Response Fields**:
| Field | Type | Description |
|-------|------|-------------|
| `message` | string | AI's natural language response |
| `thread_id` | UUID | Conversation thread ID (for multi-turn) |
| `actions_taken` | array | Tools executed by agent |
| `suggestions` | array | Suggested follow-up messages |

### Action Object
```json
{
  "tool": "create_todo",
  "description": "Human-readable description of action",
  "result": {
    "success": boolean,
    "todo": { ... } | null,
    "todos": [ ... ] | null,
    "deleted_id": number | null,
    "error": string | null
  }
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Message is required"
}
```

### 401 Unauthorized
```json
{
  "error": "Not authenticated. Please sign in."
}
```

### 408 Request Timeout
```json
{
  "error": "Request timed out. Please try again."
}
```

### 429 Too Many Requests
```json
{
  "error": "Too many requests. Please wait a moment before trying again."
}
```

### 500 Internal Error
```json
{
  "error": "Something went wrong. Please try again."
}
```

---

## Intent Detection Examples

| User Message | Detected Intent | Parameters |
|---------------|-----------------|------------|
| "Add a task to buy milk" | `create_todo` | title: "Buy milk" |
| "Show me my todos" | `list_todos` | - |
| "I finished buying milk" | `toggle_complete` | Needs clarification |
| "Change task 1 to new title" | `update_todo` | todo_id: 1, title: "new title" |
| "Delete the first task" | `delete_todo` | Needs clarification |
| "What do I have?" | `list_todos` | - |

---

## Tool Responses

### create_todo
```json
{
  "tool": "create_todo",
  "result": {
    "success": true,
    "todo": {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "description": "Buy groceries",
      "is_complete": false
    }
  }
}
```

### list_todos
```json
{
  "tool": "list_todos",
  "result": {
    "success": true,
    "todos": [
      {
        "id": "660e8400-e29b-41d4-a716-446655440001",
        "description": "Buy groceries",
        "is_complete": false
      }
    ],
    "count": 1
  }
}
```

### toggle_todo_complete
```json
{
  "tool": "toggle_todo_complete",
  "result": {
    "success": true,
    "todo": {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "description": "Buy groceries",
      "is_complete": true
    }
  }
}
```

### delete_todo
```json
{
  "tool": "delete_todo",
  "result": {
    "success": true,
    "deleted_id": 1
  }
}
```

---

## Multi-Turn Conversation Example

### Request 1: New conversation
```json
POST /api/chat
{
  "message": "Add a task"
}
```

Response:
```json
{
  "message": "What would you like the task to be?",
  "thread_id": "770e8400-e29b-41d4-a716-446655440000",
  "actions_taken": [],
  "suggestions": []
}
```

### Request 2: Continue conversation
```json
POST /api/chat
{
  "message": "to buy milk",
  "thread_id": "770e8400-e29b-41d4-a716-446655440000"
}
```

Response:
```json
{
  "message": "I've created: 'Buy milk'",
  "thread_id": "770e8400-e29b-41d4-a716-446655440000",
  "actions_taken": [...],
  "suggestions": ["Add another task", "Show my todos"]
}
```

---

## Rate Limiting

| Plan | Requests/minute |
|------|-----------------|
| Default | 30 |

**429 Response** includes `Retry-After` header.

---

## Webhook/Streaming (Not in Phase III)

Phase III uses request/response pattern only. Future phases may add:
- Server-Sent Events (SSE)
- WebSocket for real-time
