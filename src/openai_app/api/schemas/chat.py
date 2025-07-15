"""
Pydantic schemas for chat-related API endpoints.

These models define the structure of request and response data
for chat interactions with the AI agent.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class ChatMessage(BaseModel):
    """Request model for sending a message to the AI agent"""
    message: str = Field(..., description="The message to send to the AI agent", min_length=1, max_length=5000)
    conversation_id: Optional[str] = Field(None, description="Optional conversation ID to continue existing chat")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "What's the weather like in London?",
                "conversation_id": "conv_123456"
            }
        }


class ToolUsage(BaseModel):
    """Model representing a tool that was used during processing"""
    tool_name: str = Field(..., description="Name of the tool that was used")
    parameters: Dict[str, Any] = Field(..., description="Parameters passed to the tool")
    result: Optional[str] = Field(None, description="Result returned by the tool")
    status: str = Field(..., description="Status of tool execution (pending, success, error)")
    execution_time: Optional[float] = Field(None, description="Time taken to execute the tool in seconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "tool_name": "get_weather",
                "parameters": {"city": "London"},
                "result": "Weather in London: 15°C, partly cloudy",
                "status": "success",
                "execution_time": 1.23
            }
        }


class ChatResponse(BaseModel):
    """Response model for chat messages"""
    response: str = Field(..., description="The AI agent's response")
    conversation_id: str = Field(..., description="Unique identifier for this conversation")
    tool_usage: List[ToolUsage] = Field(default=[], description="List of tools used to generate this response")
    timestamp: datetime = Field(default_factory=datetime.now, description="When this response was generated")
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "The weather in London is currently 15°C with partly cloudy skies.",
                "conversation_id": "conv_123456",
                "tool_usage": [
                    {
                        "tool_name": "get_weather",
                        "parameters": {"city": "London"},
                        "result": "Weather in London: 15°C, partly cloudy",
                        "status": "success",
                        "execution_time": 1.23
                    }
                ],
                "timestamp": "2025-07-15T10:30:00"
            }
        }


class ConversationHistory(BaseModel):
    """Model for conversation history"""
    conversation_id: str = Field(..., description="Unique identifier for the conversation")
    messages: List[Dict[str, Any]] = Field(..., description="List of messages in the conversation")
    created_at: datetime = Field(..., description="When the conversation was created")
    updated_at: datetime = Field(..., description="When the conversation was last updated")
    
    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": "conv_123456",
                "messages": [
                    {
                        "role": "user",
                        "content": "What's the weather like?",
                        "timestamp": "2025-07-15T10:29:00"
                    },
                    {
                        "role": "assistant",
                        "content": "I can help you check the weather. Which city would you like to know about?",
                        "timestamp": "2025-07-15T10:29:05"
                    }
                ],
                "created_at": "2025-07-15T10:29:00",
                "updated_at": "2025-07-15T10:30:00"
            }
        }
