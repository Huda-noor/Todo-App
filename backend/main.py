from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from src.config.logging_config import setup_logging
from src.routers import chat
from src.middleware.error_handler import ErrorHandlerMiddleware
from src.db.database import engine
from src.models.conversation_thread import ConversationThread, ConversationMessage


# Set up logging
setup_logging()

# Create FastAPI app
app = FastAPI(
    title="AI Conversational Todo Interface",
    description="API for managing todos through natural language conversation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom error handler middleware
app.add_middleware(ErrorHandlerMiddleware)

# Include routers
app.include_router(chat.router)

# Create database tables
from sqlmodel import SQLModel
@app.on_event("startup")
def on_startup():
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully.")


@app.get("/")
def read_root():
    return {"message": "AI Conversational Todo Interface - Phase III", "status": "running"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "conversational-todo-api"}


# Initialize MCP server if needed
def initialize_mcp_server():
    """
    Initialize the MCP server to serve the tools.
    This would typically run in a separate process.
    """
    pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("SERVER_HOST", "0.0.0.0"),
        port=int(os.getenv("SERVER_PORT", 8000)),
        reload=True
    )