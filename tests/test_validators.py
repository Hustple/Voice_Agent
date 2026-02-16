"""Tests for input validators"""
import pytest
from src.utils.validators import (
    validate_user_input,
    validate_company_name,
    validate_email_content
)
from src.exceptions import ValidationError

def test_validate_user_input_valid():
    result = validate_user_input("  check invoices  ")
    assert result == "check invoices"

def test_validate_user_input_empty():
    with pytest.raises(ValidationError):
        validate_user_input("")

def test_validate_user_input_too_long():
    with pytest.raises(ValidationError):
        validate_user_input("a" * 501)

def test_validate_company_name_valid():
    result = validate_company_name("Acme Corp")
    assert result == "Acme Corp"

def test_validate_company_name_invalid_chars():
    with pytest.raises(ValidationError):
        validate_company_name("Acme<script>alert(1)</script>")

def test_validate_email_content():
    assert validate_email_content("Dear customer, please pay.") == True
    assert validate_email_content("<script>alert(1)</script>") == False
