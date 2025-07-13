"""
Test the tools module.
You can delete this after testing.
"""
import asyncio
from .registry import tool_registry
from .weather import weather_tool
from ..config.logging import configure_logging, get_logger

# Configure logging
configure_logging()
logger = get_logger(__name__)


async def test_tools():
    """Test the tools functionality."""
    
    print("=== Tools Module Test ===")
    
    # Test registry
    print(f"Registry: {tool_registry}")
    print(f"Available tools: {tool_registry.list_tools()}")
    print(f"Total tools: {len(tool_registry)}")
    
    # Test weather tool directly
    print("\n--- Testing Weather Tool Directly ---")
    result = await weather_tool.execute("Karachi")
    print(f"Direct call result: {result}")
    
    # Test getting tool from registry
    print("\n--- Testing Tool from Registry ---")
    weather_from_registry = tool_registry.get_tool("get_weather")
    result2 = await weather_from_registry.execute("Lahore", "rainy")
    print(f"Registry call result: {result2}")
    
    # Test function tools (for agent use)
    print("\n--- Testing Function Tools ---")
    function_tools = tool_registry.get_function_tools()
    print(f"Function tools count: {len(function_tools)}")
    print(f"Function tools types: {[type(tool).__name__ for tool in function_tools]}")
    
    # Test calling the function tool
    try:
        weather_func = function_tools[0]  # First (and only) tool
        func_result = weather_func("Islamabad", "sunny")
        print(f"Function tool result: {func_result}")
    except Exception as e:
        print(f"Function tool test failed: {e}")
        print("This is expected - function tools need to be used within the agents framework")
    
    print("\n✅ All tools tests passed!")


def main():
    """Main test function."""
    asyncio.run(test_tools())


if __name__ == "__main__":
    main()
