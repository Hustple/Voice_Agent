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
