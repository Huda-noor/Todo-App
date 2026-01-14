import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from uuid import UUID
import sys
import os

# Add the backend/src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend', 'src'))

from main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_health_endpoint(client):
    """Test the health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "AI Conversational Todo Interface" in response.json()["message"]


@patch('src.middleware.auth.auth_middleware.get_current_user_id')
def test_chat_endpoint(mock_get_current_user_id, client):
    """Test the chat endpoint with mocked authentication."""
    # Mock the authentication to return a valid user ID
    mock_user_id = UUID("12345678-1234-5678-1234-567812345678")
    mock_get_current_user_id.return_value = mock_user_id
    
    # Mock the agent response
    with patch('src.agents.todo_agent.todo_agent.run_conversation') as mock_run_conversation:
        mock_run_conversation.return_value = {
            "response": "I've created a new todo: 'Buy groceries'",
            "actions_taken": [
                {
                    "tool": "create_todo",
                    "arguments": {"user_id": str(mock_user_id), "title": "Buy groceries"},
                    "result": "executed"
                }
            ],
            "suggestions": ["Show me my todos", "Add another task"]
        }
        
        # Make a request to the chat endpoint
        response = client.post(
            "/api/v1/chat/converse",
            json={"message": "Add a task to buy groceries"},
            headers={"Authorization": "Bearer fake-token"}
        )
        
        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert "Buy groceries" in data["response"]
        assert len(data["actions_taken"]) == 1
        assert data["actions_taken"][0]["tool"] == "create_todo"
        assert len(data["suggestions"]) >= 1


if __name__ == "__main__":
    pytest.main([__file__])