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
