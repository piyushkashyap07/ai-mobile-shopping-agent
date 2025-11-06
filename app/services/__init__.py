from app.services.conversation_service import conversation_service
async def initialize_services():
    """Call this during application startup"""
    await conversation_service.initialize()