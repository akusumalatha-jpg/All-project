"""
Configuration Management
Handles application settings and paths.
"""

import os
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)


class Config:
    """Application configuration."""

    def __init__(self, config_file=None):
        """
        Initialize configuration.
        
        Args:
            config_file: Path to config JSON file (optional)
        """
        # Base paths
        self.base_dir = Path(__file__).parent.parent
        self.input_dir = self.base_dir / 'input'
        self.output_dir = self.base_dir / 'output'
        self.templates_dir = self.base_dir / 'templates'
        self.charts_dir = self.base_dir / 'charts'
        self.assets_dir = self.base_dir / 'assets'
        self.logs_dir = self.base_dir / 'logs'

        # Create directories if they don't exist
        for directory in [self.input_dir, self.output_dir, self.templates_dir,
                         self.charts_dir, self.assets_dir, self.logs_dir]:
            directory.mkdir(parents=True, exist_ok=True)

        # Settings
        self.settings = {
            'app_name': 'SN Report Automation',
            'version': '1.0.0',
            'log_level': 'INFO',
            'chart_dpi': 300,
            'chart_format': 'png',
            'ppt_theme': 'default',
            'excel_sheets': ['Data', 'Metrics'],
        }

        # Load custom config if provided
        if config_file and Path(config_file).exists():
            self.load_config(config_file)

    def load_config(self, config_file):
        """
        Load configuration from JSON file.
        
        Args:
            config_file: Path to config JSON file
        """
        try:
            with open(config_file, 'r') as f:
                custom_settings = json.load(f)
                self.settings.update(custom_settings)
                logger.info(f"Loaded config from {config_file}")
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")

    def save_config(self, config_file):
        """
        Save configuration to JSON file.
        
        Args:
            config_file: Path to save config
        """
        try:
            with open(config_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
                logger.info(f"Saved config to {config_file}")
        except Exception as e:
            logger.error(f"Error saving config: {str(e)}")

    def get(self, key, default=None):
        """Get configuration value."""
        return self.settings.get(key, default)

    def set(self, key, value):
        """Set configuration value."""
        self.settings[key] = value

    def to_dict(self):
        """Return all settings as dictionary."""
        return self.settings.copy()


# Global config instance
_config = None


def get_config():
    """Get global config instance."""
    global _config
    if _config is None:
        _config = Config()
    return _config
