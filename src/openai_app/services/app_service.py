"""
Main application service.
Orchestrates the entire application flow.
"""
import asyncio
from typing import Optional, Dict, Any

from .agent_service import agent_service
from ..config.settings import settings
from ..config.logging import configure_logging, get_logger
from ..core.exceptions import OpenAIAppError
from agents import set_tracing_disabled

logger = get_logger(__name__)


class AppService:
    """Main application service."""
    
    def __init__(self):
        self._initialized = False
        self._setup_complete = False
    
    def initialize(self, quiet_mode: bool = False):
        """Initialize the application."""
        if self._initialized:
            return
        
        # Set quiet mode on tool registry FIRST (before any tools are used)
        from ..tools import tool_registry
        tool_registry.set_quiet_mode(quiet_mode)
        
        # Configure logging
        configure_logging()
        
        # If in quiet mode, suppress almost all logging
        if quiet_mode:
            import logging
            # Set root logger to only show ERROR and above
            logging.getLogger().setLevel(logging.ERROR)
            # Also set specific noisy loggers to ERROR
            logging.getLogger("openai_app").setLevel(logging.ERROR)
            logging.getLogger("src.openai_app").setLevel(logging.ERROR)
            logging.getLogger("httpx").setLevel(logging.ERROR)
            logging.getLogger("openai").setLevel(logging.ERROR)
        
        if not quiet_mode:
            logger.info("Initializing OpenAI App", environment=settings.environment)
        
        # Disable tracing if configured
        if not settings.tracing_enabled:
            set_tracing_disabled(disabled=True)
            if not quiet_mode:
                logger.info("Tracing disabled")
        
        # Log configuration only in verbose mode
        if not quiet_mode:
            logger.info("Application initialized", 
                       model=settings.gemini_model,
                       log_level=settings.log_level,
                       debug=settings.debug)
        
        self._initialized = True
    
    async def run_interactive_session(self):
        """Run an interactive chat session."""
        self.initialize(quiet_mode=True)  # Quiet mode for interactive sessions
        
        print("🤖 Welcome to OpenAI App!")
        print("Type 'help' for commands, 'quit' to exit")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\n💬 You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Goodbye!")
                    break
                
                if user_input.lower() == 'help':
                    self._show_help()
                    continue
                
                if user_input.lower() == 'stats':
                    self._show_stats()
                    continue
                
                if user_input.lower() == 'clear':
                    agent_service.clear_conversation_history()
                    print("🧹 Conversation history cleared!")
                    continue
                
                # Determine query type and route accordingly
                response = await self._process_query(user_input)
                print(f"\n🤖 Assistant: {response}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                logger.error("Error in interactive session", error=str(e))
                print(f"❌ Error: {str(e)}")
    
    async def run_single_query(self, query: str, query_type: str = "auto", quiet_mode: bool = False) -> str:
        """
        Run a single query and return the response.
        
        Args:
            query: The user's question
            query_type: Type of query ("weather", "general", "auto")
            quiet_mode: Whether to suppress logging
            
        Returns:
            The agent's response
        """
        self.initialize(quiet_mode=quiet_mode)
        
        # Set quiet mode on agent service
        agent_service.set_quiet_mode(quiet_mode)
        
        if not quiet_mode:
            logger.info("Running single query", query=query[:50], type=query_type)
        
        try:
            if query_type == "weather":
                return await agent_service.run_weather_query(query)
            elif query_type == "general":
                return await agent_service.run_general_query(query)
            elif query_type == "auto":
                # Auto-detect query type
                if any(word in query.lower() for word in ['weather', 'temperature', 'rain', 'sunny', 'cloudy']):
                    return await agent_service.run_weather_query(query)
                else:
                    return await agent_service.run_general_query(query)
            else:
                raise ValueError(f"Unknown query type: {query_type}")
                
        except Exception as e:
            if not quiet_mode:
                logger.error("Error running single query", error=str(e))
            raise OpenAIAppError(f"Failed to process query: {str(e)}")
    
    def _process_query(self, query: str) -> str:
        """Process a query and return response."""
        return asyncio.create_task(self.run_single_query(query))
    
    async def _process_query(self, query: str) -> str:
        """Process a query and return response."""
        return await self.run_single_query(query)
    
    def _show_help(self):
        """Show help information."""
        help_text = """
📖 Available Commands:
• help     - Show this help message
• stats    - Show application statistics
• clear    - Clear conversation history
• quit     - Exit the application

🔍 Query Types:
• Weather questions are automatically detected
• General questions use the general assistant
• Just type your question naturally!

💡 Examples:
• "What's the weather in London?"
• "How do I learn Python?"
• "Tell me about artificial intelligence"
        """
        print(help_text)
    
    def _show_stats(self):
        """Show application statistics."""
        stats = agent_service.get_agent_stats()
        
        print("\n📊 Application Statistics:")
        print(f"• Total conversations: {stats['total_conversations']}")
        print(f"• Weather queries: {stats['weather_queries']}")
        print(f"• General queries: {stats['general_queries']}")
        print(f"• Custom queries: {stats['custom_queries']}")
        print(f"• Current agent: {stats['current_agent'] or 'None'}")
        print(f"• Available agents: {', '.join(stats['available_agents']) if stats['available_agents'] else 'None'}")
    
    def get_app_info(self) -> Dict[str, Any]:
        """Get application information."""
        return {
            "name": "OpenAI App",
            "version": "0.1.0",
            "environment": settings.environment,
            "model": settings.gemini_model,
            "debug": settings.debug,
            "initialized": self._initialized,
            "stats": agent_service.get_agent_stats()
        }


# Create global app service instance
app_service = AppService()
