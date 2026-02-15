"""Groq LLM Provider"""
import os
from groq import Groq
from loguru import logger

class GroqProvider:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found")
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"  # ← UPDATED MODEL
        logger.info(f"Groq initialized: {self.model}")
    
    async def complete(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq error: {e}")
            raise
