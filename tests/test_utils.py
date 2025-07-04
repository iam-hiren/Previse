import pytest
from utils.date_utils import is_valid_date

@pytest.mark.parametrize("valid_date", [
    "2024-01-01",
    "2024-06-15",
    "2024-12-31"
])
def test_valid_dates(valid_date):
    result = is_valid_date(valid_date)
    if isinstance(result, tuple):
        is_valid, _ = result
        assert is_valid is True
    else:
        assert result is True

@pytest.mark.parametrize("invalid_date", [
    "2023-12-31",     # before allowed range
    "2025-01-01",     # after allowed range
    "2024-13-01",     # invalid month
    "2024-02-30",     # invalid day
    "not-a-date",     # invalid format
    "",               # empty string
    "2024/01/01",     # wrong format
])
def test_invalid_dates(invalid_date):
    result = is_valid_date(invalid_date)
    if isinstance(result, tuple):
        is_valid, _ = result
        assert is_valid is False
    else:
        assert result is False
