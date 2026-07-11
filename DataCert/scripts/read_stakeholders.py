import csv
from pathlib import Path

from .utils import validate_email


def _normalize_headers(headers):
    return [str(header).strip().lower() for header in headers]


def _normalize_row(row, headers):
    data = {headers[i]: (row[i] if i < len(row) else "") for i in range(len(headers))}
    return {
        "Name": str(data.get("name", "")).strip(),
        "Email": str(data.get("email", "")).strip(),
        "Application": str(data.get("application", "")).strip(),
        "Due Date": str(data.get("due date", "")).strip(),
        **{k: v for k, v in data.items() if k not in {"name", "email", "application", "due date"}},
    }


def read_stakeholders(path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Stakeholder file not found: {path}")

    extension = path.suffix.lower()
    rows = []

    if extension in {".xlsx", ".xls"}:
        try:
            import pandas as pd
        except ImportError as exc:
            raise ImportError("pandas is required to read Excel files. Install it with pip install pandas openpyxl") from exc

        df = pd.read_excel(path, dtype=str)
        df = df.fillna("")
        headers = _normalize_headers(df.columns)
        for _, row in df.iterrows():
            stakeholder = _normalize_row(list(row.values), headers)
            rows.append(stakeholder)

    elif extension == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            headers = None
            for row in reader:
                if not row or all(cell.strip() == "" for cell in row):
                    continue
                if headers is None:
                    headers = _normalize_headers(row)
                    continue
                stakeholder = _normalize_row(row, headers)
                rows.append(stakeholder)
    else:
        raise ValueError("Unsupported stakeholder file format. Use .csv or .xlsx")

    valid_rows = []
    for stakeholder in rows:
        if not stakeholder["Name"] or not stakeholder["Email"]:
            continue
        if not validate_email(stakeholder["Email"]):
            continue
        valid_rows.append(stakeholder)

    return valid_rows
