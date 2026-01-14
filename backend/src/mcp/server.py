from mcp.server.fastmcp import FastMCP
from .tools import create_todo, list_todos, update_todo, delete_todo, toggle_todo_completion


# Create MCP server instance
mcp_server = FastMCP(
    tools=[
        create_todo,
        list_todos,
        update_todo,
        delete_todo,
        toggle_todo_completion
    ]
)


# Run the server
if __name__ == "__main__":
    import uvicorn
    import os
    
    uvicorn.run(
        "mcp_server:mcp_server.app",  # This would be the actual FastAPI app inside the FastMCP
        host=os.getenv("MCP_SERVER_HOST", "0.0.0.0"),
        port=int(os.getenv("MCP_SERVER_PORT", 8001)),
        reload=True
    )