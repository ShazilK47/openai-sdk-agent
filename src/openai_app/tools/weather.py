"""
Weather tool implementation with real API.
"""
from typing import Optional, Dict, Any
from agents.tool import function_tool

from .base import BaseTool
from ..config.logging import get_logger
from ..utils.weather_api import weather_api_service

logger = get_logger(__name__)


class WeatherTool(BaseTool):
    """Tool for getting weather information."""
    
    def __init__(self):
        super().__init__(
            name="get_weather",
            description="Get current weather information for any city"
        )
    
    @property
    def parameters(self) -> Dict[str, Any]:
        """JSON schema for weather tool parameters"""
        return {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name to get weather for"
                },
                "weather_type": {
                    "type": "string",
                    "description": "Optional weather type (current, forecast, etc.)",
                    "default": "current"
                }
            },
            "required": ["city"]
        }
    
    async def execute(self, city: str, weather_type: Optional[str] = None) -> str:
        """
        Get weather information for a city.
        
        Args:
            city: The city name to get weather for
            weather_type: Optional weather type (not used with real API)
            
        Returns:
            Weather information as a string
        """
        logger.info("Getting weather information", city=city, weather_type=weather_type)
        
        # Use real weather API service
        result = await weather_api_service.get_current_weather(city)
        
        logger.info("Weather information retrieved", city=city, result=result[:50])
        return result
    
    def get_function_tool(self):
        """Return the function_tool decorated version."""
        
        @function_tool
        def get_weather(city: str, weather_type: Optional[str] = None) -> str:
            """
            Get weather information for a city.
            
            Args:
                city: The city name to get weather for
                weather_type: Optional weather type (not used with real API)
            
            Returns:
                Weather information as a string
            """            
            logger.info("Getting weather information via function tool", city=city, weather_type=weather_type)
            
            # Use synchronous weather API service for function tools
            try:
                result = weather_api_service.get_current_weather_sync(city)
                logger.info("Weather information retrieved via function tool", city=city, result=result[:50])
                return result
                
            except Exception as e:
                logger.error("Error getting weather via function tool", error=str(e), city=city)
                # Fallback to simulation if real API fails
                fallback_result = f"Weather API temporarily unavailable. Simulated: The weather in {city} is sunny with 25°C."
                return fallback_result
        
        return get_weather


# Create a global instance for easy import
weather_tool = WeatherTool()