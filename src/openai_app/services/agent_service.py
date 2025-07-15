"""
Agent service for handling agent operations.
"""
from typing import Optional, Dict, Any
from agents import Agent, Runner

from ..core import agent_factory, AgentError
from ..config.logging import get_logger

logger = get_logger(__name__)


class AgentService:
    """Service for managing agent operations."""
    
    def __init__(self):
        self._current_agent: Optional[Agent] = None
        self._conversation_history: list = []
        self._quiet_mode: bool = False
    
    def set_quiet_mode(self, quiet: bool):
        """Set quiet mode for this service."""
        self._quiet_mode = quiet
    
    async def run_weather_query(
        self, 
        query: str, 
        agent_name: str = "Weather Assistant"
    ) -> str:
        """
        Run a weather-related query.
        
        Args:
            query: The user's weather question
            agent_name: Name of the agent to use
            
        Returns:
            The agent's response
        """
        logger.info("Running weather query", query=query[:50], agent=agent_name)
        
        try:
            # Get or create weather agent
            agent = agent_factory.get_agent(agent_name)
            if agent is None:
                if not self._quiet_mode:
                    logger.info("Creating new weather agent", name=agent_name)
                agent = agent_factory.create_weather_agent(agent_name)
            
            self._current_agent = agent
            
            # Run the query
            result = await Runner.run(agent, query)
            
            # Store in conversation history
            self._conversation_history.append({
                "query": query,
                "response": result.final_output,
                "agent": agent_name,
                "type": "weather"
            })
            
            logger.info("Weather query completed", 
                       query_length=len(query), 
                       response_length=len(result.final_output))
            
            return result.final_output
            
        except Exception as e:
            logger.error("Error running weather query", error=str(e))
            raise AgentError(f"Failed to run weather query: {str(e)}")
    
    async def run_general_query(
        self, 
        query: str, 
        agent_name: str = "General Assistant",
        instructions: Optional[str] = None
    ) -> str:
        """
        Run a general query.
        
        Args:
            query: The user's question
            agent_name: Name of the agent to use
            instructions: Custom instructions (optional)
            
        Returns:
            The agent's response
        """
        logger.info("Running general query", query=query[:50], agent=agent_name)
        
        try:
            # Get or create general agent
            agent = agent_factory.get_agent(agent_name)
            if agent is None:
                logger.info("Creating new general agent", name=agent_name)
                agent = agent_factory.create_general_agent(agent_name, instructions)
            
            self._current_agent = agent
            
            # Run the query
            result = await Runner.run(agent, query)
            
            # Store in conversation history
            self._conversation_history.append({
                "query": query,
                "response": result.final_output,
                "agent": agent_name,
                "type": "general"
            })
            
            logger.info("General query completed", 
                       query_length=len(query), 
                       response_length=len(result.final_output))
            
            return result.final_output
            
        except Exception as e:
            logger.error("Error running general query", error=str(e))
            raise AgentError(f"Failed to run general query: {str(e)}")
    
    async def run_custom_query(
        self,
        query: str,
        agent_name: str,
        instructions: str,
        model_type: str = "gemini"
    ) -> str:
        """
        Run a query with a custom agent.
        
        Args:
            query: The user's question
            agent_name: Name for the custom agent
            instructions: Custom instructions for the agent
            model_type: Type of model to use
            
        Returns:
            The agent's response
        """
        logger.info("Running custom query", 
                   query=query[:50], 
                   agent=agent_name, 
                   model=model_type)
        
        try:
            # Create custom agent
            agent = agent_factory.create_general_agent(
                name=agent_name,
                instructions=instructions,
                model_type=model_type
            )
            
            self._current_agent = agent
            
            # Run the query
            result = await Runner.run(agent, query)
            
            # Store in conversation history
            self._conversation_history.append({
                "query": query,
                "response": result.final_output,
                "agent": agent_name,
                "type": "custom",
                "instructions": instructions
            })
            
            logger.info("Custom query completed", 
                       query_length=len(query), 
                       response_length=len(result.final_output))
            
            return result.final_output
            
        except Exception as e:
            logger.error("Error running custom query", error=str(e))
            raise AgentError(f"Failed to run custom query: {str(e)}")
    
    async def process_message(
        self,
        message: str,
        conversation_id: str = None,
        agent_name: str = "AI Assistant"
    ) -> Dict[str, Any]:
        """
        Process a message through the AI agent for API usage.
        
        Args:
            message: The user's message
            conversation_id: Optional conversation ID for tracking
            agent_name: Name of the agent to use
            
        Returns:
            Dict containing response, conversation_id, and tool usage info
        """
        logger.info("Processing API message", 
                   message=message[:50], 
                   conversation_id=conversation_id,
                   agent=agent_name)
        
        try:
            # Get or create agent
            agent = agent_factory.get_agent(agent_name)
            if agent is None:
                logger.info("Creating new agent for API", name=agent_name)
                agent = agent_factory.create_general_agent(agent_name)
            
            self._current_agent = agent
            
            # Run the message through the agent
            result = await Runner.run(agent, message)
            
            # Extract tool usage information from the result
            tool_usage = []
            if hasattr(result, 'tool_calls') and result.tool_calls:
                for tool_call in result.tool_calls:
                    tool_usage.append({
                        "tool_name": tool_call.get("function", {}).get("name", "unknown"),
                        "parameters": tool_call.get("function", {}).get("arguments", {}),
                        "result": getattr(tool_call, 'result', None),
                        "status": "success" if hasattr(tool_call, 'result') else "unknown",
                        "execution_time": getattr(tool_call, 'execution_time', None)
                    })
            
            # Store in conversation history with API context
            conversation_entry = {
                "query": message,
                "response": result.final_output,
                "agent": agent_name,
                "type": "api",
                "conversation_id": conversation_id,
                "tool_usage": tool_usage
            }
            self._conversation_history.append(conversation_entry)
            
            response_data = {
                "content": result.final_output,
                "conversation_id": conversation_id,
                "tool_usage": tool_usage
            }
            
            logger.info("API message processed successfully", 
                       response_length=len(result.final_output),
                       tools_used=len(tool_usage))
            
            return response_data
            
        except Exception as e:
            logger.error("Error processing API message", error=str(e))
            raise AgentError(f"Failed to process message: {str(e)}")
    
    def get_conversation_history(self) -> list:
        """Get the conversation history."""
        return self._conversation_history.copy()
    
    def clear_conversation_history(self):
        """Clear the conversation history."""
        self._conversation_history.clear()
        logger.info("Conversation history cleared")
    
    def get_current_agent(self) -> Optional[Agent]:
        """Get the currently active agent."""
        return self._current_agent
    
    def get_agent_stats(self) -> Dict[str, Any]:
        """Get statistics about agent usage."""
        stats = {
            "total_conversations": len(self._conversation_history),
            "weather_queries": len([c for c in self._conversation_history if c["type"] == "weather"]),
            "general_queries": len([c for c in self._conversation_history if c["type"] == "general"]),
            "custom_queries": len([c for c in self._conversation_history if c["type"] == "custom"]),
            "api_queries": len([c for c in self._conversation_history if c["type"] == "api"]),
            "current_agent": self._current_agent.name if self._current_agent else None,
            "available_agents": agent_factory.list_agents()
        }
        return stats


# Create global agent service instance
agent_service = AgentService()
