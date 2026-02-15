"""Groq LLM Provider with retry logic"""
import os
import asyncio
from groq import Groq
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

from exceptions import LLMError
from constants import (
    GROQ_MODEL, MAX_RETRIES, RETRY_MIN_WAIT, RETRY_MAX_WAIT
)

class GroqProvider:
    """Groq LLM provider with proper async and retry"""
    
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found")
        self.client = Groq(api_key=api_key)
        self.model = GROQ_MODEL
        logger.info(f"Groq initialized: {self.model}")
    
    @retry(
        stop=stop_after_attempt(MAX_RETRIES),
        wait=wait_exponential(multiplier=1, min=RETRY_MIN_WAIT, max=RETRY_MAX_WAIT),
        reraise=True
    )
    async def complete(
        self, 
        prompt: str, 
        max_tokens: int = 1000, 
        temperature: float = 0.7
    ) -> str:
        """Generate completion with retry logic"""
        try:
            # Run in executor for proper async
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
            )
            
            result = response.choices[0].message.content
            logger.debug(f"Groq response: {result[:100]}...")
            return result
            
        except Exception as e:
            logger.error(f"Groq API error: {e}")
            raise LLMError(f"Failed to get LLM response: {str(e)}")
