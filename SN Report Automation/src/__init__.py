"""
SN Report Automation Package
Automates the creation of reports from Excel data to PowerPoint presentations.
"""

from .config import Config, get_config
from .excel_reader import ExcelReader, read_excel_file
from .metrics import MetricsCalculator
from .ppt_updater import PowerPointUpdater
from .chart_generator import ChartGenerator
from .main import ReportAutomation

__version__ = "1.0.0"
__all__ = [
    'Config',
    'get_config',
    'ExcelReader',
    'read_excel_file',
    'MetricsCalculator',
    'PowerPointUpdater',
    'ChartGenerator',
    'ReportAutomation',
]
