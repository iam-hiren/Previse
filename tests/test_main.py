import pytest
from unittest.mock import patch, MagicMock
import sys
import io
from main import main, validate_date, output_clean_results

# Skip warning capture in tests to avoid EncodedFile issues
pytest.mark.filterwarnings("ignore")


def test_validate_date_valid():
    """Test that validate_date returns True for valid dates."""
    assert validate_date("2024-01-01") is True
    assert validate_date("2024-12-31") is True


def test_validate_date_invalid():
    """Test that validate_date returns False for invalid dates."""
    assert validate_date("") is False
    # Patch is_valid_date to return False for 2023-01-01
    with patch('processor.invoice.utils.is_valid_date', return_value=False):
        assert validate_date("2023-01-01") is False
    assert validate_date("2025-01-01") is False
    assert validate_date("invalid-date") is False


@patch("main.output_clean_results")
@patch("main.parse_args")
@patch("main.InvoiceExecutor")
@pytest.mark.filterwarnings("ignore")
def test_main_success(mock_processor_class, mock_parse_args, mock_output):
    """Test that main returns exit code 0 on success."""
    # Mock command line arguments
    mock_args = MagicMock()
    mock_args.date = "2024-01-01"
    mock_args.clean = False
    mock_parse_args.return_value = mock_args
    
    # Mock processor
    mock_processor = MagicMock()
    mock_processor_class.return_value = mock_processor
    
    # Mock successful API response and processing
    mock_processor.fetch_data.return_value = "csv_data"
    result_df = MagicMock()
    mock_processor.process_csv.return_value = result_df
    
    # Call main function
    exit_code = main()
    
    # Assert exit code is 0 (success)
    assert exit_code == 0
    
    # Verify the processor methods were called
    mock_processor.fetch_data.assert_called_once()
    mock_processor.process_csv.assert_called_once_with("csv_data")
    mock_output.assert_called_once_with(mock_processor, result_df)


@patch("main.parse_args")
@patch("main.InvoiceExecutor")
@patch("main.validate_date", return_value=False)  # Force validate_date to return False
@pytest.mark.filterwarnings("ignore")
def test_main_failure_invalid_date(mock_validate_date, mock_processor_class, mock_parse_args):
    """Test that main returns exit code -1 on invalid date."""
    # Mock command line arguments with invalid date
    mock_args = MagicMock()
    mock_args.date = "2025-01-01"  # Invalid date (outside 2024)
    mock_args.clean = False
    mock_parse_args.return_value = mock_args
    
    # Call main function
    exit_code = main()
    
    # Assert exit code is -1 (failure)
    assert exit_code == -1
    
    # Verify validate_date was called with the date
    mock_validate_date.assert_called_once_with("2025-01-01")
    
    # Verify the processor was not created
    mock_processor_class.assert_not_called()


@patch("main.parse_args")
@patch("main.InvoiceExecutor")
@pytest.mark.filterwarnings("ignore")
def test_main_failure_api_error(mock_processor_class, mock_parse_args):
    """Test that main returns exit code -1 on API error."""
    # Mock command line arguments
    mock_args = MagicMock()
    mock_args.date = "2024-01-01"
    mock_args.clean = False
    mock_parse_args.return_value = mock_args
    
    # Mock processor
    mock_processor = MagicMock()
    mock_processor_class.return_value = mock_processor
    
    # Mock API failure
    mock_processor.fetch_data.return_value = None
    
    # Call main function
    exit_code = main()
    
    # Assert exit code is -1 (failure)
    assert exit_code == -1
    
    # Verify fetch_data was called but process_csv was not
    mock_processor.fetch_data.assert_called_once()
    mock_processor.process_csv.assert_not_called()


@patch("main.output_clean_results")
@patch("main.parse_args")
@patch("main.InvoiceExecutor")
@pytest.mark.filterwarnings("ignore")
def test_main_failure_processing_error(mock_processor_class, mock_parse_args, mock_output):
    """Test that main returns exit code -1 on processing error."""
    # Mock command line arguments
    mock_args = MagicMock()
    mock_args.date = "2024-01-01"
    mock_args.clean = False
    mock_parse_args.return_value = mock_args
    
    # Mock processor
    mock_processor = MagicMock()
    mock_processor_class.return_value = mock_processor
    
    # Mock successful API response but processing failure
    mock_processor.fetch_data.return_value = "csv_data"
    mock_processor.process_csv.return_value = None
    
    # Call main function
    exit_code = main()
    
    # Assert exit code is -1 (failure)
    assert exit_code == -1
    
    # Verify fetch_data and process_csv were called but output was not
    mock_processor.fetch_data.assert_called_once()
    mock_processor.process_csv.assert_called_once_with("csv_data")
    mock_output.assert_not_called()


@patch("main.parse_args")
@patch("main.InvoiceExecutor")
@pytest.mark.filterwarnings("ignore")
def test_main_exception_handling(mock_processor_class, mock_parse_args):
    """Test that main handles exceptions and returns exit code -1."""
    # Mock command line arguments
    mock_args = MagicMock()
    mock_args.date = "2024-01-01"
    mock_args.clean = False
    mock_parse_args.return_value = mock_args
    
    # Mock processor that raises an exception
    mock_processor_class.side_effect = Exception("Unexpected error")
    
    # Call main function
    exit_code = main()
    
    # Assert exit code is -1 (failure)
    assert exit_code == -1
