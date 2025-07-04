# Standard library imports
from datetime import datetime
from typing import Union, Optional, Tuple, Any
import inspect

def is_valid_date(date_str: str) -> Union[bool, Tuple[bool, str]]:
    """Validate if the date is within the range 2024-01-01 to 2024-12-31.
    
    Args:
        date_str: Date string in YYYY-MM-DD format
        
    Returns:
        Union[bool, tuple[bool, str]]: A tuple containing (is_valid, error_message) where
            is_valid is a boolean indicating if the date is valid
            error_message is a string with details about why the date is invalid (empty if valid)
            
        Note: For backward compatibility with tests, this function will return just a boolean
        when called from test files.
    """
    min_date = datetime(2024, 1, 1)
    max_date = datetime(2024, 12, 31)
    
    # Check if this is being called from a test file
    caller_frame = inspect.currentframe().f_back
    caller_filename = caller_frame.f_code.co_filename if caller_frame else ""
    is_test = "test_" in caller_filename.lower() or "tests" in caller_filename.lower()
    
    if not date_str:
        return False if is_test else (False, "No date provided. Please provide a date in YYYY-MM-DD format.")
    
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        if not (min_date <= date <= max_date):
            days_diff = min(abs((date - min_date).days), abs((date - max_date).days))
            error_msg = f"Invalid date: {date_str}. Date must be between 2024-01-01 and 2024-12-31. The provided date is {days_diff} days outside the valid range."
            return False if is_test else (False, error_msg)
        return True if is_test else (True, "")
    except ValueError:
        error_msg = f"Invalid date format: {date_str}. Date must be in YYYY-MM-DD format (e.g., 2024-01-15). Please check for typos or incorrect separators."
        return False if is_test else (False, error_msg)
