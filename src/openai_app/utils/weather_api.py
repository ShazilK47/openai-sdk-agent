"""
Weather API service for fetching real weather data.
"""
import httpx
from typing import Optional, Dict, Any
from ..config.settings import settings
from ..config.logging import get_logger

logger = get_logger(__name__)


class WeatherAPIService:
    """Service for fetching real weather data from OpenWeatherMap API."""
    
    def __init__(self):
        self.api_key = settings.weather_api_key
        self.base_url = settings.weather_api_base_url
        self._client = None
    
    @property
    def client(self):
        """Get or create HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=10.0)
        return self._client
    
    async def get_current_weather(self, city: str) -> str:
        """
        Get current weather for a city.
        
        Args:
            city: City name
            
        Returns:
            Formatted weather description
        """
        if not self.api_key:
            logger.warning("Weather API key not configured, using simulation")
            return f"Weather API not configured. Simulated: The weather in {city} is sunny with 25°C."
        
        try:
            url = f"{self.base_url}/weather"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric"  # Celsius
            }
            
            logger.info("Fetching weather data", city=city)
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return self._format_weather_response(data, city)
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return f"City '{city}' not found. Please check the spelling."
            else:
                logger.error("Weather API HTTP error", status_code=e.response.status_code, city=city)
                return f"Weather service temporarily unavailable for {city}."
                
        except Exception as e:
            logger.error("Weather API error", error=str(e), city=city)
            return f"Unable to fetch weather for {city} at the moment."
    
    def _format_weather_response(self, data: Dict[str, Any], city: str) -> str:
        """Format the API response into a readable string."""
        try:
            weather = data["weather"][0]
            main = data["main"]
            wind = data.get("wind", {})
            
            description = weather["description"].title()
            temp = round(main["temp"])
            feels_like = round(main["feels_like"])
            humidity = main["humidity"]
            wind_speed = wind.get("speed", 0)
            
            response = f"The weather in {city} is {description.lower()} with a temperature of {temp}°C"
            
            if feels_like != temp:
                response += f" (feels like {feels_like}°C)"
            
            response += f", humidity {humidity}%"
            
            if wind_speed > 0:
                response += f", and wind speed {wind_speed} m/s"
            
            response += "."
            
            return response
            
        except KeyError as e:
            logger.error("Error parsing weather data", error=str(e))
            return f"Received weather data for {city} but couldn't parse it properly."
    
    def get_current_weather_sync(self, city: str) -> str:
        """
        Get current weather for a city synchronously.
        
        Args:
            city: City name
            
        Returns:
            Formatted weather description
        """
        if not self.api_key:
            logger.warning("Weather API key not configured, using simulation")
            return f"Weather API not configured. Simulated: The weather in {city} is sunny with 25°C."
        
        try:
            url = f"{self.base_url}/weather"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric"  # Celsius
            }
            
            logger.info("Fetching weather data synchronously", city=city)
            
            # Use synchronous httpx client for function tools
            with httpx.Client(timeout=10.0) as client:
                response = client.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                return self._format_weather_response(data, city)
                
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return f"City '{city}' not found. Please check the spelling."
            else:
                logger.error("Weather API HTTP error", status_code=e.response.status_code, city=city)
                return f"Weather service temporarily unavailable for {city}."
                
        except Exception as e:
            logger.error("Weather API error", error=str(e), city=city)
            return f"Unable to fetch weather for {city} at the moment."
    
    async def close(self):
        """Close the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None


# Global instance
weather_api_service = WeatherAPIService()