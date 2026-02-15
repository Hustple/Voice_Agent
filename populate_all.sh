#!/bin/bash

echo "🚀 Populating all source files..."

cd ~/Desktop/peakflo_project

# 1. Main.py
cat > src/main.py << 'MAIN_EOF'
"""
Invoice Reminder Agent - Main Entry Point
"""
import asyncio
import os
from rich.console import Console
from rich.panel import Panel
from dotenv import load_dotenv

from voice_handler import VoiceHandler
from agent import InvoiceAgent
from utils.logger import setup_logger
from utils.config import Config

load_dotenv()
console = Console()
logger = setup_logger()

async def main():
    console.print(Panel.fit(
        "[bold cyan]🎙️ Invoice Reminder Agent[/bold cyan]\n"
        "[dim]Voice-enabled AR automation[/dim]\n\n"
        "Commands:\n"
        "  • 'Check overdue invoices'\n"
        "  • 'Send reminder to [company name]'\n"
        "  • 'Exit' to quit",
        title="Welcome",
        border_style="cyan"
    ))
    
    try:
        config = Config()
        voice = VoiceHandler(config)
        agent = InvoiceAgent(config)
        logger.info("Agent initialized")
        console.print("✅ [green]Ready![/green]\n")
    except Exception as e:
        console.print(f"❌ [red]Error: {e}[/red]")
        return
    
    while True:
        try:
            console.print("\n[yellow]🎤 Listening...[/yellow]")
            user_input = await voice.listen()
            
            if not user_input:
                continue
            
            console.print(f"[bold]👤 You:[/bold] {user_input}")
            
            if any(word in user_input.lower() for word in ['exit', 'quit', 'bye']):
                farewell = "Goodbye!"
                console.print(f"[bold]🤖 Agent:[/bold] {farewell}")
                await voice.speak(farewell)
                break
            
            response = await agent.process(user_input)
            console.print(f"[bold]🤖 Agent:[/bold] {response}")
            await voice.speak(response)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[red]❌ {e}[/red]")

if __name__ == "__main__":
    asyncio.run(main())
MAIN_EOF

echo "✅ main.py created"

# 2. Agent.py
cat > src/agent.py << 'AGENT_EOF'
"""Invoice Agent - Core logic"""
from typing import Optional
from pydantic import BaseModel
from loguru import logger

from llm_provider import GroqProvider
from mcp_client_mock import MockMCPClient
from utils.formatters import format_currency_for_voice, format_email_for_voice, format_date_for_voice
from prompts.system_prompts import SystemPrompts
from prompts.templates import EmailTemplates

class Invoice(BaseModel):
    id: str
    customer_name: str
    customer_email: str
    amount: float
    due_date: str
    status: str
    days_overdue: int = 0

class InvoiceAgent:
    def __init__(self, config):
        self.config = config
        self.llm = GroqProvider()
        self.mcp = MockMCPClient(config)
        logger.info("Agent initialized")
    
    async def process(self, user_input: str) -> str:
        intent = await self._classify_intent(user_input)
        
        if intent == "check_invoices":
            return await self._handle_check_invoices()
        elif intent == "send_reminder":
            company = await self._extract_company_name(user_input)
            if company:
                return await self._handle_send_reminder(company)
            return "Which company should I send a reminder to?"
        else:
            return "I can check invoices or send reminders. What would you like?"
    
    async def _classify_intent(self, text: str) -> str:
        prompt = SystemPrompts.INTENT_CLASSIFICATION.format(user_input=text)
        response = await self.llm.complete(prompt, max_tokens=50, temperature=0.1)
        intent = response.strip().lower()
        valid = ["check_invoices", "send_reminder", "help", "other"]
        return intent if intent in valid else "other"
    
    async def _handle_check_invoices(self) -> str:
        try:
            invoices_data = await self.mcp.call_tool("stripe", "list_invoices", {"status": "past_due"})
            
            if not invoices_data:
                return "No overdue invoices!"
            
            invoices = [Invoice(**inv) for inv in invoices_data]
            total = sum(inv.amount for inv in invoices)
            
            response = f"You have {len(invoices)} overdue invoice"
            response += "s" if len(invoices) > 1 else ""
            response += f", totaling {format_currency_for_voice(total)}. "
            
            for inv in invoices[:3]:
                response += f"{inv.customer_name}, {format_currency_for_voice(inv.amount)}, "
                response += f"due {format_date_for_voice(inv.due_date)}. "
            
            return response
        except Exception as e:
            logger.error(f"Error: {e}")
            return "Error fetching invoices."
    
    async def _handle_send_reminder(self, company_name: str) -> str:
        try:
            invoice_data = await self.mcp.call_tool("stripe", "search_invoices", 
                {"customer_name": company_name, "status": "past_due"})
            
            if not invoice_data:
                return f"No overdue invoices for {company_name}."
            
            invoice = Invoice(**invoice_data[0])
            email_body = await self._generate_reminder_email(invoice)
            
            await self.mcp.call_tool("gmail", "send_email", {
                "to": invoice.customer_email,
                "subject": f"Payment Reminder - Invoice {invoice.id}",
                "body": email_body
            })
            
            return f"Email sent to {company_name} at {format_email_for_voice(invoice.customer_email)}."
        except Exception as e:
            logger.error(f"Error: {e}")
            return "Error sending reminder."
    
    async def _generate_reminder_email(self, invoice: Invoice) -> str:
        prompt = EmailTemplates.PAYMENT_REMINDER.format(
            customer_name=invoice.customer_name, invoice_id=invoice.id,
            amount=invoice.amount, due_date=invoice.due_date, days_overdue=invoice.days_overdue
        )
        return await self.llm.complete(prompt, max_tokens=400, temperature=0.7)
    
    async def _extract_company_name(self, text: str) -> Optional[str]:
        prompt = f'Extract company name from: "{text}". Return only the name or "NONE".'
        company = await self.llm.complete(prompt, max_tokens=50, temperature=0)
        return None if company.strip() == "NONE" else company.strip()
