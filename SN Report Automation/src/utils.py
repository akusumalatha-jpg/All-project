"""
Utility Functions
Helper functions for the application.
"""

import logging
from pathlib import Path
from datetime import datetime
import json


def setup_logging(log_dir='logs', level=logging.INFO):
    """
    Configure logging.
    
    Args:
        log_dir: Directory for log files
        level: Logging level
        
    Returns:
        Logger instance
    """
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {log_file}")
    return logger


def safe_file_path(directory, filename):
    """
    Create safe file path preventing directory traversal.
    
    Args:
        directory: Target directory
        filename: Filename
        
    Returns:
        Safe Path object
    """
    base_path = Path(directory).resolve()
    file_path = (base_path / filename).resolve()

    if not str(file_path).startswith(str(base_path)):
        raise ValueError(f"Invalid path: {filename}")

    return file_path


def format_number(value, decimals=2):
    """Format number for display."""
    try:
        return round(float(value), decimals)
    except (ValueError, TypeError):
        return value


def format_currency(value, symbol='$'):
    """Format number as currency."""
    try:
        return f"{symbol}{float(value):,.2f}"
    except (ValueError, TypeError):
        return value


def format_percentage(value, decimals=1):
    """Format number as percentage."""
    try:
        return f"{float(value):.{decimals}f}%"
    except (ValueError, TypeError):
        return value


def read_json_file(file_path):
    """
    Read JSON file safely.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Parsed JSON data or None
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error reading JSON: {str(e)}")
        return None


def write_json_file(file_path, data):
    """
    Write JSON file safely.
    
    Args:
        file_path: Path to JSON file
        data: Data to write
        
    Returns:
        True if successful
    """
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        logging.error(f"Error writing JSON: {str(e)}")
        return False


def get_file_size(file_path):
    """Get file size in MB."""
    try:
        return round(Path(file_path).stat().st_size / (1024 * 1024), 2)
    except:
        return 0


def get_timestamp():
    """Get current timestamp string."""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_date_string(format_str='%Y-%m-%d'):
    """Get current date as string."""
    return datetime.now().strftime(format_str)
