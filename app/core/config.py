from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = os.getenv("APP_NAME", "Mobile Shopping Chat Agent - India")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    API_PREFIX: str = os.getenv("API_PREFIX", "/api/v1")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # OpenAI settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Mobile Data JSON path
    MOBILE_DATA_JSON_PATH: str = os.getenv("MOBILE_DATA_JSON_PATH", "mobile_phones_data.json")
    
    # MongoDB settings (required for conversation storage)
    MONGODB_URI: str = os.getenv("MONGODB_URI", "")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "mobile_shopping_chatbot")
    
    # API version
    API_VERSION: str = os.getenv("API_VERSION", "1.0.0")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Ignore extra environment variables (like legacy Tavily settings)

# Create a global settings instance
settings = Settings()