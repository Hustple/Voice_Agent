"""System Prompts"""

class SystemPrompts:
    INTENT_CLASSIFICATION = """Classify: "{user_input}"
Categories: check_invoices, send_reminder, help, other
Return only the category."""
