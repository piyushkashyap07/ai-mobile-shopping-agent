import json
import logging
from typing import Dict, Any

from llama_index.core.agent.workflow import FunctionAgent, ToolCallResult, ToolCall
from llama_index.core.workflow import Context

from app.utils.chat_utils import format_conversation_history

logger = logging.getLogger(__name__)

def _serialize_recursively(data: Any) -> Any:
    """
    Recursively convert data to a BSON/JSON serializable format.
    Handles basic types, lists, dicts, and Pydantic models.
    Converts other types to their string representation.
    """
    # Handle None and primitives first
    if data is None or isinstance(data, (str, int, float, bool)):
        return data
    
    # Handle dict
    if isinstance(data, dict):
        return {key: _serialize_recursively(value) for key, value in data.items()}
    
    # Handle list/tuple
    if isinstance(data, (list, tuple)):
        return [_serialize_recursively(item) for item in data]
    
    # Try Pydantic models or objects with dict methods
    if hasattr(data, 'dict'):
        try:
            return _serialize_recursively(data.dict())
        except Exception:
            pass
    
    if hasattr(data, 'to_dict'):
        try:
            return _serialize_recursively(data.to_dict())
        except Exception:
            pass
    
    # For any other type (like FunctionTool), convert to string
    return str(data)

async def execute_mobile_shopping_workflow(agent: FunctionAgent, payload: Dict[str, Any]):
    """
    Execute the mobile shopping workflow using the FunctionAgent.
    
    Args:
        agent: The mobile shopping FunctionAgent
        payload: Dictionary containing conversation_id, user_message, and conversation_history
    
    Returns:
        Dictionary with response, tool_calls, output, and user_query
    """
    ctx = Context(agent)
    
    conversation_history = payload.get("conversation_history", [])
    user_message = payload.get("user_message", "")

    formatted_conversation_history = await format_conversation_history(conversation_history)
    formatted_payload = payload.copy()
    formatted_payload["conversation_history"] = formatted_conversation_history

    await ctx.store.set("payload", formatted_payload)
    
    # Build enhanced query with conversation history
    if formatted_conversation_history:
        enhanced_query = f"""
Conversation History:
{formatted_conversation_history}

Current User Query: 
{user_message}

Please help the user find their ideal mobile phone based on their needs.
"""
    else:
        enhanced_query = user_message
    
    handler = agent.run(enhanced_query, ctx=ctx)
    tool_calls_info = []

    async for event in handler.stream_events():
        if isinstance(event, ToolCall):
            tool_name = getattr(event, 'tool_name', None)
            tool_kwargs = getattr(event, 'tool_kwargs', None)
            
            logger.info(f"🔧 Tool Call: {tool_name} | Data Source: 📊 JSON Database")
            logger.info(f"   Arguments: {tool_kwargs}")
        if isinstance(event, ToolCallResult):
            tool_output = getattr(event, 'tool_output', None)
            serialized_output = _serialize_recursively(tool_output)

            tool_info = {
                'tool_name': getattr(event, 'tool_name', None),
                'tool_kwargs': _serialize_recursively(getattr(event, "tool_kwargs", None)),
                'tool_output': serialized_output,
            }
            tool_calls_info.append(tool_info)

    # Get the final result
    result = await handler

    # Extract response content
    if (hasattr(result, 'response') and 
        hasattr(result.response, 'blocks') and 
        result.response.blocks): 
        response_content = str(result.response.blocks[0].text)
    elif hasattr(result, 'response') and hasattr(result.response, 'text'):
        response_content = result.response.text
    else:
        response_content = str(result)

    # Extract tool outputs for mobile shopping tools
    output = None
    for tool_call in tool_calls_info:
        tool_name = tool_call.get("tool_name")
        tool_output_dict = tool_call.get("tool_output", {})
        
        # Extract results from mobile shopping tools
        if tool_name in ["search_mobile_phones", "compare_mobile_phones", "get_mobile_details"]:
            output = tool_output_dict
            logger.info(f"Tool {tool_name} returned {len(output.get('results', [])) if isinstance(output.get('results'), list) else 'N/A'} results")

    return {
        "response": response_content,
        "tool_calls": tool_calls_info,
        "output": output,
        "predicted_sql_query": None,  # Not used for mobile shopping
        "user_query": user_message,
    }


# Keep old function for backwards compatibility (if needed)
async def execute_workflow(bq_agent: FunctionAgent, payload: Dict[str, Any]):
    """
    Execute the query using the NoSQL agent with full schema context.
    DEPRECATED: Use execute_mobile_shopping_workflow instead.
    """
    return await execute_mobile_shopping_workflow(bq_agent, payload)