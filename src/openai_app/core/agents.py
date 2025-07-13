"""
Agent factory and configuration.
Creates and manages AI agents with different configurations.
"""
from typing import List, Optional
from agents import Agent

from .models import model_provider
from ..tools import tool_registry
from ..config.logging import get_logger
from .exceptions import AgentError

logger = get_logger(__name__)


class AgentFactory:
    """Factory for creating and configuring agents."""
    
    def __init__(self):
        self._agents = {}
    
    def create_weather_agent(
        self,
        name: str = "Weather Assistant",
        model_type: str = "gemini"
    ) -> Agent:
        """
        Create a weather-focused agent.
        
        Args:
            name: Agent name
            model_type: Type of model to use ("gemini" or "openai")
            
        Returns:
            Configured Agent instance
        """
        logger.info("Creating weather agent", name=name, model_type=model_type)
        
        try:
            # Get the appropriate model
            if model_type == "gemini":
                logger.info("Getting Gemini model")
                model = model_provider.get_gemini_model()
                logger.info("Gemini model obtained successfully")
            elif model_type == "openai":
                model = model_provider.get_openai_model()
            else:
                raise ValueError(f"Unknown model type: {model_type}")
            
            # Get weather tools
            logger.info("Getting tools from registry")
            tools = tool_registry.get_function_tools()
            logger.info("Tools obtained", tool_count=len(tools))
            
            # Create agent with weather-specific instructions
            instructions = """
            You are a helpful weather assistant. Your primary function is to provide weather information for cities.
            
            When users ask about weather:
            1. Use the get_weather tool to fetch weather information
            2. Provide clear, conversational responses
            3. If asked about weather conditions, be specific about temperature and conditions
            
            Always be friendly and helpful in your responses.
            """
            
            logger.info("Creating Agent instance")
            agent = Agent(
                name=name,
                instructions=instructions.strip(),
                model=model,
                tools=tools
            )
            logger.info("Agent instance created successfully")
            
            # Store agent for reuse
            self._agents[name] = agent
            logger.info("Weather agent created successfully", name=name, tools_count=len(tools))
            
            return agent
            
        except Exception as e:
            logger.error("Error creating weather agent", error=str(e), name=name)
            raise AgentError(f"Failed to create weather agent: {str(e)}")
        
        return agent
    
    def create_general_agent(
        self,
        name: str = "General Assistant",
        instructions: Optional[str] = None,
        model_type: str = "gemini"
    ) -> Agent:
        """
        Create a general-purpose agent.
        
        Args:
            name: Agent name
            instructions: Custom instructions (optional)
            model_type: Type of model to use
            
        Returns:
            Configured Agent instance
        """
        logger.info("Creating general agent", name=name, model_type=model_type)
        
        # Get the appropriate model
        if model_type == "gemini":
            model = model_provider.get_gemini_model()
        elif model_type == "openai":
            model = model_provider.get_openai_model()
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        # Default instructions if none provided
        if instructions is None:
            instructions = """
            You are a helpful AI assistant. You can help with various tasks and answer questions.
            You have access to various tools to help provide accurate information.
            Always be helpful, accurate, and friendly in your responses.
            """
        
        # Get all available tools
        tools = tool_registry.get_function_tools()
        
        agent = Agent(
            name=name,
            instructions=instructions.strip(),
            model=model,
            tools=tools
        )
        
        # Store agent for reuse
        self._agents[name] = agent
        logger.info("General agent created successfully", name=name, tools_count=len(tools))
        
        return agent
    
    def get_agent(self, name: str) -> Optional[Agent]:
        """Get a previously created agent by name."""
        return self._agents.get(name)
    
    def list_agents(self) -> List[str]:
        """List all created agent names."""
        return list(self._agents.keys())
    
    def clear_agents(self):
        """Clear all stored agents."""
        self._agents.clear()
        logger.info("All agents cleared")


# Create global agent factory instance
agent_factory = AgentFactory()
