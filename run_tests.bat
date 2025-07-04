@echo off
echo Running all tests...
python -m pytest

echo.
echo Running linting...
python -m flake8 invoice_processor tests main.py

echo.
echo Running type checking...
python -m mypy invoice_processor main.py
