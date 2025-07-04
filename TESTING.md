# Testing Documentation for Previse Project

## Overview
This document outlines the testing approach, test cases, and security considerations for the Previse invoice processing application. The application fetches invoice data from an API, processes it, and outputs aggregated results grouped by supplier and month.

## Testing Approach

### Unit Testing
- Individual components are tested in isolation
- Focus on testing business logic and utility functions
- Mock external dependencies (API calls, file system operations)
- Tests are located in the `tests/` directory

### Integration Testing
- Test the interaction between components
- Verify data flow through the application
- Test with mock API responses using the `responses` library

### Security Testing
- Credential handling and storage
- Environment variable validation
- Secure logging practices (credential masking)

## Test Environment Setup

1. Clone the repository
2. Create a `.env` file based on `.env.example` with the following variables:
   ```
   API_URL="https://deng-interview.previsedigital.com/deng-coding-task/fetch-invoices/"
   API_USERNAME=your_username_here
   API_PASSWORD=your_password_here
   ```
3. Install dependencies: `pip install -r requirements.txt`
4. Install development dependencies: `pip install -r dev-requirements.txt`

## Running Tests

### Using Nox (Recommended)
```bash
nox -s tests
```

### Using Pytest Directly
```bash
pytest -v tests/
```

## Test Cases

### Date Validation (`test_utils.py`)
- Tests valid date formats (YYYY-MM-DD) within the year 2024
- Tests invalid dates (wrong format, outside allowed range, non-existent dates)
- Parameterized tests cover multiple scenarios

### API Integration (`test_processor.py`, `test_integration.py`)
- Tests successful API connection and data retrieval
- Tests handling of API errors with mocked responses
- Tests retry mechanism for transient failures
- Tests proper authentication using environment variables

### Data Processing (`test_processor.py`, `test_integration.py`)
- Tests CSV parsing with valid data
- Tests handling of malformed CSV data
- Tests data aggregation and grouping by supplier_id and invoice_month
- Verifies correct sum calculation for grouped invoices

### Main Application Flow (`test_main.py`)
- Tests end-to-end application flow
- Tests command-line argument parsing
- Tests error handling for various failure scenarios
- Tests output formatting

### Error Handling and Logging
- Tests validation of input parameters
- Tests logging of errors
- Tests graceful failure modes
- Tests exception handling

## Security Considerations

### Credential Management
- **DO NOT** commit `.env` file with actual credentials
- Use `.env.example` as a template for required variables
- Ensure credentials are masked in logs (implemented in `config.py`)
- Validate presence of required environment variables at startup

### API Authentication
- Verify proper use of authentication headers
- Test handling of authentication failures
- Use environment variables for storing credentials

## Continuous Integration

The test suite runs automatically on:
- Pull requests
- Commits to main branch

## Test Coverage

The test suite provides comprehensive coverage of:
- Date validation logic
- API interaction and error handling
- CSV processing and data aggregation
- Command-line interface
- Error handling and logging

Areas that could benefit from additional coverage:
- Edge cases in CSV parsing
- More extensive error handling scenarios
- Performance testing with large datasets

## Known Issues

- Tests currently use mocked API responses and don't test against the actual API
- No performance benchmarks for large datasets

## Future Improvements

- Add performance testing with larger datasets
- Implement end-to-end testing against a test API endpoint
- Add security scanning tools to CI pipeline
- Implement code coverage reporting
- Add property-based testing for more robust validation
