"""
Model provider and configuration.
Manages different AI models (Gemini, OpenAI, etc.).
"""
from typing import Optional
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel

from ..config.settings import settings
from ..config.logging import get_logger

logger = get_logger(__name__)


class ModelProvider:
    """Provider for managing AI models."""
    
    def __init__(self):
        self._gemini_client: Optional[AsyncOpenAI] = None
        self._gemini_model: Optional[OpenAIChatCompletionsModel] = None
        self._openai_client: Optional[AsyncOpenAI] = None
        self._openai_model: Optional[OpenAIChatCompletionsModel] = None
    
    def get_gemini_client(self) -> AsyncOpenAI:
        """Get or create Gemini client."""
        if self._gemini_client is None:
            logger.info("Creating Gemini client", base_url=settings.gemini_base_url)
            self._gemini_client = AsyncOpenAI(
                api_key=settings.gemini_api_key,
                base_url=settings.gemini_base_url
            )
        return self._gemini_client
    
    def get_gemini_model(self) -> OpenAIChatCompletionsModel:
        """Get or create Gemini model."""
        if self._gemini_model is None:
            logger.info("Creating Gemini model", model=settings.gemini_model)
            client = self.get_gemini_client()
            self._gemini_model = OpenAIChatCompletionsModel(
                model=settings.gemini_model,
                openai_client=client
            )
        return self._gemini_model
    
    def get_openai_client(self) -> AsyncOpenAI:
        """Get or create OpenAI client (if API key is available)."""
        if not settings.openai_api_key:
            raise ValueError("OpenAI API key not configured")
        
        if self._openai_client is None:
            logger.info("Creating OpenAI client")
            self._openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
        return self._openai_client
    
    def get_openai_model(self, model_name: str = "gpt-4") -> OpenAIChatCompletionsModel:
        """Get or create OpenAI model."""
        if self._openai_model is None:
            logger.info("Creating OpenAI model", model=model_name)
            client = self.get_openai_client()
            self._openai_model = OpenAIChatCompletionsModel(
                model=model_name,
                openai_client=client
            )
        return self._openai_model
    
    def get_default_model(self) -> OpenAIChatCompletionsModel:
        """Get the default model (Gemini)."""
        return self.get_gemini_model()
    
    def list_available_models(self) -> list[str]:
        """List available model types."""
        models = ["gemini"]
        if settings.openai_api_key:
            models.append("openai")
        return models


# Create global model provider instance
model_provider = ModelProvider()
