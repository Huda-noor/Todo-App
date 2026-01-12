# Phase II - REST API Contract

## Base URL
- **Development**: `http://localhost:8000/api`
- **Production**: `https://api.example.com/api`

## Authentication
All endpoints (except signup/signin) require authentication via session cookie:
```
Cookie: better-auth.session_token={session_token}
```

---

## Authentication Endpoints

### POST /api/auth/signup
Create a new user account.

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Success Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "created_at": "2025-12-28T10:00:00Z"
}
```

**Error Responses**:
- 400 Bad Request: `{"error": "Invalid email format"}`
- 400 Bad Request: `{"error": "Password must be at least 8 characters"}`
- 409 Conflict: `{"error": "An account with this email already exists"}`

---

### POST /api/auth/signin
Authenticate a user.

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Success Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "created_at": "2025-12-28T10:00:00Z"
}
```

**Set-Cookie**:
```
Set-Cookie: better-auth.session_token={token}; Path=/; HttpOnly; SameSite=Lax
```

**Error Responses**:
- 400 Bad Request: `{"error": "Email is required"}`
- 400 Bad Request: `{"error": "Password is required"}`
- 401 Unauthorized: `{"error": "Invalid email or password"}`

---

### POST /api/auth/signout
End the current session.

**Request**: (No body, uses cookie)

**Success Response** (200 OK):
```json
{
  "message": "Signed out successfully"
}
```

**Set-Cookie** (clear session):
```
Set-Cookie: better-auth.session_token=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT
```

**Error Responses**:
- 401 Unauthorized: `{"error": "Not authenticated"}`

---

### GET /api/auth/me
Get current authenticated user.

**Request**: (No body, uses cookie)

**Success Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "created_at": "2025-12-28T10:00:00Z"
}
```

**Error Responses**:
- 401 Unauthorized: `{"error": "Not authenticated"}`

---

## Todo Endpoints

### GET /api/todos
List all todos for the authenticated user.

**Request**: (No body, uses cookie)

**Success Response** (200 OK):
```json
{
  "todos": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "description": "Buy groceries",
      "is_complete": false,
      "created_at": "2025-12-28T10:00:00Z",
      "updated_at": "2025-12-28T10:00:00Z"
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440002",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "description": "Clean house",
      "is_complete": true,
      "created_at": "2025-12-28T11:00:00Z",
      "updated_at": "2025-12-28T12:00:00Z"
    }
  ],
  "count": 2
}
```

**Error Responses**:
- 401 Unauthorized: `{"error": "Not authenticated"}`

---

### POST /api/todos
Create a new todo.

**Request**:
```json
{
  "description": "Buy groceries"
}
```

**Success Response** (201 Created):
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440003",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "description": "Buy groceries",
  "is_complete": false,
  "created_at": "2025-12-28T10:00:00Z",
  "updated_at": "2025-12-28T10:00:00Z"
}
```

**Error Responses**:
- 400 Bad Request: `{"error": "Todo description cannot be empty"}`
- 400 Bad Request: `{"error": "Todo description cannot exceed 500 characters"}`
- 401 Unauthorized: `{"error": "Not authenticated"}`

---

### GET /api/todos/{id}
Get a single todo by ID.

**Request**: (No body)

**Success Response** (200 OK):
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "description": "Buy groceries",
  "is_complete": false,
  "created_at": "2025-12-28T10:00:00Z",
  "updated_at": "2025-12-28T10:00:00Z"
}
```

**Error Responses**:
- 401 Unauthorized: `{"error": "Not authenticated"}`
- 404 Not Found: `{"error": "Todo not found"}`

---

### PUT /api/todos/{id}
Update a todo's description.

**Request**:
```json
{
  "description": "Buy groceries and milk"
}
```

**Success Response** (200 OK):
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "description": "Buy groceries and milk",
  "is_complete": false,
  "created_at": "2025-12-28T10:00:00Z",
  "updated_at": "2025-12-28T11:00:00Z"
}
```

**Error Responses**:
- 400 Bad Request: `{"error": "Todo description cannot be empty"}`
- 400 Bad Request: `{"error": "Todo description cannot exceed 500 characters"}`
- 401 Unauthorized: `{"error": "Not authenticated"}`
- 404 Not Found: `{"error": "Todo not found"}`

---

### DELETE /api/todos/{id}
Delete a todo.

**Request**: (No body)

**Success Response** (200 OK):
```json
{
  "message": "Todo deleted successfully"
}
```

**Error Responses**:
- 401 Unauthorized: `{"error": "Not authenticated"}`
- 404 Not Found: `{"error": "Todo not found"}`

---

### PATCH /api/todos/{id}/toggle
Toggle a todo's completion status.

**Request**: (No body)

**Success Response** (200 OK):
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "description": "Buy groceries",
  "is_complete": true,
  "created_at": "2025-12-28T10:00:00Z",
  "updated_at": "2025-12-28T11:00:00Z"
}
```

**Error Responses**:
- 401 Unauthorized: `{"error": "Not authenticated"}`
- 404 Not Found: `{"error": "Todo not found"}`

---

## Health Check

### GET /health
Health check endpoint (no auth required).

**Success Response** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2025-12-28T10:00:00Z"
}
```

---

## HTTP Status Code Summary

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET, PUT, PATCH, DELETE |
| 201 | Created | Successful POST (resource created) |
| 400 | Bad Request | Validation errors |
| 401 | Unauthorized | Missing/invalid authentication |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Duplicate resource |
| 422 | Unprocessable Entity | Pydantic validation errors |
| 500 | Internal Server Error | Unexpected errors |

---

## Rate Limiting (Future Phase)
Not implemented in Phase II. Consider in future phases:
- 100 requests per minute per user
- 429 Too Many Requests response
