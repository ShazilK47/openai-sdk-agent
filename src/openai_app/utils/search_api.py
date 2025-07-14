"""
Search API service using Tavily for web search capabilities.
"""
from typing import List, Dict, Any, Optional
from tavily import TavilyClient
from ..config.settings import settings
from ..config.logging import get_logger

logger = get_logger(__name__)


class SearchAPIService:
    """Service for performing web searches using Tavily."""
    
    def __init__(self):
        # Initialize Tavily client
        self.api_key = settings.tavily_api_key
        self.max_results = settings.tavily_max_results
        self.include_answer = settings.tavily_include_answer
        self.include_raw_content = settings.tavily_include_raw_content
        
        # Create client if API key is available
        if self.api_key:
            self.client = TavilyClient(api_key=self.api_key)
        else:
            self.client = None
            logger.warning("Tavily API key not configured")
    
    async def search_web(self, query: str, max_results: Optional[int] = None) -> str:
        """
        Perform web search asynchronously.
        
        Args:
            query: Search query string
            max_results: Optional override for max results
            
        Returns:
            Formatted search results as string
        """
        return self.search_web_sync(query, max_results)
    
    def search_web_sync(self, query: str, max_results: Optional[int] = None) -> str:
        """
        Perform web search synchronously.
        
        Args:
            query: Search query string
            max_results: Optional override for max results
            
        Returns:
            Formatted search results as string
        """
        if not self.client:
            return "Search API not configured. Please add TAVILY_API_KEY to your environment."
        
        try:
            # Use provided max_results or fall back to configured default
            num_results = max_results if max_results is not None else self.max_results
            
            logger.info("Performing web search", query=query, max_results=num_results)
            
            # Perform search using Tavily
            response = self.client.search(
                query=query,
                max_results=num_results,
                include_answer=self.include_answer,
                include_raw_content=self.include_raw_content
            )
            
            # Format and return results
            formatted_results = self._format_search_results(response, query)
            logger.info("Search completed", query=query, results_count=len(response.get('results', [])))
            
            return formatted_results
            
        except Exception as e:
            logger.error("Search API error", error=str(e), query=query)
            return f"Unable to perform search for '{query}' at the moment. Error: {str(e)}"
    
    def _format_search_results(self, response: Dict[str, Any], query: str) -> str:
        """Format search results into a readable string."""
        if not response or 'results' not in response:
            return f"No search results found for '{query}'."
        
        results = response['results']
        if not results:
            return f"No search results found for '{query}'."
        
        # Start building formatted response
        formatted = f"Search results for '{query}':\n\n"
        
        # Add AI-generated answer if available
        if self.include_answer and 'answer' in response and response['answer']:
            formatted += f"**Quick Answer:** {response['answer']}\n\n"
        
        # Add individual search results
        for i, result in enumerate(results, 1):
            title = result.get('title', 'No title')
            url = result.get('url', 'No URL')
            content = result.get('content', 'No content available')
            
            # Truncate content if it's too long
            if len(content) > 200:
                content = content[:200] + "..."
            
            formatted += f"{i}. **{title}**\n"
            formatted += f"   URL: {url}\n"
            formatted += f"   Summary: {content}\n\n"
        
        return formatted.strip()


# Global instance
search_api_service = SearchAPIService()