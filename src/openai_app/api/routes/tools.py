"""
Tools API routes.

Provides endpoints for managing and executing AI agent tools.
"""

from fastapi import APIRouter, HTTPException
import time
import logging
from typing import Dict, Any

from ..schemas.tools import (
    AvailableToolsResponse, 
    ToolInfo, 
    ToolExecutionRequest, 
    ToolExecutionResponse
)
from ...tools.registry import tool_registry

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/tools/available", response_model=AvailableToolsResponse)
async def get_available_tools() -> AvailableToolsResponse:
    """
    Get list of all available tools.
    
    Returns:
        AvailableToolsResponse containing all registered tools and their information
    """
    try:
        tools = tool_registry.get_all_tools()
        
        tool_infos = []
        for tool in tools:
            tool_info = ToolInfo(
                name=tool.name,
                description=tool.description,
                parameters=tool.parameters
            )
            tool_infos.append(tool_info)
        
        return AvailableToolsResponse(
            tools=tool_infos,
            total_count=len(tool_infos)
        )
        
    except Exception as e:
        logger.error(f"Error getting available tools: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve available tools")


@router.post("/tools/execute", response_model=ToolExecutionResponse)
async def execute_tool(request: ToolExecutionRequest) -> ToolExecutionResponse:
    """
    Execute a specific tool with given parameters.
    
    Args:
        request: ToolExecutionRequest containing tool name and parameters
        
    Returns:
        ToolExecutionResponse with execution result
    """
    start_time = time.time()
    
    try:
        # Get the tool from registry
        tool = tool_registry.get_tool(request.tool_name)
        if not tool:
            raise HTTPException(
                status_code=404, 
                detail=f"Tool '{request.tool_name}' not found"
            )
        
        logger.info(f"Executing tool: {request.tool_name} with parameters: {request.parameters}")
        
        # Execute the tool
        result = await tool.execute(**request.parameters)
        
        execution_time = time.time() - start_time
        
        return ToolExecutionResponse(
            tool_name=request.tool_name,
            parameters=request.parameters,
            result=result,
            status="success",
            execution_time=round(execution_time, 3),
            error_message=None
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        execution_time = time.time() - start_time
        error_message = str(e)
        
        logger.error(f"Tool execution failed: {error_message}")
        
        return ToolExecutionResponse(
            tool_name=request.tool_name,
            parameters=request.parameters,
            result="",
            status="error",
            execution_time=round(execution_time, 3),
            error_message=error_message
        )


@router.get("/tools/{tool_name}")
async def get_tool_info(tool_name: str) -> ToolInfo:
    """
    Get detailed information about a specific tool.
    
    Args:
        tool_name: Name of the tool to get information for
        
    Returns:
        ToolInfo containing tool details
    """
    try:
        tool = tool_registry.get_tool(tool_name)
        if not tool:
            raise HTTPException(
                status_code=404, 
                detail=f"Tool '{tool_name}' not found"
            )
        
        return ToolInfo(
            name=tool.name,
            description=tool.description,
            parameters=tool.parameters
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting tool info: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve tool information")
