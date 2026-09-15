from datetime import datetime
import re


def validate_email(email):
    """Validate email format"""
    if not email:
        return True 
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_dob(dob_str):
    """Validate and parse date of birth"""
    if not dob_str:
        return True, None
    
    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
        if dob > datetime.now().date():
            return False, "Date of birth cannot be in the future"
        if dob.year < 1940:
            return False, "Invalid date of birth"
        return True, dob
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD"


def calculate_age(dob):
    """Calculate age from date of birth"""
    if not dob:
        return None
    today = datetime.now().date()
    if isinstance(dob, str):
        dob = datetime.strptime(dob, "%Y-%m-%d").date()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))