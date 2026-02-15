"""Invoice Agent - Core logic with validation and error handling"""
from typing import Optional
from pydantic import BaseModel
from loguru import logger

from llm_provider import GroqProvider
from mcp_client_mock import MockMCPClient
from utils.formatters import (
    format_currency_for_voice,
    format_email_for_voice, 
    format_date_for_voice
)
from utils.validators import (
    validate_user_input,
    validate_company_name,
    validate_email_content
)
from prompts.system_prompts import SystemPrompts
from prompts.templates import EmailTemplates
from exceptions import ValidationError, LLMError, MCPError
from constants import MAX_INVOICES_TO_DISPLAY, MAX_TOKENS_INTENT

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
        self.conversation_history = []
        logger.info("Agent initialized")
    
    async def process(self, user_input: str) -> str:
        """Process user request with validation"""
        try:
            # Validate input
            user_input = validate_user_input(user_input)
            
            # Add to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Classify intent
            intent = await self._classify_intent(user_input)
            
            # Route to handler
            if intent == "check_invoices":
                response = await self._handle_check_invoices()
            elif intent == "send_reminder":
                company = await self._extract_company_name(user_input)
                if company:
                    response = await self._handle_send_reminder(company)
                else:
                    response = "Which company should I send a reminder to?"
            else:
                response = "I can check invoices or send reminders. What would you like?"
            
            # Add response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })
            
            return response
            
        except ValidationError as e:
            logger.warning(f"Validation error: {e}")
            return f"Invalid input: {str(e)}"
        except LLMError as e:
            logger.error(f"LLM error: {e}")
            return "I'm having trouble understanding. Please try again."
        except MCPError as e:
            logger.error(f"MCP error: {e}")
            return "I'm having trouble accessing invoice data. Please try again."
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return "An unexpected error occurred. Please try again."
    
    async def _classify_intent(self, text: str) -> str:
        """Classify user intent"""
        prompt = SystemPrompts.INTENT_CLASSIFICATION.format(user_input=text)
        response = await self.llm.complete(
            prompt, 
            max_tokens=MAX_TOKENS_INTENT,
            temperature=0.1
        )
        
        intent = response.strip().lower()
        valid = ["check_invoices", "send_reminder", "help", "other"]
        return intent if intent in valid else "other"
    
    async def _handle_check_invoices(self) -> str:
        """Fetch and report overdue invoices"""
        try:
            invoices_data = await self.mcp.call_tool(
                "stripe", "list_invoices", {"status": "past_due"}
            )
            
            if not invoices_data:
                return "No overdue invoices!"
            
            invoices = [Invoice(**inv) for inv in invoices_data]
            total = sum(inv.amount for inv in invoices)
            
            response = f"You have {len(invoices)} overdue invoice"
            response += "s" if len(invoices) > 1 else ""
            response += f", totaling {format_currency_for_voice(total)}. "
            
            # Show top N invoices
            for inv in invoices[:MAX_INVOICES_TO_DISPLAY]:
                response += (
                    f"{inv.customer_name}, "
                    f"{format_currency_for_voice(inv.amount)}, "
                    f"due {format_date_for_voice(inv.due_date)}. "
                )
            
            if len(invoices) > MAX_INVOICES_TO_DISPLAY:
                response += f"And {len(invoices) - MAX_INVOICES_TO_DISPLAY} more. "
            
            return response
            
        except Exception as e:
            logger.error(f"Error fetching invoices: {e}")
            raise MCPError("Failed to fetch invoice data")
    
    async def _handle_send_reminder(self, company_name: str) -> str:
        """Send payment reminder email"""
        try:
            # Validate company name
            company_name = validate_company_name(company_name)
            
            invoice_data = await self.mcp.call_tool(
                "stripe", "search_invoices",
                {"customer_name": company_name, "status": "past_due"}
            )
            
            if not invoice_data:
                return f"No overdue invoices for {company_name}."
            
            invoice = Invoice(**invoice_data[0])
            email_body = await self._generate_reminder_email(invoice)
            
            # Validate email content
            if not validate_email_content(email_body):
                raise ValidationError("Generated email content failed validation")
            
            await self.mcp.call_tool("gmail", "send_email", {
                "to": invoice.customer_email,
                "subject": f"Payment Reminder - Invoice {invoice.id}",
                "body": email_body
            })
            
            return (
                f"Email sent to {company_name} at "
                f"{format_email_for_voice(invoice.customer_email)}."
            )
            
        except ValidationError as e:
            raise
        except Exception as e:
            logger.error(f"Error sending reminder: {e}")
            raise MCPError("Failed to send reminder")
    
    async def _generate_reminder_email(self, invoice: Invoice) -> str:
        """Generate polite payment reminder"""
        prompt = EmailTemplates.PAYMENT_REMINDER.format(
            customer_name=invoice.customer_name,
            invoice_id=invoice.id,
            amount=invoice.amount,
            due_date=invoice.due_date,
            days_overdue=invoice.days_overdue
        )
        return await self.llm.complete(prompt, max_tokens=400, temperature=0.7)
    
    async def _extract_company_name(self, text: str) -> Optional[str]:
        """Extract company name from user input"""
        prompt = f'Extract company name from: "{text}". Return only the name or "NONE".'
        company = await self.llm.complete(prompt, max_tokens=50, temperature=0)
        company = company.strip()
        
        if company == "NONE":
            return None
        
        try:
            return validate_company_name(company)
        except ValidationError:
            return None
