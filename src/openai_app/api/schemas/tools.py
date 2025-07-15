"""
Pydantic schemas for tool-related API endpoints.

These models define the structure of request and response data
for tool management and execution.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class ToolInfo(BaseModel):
    """Model representing information about an available tool"""
    name: str = Field(..., description="Unique name of the tool")
    description: str = Field(..., description="Description of what the tool does")
    parameters: Dict[str, Any] = Field(..., description="JSON schema for tool parameters")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "get_weather",
                "description": "Get current weather information for any city",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "City name to get weather for"
                        }
                    },
                    "required": ["city"]
                }
            }
        }


class AvailableToolsResponse(BaseModel):
    """Response model for available tools endpoint"""
    tools: List[ToolInfo] = Field(..., description="List of available tools")
    total_count: int = Field(..., description="Total number of available tools")
    
    class Config:
        json_schema_extra = {
            "example": {
                "tools": [
                    {
                        "name": "get_weather",
                        "description": "Get current weather information for any city",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "city": {"type": "string", "description": "City name"}
                            },
                            "required": ["city"]
                        }
                    },
                    {
                        "name": "calculator",
                        "description": "Perform mathematical calculations",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "expression": {"type": "string", "description": "Math expression"}
                            },
                            "required": ["expression"]
                        }
                    }
                ],
                "total_count": 2
            }
        }


class ToolExecutionRequest(BaseModel):
    """Request model for executing a specific tool"""
    tool_name: str = Field(..., description="Name of the tool to execute")
    parameters: Dict[str, Any] = Field(..., description="Parameters to pass to the tool")
    
    class Config:
        json_schema_extra = {
            "example": {
                "tool_name": "get_weather",
                "parameters": {"city": "London"}
            }
        }


class ToolExecutionResponse(BaseModel):
    """Response model for tool execution"""
    tool_name: str = Field(..., description="Name of the executed tool")
    parameters: Dict[str, Any] = Field(..., description="Parameters that were used")
    result: str = Field(..., description="Result returned by the tool")
    status: str = Field(..., description="Execution status (success, error)")
    execution_time: float = Field(..., description="Time taken to execute in seconds")
    error_message: Optional[str] = Field(None, description="Error message if execution failed")
    
    class Config:
        json_schema_extra = {
            "example": {
                "tool_name": "get_weather",
                "parameters": {"city": "London"},
                "result": "🌤️ Weather in London, GB: Temperature: 15°C (feels like 12°C)",
                "status": "success",
                "execution_time": 1.23,
                "error_message": None
            }
        }
