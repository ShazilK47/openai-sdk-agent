"""
Chat API routes.

Provides endpoints for interacting with the AI agent through chat.
"""

from fastapi import APIRouter, HTTPException
import uuid
import time
import logging
from datetime import datetime

from ..schemas.chat import ChatMessage, ChatResponse, ToolUsage
from ...services.agent_service import agent_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/chat/message", response_model=ChatResponse)
async def send_chat_message(message: ChatMessage) -> ChatResponse:
    """
    Send a message to the AI agent and get a response.
    
    Args:
        message: ChatMessage containing the user's message and optional conversation ID
        
    Returns:
        ChatResponse with the agent's reply and any tool usage information
    """
    try:
        # Generate conversation ID if not provided
        conversation_id = message.conversation_id or str(uuid.uuid4())
        
        logger.info(f"Processing chat message in conversation {conversation_id}")
        logger.debug(f"Message content: {message.message}")
        
        start_time = time.time()
        
        # Process the message through the agent service
        response_data = await agent_service.process_message(
            message=message.message,
            conversation_id=conversation_id
        )
        
        processing_time = time.time() - start_time
        logger.info(f"Message processed in {processing_time:.2f} seconds")
        
        # Convert tool usage data to ToolUsage models
        tool_usage = []
        if "tool_usage" in response_data:
            for tool_data in response_data["tool_usage"]:
                tool_usage.append(ToolUsage(
                    tool_name=tool_data.get("tool_name", ""),
                    parameters=tool_data.get("parameters", {}),
                    result=tool_data.get("result"),
                    status=tool_data.get("status", "unknown"),
                    execution_time=tool_data.get("execution_time")
                ))
        
        return ChatResponse(
            response=response_data["content"],
            conversation_id=conversation_id,
            tool_usage=tool_usage,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error processing chat message: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to process message: {str(e)}"
        )


@router.get("/chat/history/{conversation_id}")
async def get_conversation_history(conversation_id: str):
    """
    Get the history of a conversation.
    
    Args:
        conversation_id: ID of the conversation to retrieve
        
    Returns:
        Conversation history (implementation depends on storage solution)
    """
    # This is a placeholder - you would implement conversation storage
    # For now, return a simple response
    return {
        "conversation_id": conversation_id,
        "message": "Conversation history feature not yet implemented",
        "note": "This would return the full conversation history from storage"
    }


@router.delete("/chat/history/{conversation_id}")
async def clear_conversation_history(conversation_id: str):
    """
    Clear the history of a conversation.
    
    Args:
        conversation_id: ID of the conversation to clear
        
    Returns:
        Confirmation of deletion
    """
    # This is a placeholder - you would implement conversation storage
    return {
        "conversation_id": conversation_id,
        "message": "Conversation cleared",
        "note": "This would clear the conversation from storage"
    }
