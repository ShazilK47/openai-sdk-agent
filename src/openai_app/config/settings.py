"""
Application settings and configuration management.
Uses Pydantic to load and validate environment variables.
"""
from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration
    gemini_api_key: str = Field(..., description="Gemini API key")
    openai_api_key: Optional[str] = Field(None, description="OpenAI API key (backup)")
    gemini_model: str = Field(default="gemini-2.0-flash-exp", description="Gemini model to use")
    gemini_base_url: str = Field(
        default="https://generativelanguage.googleapis.com/v1beta/openai/",
        description="Gemini API base URL"
    )

     # Weather API Configuration 
    weather_api_key: Optional[str] = Field(None, description="OpenWeatherMap API key")
    weather_api_base_url: str = Field(
        default="https://api.openweathermap.org/data/2.5",
        description="Weather API base URL"
    )

    # Search API Configuration (add this after weather config)
    tavily_api_key: Optional[str] = Field(None, description="Tavily Search API key")
    tavily_max_results: int = Field(default=5, description="Maximum number of search results")
    tavily_include_answer: bool = Field(default=True, description="Include AI-generated answer")
    tavily_include_raw_content: bool = Field(default=False, description="Include raw content")
    
    # Application Settings
    log_level: str = Field(default="INFO", description="Logging level")
    debug: bool = Field(default=False, description="Debug mode")
    environment: str = Field(default="development", description="Application environment")
    
    # Optional Features
    tracing_enabled: bool = Field(default=False, description="Enable tracing")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra environment variables


# Create global settings instance
settings = Settings()
