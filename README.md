# Invoice Reminder Agent 🎙️💸

> Voice-enabled AR automation using Claude, Groq & pfMCP - 100% Free!

## 🎥 Demo

[Link to demo video]

## ✨ Features

- ✅ Voice input/output (Whisper + gTTS - FREE)
- ✅ Checks overdue invoices (Stripe MCP)
- ✅ Sends email reminders (Gmail MCP)
- ✅ Natural language processing (Groq LLaMA - FREE)
- ✅ Voice-optimized responses (spells out numbers, emails)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- ffmpeg (for audio processing)
- Microphone & speakers

### Installation
```bash
# 1. Clone repository
git clone <your-repo-url>
cd invoice-reminder-agent

# 2. Run setup script
./scripts/setup.sh

# 3. Configure environment
cp .env
# Edit .env and add your GROQ_API_KEY

# 4. Run the agent
./scripts/run.sh
```

## 🔑 Getting API Keys

### Groq API (FREE)
1. Go to https://console.groq.com
2. Sign up for free account
3. Create API key
4. Add to `.env`: `GROQ_API_KEY=gsk_xxxxx`

### Stripe Test Key (FREE)
1. Go to https://stripe.com
2. Sign up for free account
3. Get test API key from dashboard
4. Add to `.env`: `STRIPE_API_KEY=sk_test_xxxxx`

### Gmail OAuth (FREE)
1. Go to Google Cloud Console
2. Create OAuth credentials
3. Add credentials to `.env`

## �� Usage

Start the agent:
```bash
./scripts/run.sh
```

Voice commands:
- **"Check overdue invoices"** - Lists all overdue invoices
- **"Send reminder to [Company Name]"** - Sends payment reminder email
- **"Exit"** - Quit the agent

## 🏗️ Architecture
```
User Voice → Whisper (STT) → Groq LLaMA (Intent) → pfMCP (Data) → Groq (Generate) → gTTS (TTS) → User Hears
```

## 🛠️ Tech Stack

- **LLM**: Groq (LLaMA 3.1) - FREE
- **Speech-to-Text**: OpenAI Whisper (local) - FREE
- **Text-to-Speech**: Google gTTS - FREE
- **Integrations**: pfMCP servers (Stripe, Gmail)

## 📁 Project Structure
```
invoice-reminder-agent/
├── src/              # Source code
├── tests/            # Tests
├── scripts/          # Setup/run scripts
├── data/             # Runtime data
└── docs/             # Documentation
```

## 🧪 Testing
```bash
# Run all tests
pytest

# Test MCP connection
python scripts/test_mcp.py
```

## 🤝 Contributing

This project was built as part of a Peakflo ML Engineer internship application.

## 📄 License

MIT License

## 👤 Author

[Your Name]
- Email: your.email@example.com
- GitHub: @yourusername

---

Built for Peakflo ML Engineer Intern Application 🚀
