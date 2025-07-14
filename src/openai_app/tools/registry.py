"""
Tool registry for managing all available tools.
"""
from typing import Dict, List
from .base import BaseTool
from .weather import weather_tool
from .calculator import calculator_tool
from .search import search_tool
from ..config.logging import get_logger

logger = get_logger(__name__)


class ToolRegistry:
    """Registry for managing all available tools."""
    
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._quiet_mode = False
        self._initialized = False
    
    def set_quiet_mode(self, quiet: bool):
        """Set quiet mode for this registry."""
        self._quiet_mode = quiet
        if not self._initialized:
            self._register_default_tools()
    
    def _register_default_tools(self):
        """Register the default tools."""
        if self._initialized:
            return
            
        self.register_tool(weather_tool)
        self.register_tool(calculator_tool)
        self.register_tool(search_tool)
        if not self._quiet_mode:
            logger.info("Default tools registered", tool_count=len(self._tools))
        self._initialized = True
    
    def register_tool(self, tool: BaseTool):
        """Register a new tool."""
        self._tools[tool.name] = tool
        if not self._quiet_mode:
            logger.info("Tool registered", tool_name=tool.name)
    
    def get_tool(self, name: str) -> BaseTool:
        """Get a tool by name."""
        if not self._initialized:
            self._register_default_tools()
        if name not in self._tools:
            raise ValueError(f"Tool '{name}' not found. Available tools: {list(self._tools.keys())}")
        return self._tools[name]
    
    def get_all_tools(self) -> List[BaseTool]:
        """Get all registered tools."""
        if not self._initialized:
            self._register_default_tools()
        return list(self._tools.values())
    
    def get_function_tools(self) -> List:
        """Get all tools as function_tool decorated functions."""
        if not self._initialized:
            self._register_default_tools()
        return [tool.get_function_tool() for tool in self._tools.values()]
    
    def list_tools(self) -> List[str]:
        """List all available tool names."""
        if not self._initialized:
            self._register_default_tools()
        return list(self._tools.keys())
    
    def __len__(self) -> int:
        return len(self._tools)
    
    def __str__(self) -> str:
        return f"ToolRegistry(tools={list(self._tools.keys())})"


# Create global registry instance
tool_registry = ToolRegistry()
