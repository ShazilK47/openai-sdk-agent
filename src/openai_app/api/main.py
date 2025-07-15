"""
FastAPI main application module.

This is the entry point for the FastAPI web server that provides
HTTP API endpoints for the AI agent functionality.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
from typing import Dict, Any
import logging

from ..config.settings import settings
from ..config.logging import configure_logging
from .routes.health import router as health_router
from .routes.chat import router as chat_router
from .routes.tools import router as tools_router

# Setup logging
configure_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting AI Agent API server...")
    logger.info(f"API Documentation available at: /docs")
    yield
    # Shutdown
    logger.info("Shutting down AI Agent API server...")

# Create FastAPI application
app = FastAPI(
    title="AI Agent API",
    description="Backend API for the AI Agent with tool capabilities",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc documentation
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js development server
        "http://127.0.0.1:3000",  # Alternative localhost
        "http://localhost:5173",  # Vite development server
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router, prefix="/api", tags=["Health"])
app.include_router(chat_router, prefix="/api", tags=["Chat"])
app.include_router(tools_router, prefix="/api", tags=["Tools"])

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors"""
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Root endpoint
@app.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint with API information"""
    return {
        "message": "AI Agent API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }

def run_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = True):
    """Run the FastAPI server"""
    uvicorn.run(
        "openai_app.api.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )

if __name__ == "__main__":
    run_server()
