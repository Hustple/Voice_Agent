"""Templates"""

class EmailTemplates:
    PAYMENT_REMINDER = """Write polite payment reminder:
Customer: {customer_name}
Invoice: {invoice_id}
Amount: ${amount}
Due: {due_date}
Days Overdue: {days_overdue}
Keep it under 200 words."""
