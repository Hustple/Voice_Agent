"""Configuration"""
import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self._config = {
            "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
            "WHISPER_MODEL": os.getenv("WHISPER_MODEL", "base"),
            "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
        }
    
    def get(self, key: str, default=None):
        return self._config.get(key, default)
