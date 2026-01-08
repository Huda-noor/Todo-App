"""
Vercel Python Runtime Handler

This file is the entry point for Vercel's Python runtime.
It wraps the FastAPI application to handle Vercel's request format.
"""

import os
import sys
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import app after adding path
from app.main import app as fastapi_app
from app.config import get_settings

settings = get_settings()

# Create a new app for Vercel
vercel_app = FastAPI(
    title="Phase II Todo API",
    description="RESTful API for the Phase II Full-Stack Todo Web Application",
    version="1.0.0",
)

# Configure CORS
vercel_app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers from the original app
vercel_app.include_router(fastapi_app.router, prefix="")

# Health check
@vercel_app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Vercel handler function
def handler(request: Request):
    """Handle requests for Vercel."""
    return vercel_app(request)
