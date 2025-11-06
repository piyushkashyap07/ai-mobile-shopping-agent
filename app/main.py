from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.api import api_router
from app.db.mongodb import mongodb
from app.services import initialize_services
from app.services.mobile_data_service import initialize_mobile_data_service
from app.utils import log

import logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Mobile Shopping Chat Agent...")
    
    # Connect to MongoDB
    print("Connecting to MongoDB...")
    try:
        mongodb.connect_to_mongodb()
        print("Connected to MongoDB successfully")
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}", exc_info=True)
        raise
    
    # Initialize mobile data service (loads JSON)
    print("Loading mobile phone data from JSON...")
    try:
        initialize_mobile_data_service()
        print("Mobile phone data loaded successfully")
    except Exception as e:
        logger.error(f"Error loading mobile data: {e}", exc_info=True)
        raise
    
    # Initialize conversation service (creates agent)
    print("Initializing mobile shopping agent...")
    await initialize_services()
    print("Mobile shopping agent initialized successfully")
    
    logger.info("Application startup complete")
    
    yield
    
    # Shutdown
    print("Shutting down...")
    mongodb.close_mongodb_connection()
    print("MongoDB connection closed")
    logger.info("Application shutdown complete")

def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
        lifespan=lifespan
    )

    # Add CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API router
    application.include_router(api_router, prefix=settings.API_PREFIX)

    @application.get("/")
    async def root():
        print(f"Welcome to {settings.APP_NAME}!")
        return {
            "message": f"Welcome to {settings.APP_NAME}!",
            "description": "AI-powered mobile phone shopping assistant for Indian market",
            "market": "India",
            "currency": "INR (₹)",
            "endpoints": {
                "health": "/health",
                "api": settings.API_PREFIX,
                "docs": "/docs"
            }
        }

    @application.get("/health")
    async def health_check():
        return {"status": "healthy"}

    return application

app = create_application() 