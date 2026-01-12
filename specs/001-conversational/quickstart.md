# Quickstart: Phase III - Conversational AI Interface

**Feature**: Phase III - Conversational AI Interface
**Date**: 2026-01-10
**Prerequisites**: Phase II backend deployed and operational

---

## Overview

Phase III adds a conversational AI interface to the existing Todo application. This quickstart guide demonstrates how to interact with the new chat endpoint to manage todos using natural language.

---

## Setup

### 1. Environment Configuration

Add the following environment variables to your backend environment:

```bash
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o  # or gpt-4o-mini for cost savings

# Database (reuse Phase II configuration)
DATABASE_URL=postgresql://user:password@host:port/database
```

### 2. Install Dependencies

```bash
# Install Phase III dependencies
pip install openai
pip install mcp

# Note: FastAPI, SQLModel, and other Phase II dependencies already installed
```

### 3. Run Database Migration

```bash
# Apply the conversation tables migration
python -m alembic upgrade head
```

### 4. Start the Backend

```bash
# Start the FastAPI server (same as Phase II)
uvicorn backend.main:app --reload
```

---

## Authentication

The chat endpoint requires authentication. Use the same authentication method as Phase II (Better Auth session/token).

**Example**: Include the authentication cookie or token in your HTTP request.

---

## Using the Chat Endpoint

### Endpoint

```
POST /api/chat
```

### Request Format

```json
{
  "message": "Add a task to buy milk",
  "thread_id": "optional-existing-thread-uuid"
}
```

### Response Format

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

## Example Interactions

### Create a Todo

**Request**:
```json
{
  "message": "Add a task to buy groceries"
}
```

**Response**:
```json
{
  "message": "I've created a new todo: 'Buy groceries'",
  "thread_id": "550e8400-e29b-41d4-a716-446655440000",
  "actions_taken": [
    {
      "tool": "create_todo",
      "description": "Created todo with title 'Buy groceries'"
    }
  ],
  "suggestions": []
}
```

---

### List Todos

**Request**:
```json
{
  "message": "Show me my tasks",
  "thread_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response**:
```json
{
  "message": "You have 1 task:\n1. Buy groceries",
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

### Mark Todo Complete

**Request**:
```json
{
  "message": "I finished buying groceries",
  "thread_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response**:
```json
{
  "message": "Marked 'Buy groceries' as complete",
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

### Update Todo

**Request**:
```json
{
  "message": "Change 'Buy groceries' to 'Buy milk and eggs'",
  "thread_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response**:
```json
{
  "message": "Updated the task to: 'Buy milk and eggs'",
  "thread_id": "550e8400-e29b-41d4-a716-446655440000",
  "actions_taken": [
    {
      "tool": "update_todo",
      "description": "Updated todo title"
    }
  ],
  "suggestions": []
}
```

---

### Delete Todo (Requires Confirmation)

**Request 1**:
```json
{
  "message": "Delete the grocery task",
  "thread_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response 1**:
```json
{
  "message": "Are you sure you want to delete 'Buy milk and eggs'? (yes/no)",
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
  "message": "Deleted 'Buy milk and eggs'",
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

### Clarification Example

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
  "message": "Which todo would you like to mark as done? You have: 1) Buy milk and eggs",
  "thread_id": "550e8400-e29b-41d4-a716-446655440000",
  "actions_taken": [],
  "suggestions": []
}
```

---

## Error Handling

### Authentication Failed (401)

**Response**:
```json
{
  "error": "Authentication required"
}
```

### Invalid Request (400)

**Response**:
```json
{
  "error": "Invalid request: 'message' is required"
}
```

### Rate Limit Exceeded (429)

**Response**:
```json
{
  "error": "Rate limit exceeded, please try again later"
}
```

---

## Testing with cURL

### Create a Todo

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Cookie: your_auth_session_here" \
  -d '{"message": "Add a task to buy milk"}'
```

### Continue Conversation

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Cookie: your_auth_session_here" \
  -d '{"message": "Show me my tasks", "thread_id": "your-thread-id-here"}'
```

---

## Testing with Python

```python
import requests

# Configuration
BASE_URL = "http://localhost:8000"
AUTH_COOKIE = "your_auth_session_here"

# Create a todo
response = requests.post(
    f"{BASE_URL}/api/chat",
    json={"message": "Add a task to buy milk"},
    cookies={"session": AUTH_COOKIE}
)
print(response.json())

# Continue conversation with thread_id
thread_id = response.json()["thread_id"]
response = requests.post(
    f"{BASE_URL}/api/chat",
    json={
        "message": "Show me my tasks",
        "thread_id": thread_id
    },
    cookies={"session": AUTH_COOKIE}
)
print(response.json())
```

---

## Common Patterns

### Start a New Conversation

Omit the `thread_id` parameter:

```json
{
  "message": "Add a task to call mom"
}
```

### Continue an Existing Conversation

Include the `thread_id` from the previous response:

```json
{
  "message": "Change 'call mom' to 'call mom tomorrow'",
  "thread_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Handle Clarifications

The agent may ask for clarification. Provide the requested information:

```
User: "Delete the task"
Agent: "Which task would you like to delete?"
User: "The one about groceries"
```

---

## Troubleshooting

### "Authentication required" (401)
- Ensure you're including valid authentication cookie or token
- Check that Phase II authentication is working correctly

### "Conversation thread not found" (400)
- Verify the `thread_id` belongs to your user account
- Check that the thread hasn't been deleted

### "Rate limit exceeded" (429)
- Wait before sending another message
- Check your rate limit configuration

### Tool Execution Errors
- The agent will explain the error in the response message
- Try rephrasing your request or providing more information

---

## Next Steps

- Review the full [specification](./spec.md) for detailed requirements
- Review the [implementation plan](./plan.md) for architecture details
- Review the [data model](./data-model.md) for database schema
- Run `/sp.tasks` to generate implementation tasks

---

**Status**: Ready for testing and implementation
