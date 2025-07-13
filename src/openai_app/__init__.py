"""
OpenAI App - Professional AI Assistant Application.

A modern, well-structured AI application using OpenAI agents with proper
configuration management, logging, and professional architecture.
"""

__version__ = "0.1.0"
__author__ = "ShazilK47"

from .main import main, start
from .services import app_service, agent_service
from .config import settings
from .core import agent_factory, model_provider
from .tools import tool_registry

__all__ = [
    "main",
    "start", 
    "app_service",
    "agent_service",
    "settings",
    "agent_factory",
    "model_provider", 
    "tool_registry",
]
