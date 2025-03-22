"""Configuration settings for the application."""
import os
import sys
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

    def validate_critical_settings(self):
        """Validates that critical environment variables are set."""
        if not self.OPENAI_API_KEY:
            print("❌ Error: OPENAI_API_KEY environment variable is not set.")
            print("   This is required for the application to function.")
            print("   Please set this in your .env file or environment variables.")
            sys.exit(1)
        
        try:
            origins = self.ALLOWED_ORIGINS.split(",")
            if not origins or all(not origin.strip() for origin in origins):
                print("⚠️ Warning: ALLOWED_ORIGINS is empty. CORS may not work correctly.")
        except Exception:
            print("⚠️ Warning: ALLOWED_ORIGINS is not properly formatted.")
            
        if self.RATE_LIMIT_PER_MINUTE <= 0:
            print("⚠️ Warning: RATE_LIMIT_PER_MINUTE is set to 0 or less. Rate limiting is disabled.")
            
        print("✅ All critical environment variables validated!")

settings = Settings()

# Validate critical settings in non-test environments
if "pytest" not in sys.modules:
    settings.validate_critical_settings() 