"""
Test the services module.
You can delete this after testing.
"""
import asyncio
from .agent_service import agent_service
from .app_service import app_service


async def test_services():
    """Test the services functionality."""
    
    print("=== Services Module Test ===")
    
    # Initialize app service
    app_service.initialize()
    print("✅ App service initialized")
    
    # Test weather query
    print("\n--- Testing Weather Query ---")
    try:
        weather_response = await agent_service.run_weather_query(
            "What's the weather like in Tokyo?"
        )
        print(f"Weather response: {weather_response[:100]}...")
        print("✅ Weather query successful")
    except Exception as e:
        print(f"❌ Weather query failed: {e}")
    
    # Test general query
    print("\n--- Testing General Query ---")
    try:
        general_response = await agent_service.run_general_query(
            "What is artificial intelligence?"
        )
        print(f"General response: {general_response[:100]}...")
        print("✅ General query successful")
    except Exception as e:
        print(f"❌ General query failed: {e}")
    
    # Test app service single query
    print("\n--- Testing App Service Query ---")
    try:
        app_response = await app_service.run_single_query(
            "Tell me about the weather in Paris",
            query_type="auto"
        )
        print(f"App service response: {app_response[:100]}...")
        print("✅ App service query successful")
    except Exception as e:
        print(f"❌ App service query failed: {e}")
    
    # Test statistics
    print("\n--- Testing Statistics ---")
    stats = agent_service.get_agent_stats()
    print(f"Conversation stats: {stats}")
    
    app_info = app_service.get_app_info()
    print(f"App info: {app_info['name']} v{app_info['version']}")
    
    print("\n✅ All services tests completed!")


def main():
    """Main test function."""
    asyncio.run(test_services())


if __name__ == "__main__":
    main()
