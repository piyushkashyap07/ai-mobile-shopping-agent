import os
import uuid
import shutil
import logging
from fastapi import APIRouter, HTTPException, status, File, UploadFile
from fastapi.responses import JSONResponse
# from app.utils.embeddings import load_and_upload_data
from app.services.conversation_service import conversation_service
from app.schemas.conversation import (
    ConversationCreate, 
    ConversationResponse, 
    MessageCreate, 
    MessageResponse
)

# Configure logger
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(conversation_data: ConversationCreate):
    """
    Create a new conversation
    
    Takes a user's email and creates a new conversation with a unique ID.
    """
    try:
        result = conversation_service.create_conversation(conversation_data.email)
        return result
    except Exception as e:
        logger.error(f"Failed to create conversation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create conversation: {str(e)}"
        )


@router.post("/message", response_model=MessageResponse)
async def send_message(message_data: MessageCreate):
    """
    Send a message to an existing conversation
    
    Takes a conversation ID and user message, returns a response.
    """
    try:
        result = await conversation_service.get_message_response(
            message_data.conversation_id,
            message_data.user_message
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to process message: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process message: {str(e)}"
        ) 