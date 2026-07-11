import csv
from pathlib import Path

from .utils import ensure_folder, format_timestamp


class CsvLogger:
    def __init__(self, output_path):
        self.output_path = Path(output_path)
        ensure_folder(self.output_path.parent)
        if not self.output_path.exists():
            with self.output_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerow(["Timestamp", "Recipient", "Application", "Status", "Message"])

    def log(self, recipient, application, status, message=""):
        timestamp = format_timestamp()
        with self.output_path.open("a", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow([timestamp, recipient, application, status, message])
