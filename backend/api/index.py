"""
Deployment Handler for Hugging Face Spaces and Vercel

This file wraps the FastAPI application to support both:
- Hugging Face Spaces (using gradio for the demo interface)
- Vercel Serverless Functions
"""

import os
import sys
from typing import Any

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.middleware.wsgi import WSGIMiddleware

# Import app after adding path
from app.main import app as fastapi_app
from app.config import get_settings

settings = get_settings()

# Create a new app for deployment
deployment_app = FastAPI(
    title="Phase II Todo API",
    description="RESTful API for the Phase II Full-Stack Todo Web Application",
    version="1.0.0",
)

# Configure CORS - allow Vercel frontend, Hugging Face Space, and localhost
cors_origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://frontend-jei1yp699-huda-noors-projects.vercel.app",
    "https://*.vercel.app",
    "https://huda11noor-todo-backend.hf.space",
    "https://*.hf.space",
]

deployment_app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers from the original app
deployment_app.include_router(fastapi_app.router, prefix="")

# Health check
@deployment_app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# =====================
# Vercel Handler
# =====================
def vercel_handler(request: Request) -> Any:
    """Handle requests for Vercel serverless functions."""
    return deployment_app(request)


# =====================
# Hugging Face Spaces Handler
# =====================
try:
    import gradio

    # Create a Gradio interface for the API
    def create_gradio_interface():
        """Create a simple demo interface for Hugging Face Spaces."""
        import json

        def query_api(endpoint: str, method: str = "GET", body: str = "{}") -> str:
            """Query the API from Gradio."""
            import httpx

            base_url = os.environ.get("HF_API_URL", "http://localhost:8000")
            url = f"{base_url}{endpoint}"

            try:
                if method.upper() == "GET":
                    resp = httpx.get(url, timeout=30.0)
                else:
                    resp = httpx.request(method, url, content=body, timeout=30.0)

                return json.dumps(resp.json(), indent=2)
            except Exception as e:
                return f"Error: {str(e)}"

        with gr.Blocks(title="Todo API") as demo:
            gr.Markdown("# Phase II Todo API")
            gr.Markdown("Backend API for the Todo Application")

            with gr.Tab("Health Check"):
                if endpoint := gr.Textbox(value="/health", label="Endpoint"):
                    result = gr.Code(label="Result", language="json")

            gr.Button("Query", onclick=lambda: query_api("/health")).click(
                fn=lambda: query_api("/health"),
                outputs=result,
            )

        return demo

    # Create the Gradio demo
    gradio_app = create_gradio_interface()

    # Mount the Gradio app
    deployment_app.mount("/gradio", WSGIMiddleware(gradio_app.queue().app))

except ImportError:
    pass


# =====================
# Standalone Server Entry Point
# =====================
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(
        "api.index:deployment_app",
        host="0.0.0.0",
        port=port,
        reload=False,
    )
