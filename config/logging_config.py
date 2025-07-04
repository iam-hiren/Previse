import logging
import sys
import os

def configure_logging(mode='normal'):
    """
    Configure logging based on the specified mode.
    
    Args:
        mode (str): Logging mode - 'normal', 'quiet', 'debug', or 'clean_output'
                   - normal: INFO level to console and file
                   - quiet: ERROR level to console, INFO to file
                   - debug: DEBUG level to console and file
                   - clean_output: ERROR level to console, INFO to file, for clean stdout
    """
    # Create a file handler for all logs
    file_handler = logging.FileHandler("app.log")
    file_handler.setLevel(logging.INFO)  # Always log INFO and above to file
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s - %(message)s'))
    
    # Create a stderr handler for console output
    # This ensures logs don't interfere with stdout which is used for application output
    console_handler = logging.StreamHandler(stream=sys.stderr)
    
    # Set console level based on mode
    if mode == 'debug':
        console_level = logging.DEBUG
    elif mode in ('quiet', 'clean_output'):
        console_level = logging.ERROR
    else:  # normal mode
        console_level = logging.INFO
        
    console_handler.setLevel(console_level)
    console_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s - %(message)s'))
    
    # Configure the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # Capture all logs, handlers will filter
    
    # Remove any existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Add our handlers
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # If in clean_output mode, ensure all existing loggers are set to ERROR for console
    if mode == 'clean_output':
        for logger_name in logging.root.manager.loggerDict:
            logging.getLogger(logger_name).setLevel(logging.ERROR)

# Default configuration - can be overridden by calling configure_logging()
configure_logging(os.environ.get('LOG_MODE', 'normal'))
