import pytest
from unittest.mock import patch
from processor.invoice.executor import InvoiceExecutor
import pandas as pd

SAMPLE_CSV = """supplier_id,invoice_date,amount
SUP001,2024-01-05,100.00
SUP001,2024-01-10,200.00
SUP002,2024-01-15,300.50
SUP001,2024-02-01,50.00
"""

EXPECTED_OUTPUT = [
    ("SUP001", "2024-01", "300.00"),
    ("SUP001", "2024-02", "50.00"),
    ("SUP002", "2024-01", "300.50"),
]

@pytest.fixture
def processor():
    return InvoiceExecutor("2024-01-01")

def test_process_csv_grouping_and_formatting(processor):
    df = processor.process_csv(SAMPLE_CSV)
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 3
    output = list(df.itertuples(index=False, name=None))
    for expected in EXPECTED_OUTPUT:
        assert expected in output

@patch("processor.invoice.executor.requests.get")
def test_fetch_data_success(mock_get, processor):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = SAMPLE_CSV
    response = processor.fetch_data()
    assert SAMPLE_CSV in response

@patch("processor.invoice.executor.requests.get")
def test_fetch_data_failure(mock_get, processor):
    mock_get.side_effect = Exception("API failure")
    response = processor.fetch_data()
    assert response is None

def test_process_csv_invalid_format(processor):
    bad_csv = "wrong_column\n2024-01-01\n"
    df = processor.process_csv(bad_csv)
    assert df is None

def test_fetch_data_logs_error(monkeypatch, caplog):
    processor = InvoiceExecutor("2024-01-01")

    def fake_get(*args, **kwargs):
        raise Exception("Simulated API failure")

    monkeypatch.setattr("processor.invoice.executor.requests.get", fake_get)

    with caplog.at_level("ERROR"):
        result = processor.fetch_data()
        assert result is None
        assert "Unexpected error fetching data" in caplog.text

def test_process_csv_logs_error(caplog):
    processor = InvoiceExecutor("2024-01-01")
    bad_csv = "bad_column\nvalue\n"

    with caplog.at_level("ERROR"):
        result = processor.process_csv(bad_csv)
        assert result is None
        assert "CSV missing required columns" in caplog.text
