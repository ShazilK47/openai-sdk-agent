"""
Custom exceptions for the application.
"""


class OpenAIAppError(Exception):
    """Base exception for the application."""
    pass


class ModelError(OpenAIAppError):
    """Model-related errors."""
    pass


class AgentError(OpenAIAppError):
    """Agent-related errors."""
    pass


class ToolError(OpenAIAppError):
    """Tool-related errors."""
    pass


class ConfigurationError(OpenAIAppError):
    """Configuration-related errors."""
    pass


class APIError(OpenAIAppError):
    """API-related errors."""
    pass
