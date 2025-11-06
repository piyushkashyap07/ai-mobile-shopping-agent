from fastapi import APIRouter, Depends, HTTPException, status
from app.core.config import settings
import os

router = APIRouter()

@router.get("/")
async def health_check():
    """
    Health check endpoint to verify API is running
    """
    print("Health check endpoint called ================================")
    return {
        "status": "ok",
        "message": "Service is healthy"
    }

@router.get("/details")
async def health_details():
    """
    Detailed health check with more information
    """
    # Check if API keys are set
    openai_key_status = "configured" if settings.OPENAI_API_KEY else "not configured"
    
    # Check if mobile data service is initialized
    try:
        from app.services.mobile_data_service import mobile_data_service
        mobile_data_status = "initialized" if mobile_data_service is not None else "not initialized"
        if mobile_data_service:
            stats = mobile_data_service.get_statistics()
            mobile_data_info = {
                "total_mobiles": stats.get("total_mobiles", 0),
                "total_brands": stats.get("total_brands", 0)
            }
        else:
            mobile_data_info = None
    except Exception as e:
        mobile_data_status = f"error: {str(e)}"
        mobile_data_info = None
    
    return {
        "status": "ok",
        "details": {
            "openai_api": openai_key_status,
            "mobile_data_service": mobile_data_status,
            "mobile_data": mobile_data_info,
            "environment": settings.ENVIRONMENT,
            "app_name": settings.APP_NAME
        }
    }