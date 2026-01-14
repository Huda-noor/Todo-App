# API Contract: Chat Endpoint

**Feature**: Phase III - Conversational AI Interface
**Version**: 1.0.0
**Date**: 2026-01-10

---

## Endpoint: POST /api/chat

### Description

Accepts natural language messages from authenticated users and returns AI-generated responses. The system interprets user intent and manages todos through conversational interaction.

### Authentication

**Required**: Yes (reuses Phase II Better Auth)

**Mechanism**: Session cookie or Bearer token

**Headers**:
```
Authorization: Bearer {token}
```
or
```
Cookie: session={session_id}
```

---

## Request

### Method

`POST`

### Path

`/api/chat`

### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| Authorization | string | Yes* | Bearer token (if using token auth) |
| Content-Type | string | Yes | application/json |

\* Either Authorization header or session cookie is required, not both.

### Body

```json
{
  "message": "string (required)",
  "thread_id": "string (optional)"
}
```

### Fields

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| message | string | Yes | 1-1000 characters | User's natural language message |
| thread_id | string | No | UUID format | Existing conversation thread ID (omit for new conversation) |

### Validation Rules

- `message` must be non-empty
- `message` must not exceed 1000 characters
- `thread_id` (if provided) must be valid UUID format
- `thread_id` (if provided) must belong to authenticated user

---

## Response

### Success (HTTP 200)

```json
{
  "message": "string",
  "thread_id": "string",
  "actions_taken": [
    {
      "tool": "string",
      "description": "string"
    }
  ],
  "suggestions": [
    "string"
  ]
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| message | string | AI agent's natural language response to the user |
| thread_id | string | UUID of the conversation thread (for continuation) |
| actions_taken | array | List of tool actions performed during processing |
| actions_taken[].tool | string | Name of the tool that was called |
| actions_taken[].description | string | Human-readable description of the action |
| suggestions | array | Optional follow-up suggestions for the user |

### Example Response

```json
{
  "message": "I've created a new todo: 'Buy milk'",
  "thread_id": "550e8400-e29b-41d4-a716-446655440000",
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

## Error Responses

### 400 Bad Request

**Causes**: Invalid request body, missing required fields, invalid thread_id

**Response**:
```json
{
  "error": "Invalid request: 'message' is required"
}
```

### 401 Unauthorized

**Causes**: Missing or invalid authentication

**Response**:
```json
{
  "error": "Authentication required"
}
```

### 403 Forbidden

**Causes**: User does not own the specified thread

**Response**:
```json
{
  "error": "Access denied to conversation thread"
}
```

### 429 Too Many Requests

**Causes**: Rate limit exceeded

**Response**:
```json
{
  "error": "Rate limit exceeded, please try again later"
}
```

**Response Headers**:
```
Retry-After: 30
```

### 500 Internal Server Error

**Causes**: Unexpected server error

**Response**:
```json
{
  "error": "Internal error processing request"
}
```

---

## Usage Examples

### Example 1: Create Todo (New Conversation)

**Request**:
```bash
POST /api/chat
Content-Type: application/json
Authorization: Bearer {token}

{
  "message": "Add a task to buy milk"
}
```

**Response**:
```json
{
  "message": "I've created a new todo: 'Buy milk'",
  "thread_id": "550e8400-e29b-41d4-a716-446655440000",
  "actions_taken": [
    {
      "tool": "create_todo",
      "description": "Created todo with title 'Buy milk'"
    }
  ],
  "suggestions": []
}
```

---

### Example 2: List Todos (Continue Conversation)

**Request**:
```bash
POST /api/chat
Content-Type: application/json
Authorization: Bearer {token}

{
  "message": "Show me my tasks",
  "thread_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response**:
```json
{
  "message": "You have 1 task:\n1. Buy milk",
  "thread_id": "550e8400-e29b-41d4-a716-446655440000",
  "actions_taken": [
    {
      "tool": "list_todos",
      "description": "Listed all todos"
    }
  ],
  "suggestions": []
}
```

---

### Example 3: Mark Complete (Multi-Turn)

**Request 1**:
```json
{
  "message": "I finished buying milk",
  "thread_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response 1**:
```json
{
  "message": "Marked 'Buy milk' as complete",
  "thread_id": "550e8400-e29b-41d4-a716-446655440000",
  "actions_taken": [
    {
      "tool": "toggle_todo_complete",
      "description": "Marked todo as complete"
    }
  ],
  "suggestions": []
}
```

---

### Example 4: Delete with Confirmation

**Request 1**:
```json
{
  "message": "Delete 'Buy milk'",
  "thread_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response 1**:
```json
{
  "message": "Are you sure you want to delete 'Buy milk'? (yes/no)",
  "thread_id": "550e8400-e29b-41d4-a716-446655440000",
  "actions_taken": [],
  "suggestions": []
}
```

**Request 2**:
```json
{
  "message": "yes",
  "thread_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response 2**:
```json
{
  "message": "Deleted 'Buy milk'",
  "thread_id": "550e8400-e29b-41d4-a716-446655440000",
  "actions_taken": [
    {
      "tool": "delete_todo",
      "description": "Deleted todo"
    }
  ],
  "suggestions": []
}
```

---

### Example 5: Clarification Required

**Request**:
```json
{
  "message": "I'm done with that",
  "thread_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response**:
```json
{
  "message": "Which todo would you like to mark as done? You have: 1) Buy milk",
  "thread_id": "550e8400-e29b-41d4-a716-446655440000",
  "actions_taken": [],
  "suggestions": []
}
```

---

## Rate Limiting

- **Limit**: 30 requests per minute per user
- **Window**: Sliding window algorithm
- **Key**: `user_id` from authentication

**Response on Rate Limit**:
- HTTP Status: 429
- `Retry-After` header: Seconds to wait

---

## Security Considerations

1. **Authentication**: All requests require valid authentication
2. **Authorization**: Users can only access their own conversations
3. **Input Validation**: Message length and content validated
4. **Thread Ownership**: Thread IDs verified against authenticated user
5. **Error Obfuscation**: Generic errors to prevent information leakage

---

## Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| Simple requests (no tools) | <3 seconds |
| Tool calls | +1-2 seconds per tool |
| Complex requests (multiple tools) | <5 seconds |
| Maximum latency | <10 seconds |
| Message length | 1-1000 characters |
| Conversation depth | Unlimited (append-only) |

---

## Testing

### Unit Tests
- Validate request parsing
- Validate authentication handling
- Validate conversation thread creation/loading

### Integration Tests
- Test full request lifecycle with database
- Test multi-turn conversations
- Test all five todo operations via chat

### Contract Tests
- Verify request/response schema
- Verify error responses
- Verify HTTP status codes

---

**Status**: Ready for implementation
