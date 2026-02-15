"""Logger"""
import sys
from loguru import logger
from pathlib import Path

def setup_logger():
    logger.remove()
    logger.add(sys.stdout, format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>", level="INFO", colorize=True)
    Path("data/logs").mkdir(parents=True, exist_ok=True)
    logger.add("data/logs/agent.log", rotation="10 MB")
    return logger
