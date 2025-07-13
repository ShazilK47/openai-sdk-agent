"""
Test the core module.
You can delete this after testing.
"""
from .models import model_provider
from .agents import agent_factory
from ..config.logging import configure_logging, get_logger

# Configure logging
configure_logging()
logger = get_logger(__name__)


def test_core():
    """Test the core functionality."""
    
    print("=== Core Module Test ===")
    
    # Test model provider
    print("\n--- Testing Model Provider ---")
    available_models = model_provider.list_available_models()
    print(f"Available models: {available_models}")
    
    # Test creating Gemini model
    print("Creating Gemini model...")
    gemini_model = model_provider.get_gemini_model()
    print(f"Gemini model created: {type(gemini_model).__name__}")
    
    # Test agent factory
    print("\n--- Testing Agent Factory ---")
    
    # Create weather agent
    print("Creating weather agent...")
    weather_agent = agent_factory.create_weather_agent("Test Weather Agent")
    print(f"Weather agent created: {weather_agent.name}")
    
    # Create general agent
    print("Creating general agent...")
    general_agent = agent_factory.create_general_agent("Test General Agent")
    print(f"General agent created: {general_agent.name}")
    
    # Test agent retrieval
    print("\n--- Testing Agent Retrieval ---")
    agent_list = agent_factory.list_agents()
    print(f"Created agents: {agent_list}")
    
    retrieved_agent = agent_factory.get_agent("Test Weather Agent")
    print(f"Retrieved agent: {retrieved_agent.name if retrieved_agent else 'None'}")
    
    print("\n✅ All core tests passed!")


def main():
    """Main test function."""
    test_core()


if __name__ == "__main__":
    main()
