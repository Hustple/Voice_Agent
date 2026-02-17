# 🎙️ Voice-Enabled Invoice Agent

> AI-powered accounts receivable automation with natural voice interaction

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Groq](https://img.shields.io/badge/LLM-Groq%20LLaMA%203.1-orange.svg)](https://groq.com/)

A voice-controlled agent for managing overdue invoices, built with production-grade error handling, input validation, and enterprise-ready architecture patterns.

---

## 🎯 Project Overview

This project demonstrates an end-to-end implementation of a conversational AI agent that:
- Accepts voice commands through natural speech
- Understands user intent using LLM-powered classification
- Queries invoice data and generates personalized payment reminders
- Responds with voice output optimized for clarity (spelling out currency, emails, dates)

**Current Status**: Fully functional proof-of-concept with mock data layer, ready for production integration.

---

## ✨ Key Features

### 🎤 Voice Interface
- **Speech-to-Text**: OpenAI Whisper running locally (no API costs)
- **Text-to-Speech**: Google TTS with automatic cleanup
- **Audio Processing**: 5-second recording with 16kHz sampling
- **Resource Management**: Automatic temp file cleanup and error recovery

### 🤖 Intelligent Agent
- **Intent Classification**: Groq LLaMA 3.1 8B model for understanding commands
- **Entity Extraction**: Automatically identifies company names from natural language
- **Email Generation**: Creates polite, contextual payment reminders
- **Conversation Memory**: Maintains dialogue history for context-aware responses

### 🔒 Production-Ready Engineering
- **Input Validation**: Protection against injection attacks and malformed data
- **Error Handling**: Graceful degradation with custom exception hierarchy
- **Retry Logic**: Exponential backoff for LLM API failures
- **Logging**: Structured logging with rotation and colorized console output
- **Type Safety**: Pydantic models for data validation

### 🎯 Smart Formatting
- **Currency**: "500.50" → "500 dollars and 50 cents"
- **Email**: "john@acme.com" → "john at acme dot com"
- **Dates**: "2024-02-16" → "February 16, 2024"

---

## 🏗️ Architecture
```
┌─────────────┐
│   User      │
│   Voice     │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────────┐
│           VoiceHandler (voice_handler.py)       │
│  ┌─────────────────┐      ┌─────────────────┐  │
│  │  Whisper STT    │  →   │   gTTS TTS      │  │
│  └─────────────────┘      └─────────────────┘  │
└──────┬──────────────────────────────▲───────────┘
       │                               │
       ▼                               │
┌─────────────────────────────────────────────────┐
│           InvoiceAgent (agent.py)               │
│  ┌─────────────────────────────────────────┐   │
│  │  • Intent Classification                │   │
│  │  • Entity Extraction                    │   │
│  │  • Conversation Management              │   │
│  │  • Response Generation                  │   │
│  └─────────────────────────────────────────┘   │
└──────┬──────────────────┬───────────────────────┘
       │                  │
       ▼                  ▼
┌──────────────┐   ┌──────────────────┐
│ GroqProvider │   │  MockMCPClient   │
│ (LLaMA 3.1)  │   │  (Data Layer)    │
└──────────────┘   └──────────────────┘
```

**Flow**: Voice Input → Transcription → Intent Classification → Data Retrieval → Response Generation → Voice Output

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (tested on 3.10)
- **ffmpeg** - required for audio processing
```bash
  # macOS
  brew install ffmpeg

  # Ubuntu/Debian
  sudo apt-get install ffmpeg

  # Windows - Download from https://ffmpeg.org/download.html
```
- **Microphone and speakers** for voice interaction

### Installation
```bash
# 1. Clone repository
git clone https://github.com/Hustple/Voice_Agent.git
cd Voice_Agent

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### Getting Your Groq API Key (Free)

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to API Keys section
4. Create new API key
5. Add to `.env` file:
```
   GROQ_API_KEY=gsk_your_key_here
```

### Running the Agent

**Voice Mode** (recommended):
```bash
python src/main.py
```

**Text Mode** (for testing without microphone):
```bash
python src/main_text.py
```

---

## 💬 Usage Examples

### Voice Commands

**Check Invoices**:
- "Check overdue invoices"
- "Show me past due invoices"
- "What invoices are overdue?"

**Send Reminders**:
- "Send reminder to Acme Corp"
- "Email Beta Industries about their invoice"
- "Remind XYZ Company about payment"

**Exit**:
- "Exit" / "Quit" / "Goodbye"

### Sample Interaction
```
🎤 Listening...
👤 You: Check overdue invoices

🤖 Agent: You have 2 overdue invoices, totaling 1100 dollars. 
Acme Corp, 500 dollars, due February 6, 2024. 
Beta Industries, 600 dollars, due February 1, 2024.

🎤 Listening...
👤 You: Send reminder to Acme Corp

🤖 Agent: Email sent to Acme Corp at john at acme dot com.
```

---

## 📁 Project Structure
```
Voice_Agent/
├── src/
│   ├── agent.py              # Core agent logic with invoice handling
│   ├── voice_handler.py      # Voice I/O with Whisper & gTTS
│   ├── llm_provider.py       # Groq API client with retry logic
│   ├── mcp_client_mock.py    # Mock data layer (Stripe/Gmail simulation)
│   ├── main.py               # Voice mode entry point
│   ├── main_text.py          # Text-only mode entry point
│   ├── constants.py          # Application constants
│   ├── exceptions.py         # Custom exception hierarchy
│   │
│   ├── prompts/
│   │   ├── system_prompts.py # LLM system prompts
│   │   └── templates.py      # Email templates
│   │
│   └── utils/
│       ├── config.py         # Configuration management
│       ├── validators.py     # Input validation & sanitization
│       ├── formatters.py     # Voice-optimized formatting
│       └── logger.py         # Structured logging setup
│
├── scripts/                  # Setup and deployment scripts
├── requirements.txt          # Python dependencies
├── .env                    # Environment variables template
└── README.md                 # This file
```

---

## 🔧 Configuration

### Environment Variables
```bash
# Required
GROQ_API_KEY=gsk_xxxxx           # Get from console.groq.com

# Optional
WHISPER_MODEL=base               # Options: tiny, base, small, medium, large
LOG_LEVEL=INFO                   # Options: DEBUG, INFO, WARNING, ERROR
PFMCP_BASE_URL=http://localhost  # For future MCP integration
```

### Whisper Model Selection

| Model  | Size   | Speed    | Accuracy  | Use Case                  |
|--------|--------|----------|-----------|---------------------------|
| tiny   | 39 MB  | Fastest  | Good      | Testing, low-resource     |
| base   | 74 MB  | Fast     | Better    | **Recommended default**   |
| small  | 244 MB | Moderate | Great     | Production quality        |
| medium | 769 MB | Slow     | Excellent | High accuracy requirement |
| large  | 1.5 GB | Slowest  | Best      | Maximum quality           |

---

## 🧪 Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_agent.py -v
```

---

## 🛠️ Technical Deep Dive

### LLM Integration

The project uses **Groq** with the **LLaMA 3.1 8B** model for:

1. **Intent Classification** (50 tokens, temp=0.1) — classifies into `check_invoices`, `send_reminder`, `help`, `other`
2. **Entity Extraction** (50 tokens, temp=0.0) — extracts company names from natural language
3. **Email Generation** (400 tokens, temp=0.7) — creates contextual payment reminders

### Error Handling Strategy
```python
AgentException
├── LLMError           # LLM API failures
├── MCPError           # Data layer issues
├── VoiceInputError    # Audio processing problems
├── ValidationError    # Input sanitization failures
└── ConfigurationError # Missing/invalid config
```

Each layer catches specific exceptions and provides user-friendly error messages while logging technical details.

### Input Validation

- **Injection attacks**: Regex patterns block `<script>`, `javascript:`, etc.
- **Length validation**: Max 500 chars for input, 100 for company names
- **Character whitelist**: Only alphanumeric + safe punctuation for company names
- **Email safety**: Content scanning before sending

---

## 🚧 Roadmap

**Phase 1: Production Data Integration**
- [ ] Real Stripe API integration
- [ ] Gmail OAuth implementation
- [ ] Database for conversation history

**Phase 2: Enhanced Features**
- [ ] Multi-language support
- [ ] Batch reminder sending
- [ ] Scheduled reminder campaigns

**Phase 3: Deployment**
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Cloud deployment (AWS/GCP)

---

## 👤 Author

- **GitHub**: [@Hustple](https://github.com/Hustple)
- **Project**: [Voice_Agent](https://github.com/Hustple/Voice_Agent)

---
