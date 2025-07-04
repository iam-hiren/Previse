# Standard library imports
import logging
import time
import warnings
from io import StringIO
from typing import Optional, Dict, Any

# Third-party imports
import pandas as pd
import requests
from requests.exceptions import RequestException, HTTPError, Timeout

# Local application imports
from config.config import API_URL, AUTH

# Configure logger for this module
logger = logging.getLogger(__name__)

# Suppress pandas warnings
warnings.filterwarnings('ignore', module='pandas')

class InvoiceExecutor:
    """Process invoice data from an external API.
    
    This class handles fetching invoice data from an API, processing the CSV data,
    and outputting the results grouped by supplier_id and invoice_month.
    """
    
    def __init__(self, date_str: str):
        """Initialize the InvoiceExecutor with a date string.
        
        Args:
            date_str: Date string in YYYY-MM-DD format
        """
        self.date_str = date_str
        self.max_retries = 3
        self.retry_delay = 1  # seconds

    def fetch_data(self) -> Optional[str]:
        """Fetch invoice data from the API for the specified date.
        
        Returns:
            The CSV data as a string if successful, None otherwise.
            
        Raises:
            No exceptions are raised; errors are logged and None is returned.
        """
        url = f"{API_URL}{self.date_str}"
        
        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info(f"Fetching data for {self.date_str} (attempt {attempt}/{self.max_retries})")
                response = requests.get(url, auth=AUTH, timeout=10)
                response.raise_for_status()
                logger.info(f"Successfully fetched data for {self.date_str}")
                return response.text
            except HTTPError as exc:
                logger.error(f"HTTP error fetching data: {exc} (Status code: {exc.response.status_code})")
                # Don't retry for client errors (4xx)
                if 400 <= exc.response.status_code < 500:
                    break
            except Timeout:
                logger.error(f"Timeout fetching data for {self.date_str} (attempt {attempt}/{self.max_retries})")
            except RequestException as exc:
                logger.error(f"Request error fetching data: {exc}")
            except Exception as exc:
                logger.error(f"Unexpected error fetching data: {exc}")
                
            # Implement exponential backoff if not the last attempt
            if attempt < self.max_retries:
                # Calculate exponential backoff delay: 2^attempt seconds with base delay
                backoff_delay = (2 ** (attempt - 1)) * self.retry_delay
                logger.info(f"Retrying in {backoff_delay} seconds (exponential backoff)...")
                time.sleep(backoff_delay)
            
        return None

    def process_csv(self, csv_text: str) -> Optional[pd.DataFrame]:
        """Process CSV data and group by supplier_id and invoice_month.
        
        Args:
            csv_text: CSV data as a string
            
        Returns:
            DataFrame with grouped results if successful, None otherwise
            
        Raises:
            No exceptions are raised; errors are logged and None is returned.
        """
        try:
            # Read CSV data into DataFrame
            df = pd.read_csv(StringIO(csv_text))
            
            # Validate required columns
            required_columns = {"supplier_id", "invoice_date"}
            if not required_columns.issubset(df.columns):
                missing = required_columns - set(df.columns)
                logger.error(f"CSV missing required columns: {missing}")
                return None
            
            # Handle both 'amount' and 'gross_amount' column names
            amount_column = self._determine_amount_column(df)
            if amount_column is None:
                return None
            
            if amount_column != 'gross_amount':
                df['gross_amount'] = df[amount_column]
            
            # Convert invoice_date to datetime
            df = self._parse_dates(df)
            if df is None or df.empty:
                logger.error("No valid invoice dates found after parsing")
                return None
            
            # Extract invoice_month from invoice_date
            df['invoice_month'] = df['invoice_date_parsed'].dt.strftime('%Y-%m')
            
            # Group by supplier_id and invoice_month, sum gross_amount
            grouped = self._group_and_format(df)
            
            logger.info(f"Processed {len(df)} rows into {len(grouped)} grouped records")
            return grouped
        except pd.errors.ParserError as exc:
            logger.error(f"CSV parsing error: {exc}")
            return None
        except Exception as exc:
            logger.error(f"Failed to process CSV: {exc}")
            return None
    
    def _determine_amount_column(self, df: pd.DataFrame) -> Optional[str]:
        """Determine which column contains the invoice amount.
        
        Args:
            df: DataFrame containing invoice data
            
        Returns:
            Column name containing amount data, or None if not found
        """
        if 'gross_amount' in df.columns:
            return 'gross_amount'
        elif 'amount' in df.columns:
            return 'amount'
        else:
            logger.error("CSV missing required amount column (either 'amount' or 'gross_amount')")
            return None
    
    def _parse_dates(self, df: pd.DataFrame) -> Optional[pd.DataFrame]:
        """Parse invoice_date column to datetime.
        
        Args:
            df: DataFrame containing invoice data
            
        Returns:
            DataFrame with parsed dates, or None if parsing fails
        """
        try:
            # Try multiple date formats with coercion
            df['invoice_date_parsed'] = pd.to_datetime(df['invoice_date'], errors='coerce')
            
            # Check for unparseable dates
            null_dates = df['invoice_date_parsed'].isnull().sum()
            if null_dates > 0:
                # Log to file only, not to console
                file_logger = logging.getLogger('file_only')
                if not file_logger.handlers:
                    file_handler = logging.FileHandler("app.log")
                    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s - %(message)s'))
                    file_logger.addHandler(file_handler)
                    file_logger.propagate = False  # Don't propagate to root logger
                file_logger.warning(f"{null_dates} invoice_date rows could not be parsed and will be ignored")
            
            # Drop rows with invalid dates
            df = df.dropna(subset=['invoice_date_parsed'])
            
            if df.empty:
                logger.error("All invoice dates were invalid")
                return None
                
            return df
        except Exception as exc:
            logger.error(f"Error parsing dates: {exc}")
            return None
    
    def _group_and_format(self, df: pd.DataFrame) -> pd.DataFrame:
        """Group data by supplier_id and invoice_month, and format amounts.
        
        Args:
            df: DataFrame with parsed dates and gross_amount
            
        Returns:
            Grouped DataFrame with formatted amounts
        """
        # Group by supplier_id and invoice_month, sum gross_amount
        grouped = (
            df.groupby(['supplier_id', 'invoice_month'], as_index=False)['gross_amount']
            .sum()
            .sort_values(['supplier_id', 'invoice_month'])
        )
        
        # Format gross_amount to 2 decimal places
        grouped['gross_amount'] = grouped['gross_amount'].map(lambda x: f"{x:.2f}")
        
        return grouped

    def output_result(self, grouped_df: pd.DataFrame) -> None:
        """Output the grouped results to stdout.
        
        Args:
            grouped_df: DataFrame with grouped results
        """
        # Store all output lines first, then print them all at once to avoid log messages interfering
        output_lines = []
        for _, row in grouped_df.iterrows():
            output_lines.append(f"{row['supplier_id']},{row['invoice_month']},{row['gross_amount']}")
        
        # Print all lines at once
        print("\n".join(output_lines))
