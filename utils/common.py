# Standard library imports
import logging
from typing import Any, Dict, List, Optional, Union

# Configure logger for this module
logger = logging.getLogger(__name__)

def safe_get(data: Dict[str, Any], key: str, default: Any = None) -> Any:
    """
    Safely get a value from a dictionary without raising KeyError.
    
    Args:
        data: Dictionary to get value from
        key: Key to look up
        default: Default value to return if key is not found
        
    Returns:
        Value from dictionary or default if key not found
    """
    return data.get(key, default)

def format_currency(amount: Union[float, str]) -> str:
    """
    Format a number as a currency string with 2 decimal places.
    
    Args:
        amount: Amount to format, can be float or string
        
    Returns:
        Formatted string with 2 decimal places
    """
    try:
        # Convert to float if it's a string
        if isinstance(amount, str):
            amount = float(amount)
        
        # Format with 2 decimal places
        return f"{amount:.2f}"
    except (ValueError, TypeError) as e:
        logger.warning(f"Failed to format currency value: {amount}. Error: {e}")
        return str(amount)
