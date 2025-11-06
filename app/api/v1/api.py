from fastapi import APIRouter
from app.api.v1.endpoints import health, conversation

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(conversation.router, prefix="/conversation", tags=["conversation"])

# Evaluation and chart endpoints removed - not required for mobile shopping agent 