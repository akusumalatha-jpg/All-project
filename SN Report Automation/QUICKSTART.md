# Quick Start Guide

## Running the Desktop GUI

```bash
python -m src.gui
```

This launches the desktop application with:
- **Workflow Tab**: Select Excel file, template (optional), and generate reports
- **Settings Tab**: View configuration paths and settings
- **Logs Tab**: Monitor execution and troubleshoot

## Running from Command Line

```bash
python -m src.main
```

This runs the test mode and shows all modules are functional.

## Using the Python API

```python
from src.main import ReportAutomation

app = ReportAutomation()

# Run full workflow
app.run_full_workflow(
    excel_file='input/data.xlsx',
    template_file='templates/template.pptx',
    output_name='report.pptx'
)

# Run test
app.run_minimal_test()

# List input files
files = app.list_input_files()
```

## Workflow Steps

1. **Place Excel file** in `input/` directory
2. **Place template** (optional) in `templates/` directory
3. **Run GUI** or use Python API
4. **View output** in `output/` directory

## Project Structure

```
src/
├── excel_reader.py      - Load Excel files
├── metrics.py           - Calculate KPIs
├── ppt_updater.py       - Create/update presentations
├── chart_generator.py   - Generate visualizations
├── gui.py               - Desktop interface
├── main.py              - Main orchestrator
├── config.py            - Settings management
├── utils.py             - Helper functions
└── __init__.py          - Package initialization

input/                  - Place Excel files here
output/                 - Reports generated here
templates/              - PowerPoint templates
charts/                 - Generated chart images
logs/                   - Application logs
```

## Module Summary

### Excel Reader
```python
from src.excel_reader import ExcelReader

reader = ExcelReader('input')
wb = reader.load_workbook('data.xlsx')
data = reader.read_sheet_as_dict(wb, 'Sheet1')
```

### Metrics Calculator
```python
from src.metrics import MetricsCalculator

calc = MetricsCalculator()
summary = calc.create_summary(data, [
    {'type': 'sum', 'column': 'Sales'},
    {'type': 'average', 'column': 'Sales'},
])
```

### Chart Generator
```python
from src.chart_generator import ChartGenerator

charts = ChartGenerator('charts')
charts.create_bar_chart([100, 200, 150], ['Q1', 'Q2', 'Q3'],
    title='Sales', x_label='Quarter', y_label='$',
    filename='sales.png')
```

### PowerPoint Updater
```python
from src.ppt_updater import PowerPointUpdater

ppt = PowerPointUpdater()
ppt.load_template('templates/template.pptx')
ppt.add_slide_with_title('Report', 'Auto-generated')
ppt.save_presentation('output/report.pptx')
```

## Key Features

✓ Load & parse Excel files  
✓ Calculate comprehensive KPIs  
✓ Generate professional charts  
✓ Create/update PowerPoint presentations  
✓ Desktop GUI with status monitoring  
✓ Comprehensive logging  
✓ Error handling throughout  

## Support

- Check `logs/` for detailed execution logs
- See `README.md` for full documentation
- Module source code includes docstrings
