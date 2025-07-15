"""
Health check API routes.

Provides endpoints for monitoring the health and status
of the AI agent API service.
"""

from fastapi import APIRouter
from typing import Dict, Any
import psutil
import os
from datetime import datetime

from ...config.settings import settings

router = APIRouter()


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint to verify the API is running properly.
    
    Returns:
        Dict containing health status, version, and system information
    """
    return {
        "status": "healthy",
        "message": "AI Agent API is running",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "environment": {
            "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
            "log_level": settings.log_level,
        }
    }


@router.get("/health/detailed")
async def detailed_health_check() -> Dict[str, Any]:
    """
    Detailed health check with system metrics.
    
    Returns:
        Dict containing detailed system health information
    """
    # Get system information
    memory = psutil.virtual_memory()
    cpu_percent = psutil.cpu_percent(interval=1)
    
    return {
        "status": "healthy",
        "message": "AI Agent API is running",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "system": {
            "cpu_usage_percent": cpu_percent,
            "memory": {
                "total_mb": round(memory.total / 1024 / 1024, 2),
                "available_mb": round(memory.available / 1024 / 1024, 2),
                "used_percent": memory.percent
            },
            "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
        },
        "configuration": {
            "log_level": settings.log_level,
            "gemini_api_configured": bool(settings.gemini_api_key),
            "weather_api_configured": bool(settings.weather_api_key),
            "tavily_api_configured": bool(settings.tavily_api_key),
        }
    }
