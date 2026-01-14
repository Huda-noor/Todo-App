# Quickstart Guide: AI Conversational Todo Interface (Phase III)

## Overview
This guide provides a quick introduction to setting up and running the AI Conversational Todo Interface (Phase III) for development and testing purposes.

## Prerequisites

### System Requirements
- Python 3.11+
- PostgreSQL (or Neon PostgreSQL connection)
- OpenAI API key
- MCP SDK installed

### Environment Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## Configuration

### Environment Variables
Create a `.env` file with the following variables:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini  # Recommended model

# Database Configuration
DATABASE_URL=postgresql://username:password@host:port/database_name
NEON_DATABASE_URL=your_neon_postgresql_connection_string

# Phase II Authentication (reuse existing)
PHASE_II_AUTH_SECRET=your_phase_ii_auth_secret

# Application Settings
APP_ENV=development  # or production
LOG_LEVEL=INFO
```

### Database Setup
1. Run migrations to create the new conversation tables:
   ```bash
   python -m scripts.db_migrate
   ```
   
   This will create the `conversation_thread` and `conversation_message` tables while preserving existing Phase II tables.

## Running the Application

### Development Mode
```bash
# Start the backend server
python -m backend.main

# The chat endpoint will be available at:
# POST http://localhost:8000/api/v1/chat/converse
```

### Using the Chat API
Once the server is running, you can interact with the chat API:

#### Example Request
```bash
curl -X POST http://localhost:8000/api/v1/chat/converse \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_PHASE_II_SESSION_TOKEN" \
  -d '{
    "message": "Add a task to buy groceries",
    "thread_id": null
  }'
```

#### Example Response
```json
{
  "response": "I've created a new todo: 'Buy groceries'",
  "thread_id": "770e8400-e29b-41d4-a716-446655440000",
  "actions_taken": [
    {
      "tool": "create_todo",
      "description": "Created todo with title 'Buy groceries'",
      "result": {
        "success": true,
        "todo_id": "660e8400-e29b-41d4-a716-446655440001"
      }
    }
  ],
  "suggestions": [
    "Would you like to add more todos?",
    "Show me all your tasks"
  ]
}
```

## Key Components

### 1. Chat Endpoint (`/api/v1/chat/converse`)
- Entry point for all conversational interactions
- Handles authentication using Phase II tokens
- Manages conversation threading and persistence

### 2. AI Agent (`/backend/src/agents/todo_agent.py`)
- Interprets natural language using OpenAI
- Determines intent and selects appropriate tools
- Generates natural language responses

### 3. MCP Tools (`/backend/src/mcp/tools.py`)
- `create_todo`: Creates new todo items
- `list_todos`: Retrieves existing todo items
- `update_todo`: Updates existing todo items
- `delete_todo`: Removes todo items
- `toggle_todo_completion`: Marks todos as complete/incomplete

## Testing

### Unit Tests
```bash
# Run all unit tests
pytest tests/unit/

# Run specific test module
pytest tests/unit/test_chat_endpoint.py
```

### Integration Tests
```bash
# Run integration tests
pytest tests/integration/

# Test the full conversation flow
pytest tests/integration/test_conversation_flow.py
```

### Contract Tests
```bash
# Verify API contracts
pytest tests/contract/
```

## Development Workflow

### Adding New Features
1. Create a new branch: `git checkout -b feature/new-feature-name`
2. Update the data models if needed
3. Implement the new functionality
4. Write tests for the new functionality
5. Run all tests to ensure nothing is broken
6. Submit a pull request

### Running Linters
```bash
# Check code style
flake8 .
black --check .

# Format code
black .
```

## Troubleshooting

### Common Issues

#### Issue: "Invalid authentication token"
**Solution**: Ensure you're using a valid Phase II session token in the Authorization header.

#### Issue: "Database connection failed"
**Solution**: Verify your DATABASE_URL is correct and the database is accessible.

#### Issue: "OpenAI API error"
**Solution**: Check that your OPENAI_API_KEY is valid and you have sufficient quota.

#### Issue: "Tool execution failed"
**Solution**: Check the application logs for specific error details. Verify database connectivity and permissions.

### Debugging Tips
- Enable DEBUG logging by setting LOG_LEVEL=DEBUG in your .env
- Check the application logs for detailed error messages
- Use the test suite to isolate specific functionality issues

## API Reference

### Chat Endpoint
- **Method**: POST
- **Path**: `/api/v1/chat/converse`
- **Auth**: Bearer token (Phase II session)
- **Request Body**:
  ```json
  {
    "message": "string",
    "thread_id": "string (optional)"
  }
  ```
- **Response**:
  ```json
  {
    "response": "string",
    "thread_id": "string",
    "actions_taken": "array",
    "suggestions": "array"
  }
  ```

## Next Steps

1. Explore the full API documentation in the `/docs` directory
2. Review the test suite to understand expected behaviors
3. Check out the architecture documentation in the `plan.md` file
4. Look at the data models in `data-model.md` for database schema details
5. Review the contracts in the `/contracts` directory for API specifications