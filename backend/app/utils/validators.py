"""Utility validators for phone, email, password, and dates."""
import re
from datetime import date


def validate_phone(phone: str) -> str:
    """Validate Indian mobile number (10 digits, optional +91 prefix)."""
    cleaned = re.sub(r"[\s\-\(\)]", "", phone)
    if cleaned.startswith("+91"):
        cleaned = cleaned[3:]
    elif cleaned.startswith("91") and len(cleaned) == 12:
        cleaned = cleaned[2:]
    if not re.match(r"^[6-9]\d{9}$", cleaned):
        raise ValueError("Invalid Indian mobile number. Must be 10 digits starting with 6-9.")
    return cleaned


def validate_password_strength(password: str) -> str:
    """Enforce password policy: min 8 chars, 1 uppercase, 1 digit."""
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long.")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain at least one uppercase letter.")
    if not re.search(r"\d", password):
        raise ValueError("Password must contain at least one digit.")
    return password


def validate_future_date(dt: date) -> date:
    """Ensure date is not in the past."""
    if dt < date.today():
        raise ValueError("Date cannot be in the past.")
    return dt


def validate_positive_number(value: float) -> float:
    """Ensure numeric value is positive."""
    if value <= 0:
        raise ValueError("Value must be greater than zero.")
    return value
