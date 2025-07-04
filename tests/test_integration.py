import responses
import pytest
import os
from dotenv import load_dotenv
from processor.invoice.executor import InvoiceExecutor

# Load environment variables from .env file
load_dotenv()

CSV_SAMPLE = '''"supplier_id","invoice_date","invoice_number","amount","description"
"SUP001","2024-03-01","INV-0001","100.00","Test invoice"
"SUP001","2024-03-15","INV-0002","150.50","Test invoice 2"
"SUP002","2024-03-10","INV-0003","200.25","Test invoice 3"
'''

@responses.activate
def test_fetch_and_process_integration():
    date = "2024-03-01"
    api_url = os.getenv('API_URL')
    url = f"{api_url}{date}"

    # Mock the API response
    responses.add(
        responses.GET,
        url,
        body=CSV_SAMPLE,
        status=200,
        content_type='text/csv',
    )

    processor = InvoiceExecutor(date)
    csv_text = processor.fetch_data()
    assert csv_text is not None
    assert "supplier_id" in csv_text

    df = processor.process_csv(csv_text)
    assert df is not None

    # Check aggregation correctness
    row_sup1 = df[(df['supplier_id'] == 'SUP001') & (df['invoice_month'] == '2024-03')]
    assert not row_sup1.empty
    # 100.00 + 150.50 = 250.50
    assert row_sup1.iloc[0]['gross_amount'] == "250.50"

    row_sup2 = df[(df['supplier_id'] == 'SUP002') & (df['invoice_month'] == '2024-03')]
    assert not row_sup2.empty
    assert row_sup2.iloc[0]['gross_amount'] == "200.25"
