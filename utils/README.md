# Common Utilities Module

This module contains common utility functions that can be used across the Previse application.

## Modules

### date_utils.py

Contains date validation and manipulation utilities.

- `is_valid_date(date_str)`: Validates if a date string is in the correct format (YYYY-MM-DD) and within the allowed range (2024-01-01 to 2024-12-31).

### common.py

Contains general utility functions.

- `safe_get(data, key, default)`: Safely retrieves a value from a dictionary without raising KeyError.
- `format_currency(amount)`: Formats a number as a currency string with 2 decimal places.

## Usage

```python
# Date validation
from utils.date_utils import is_valid_date

result = is_valid_date("2024-01-15")
if isinstance(result, tuple):
    is_valid, error_message = result
    if not is_valid:
        print(error_message)
else:
    # For backward compatibility with tests
    is_valid = result

# Common utilities
from utils.common import safe_get, format_currency

data = {"amount": "123.4"}
formatted_amount = format_currency(safe_get(data, "amount", "0"))
```
