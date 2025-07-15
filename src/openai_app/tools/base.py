"""
Base classes and interfaces for tools.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from agents.tool import function_tool


class BaseTool(ABC):
    """Base class for all tools in the application."""
    
    def __init__(self, name: str, description: str):
        self._name = name
        self._description = description
    
    @property
    def name(self) -> str:
        """Tool name (must be unique)"""
        return self._name
    
    @property
    def description(self) -> str:
        """What this tool does"""
        return self._description
    
    @property
    @abstractmethod
    def parameters(self) -> Dict[str, Any]:
        """JSON schema for tool parameters"""
        pass
    
    @abstractmethod
    async def execute(self, **kwargs) -> str:
        """Execute the tool with given parameters."""
        pass
    
    def execute_sync(self, **kwargs) -> str:
        """Sync execution method for function tools"""
        import asyncio
        try:
            return asyncio.run(self.execute(**kwargs))
        except RuntimeError:
            # If there's already an event loop running
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, self.execute(**kwargs))
                return future.result()
    
    @abstractmethod
    def get_function_tool(self):
        """Return the function_tool decorated version of this tool."""
        pass
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"
    
    def __repr__(self) -> str:
        return self.__str__()
