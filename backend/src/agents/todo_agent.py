from openai import OpenAI
import os
from typing import Dict, Any, List
import json


class TodoAgent:
    """
    AI Agent for handling todo management through natural language.
    Uses OpenAI GPT-4o-mini model and function calling to interact with todo operations.
    """

    def __init__(self):
        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        # System prompt defining the agent's behavior
        self.system_prompt = """
        You are a helpful todo assistant. You help users manage their todo list through natural language conversation.

        You can perform these operations:
        1. Create new todos
        2. List existing todos
        3. Update existing todos
        4. Delete todos
        5. Mark todos as complete/incomplete

        Follow these rules:
        1. Always use the appropriate function to perform operations
        2. Ask for clarification if the user's intent is ambiguous
        3. Confirm destructive actions (like deletion) before executing them
        4. Maintain context across conversation turns
        5. Respond in a friendly, helpful tone
        6. If you cannot understand the request, politely ask for clarification
        """

    def run_conversation(self, messages: List[Dict[str, str]], user_id: str) -> Dict[str, Any]:
        """
        Run a conversation with the agent.

        Args:
            messages: List of messages in the conversation (with role and content)
            user_id: ID of the authenticated user

        Returns:
            Dictionary with response, actions taken, and suggestions
        """
        # Add system prompt to the beginning of the messages
        full_messages = [
            {"role": "system", "content": self.system_prompt}
        ]

        # Add context about the user to the first user message
        if messages and messages[0]["role"] == "user":
            # Prepend user ID context to the first user message
            messages[0]["content"] = f"[CONTEXT] User ID: {user_id}[/CONTEXT]\n\n{messages[0]['content']}"

        full_messages.extend(messages)

        # Call the OpenAI API with function calling
        response = self.openai_client.chat.completions.create(
            model=self.model,
            messages=full_messages,
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "create_todo",
                        "description": "Create a new todo item",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "user_id": {"type": "string", "description": "User ID"},
                                "title": {"type": "string", "description": "Title of the todo"},
                                "description": {"type": "string", "description": "Description of the todo"},
                                "due_date": {"type": "string", "description": "Due date in ISO 8601 format (optional)"}
                            },
                            "required": ["user_id", "title"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "list_todos",
                        "description": "Retrieve todo items",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "user_id": {"type": "string", "description": "User ID"},
                                "filter": {"type": "string", "description": "Filter criteria (all, completed, pending, today, etc.)"}
                            },
                            "required": ["user_id"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "update_todo",
                        "description": "Update an existing todo item",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "user_id": {"type": "string", "description": "User ID"},
                                "todo_id": {"type": "string", "description": "ID of the todo to update"},
                                "title": {"type": "string", "description": "New title for the todo (optional)"},
                                "description": {"type": "string", "description": "New description for the todo (optional)"},
                                "completed": {"type": "boolean", "description": "New completion status (optional)"}
                            },
                            "required": ["user_id", "todo_id"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "delete_todo",
                        "description": "Delete an existing todo item",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "user_id": {"type": "string", "description": "User ID"},
                                "todo_id": {"type": "string", "description": "ID of the todo to delete"}
                            },
                            "required": ["user_id", "todo_id"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "toggle_todo_completion",
                        "description": "Mark a todo as complete/incomplete",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "user_id": {"type": "string", "description": "User ID"},
                                "todo_id": {"type": "string", "description": "ID of the todo to update"},
                                "completed": {"type": "boolean", "description": "New completion status"}
                            },
                            "required": ["user_id", "todo_id", "completed"]
                        }
                    }
                }
            ],
            tool_choice="auto"
        )

        # Process the response
        assistant_message = response.choices[0].message
        actions_taken = []
        response_text = ""

        if assistant_message.content:
            response_text = assistant_message.content

        if assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                # Execute the tool call by recording it
                function_name = tool_call.function.name
                try:
                    arguments = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    # If JSON parsing fails, skip this tool call
                    continue

                # Add user_id to arguments if not present
                if "user_id" not in arguments:
                    arguments["user_id"] = user_id

                # In a real implementation, we would execute the actual function here
                # For now, we'll just record the action for the response
                actions_taken.append({
                    "tool": function_name,
                    "arguments": arguments,
                    "result": "executed"
                })

        # Generate suggestions for follow-up actions
        suggestions = self._generate_suggestions(response_text)

        return {
            "response": response_text,
            "actions_taken": actions_taken,
            "suggestions": suggestions
        }

    def _generate_suggestions(self, response_text: str) -> List[str]:
        """
        Generate suggestions for follow-up actions based on the response.
        """
        # Simple suggestion generation based on common patterns
        suggestions = []

        if "created" in response_text.lower() or "added" in response_text.lower():
            suggestions.extend([
                "Show me my todos",
                "Add another task",
                "What else should I do?"
            ])
        elif "deleted" in response_text.lower() or "removed" in response_text.lower():
            suggestions.extend([
                "Show me my remaining todos",
                "Add a new task",
                "Mark another task as done"
            ])
        elif "completed" in response_text.lower() or "done" in response_text.lower():
            suggestions.extend([
                "Show me what's left to do",
                "Add a new task",
                "Delete completed tasks"
            ])
        else:
            suggestions.extend([
                "Show me my todos",
                "Add a new task",
                "Mark a task as complete"
            ])

        return suggestions[:3]  # Return only the first 3 suggestions


# Create a global instance of the agent
todo_agent = TodoAgent()