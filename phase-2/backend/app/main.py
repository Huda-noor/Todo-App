"""FastAPI application entry point."""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title="Phase II Todo API",
    description="RESTful API for the Phase II Full-Stack Todo Web Application",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler for consistent error responses
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions with consistent error format."""
    return JSONResponse(
        status_code=500,
        content={"error": "An unexpected error occurred. Please try again."}
    )


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Import and register routers
from app.routers import auth, todos
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(todos.router, prefix="/api/todos", tags=["Todos"])
