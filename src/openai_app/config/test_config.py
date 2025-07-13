"""
Temporary test file to verify configuration works.
You can delete this after testing.
"""
from .settings import settings
from .logging import configure_logging, get_logger


def test_configuration():
    """Test if configuration is working properly."""
    
    # Configure logging
    configure_logging()
    logger = get_logger(__name__)
    
    # Test settings
    print("=== Configuration Test ===")
    print(f"Gemini API Key (first 10 chars): {settings.gemini_api_key[:10]}...")
    print(f"Gemini Model: {settings.gemini_model}")
    print(f"Base URL: {settings.gemini_base_url}")
    print(f"Log Level: {settings.log_level}")
    print(f"Debug Mode: {settings.debug}")
    print(f"Environment: {settings.environment}")
    
    # Test logging
    logger.info("Configuration test completed successfully!", 
                gemini_model=settings.gemini_model,
                debug_mode=settings.debug)
    
    print("✅ Configuration is working!")


if __name__ == "__main__":
    test_configuration()
