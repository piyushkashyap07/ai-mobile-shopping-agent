import logging
from typing import Dict, Any, List
from datetime import datetime, timezone, timedelta
import pytz
import json

logger = logging.getLogger(__name__)

async def format_conversation_history(messages: List[Dict[str, Any]]) -> str:
    """
    Format the conversation history into a single string, suitable for LLM context.

    Args:
        messages: List of message objects from the database

    Returns:
        A formatted conversation history string
    """
    formatted_history = ""
    
    for message in messages:
        role = message.get("role", "user")
        # Content is always a string in our MongoDB storage
        content = message.get("content", "")
        
        # Handle case where content might be a dict (legacy) or string (current)
        if isinstance(content, dict):
            content = content.get("response", str(content))
        elif not isinstance(content, str):
            content = str(content)
        
        formatted_history += f"{role}: {content}\n"
    
    return formatted_history

async def format_schema_context(table_schemas: Dict[str, Any]) -> str:
    """Helper function to format table schemas for context"""
    if not table_schemas:
        logger.warning("No table schemas provided for context.")
        return ""
    schema_context = "\n\n".join([
        f"**{table_name} SCHEMA:**\n{schema_content}"
        for table_name, schema_content in table_schemas.items()
    ])
    return schema_context

async def extract_json_from_llm_response(response_text: str):
    """Helper method to extract JSON from LLM responses"""
    try:
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        if json_start != -1 and json_end != -1:
            json_str = response_text[json_start:json_end]
            return json.loads(json_str)
        return None
    except Exception as e:
        logger.error(f"Error extracting JSON: {e}")
        return None

def log_conversation(conversation_id: str, user_message: str, bot_response: str) -> None:
    """
    Log the conversation for debugging and monitoring purposes.
    
    Args:
        conversation_id: The conversation ID
        user_message: The user's message
        bot_response: The bot's response
    """
    logger.info(f"Conversation {conversation_id}: User: {user_message}")
    logger.info(f"Conversation {conversation_id}: Bot: {bot_response}")

def now_pt_iso():
    pacific = pytz.timezone("America/Los_Angeles")
    return datetime.now(pacific).isoformat()