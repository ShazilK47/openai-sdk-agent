"""
Search tool implementation with Tavily web search.
"""
from typing import Optional, Dict, Any
from agents.tool import function_tool

from .base import BaseTool
from ..config.logging import get_logger
from ..utils.search_api import search_api_service

logger = get_logger(__name__)


class SearchTool(BaseTool):
    """Tool for performing web searches."""
    
    def __init__(self):
        super().__init__(
            name="search_web",
            description="Search the internet for current information, news, facts, and answers to questions"
        )
    
    async def execute(self, query: str, max_results: Optional[int] = None) -> str:
        """
        Perform a web search.
        
        Args:
            query: The search query
            max_results: Optional maximum number of results (default: 5)
            
        Returns:
            Formatted search results as a string
        """
        logger.info("Performing web search", query=query, max_results=max_results)
        
        # Use search API service
        result = await search_api_service.search_web(query, max_results)
        
        logger.info("Web search completed", query=query, result_length=len(result))
        return result
    
    def get_function_tool(self):
        """Return the function_tool decorated version."""
        
        @function_tool
        def search_web(query: str, max_results: Optional[int] = None) -> str:
            """
            Search the internet for information.
            
            Args:
                query: The search query string
                max_results: Maximum number of results to return (default: 5)
            
            Returns:
                Formatted search results with titles, URLs, and summaries
            """
            logger.info("Performing web search via function tool", query=query, max_results=max_results)
            
            try:
                result = search_api_service.search_web_sync(query, max_results)
                logger.info("Web search completed via function tool", query=query, result_length=len(result))
                return result
                
            except Exception as e:
                logger.error("Error performing web search via function tool", error=str(e), query=query)
                return f"Unable to search the web for '{query}' at the moment. Please try again later."
        
        return search_web
    
    @property
    def parameters(self) -> Dict[str, Any]:
        """JSON schema for search tool parameters"""
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query to find information about"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of search results to return (default: 5)",
                    "default": 5,
                    "minimum": 1,
                    "maximum": 10
                }
            },
            "required": ["query"]
        }
    

# Create a global instance for easy import
search_tool = SearchTool()