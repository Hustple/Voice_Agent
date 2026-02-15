"""Configuration Management with Validation"""
import os
from typing import Any
from dotenv import load_dotenv
from exceptions import ConfigurationError

class Config:
    """Application configuration with validation"""
    
    def __init__(self):
        load_dotenv()
        self._config = {
            "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
            "PFMCP_BASE_URL": os.getenv("PFMCP_BASE_URL", "http://localhost:8000"),
            "WHISPER_MODEL": os.getenv("WHISPER_MODEL", "base"),
            "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
        }
        self._validate()
    
    def _validate(self):
        """Validate required configuration"""
        if not self._config.get("GROQ_API_KEY"):
            raise ConfigurationError(
                "GROQ_API_KEY is required. Get it from https://console.groq.com"
            )
        
        valid_whisper_models = ["tiny", "base", "small", "medium", "large"]
        whisper_model = self._config.get("WHISPER_MODEL")
        if whisper_model not in valid_whisper_models:
            raise ConfigurationError(
                f"Invalid WHISPER_MODEL: {whisper_model}. "
                f"Must be one of: {valid_whisper_models}"
            )
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self._config.get(key, default)
