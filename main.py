#!/usr/bin/env python3
"""
Invoice Processing Application

This application fetches invoice data from an external API for a given date,
processes the data by grouping and summing invoice amounts by supplier and month,
and outputs the results to stdout.

Usage:
    python main.py <date>

Where <date> is in YYYY-MM-DD format and within the year 2024.
"""

# Standard library imports
import sys
import argparse
import io
import logging
import traceback
import warnings
from contextlib import redirect_stdout, redirect_stderr

# Local application imports
import config.logging_config as logging_config
from processor.invoice.executor import InvoiceExecutor
from processor.invoice.utils import is_valid_date

# Configure logger for this module
logger = logging.getLogger(__name__)

def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: The parsed command line arguments
        
    Raises:
        SystemExit: If required arguments are missing or invalid
    """
    parser = argparse.ArgumentParser(
        description="Process invoices by date",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python main.py 2024-01-01
  python main.py 2024-06-15"""
    )
    
    parser.add_argument(
        "date", 
        help="Date in YYYY-MM-DD format (must be within 2024)"
    )
    
    return parser.parse_args()


def validate_date(date_str: str) -> bool:
    """
    Validate the input date and log appropriate error messages.
    
    Args:
        date_str: Date string to validate
        
    Returns:
        bool: True if date is valid, False otherwise
    """
    result = is_valid_date(date_str)
    
    # Handle both return types (bool or tuple)
    if isinstance(result, tuple):
        is_valid, error_message = result
        if not is_valid:
            logger.error(error_message)
            return False
    elif not result:  # If result is just a boolean False
        logger.error(f"Invalid date: {date_str}. Date must be in YYYY-MM-DD format and within 2024.")
        return False
    
    return True


def output_clean_results(processor: InvoiceExecutor, result_df) -> None:
    """
    Output clean results without log messages or warnings.
    
    Args:
        processor: The InvoiceExecutor instance
        result_df: DataFrame with grouped results
    """
    # Disable all warnings
    warnings.filterwarnings("ignore")
    
    # Process the DataFrame directly to generate clean output
    # This avoids using redirect_stdout which can cause issues in tests
    for _, row in result_df.iterrows():
        supplier_id = row["supplier_id"]
        invoice_month = row["invoice_month"]
        amount = row["gross_amount"]
        print(f"{supplier_id},{invoice_month},{amount}")
    
    # Re-enable warnings (though we'll keep them disabled in main)


def main() -> int:
    """
    Main entry point for the application.

    - Parses and validates date argument
    - Fetches invoice CSV data from API
    - Processes CSV data and aggregates amounts
    - Outputs results to stdout

    Returns:
        int: Exit code (0 for success, -1 for failure)
    """
    try:
        args = parse_args()
        
        # Configure logging to only go to stderr, not stdout
        # Suppress all warnings
        warnings.filterwarnings("ignore")
        
        # Configure logging based on whether we want clean output
        # Import here to ensure it's loaded after any command line args are processed
        import config.logging_config as logging_config
        
        # Set to clean_output mode to suppress INFO messages and get clean stdout
        logging_config.configure_logging('clean_output')
        
        if not validate_date(args.date):
            return -1
        processor = InvoiceExecutor(args.date)
        csv_data = processor.fetch_data()
        if not csv_data:
            return -1
        logger.info("Processing invoice data...")
        result_df = processor.process_csv(csv_data)
        if result_df is None:
            logger.error("Failed to process invoice data. Exiting.")
            return -1

        # Output the final aggregated results
        logger.info(f"Outputting {len(result_df)} grouped invoice records...")
        
        # Always use clean output
        output_clean_results(processor, result_df)
        
        logger.info("Processing completed successfully.")
        return 0
        
    except KeyboardInterrupt:
        logger.info("Process interrupted by user.")
        return -1
    except Exception as exc:
        logger.error(f"Unexpected error: {exc}")
        logger.debug(f"Exception details: {traceback.format_exc()}")
        return -1


def main_entry():
    """Entry point for the application when installed via pip."""
    exit_code = main()
    sys.exit(exit_code)

if __name__ == "__main__":
    main_entry()

