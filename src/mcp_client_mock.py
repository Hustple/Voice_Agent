"""Mock MCP Client"""
from typing import Dict, Any, Optional
from loguru import logger
from datetime import datetime, timedelta

class MockMCPClient:
        def __init__(self, config):
            logger.info("✅ Mock MCP (no server needed)")
    
        async def call_tool(self, server: str, tool: str, params: Optional[Dict] = None) -> Any:
            logger.info(f"[MOCK] {server}/{tool}")
            params = params or {}
    
            all_invoices = [
                 {"id": "inv_001", "customer_name": "Acme Corp", 
                   "customer_email": "john@acme.com", "amount": 500.00,
                   "due_date": (datetime.now() - timedelta(days=10)).isoformat(),
                   "status": "past_due", "days_overdue": 10},
                 {"id": "inv_002", "customer_name": "Beta Industries",
                    "customer_email": "jane@beta.com", "amount": 600.00,
                    "due_date": (datetime.now() - timedelta(days=15)).isoformat(),
                    "status": "past_due", "days_overdue": 15}
            ]
    
            if server == "stripe":
                if tool == "list_invoices":
                    return all_invoices                      # Return all
        
                elif tool == "search_invoices":
                    customer = params.get("customer_name", "").lower()
                    filtered = [
                        inv for inv in all_invoices
                        if customer in inv["customer_name"].lower()
                    ]
                    logger.info(f"[MOCK] Searching for '{customer}' → {len(filtered)} results")
                    return filtered                          # Return filtered!
    
            elif server == "gmail":
                return {"status": "sent", "to": params.get("to")}
    
            return {"status": "ok"}