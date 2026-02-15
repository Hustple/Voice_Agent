"""Input validation utilities"""
import re
from exceptions import ValidationError
from constants import MAX_USER_INPUT_LENGTH, MAX_COMPANY_NAME_LENGTH

def validate_user_input(text: str) -> str:
    """Validate and sanitize user input"""
    if not text or not text.strip():
        raise ValidationError("Input cannot be empty")
    
    text = text.strip()
    
    if len(text) > MAX_USER_INPUT_LENGTH:
        raise ValidationError(
            f"Input too long. Max {MAX_USER_INPUT_LENGTH} characters"
        )
    
    # Remove potential injection attempts
    dangerous_patterns = [
        r'<script',
        r'javascript:',
        r'onerror=',
        r'onclick=',
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            raise ValidationError("Invalid input detected")
    
    return text

def validate_company_name(name: str) -> str:
    """Validate company name"""
    if not name or not name.strip():
        raise ValidationError("Company name cannot be empty")
    
    name = name.strip()
    
    if len(name) > MAX_COMPANY_NAME_LENGTH:
        raise ValidationError(
            f"Company name too long. Max {MAX_COMPANY_NAME_LENGTH} characters"
        )
    
    # Only allow alphanumeric, spaces, and basic punctuation
    if not re.match(r'^[a-zA-Z0-9\s\.,\-&]+$', name):
        raise ValidationError("Company name contains invalid characters")
    
    return name

def validate_email_content(content: str) -> bool:
    """Validate email content for safety"""
    if len(content) > 5000:
        return False
    
    # Check for suspicious patterns
    suspicious = ['<script', 'javascript:', 'data:text/html']
    for pattern in suspicious:
        if pattern.lower() in content.lower():
            return False
    
    return True
