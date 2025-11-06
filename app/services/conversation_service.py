from typing import Dict, Any
import logging
from datetime import datetime
from bson.objectid import ObjectId

from app.utils.chat_utils import now_pt_iso
from app.db.mongodb import mongodb
from app.models.openai import openai_model
from app.agents.mobile_shopping_agent import create_mobile_shopping_agent
from app.Chat_Workflow.orchestrator import execute_mobile_shopping_workflow

logger = logging.getLogger(__name__)


class ConversationService:
    def __init__(self):
        self.mobile_agent = None
        self.collection_name = "conversations"
        self._initialized = False
    
    async def initialize(self):
        """
        Initialize the mobile shopping agent.
        This should be called once during application startup.
        """
        if self._initialized:
            return
        try:
            logger.info("Initializing mobile shopping agent...")
            text_llm = openai_model(reasoning=False, temperature=0.7)
            self.mobile_agent = create_mobile_shopping_agent(text_llm)
            self._initialized = True
            logger.info("Mobile shopping agent initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing ConversationService: {e}", exc_info=True)
            raise
    
    async def _ensure_initialized(self):
        """Ensure the service is initialized before use"""
        if not self._initialized:
            await self.initialize()
    
    def create_conversation(self, email: str) -> Dict[str, Any]:
        """
        Create a new conversation
        
        Args:
            email: User's email address
            
        Returns:
            Dict containing conversation_id, email, and created_at
        """
        try:
            collection = mongodb.get_collection(self.collection_name)
            conversation_data = {
                "email": email,
                "created_at": now_pt_iso(),
                "messages": []
            }
            
            result = collection.insert_one(conversation_data)
            conversation_id = str(result.inserted_id)
            
            return {
                "conversation_id": conversation_id,
                "email": email,
                "created_at": conversation_data["created_at"]
            }
        except Exception as e:
            logger.error(f"Error creating conversation: {e}")
            raise
    
    async def get_message_response(self, conversation_id: str, user_message: str) -> Dict[str, Any]:
        """
        Handle user message and return a response
        
        Args:
            conversation_id: Conversation ID
            user_message: User's message
            
        Returns:
            Dict containing conversation_id and response
        """
        # Ensure the service is initialized
        await self._ensure_initialized()
        
        try:
            # Verify that the conversation exists
            collection = mongodb.get_collection(self.collection_name)
            conversation = collection.find_one({"_id": ObjectId(conversation_id)})
            
            if not conversation:
                raise ValueError(f"Conversation with ID {conversation_id} not found")
            
            # Get the last 6 messages from the conversation history
            messages = conversation.get("messages", [])
            last_messages = messages[-6:] if len(messages) > 0 else []
            
            # Store the user message in the conversation history
            timestamp = now_pt_iso()
            collection.update_one(
                {"_id": ObjectId(conversation_id)},
                {"$push": {"messages": {
                    "role": "user",
                    "content": user_message,
                    "timestamp": timestamp
                }}}
            )
            
            # Use the mobile shopping workflow to generate a response
            logger.info(f"Processing message for conversation: {conversation_id}")
            payload = {
                "conversation_id": conversation_id,
                "user_message": user_message,
                "conversation_history": last_messages
            }
            
            result = await execute_mobile_shopping_workflow(agent=self.mobile_agent, payload=payload)
            logger.info(f"Workflow result: {result}")
            
            # Extract response text
            response_text = result.get("response", "I apologize, but I couldn't generate a response.")
            
            # Store the assistant response in the conversation history
            collection.update_one(
                {"_id": ObjectId(conversation_id)},
                {"$push": {"messages": {
                    "role": "assistant",
                    "content": response_text,
                    "timestamp": timestamp
                }}}
            )
            
            return {
                "conversation_id": conversation_id,
                "timestamp": timestamp,
                "response": response_text,
                "output": result.get("output"),
                "predicted_sql_query": result.get("predicted_sql_query"),
                "user_query": result.get("user_query")
            }
        except Exception as e:
            logger.error(f"Error handling message: {e}", exc_info=True)
            raise

# Singleton instance
conversation_service = ConversationService()