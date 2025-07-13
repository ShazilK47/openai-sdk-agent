"""
Base classes and interfaces for tools.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from agents.tool import function_tool


class BaseTool(ABC):
    """Base class for all tools in the application."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    async def execute(self, **kwargs) -> str:
        """Execute the tool with given parameters."""
        pass
    
    @abstractmethod
    def get_function_tool(self):
        """Return the function_tool decorated version of this tool."""
        pass
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"
    
    def __repr__(self) -> str:
        return self.__str__()