AGENT_EOF

echo "✅ agent.py created"

# 3. LLM Provider
cat > src/llm_provider.py << 'LLM_EOF'
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
        self.model = "llama-3.1-70b-versatile"
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
LLM_EOF

echo "✅ llm_provider.py created"

# 4. Mock MCP Client
cat > src/mcp_client_mock.py << 'MCP_EOF'
"""Mock MCP Client"""
from typing import Dict, Any, Optional
from loguru import logger
from datetime import datetime, timedelta

class MockMCPClient:
    def __init__(self, config):
        logger.info("✅ Mock MCP (no server needed)")
    
    async def call_tool(self, server: str, tool: str, params: Optional[Dict] = None) -> Any:
        logger.info(f"[MOCK] {server}/{tool}")
        
        if server == "stripe" and "invoice" in tool.lower():
            return [
                {"id": "inv_001", "customer_name": "Acme Corp", 
                 "customer_email": "john@acme.com", "amount": 500.00,
                 "due_date": (datetime.now() - timedelta(days=10)).isoformat(),
                 "status": "past_due", "days_overdue": 10},
                {"id": "inv_002", "customer_name": "Beta Industries",
                 "customer_email": "jane@beta.com", "amount": 600.00,
                 "due_date": (datetime.now() - timedelta(days=15)).isoformat(),
                 "status": "past_due", "days_overdue": 15}
            ]
        elif server == "gmail":
            return {"status": "sent", "to": params.get("to")}
        return {"status": "ok"}
MCP_EOF

echo "✅ mcp_client_mock.py created"

# 5. Voice Handler
cat > src/voice_handler.py << 'VOICE_EOF'
"""Voice Handler - Text mode"""
from loguru import logger

class VoiceHandler:
    def __init__(self, config):
        logger.info("Voice Handler (text mode)")
    
    async def listen(self) -> str:
        return input("You: ")
    
    async def speak(self, text: str):
        print(f"Agent: {text}")
VOICE_EOF

echo "✅ voice_handler.py created"

# 6. Utils - Config
cat > src/utils/config.py << 'CONFIG_EOF'
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
CONFIG_EOF

echo "✅ config.py created"

# 7. Utils - Logger
cat > src/utils/logger.py << 'LOGGER_EOF'
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
LOGGER_EOF

echo "✅ logger.py created"

# 8. Utils - Formatters
cat > src/utils/formatters.py << 'FORMATTER_EOF'
"""Formatters"""
from datetime import datetime

def format_currency_for_voice(amount: float) -> str:
    dollars = int(amount)
    cents = int((amount - dollars) * 100)
    return f"{dollars} dollars and {cents} cents" if cents > 0 else f"{dollars} dollars"

def format_email_for_voice(email: str) -> str:
    return email.replace("@", " at ").replace(".", " dot ")

def format_date_for_voice(date_str: str) -> str:
    try:
        date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return date_obj.strftime("%B %d, %Y")
    except:
        return date_str
FORMATTER_EOF

echo "✅ formatters.py created"

# 9. Prompts - System
cat > src/prompts/system_prompts.py << 'PROMPT_EOF'
"""System Prompts"""

class SystemPrompts:
    INTENT_CLASSIFICATION = """Classify: "{user_input}"
Categories: check_invoices, send_reminder, help, other
Return only the category."""
PROMPT_EOF

echo "✅ system_prompts.py created"

# 10. Prompts - Templates
cat > src/prompts/templates.py << 'TEMPLATE_EOF'
"""Templates"""

class EmailTemplates:
    PAYMENT_REMINDER = """Write polite payment reminder:
Customer: {customer_name}
Invoice: {invoice_id}
Amount: ${amount}
Due: {due_date}
Days Overdue: {days_overdue}
Keep it under 200 words."""
TEMPLATE_EOF

echo "✅ templates.py created"

# 11. Text-only main
cat > src/main_text.py << 'TEXT_EOF'
"""Text-only version"""
import asyncio
from agent import InvoiceAgent
from utils.config import Config
from utils.logger import setup_logger
from rich.console import Console

console = Console()
logger = setup_logger()

async def main():
    console.print("[cyan]🤖 Invoice Agent (Text Mode)[/cyan]\n")
    config = Config()
    agent = InvoiceAgent(config)
    console.print("Commands: 'check invoices', 'send reminder to [company]', 'exit'\n")
    
    while True:
        user_input = console.input("[yellow]You:[/yellow] ")
        if user_input.lower() in ['exit', 'quit']:
            console.print("[cyan]Goodbye![/cyan]")
            break
        response = await agent.process(user_input)
        console.print(f"[green]Agent:[/green] {response}\n")

if __name__ == "__main__":
    asyncio.run(main())
TEXT_EOF

echo "✅ main_text.py created"

echo ""
echo "🎉 All files created successfully!"
echo ""
echo "Next steps:"
echo "1. Add GROQ_API_KEY to .env"
echo "2. Run: python src/main_text.py"

