"""
Chart Generator Module
Creates visualizations from data.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
import logging

logger = logging.getLogger(__name__)


class ChartGenerator:
    """Generates charts from data."""

    def __init__(self, output_dir='charts', dpi=300):
        """
        Initialize chart generator.
        
        Args:
            output_dir: Directory to save charts
            dpi: Resolution in dots per inch
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.dpi = dpi

    def create_bar_chart(self, data, categories, title, x_label, y_label, filename):
        """
        Create bar chart.
        
        Args:
            data: List of values
            categories: List of category labels
            title: Chart title
            x_label: X-axis label
            y_label: Y-axis label
            filename: Output filename
            
        Returns:
            True if successful
        """
        try:
            plt.figure(figsize=(10, 6))
            plt.bar(categories, data, color='steelblue', edgecolor='black', alpha=0.7)
            plt.title(title, fontsize=14, fontweight='bold')
            plt.xlabel(x_label, fontsize=12)
            plt.ylabel(y_label, fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            output_path = self.output_dir / filename
            plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
            plt.close()

            logger.info(f"Created bar chart: {filename}")
            return True

        except Exception as e:
            logger.error(f"Error creating bar chart: {str(e)}")
            return False

    def create_line_chart(self, x_data, y_data, labels, title, x_label, y_label, filename):
        """
        Create line chart.
        
        Args:
            x_data: X-axis data
            y_data: List of y-axis data series
            labels: Series labels
            title: Chart title
            x_label: X-axis label
            y_label: Y-axis label
            filename: Output filename
            
        Returns:
            True if successful
        """
        try:
            plt.figure(figsize=(12, 6))

            for y_series, label in zip(y_data, labels):
                plt.plot(x_data, y_series, marker='o', label=label, linewidth=2)

            plt.title(title, fontsize=14, fontweight='bold')
            plt.xlabel(x_label, fontsize=12)
            plt.ylabel(y_label, fontsize=12)
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            output_path = self.output_dir / filename
            plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
            plt.close()

            logger.info(f"Created line chart: {filename}")
            return True

        except Exception as e:
            logger.error(f"Error creating line chart: {str(e)}")
            return False

    def create_pie_chart(self, data, labels, title, filename):
        """
        Create pie chart.
        
        Args:
            data: List of values
            labels: List of labels
            title: Chart title
            filename: Output filename
            
        Returns:
            True if successful
        """
        try:
            plt.figure(figsize=(10, 8))
            colors = plt.cm.Set3(range(len(data)))
            plt.pie(data, labels=labels, autopct='%1.1f%%', colors=colors,
                   startangle=90, textprops={'fontsize': 10})
            plt.title(title, fontsize=14, fontweight='bold')
            plt.tight_layout()

            output_path = self.output_dir / filename
            plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
            plt.close()

            logger.info(f"Created pie chart: {filename}")
            return True

        except Exception as e:
            logger.error(f"Error creating pie chart: {str(e)}")
            return False

    def create_histogram(self, data, bins, title, x_label, y_label, filename):
        """
        Create histogram.
        
        Args:
            data: List of values
            bins: Number of bins
            title: Chart title
            x_label: X-axis label
            y_label: Y-axis label
            filename: Output filename
            
        Returns:
            True if successful
        """
        try:
            plt.figure(figsize=(10, 6))
            plt.hist(data, bins=bins, color='skyblue', edgecolor='black', alpha=0.7)
            plt.title(title, fontsize=14, fontweight='bold')
            plt.xlabel(x_label, fontsize=12)
            plt.ylabel(y_label, fontsize=12)
            plt.grid(True, alpha=0.3, axis='y')
            plt.tight_layout()

            output_path = self.output_dir / filename
            plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
            plt.close()

            logger.info(f"Created histogram: {filename}")
            return True

        except Exception as e:
            logger.error(f"Error creating histogram: {str(e)}")
            return False

    def create_scatter_plot(self, x_data, y_data, title, x_label, y_label, filename):
        """
        Create scatter plot.
        
        Args:
            x_data: X-axis data
            y_data: Y-axis data
            title: Chart title
            x_label: X-axis label
            y_label: Y-axis label
            filename: Output filename
            
        Returns:
            True if successful
        """
        try:
            plt.figure(figsize=(10, 6))
            plt.scatter(x_data, y_data, alpha=0.6, s=50, color='steelblue', edgecolors='black')
            plt.title(title, fontsize=14, fontweight='bold')
            plt.xlabel(x_label, fontsize=12)
            plt.ylabel(y_label, fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()

            output_path = self.output_dir / filename
            plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
            plt.close()

            logger.info(f"Created scatter plot: {filename}")
            return True

        except Exception as e:
            logger.error(f"Error creating scatter plot: {str(e)}")
            return False

    def create_box_plot(self, data, labels, title, y_label, filename):
        """
        Create box plot.
        
        Args:
            data: List of data series
            labels: Series labels
            title: Chart title
            y_label: Y-axis label
            filename: Output filename
            
        Returns:
            True if successful
        """
        try:
            plt.figure(figsize=(10, 6))
            plt.boxplot(data, labels=labels)
            plt.title(title, fontsize=14, fontweight='bold')
            plt.ylabel(y_label, fontsize=12)
            plt.grid(True, alpha=0.3, axis='y')
            plt.tight_layout()

            output_path = self.output_dir / filename
            plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
            plt.close()

            logger.info(f"Created box plot: {filename}")
            return True

        except Exception as e:
            logger.error(f"Error creating box plot: {str(e)}")
            return False

    def create_heatmap(self, data, x_labels, y_labels, title, filename):
        """
        Create heatmap.
        
        Args:
            data: 2D array of values
            x_labels: X-axis labels
            y_labels: Y-axis labels
            title: Chart title
            filename: Output filename
            
        Returns:
            True if successful
        """
        try:
            import numpy as np
            plt.figure(figsize=(10, 8))
            im = plt.imshow(data, cmap='YlOrRd', aspect='auto')
            plt.colorbar(im)
            plt.xticks(range(len(x_labels)), x_labels, rotation=45, ha='right')
            plt.yticks(range(len(y_labels)), y_labels)
            plt.title(title, fontsize=14, fontweight='bold')
            plt.tight_layout()

            output_path = self.output_dir / filename
            plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
            plt.close()

            logger.info(f"Created heatmap: {filename}")
            return True

        except Exception as e:
            logger.error(f"Error creating heatmap: {str(e)}")
            return False

    def get_chart_files(self):
        """Get list of generated chart files."""
        return sorted(list(self.output_dir.glob('*.png')))
