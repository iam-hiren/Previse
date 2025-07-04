import os
import logging
from dotenv import load_dotenv

# Configure logger for this module
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# SECURITY NOTICE: Never hardcode credentials in source code
# Always use environment variables or secure credential stores

# Get API configuration from environment variables
API_URL = os.getenv("API_URL")
API_USERNAME = os.getenv("API_USERNAME")
API_PASSWORD = os.getenv("API_PASSWORD")

# Validate required environment variables
missing_vars = []
if not API_URL:
    missing_vars.append("API_URL")
if not API_USERNAME:
    missing_vars.append("API_USERNAME")
if not API_PASSWORD:
    missing_vars.append("API_PASSWORD")

if missing_vars:
    error_msg = f"Missing required environment variables: {', '.join(missing_vars)}"
    logger.error(error_msg)
    logger.error("Please ensure all required variables are set in .env file")
    raise EnvironmentError(error_msg)

# Create authentication tuple for requests
AUTH = (API_USERNAME, API_PASSWORD)

# Log successful configuration (without exposing sensitive data)
logger.debug(f"API URL configured: {API_URL}")
logger.debug(f"API credentials loaded: Username='{API_USERNAME[:1]}***' (masked for security)")

