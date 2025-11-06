from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime


class ConversationCreate(BaseModel):
    email: EmailStr = Field(..., description="User's email address")


class ConversationResponse(BaseModel):
    conversation_id: str = Field(..., description="Unique conversation ID")
    email: EmailStr = Field(..., description="User's email address")
    created_at: datetime = Field(..., description="Conversation creation timestamp")


class MessageCreate(BaseModel):
    conversation_id: str = Field(..., description="Conversation ID")
    user_message: str = Field(..., description="User's message")


class MessageResponse(BaseModel):
    conversation_id: str = Field(..., description="Conversation ID")
    response: str = Field(..., description="Bot response message")
    output: Optional[Any] = Field(None, description="Output from tool calls")
    predicted_sql_query: Optional[str] = Field(None, description="Predicted SQL query from")
    user_query: Optional[str] = Field(None, description="User's original query")
    timestamp: datetime = Field(..., description="Response timestamp")


class ChartGenerationRequest(BaseModel):
    conversation_id: str = Field(..., description="Conversation ID")
    user_query: str = Field(..., description="User's original query")
    response: str = Field(..., description="Bot response message")
    output: Optional[Any] = Field(None, description="Output from tool calls")
    predicted_sql_query: Optional[str] = Field(None, description="Predicted SQL query (optional)")


class ChartGenerationResponse(BaseModel):
    conversation_id: str = Field(..., description="Conversation ID")
    chart_config: Dict[str, Any] = Field(..., description="Chart.js configuration object")
    chart_type: str = Field(..., description="Type of chart generated (bar, line, pie, etc.)")
    chart_title: str = Field(..., description="Chart title") 