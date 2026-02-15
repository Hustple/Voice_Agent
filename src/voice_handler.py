"""Voice Handler - Text mode"""
from loguru import logger

class VoiceHandler:
    def __init__(self, config):
        logger.info("Voice Handler (text mode)")
    
    async def listen(self) -> str:
        return input("You: ")
    
    async def speak(self, text: str):
        print(f"Agent: {text}")
