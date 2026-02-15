"""Application constants"""

# Voice settings
MAX_RECORDING_DURATION = 5  # seconds
SAMPLE_RATE = 16000  # Hz

# Agent settings
MAX_USER_INPUT_LENGTH = 500  # characters
MAX_INVOICES_TO_DISPLAY = 3
MAX_COMPANY_NAME_LENGTH = 100

# LLM settings
GROQ_MODEL = "mixtral-8x7b-32768"
MAX_TOKENS_INTENT = 50
MAX_TOKENS_EMAIL = 400
MAX_TOKENS_COMPANY = 50

# Retry settings
MAX_RETRIES = 3
RETRY_MIN_WAIT = 2  # seconds
RETRY_MAX_WAIT = 10  # seconds

# Audio settings
AUDIO_FORMAT = "mp3"
VOICE_LANGUAGE = "en"
