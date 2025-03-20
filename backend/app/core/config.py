"""Configuration settings for the application."""
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    """Application settings."""
    # OpenAI settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-2024-08-06")
    
    # Token cost settings (per token)
    COST_PER_INPUT_TOKEN: float = 0.00001  # $0.01 per 1K input tokens
    COST_PER_OUTPUT_TOKEN: float = 0.00003  # $0.03 per 1K output tokens
    
    # API settings
    API_HOST: str = os.getenv("API_HOST", "localhost")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # CORS settings
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields in the settings

settings = Settings() 