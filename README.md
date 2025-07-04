# Previse - Data Engineer Coding Exercise

## Overview

This application processes invoice data fetched from an external API by grouping it based on `supplier_id` and `invoice_month`, and summing the amounts. The date for which to fetch data is provided as a command-line argument.

---

## Features

- Accepts a single date argument (`YYYY-MM-DD`) via the command line
- Validates the date is within the range: 2024-01-01 to 2024-12-31
- Fetches invoice CSV data from the provided API
- Processes and groups data by `supplier_id` and `invoice_month`
- Outputs results to standard output in the format:
  ```
  <supplier_id>,<invoice_month>,<amount>
  ```
- Handles API failures gracefully with appropriate error logging
- Returns exit code 0 on success and -1 on failure

## Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root with the following variables:
   ```
   API_URL=https://deng-interview.previsedigital.com/deng-coding-task/fetch-invoices/
   API_USERNAME=your_username
   API_PASSWORD=your_password
   ```
   
   Note: Contact the administrator for the actual API credentials.

## Usage

To process invoices for a specific date:

```bash
python main.py <date>
```

Where `<date>` is in YYYY-MM-DD format and must be within the year 2024.

The application will output the processed invoice data to stdout in the format:
`<supplier_id>,<invoice_month>,<amount>`
```
--- INVOICE PROCESSING RESULTS ---
SUP001,2023-12,12439.71
SUP001,2024-01,39438.58
SUP002,2023-12,29891.33
SUP002,2024-01,6448.48
...
--- END OF RESULTS ---
```

## Project Structure

```
.
├── config/                # Configuration modules
│   ├── __init__.py
│   ├── config.py         # Environment variable configuration
│   └── logging_config.py # Logging configuration
├── processor/            # Core processing modules
│   ├── __init__.py
│   └── invoice/          # Invoice-specific processing
│       ├── __init__.py
│       ├── processor.py  # InvoiceProcessor class
│       └── utils.py      # Utility functions
├── tests/                # Test suite
│   ├── __init__.py
│   ├── test_integration.py
│   ├── test_processor.py
│   └── test_utils.py
├── .env                  # Environment variables (not in version control)
├── main.py              # Application entry point with clean output option
├── noxfile.py           # Nox configuration for testing/linting
├── requirements.txt     # Production dependencies
└── dev-requirements.txt # Development dependencies
```

## Development

### Running Tests

#### Using pytest directly

```bash
python -m pytest tests
```

#### Using Nox (Recommended)

Nox provides an automated and consistent testing environment:

```bash
# Run all tests
nox -s tests

# Run tests with verbose output
nox -s tests -- -v

# Run a specific test file
nox -s tests -- tests/test_processor.py

# Run tests for exit code functionality
nox -s tests -- tests/test_main.py
```

Nox automatically creates a virtual environment with the correct dependencies for testing, ensuring consistent test results across different environments.

#### Exit Code Testing

The application returns specific exit codes to indicate success or failure:
- Exit code `0`: Successful execution
- Exit code `-1`: Failure (invalid date, API error, processing error, etc.)

These exit codes are thoroughly tested in `tests/test_main.py`, which verifies:
- Success path returns exit code 0
- Various failure scenarios return exit code -1
- Error handling for invalid dates
- Error handling for API failures
- Error handling for processing failures
- Exception handling

### Linting and Type Checking

```bash
nox -s lint typecheck
```

## Assumptions

- The API may be unreliable and requires error handling
- The CSV data might have different column names (e.g., 'amount' or 'gross_amount')
- Date formats in the CSV may vary and need to be handled
- The API requires HTTP Basic Authentication

## Design Decisions

- Used pandas for efficient data processing and grouping
- Implemented modular design with separation of concerns
- Added comprehensive error handling and logging
- Used environment variables for configuration
- Added extensive test coverage with mocks for external dependencies
