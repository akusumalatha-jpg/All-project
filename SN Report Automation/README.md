# SN Report Automation

Automated report generation from Excel data to PowerPoint presentations with KPI metrics and data visualizations.

## Features

- **Excel Reader**: Load and parse Excel files with error handling
- **KPI Metrics**: Calculate comprehensive metrics (sum, average, count, unique, percentiles, min/max)
- **PowerPoint Generator**: Create and update presentations with data
- **Chart Generator**: Generate professional charts (bar, line, pie, histogram, scatter, box plot, heatmap)
- **Desktop GUI**: User-friendly interface for running workflows
- **Logging**: Comprehensive logging of all operations

## Project Structure

```
SN_Report_Automation/
├── src/
│   ├── __init__.py
│   ├── main.py              # Main application orchestrator
│   ├── excel_reader.py      # Excel file handling
│   ├── metrics.py           # KPI calculations
│   ├── ppt_updater.py       # PowerPoint updates
│   ├── chart_generator.py   # Chart creation
│   ├── gui.py               # Desktop GUI
│   ├── config.py            # Configuration management
│   └── utils.py             # Utility functions
├── input/                   # Input Excel files
├── output/                  # Generated PowerPoint files
├── templates/               # PowerPoint templates
├── charts/                  # Generated chart images
├── assets/                  # Asset files
├── logs/                    # Application logs
├── requirements.txt         # Python dependencies
└── README.md
```

## Installation

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Setup

1. Clone or extract the project:
```bash
cd SN_Report_Automation
```

2. Create virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### GUI Application

```bash
python -m src.gui
```

This opens a desktop application with:
- **Workflow Tab**: Select files and run automation
- **Settings Tab**: View configuration and paths
- **Logs Tab**: Monitor execution and troubleshoot

### Command Line

```python
from src.main import ReportAutomation

app = ReportAutomation()
app.run_full_workflow('path/to/file.xlsx', template_file='path/to/template.pptx')
```

### Python API

#### Reading Excel Files
```python
from src.excel_reader import ExcelReader

reader = ExcelReader('input')
wb = reader.load_workbook('data.xlsx')
data = reader.read_sheet_as_dict(wb, 'Sheet1')
```

#### Calculating Metrics
```python
from src.metrics import MetricsCalculator

calculator = MetricsCalculator()
total_kpi = calculator.sum_column(data, 'Sales', 'Total Sales')
avg_kpi = calculator.average_column(data, 'Sales', 'Average Sales')
```

#### Creating Charts
```python
from src.chart_generator import ChartGenerator

charts = ChartGenerator('charts')
charts.create_bar_chart(
    data=[100, 200, 150],
    categories=['Q1', 'Q2', 'Q3'],
    title='Quarterly Sales',
    x_label='Quarter',
    y_label='Sales ($)',
    filename='sales.png'
)
```

#### Updating PowerPoint
```python
from src.ppt_updater import PowerPointUpdater

ppt = PowerPointUpdater()
ppt.load_template('templates/template.pptx')
ppt.add_slide_with_title('Report', 'Auto-generated')
ppt.save_presentation('output/report.pptx')
```

## Module Documentation

### ExcelReader
Loads and parses Excel files:
- `get_excel_files()` - List Excel files in directory
- `load_workbook(path)` - Load workbook
- `read_sheet_as_dict(wb, sheet)` - Read as dictionaries
- `read_sheet_as_list(wb, sheet)` - Read as lists
- `get_cell_value(wb, sheet, row, col)` - Get specific cell

### MetricsCalculator
Calculates key performance indicators:
- `sum_column()` - Sum column values
- `average_column()` - Calculate average
- `count_rows()` - Count total rows
- `count_unique()` - Count unique values
- `group_by()` - Group and aggregate
- `percentile()` - Calculate percentile
- `min_max()` - Find min/max values
- `create_summary()` - Create multi-KPI report

### ChartGenerator
Creates visualizations:
- `create_bar_chart()` - Bar chart
- `create_line_chart()` - Line chart
- `create_pie_chart()` - Pie chart
- `create_histogram()` - Histogram
- `create_scatter_plot()` - Scatter plot
- `create_box_plot()` - Box plot
- `create_heatmap()` - Heatmap

### PowerPointUpdater
Updates presentations:
- `load_template()` - Load template
- `create_blank()` - Create blank presentation
- `add_slide_with_title()` - Add titled slide
- `update_text_in_slide()` - Update text
- `add_text_box()` - Add text box
- `add_table()` - Add table
- `add_image()` - Add image
- `save_presentation()` - Save to file

## Configuration

Configuration is managed through `src/config.py`:

```python
from src.config import get_config

config = get_config()
config.get('chart_dpi')  # 300
config.set('chart_dpi', 600)
```

### Default Settings
- `app_name`: SN Report Automation
- `version`: 1.0.0
- `chart_dpi`: 300
- `chart_format`: png
- `log_level`: INFO

## Logging

Logs are saved to `logs/` directory with timestamp:
```
logs/report_20240711_152030.log
```

Access logs programmatically:
```python
from src.utils import setup_logging
logger = setup_logging('logs', logging.INFO)
logger.info("Message")
```

## Requirements

- `openpyxl` - Excel file handling
- `python-pptx` - PowerPoint generation
- `matplotlib` - Chart generation

See `requirements.txt` for all dependencies.

## Examples

### Example 1: Simple Workflow
```python
from src.main import ReportAutomation

app = ReportAutomation()
app.run_full_workflow('input/sales_data.xlsx')
```

### Example 2: Custom Metrics
```python
from src.excel_reader import ExcelReader
from src.metrics import MetricsCalculator

reader = ExcelReader()
wb = reader.load_workbook('input/data.xlsx')
data = reader.read_sheet_as_dict(wb, 'Sales')

calc = MetricsCalculator()
summary = calc.create_summary(data, [
    {'type': 'count', 'label': 'Total Records'},
    {'type': 'sum', 'column': 'Revenue', 'label': 'Total Revenue'},
    {'type': 'average', 'column': 'Revenue', 'label': 'Avg Revenue'},
    {'type': 'group', 'column': 'Region', 'aggregate_column': 'Revenue'},
])
```

### Example 3: Generate Charts
```python
from src.chart_generator import ChartGenerator

charts = ChartGenerator()
charts.create_bar_chart(
    data=[500, 1200, 800, 1500],
    categories=['Jan', 'Feb', 'Mar', 'Apr'],
    title='Monthly Revenue',
    x_label='Month',
    y_label='Revenue ($)',
    filename='revenue.png'
)
```

## Troubleshooting

### Excel file not found
- Ensure file is in the `input/` directory
- Check file extension (.xlsx or .xls)
- Verify file is not corrupted

### PowerPoint template error
- Verify template file path
- Ensure .pptx format
- Check template is not password-protected

### GUI doesn't start
- Ensure tkinter is installed (usually included with Python)
- On Linux, may need: `sudo apt-get install python3-tk`

### Charts not appearing
- Verify matplotlib is installed: `pip install matplotlib`
- Check charts/ directory has write permissions

## Testing

Run module tests:
```bash
python -c "from src.main import ReportAutomation; ReportAutomation().run_minimal_test()"
```

## License

Project maintained for internal use.

## Support

For issues or questions, check:
1. Application logs in `logs/` directory
2. Module documentation above
3. Source code comments
