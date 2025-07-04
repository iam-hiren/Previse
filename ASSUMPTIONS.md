# Assumptions

## Data Processing Assumptions

1. **Date Format**: The invoice_date in the CSV is assumed to be in MM-DD-YY format, which is converted to YYYY-MM format for grouping.

2. **Amount Column**: The code handles both 'gross_amount' and 'amount' column names in the CSV data, with 'gross_amount' taking precedence if both exist.

3. **Required Columns**: The CSV must contain 'supplier_id', 'invoice_date', and either 'gross_amount' or 'amount' columns.

4. **API Reliability**: The API is assumed to be occasionally unreliable, so the code implements 3 retry attempts with delays between attempts.

5. **Error Handling**: If any required columns are missing or if date parsing fails, the application will log errors and return a non-zero exit code.

6. **Decimal Precision**: All monetary amounts are rounded to 2 decimal places in the output.

7. **Authentication**: The API requires HTTP Basic Authentication with fixed credentials.

8. **Date Range**: Valid dates for API requests are between January 1, 2024 and December 31, 2024.

9. **Logging**: Application logs are written to app.log while keeping stdout clean for the required CSV output format.

10. **Duplicate Invoices**: If duplicate invoice records exist in the API response, they will be summed together when grouping by supplier_id and invoice_month.
