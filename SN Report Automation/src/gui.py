"""
Desktop GUI Application
User interface for SN Report Automation.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from pathlib import Path
import logging
from datetime import datetime

from src.config import get_config
from src.utils import setup_logging
from src.main import ReportAutomation


class ReportAutomationGUI:
    """Desktop GUI for SN Report Automation."""

    def __init__(self, root):
        """Initialize GUI."""
        self.root = root
        self.root.title("SN Report Automation")
        self.root.geometry("900x700")
        self.root.resizable(False, False)

        self.config = get_config()
        self.logger = setup_logging(self.config.logs_dir, logging.INFO)
        self.app = ReportAutomation()

        self.selected_excel = None
        self.selected_template = None
        self.is_running = False

        self.setup_ui()
        self.logger.info("GUI initialized")

    def setup_ui(self):
        """Setup user interface."""
        style = ttk.Style()
        style.theme_use('clam')

        self.root.configure(bg='#f0f0f0')

        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill='x', padx=20, pady=10)

        title = ttk.Label(
            header_frame,
            text="SN Report Automation",
            font=("Arial", 16, "bold")
        )
        title.pack(side='left')

        version = ttk.Label(
            header_frame,
            text=f"v{self.config.get('version')}",
            font=("Arial", 10)
        )
        version.pack(side='right')

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=20, pady=10)

        self.setup_workflow_tab(notebook)
        self.setup_settings_tab(notebook)
        self.setup_logs_tab(notebook)

        footer_frame = ttk.Frame(self.root)
        footer_frame.pack(fill='x', padx=20, pady=10)

        status_label = ttk.Label(
            footer_frame,
            text="Ready",
            font=("Arial", 9)
        )
        status_label.pack(side='left')
        self.status_label = status_label

    def setup_workflow_tab(self, notebook):
        """Setup workflow tab."""
        workflow_frame = ttk.Frame(notebook)
        notebook.add(workflow_frame, text="Workflow")

        ttk.Label(workflow_frame, text="1. Select Excel File", font=("Arial", 11, "bold")).pack(anchor='w', padx=20, pady=(20, 10))

        excel_select_frame = ttk.Frame(workflow_frame)
        excel_select_frame.pack(fill='x', padx=20, pady=10)

        self.excel_label = ttk.Label(excel_select_frame, text="No file selected", foreground="gray")
        self.excel_label.pack(side='left', fill='x', expand=True)

        ttk.Button(
            excel_select_frame,
            text="Browse",
            command=self.select_excel_file
        ).pack(side='right')

        ttk.Label(workflow_frame, text="2. Select Template (Optional)", font=("Arial", 11, "bold")).pack(anchor='w', padx=20, pady=(20, 10))

        template_select_frame = ttk.Frame(workflow_frame)
        template_select_frame.pack(fill='x', padx=20, pady=10)

        self.template_label = ttk.Label(template_select_frame, text="No template selected", foreground="gray")
        self.template_label.pack(side='left', fill='x', expand=True)

        ttk.Button(
            template_select_frame,
            text="Browse",
            command=self.select_template_file
        ).pack(side='right')

        ttk.Label(workflow_frame, text="3. Output Settings", font=("Arial", 11, "bold")).pack(anchor='w', padx=20, pady=(20, 10))

        output_frame = ttk.Frame(workflow_frame)
        output_frame.pack(fill='x', padx=20, pady=10)

        ttk.Label(output_frame, text="Output Filename:").pack(side='left', padx=(0, 10))
        self.output_entry = ttk.Entry(output_frame, width=30)
        self.output_entry.insert(0, f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx")
        self.output_entry.pack(side='left')

        ttk.Separator(workflow_frame, orient='horizontal').pack(fill='x', pady=20)

        button_frame = ttk.Frame(workflow_frame)
        button_frame.pack(padx=20, pady=20)

        self.run_button = ttk.Button(
            button_frame,
            text="▶ Run Automation",
            command=self.run_automation
        )
        self.run_button.pack(side='left', padx=5)

        ttk.Button(
            button_frame,
            text="⟳ Test",
            command=self.run_test
        ).pack(side='left', padx=5)

        ttk.Button(
            button_frame,
            text="📁 Open Output",
            command=self.open_output_folder
        ).pack(side='left', padx=5)

        progress_frame = ttk.Frame(workflow_frame)
        progress_frame.pack(fill='x', padx=20, pady=20)

        self.progress = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress.pack(fill='x')

        self.result_label = ttk.Label(workflow_frame, text="", font=("Arial", 10))
        self.result_label.pack(padx=20, pady=10)

    def setup_settings_tab(self, notebook):
        """Setup settings tab."""
        settings_frame = ttk.Frame(notebook)
        notebook.add(settings_frame, text="Settings")

        ttk.Label(settings_frame, text="Configuration", font=("Arial", 11, "bold")).pack(anchor='w', padx=20, pady=(20, 10))

        settings_inner = ttk.Frame(settings_frame)
        settings_inner.pack(fill='both', expand=True, padx=20, pady=10)

        ttk.Label(settings_inner, text="Input Directory:").grid(row=0, column=0, sticky='w', pady=5)
        ttk.Label(settings_inner, text=str(self.config.input_dir)).grid(row=0, column=1, sticky='w', pady=5)

        ttk.Label(settings_inner, text="Output Directory:").grid(row=1, column=0, sticky='w', pady=5)
        ttk.Label(settings_inner, text=str(self.config.output_dir)).grid(row=1, column=1, sticky='w', pady=5)

        ttk.Label(settings_inner, text="Charts Directory:").grid(row=2, column=0, sticky='w', pady=5)
        ttk.Label(settings_inner, text=str(self.config.charts_dir)).grid(row=2, column=1, sticky='w', pady=5)

        ttk.Label(settings_inner, text="Templates Directory:").grid(row=3, column=0, sticky='w', pady=5)
        ttk.Label(settings_inner, text=str(self.config.templates_dir)).grid(row=3, column=1, sticky='w', pady=5)

        ttk.Label(settings_inner, text="Logs Directory:").grid(row=4, column=0, sticky='w', pady=5)
        ttk.Label(settings_inner, text=str(self.config.logs_dir)).grid(row=4, column=1, sticky='w', pady=5)

        ttk.Label(settings_inner, text="Chart DPI:").grid(row=5, column=0, sticky='w', pady=5)
        ttk.Label(settings_inner, text=str(self.config.get('chart_dpi'))).grid(row=5, column=1, sticky='w', pady=5)

    def setup_logs_tab(self, notebook):
        """Setup logs tab."""
        logs_frame = ttk.Frame(notebook)
        notebook.add(logs_frame, text="Logs")

        ttk.Label(logs_frame, text="Application Logs", font=("Arial", 11, "bold")).pack(anchor='w', padx=20, pady=(20, 10))

        text_frame = ttk.Frame(logs_frame)
        text_frame.pack(fill='both', expand=True, padx=20, pady=10)

        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side='right', fill='y')

        self.logs_text = tk.Text(text_frame, height=20, width=80, yscrollcommand=scrollbar.set)
        self.logs_text.pack(fill='both', expand=True)
        scrollbar.config(command=self.logs_text.yview)

        button_frame = ttk.Frame(logs_frame)
        button_frame.pack(padx=20, pady=10)

        ttk.Button(button_frame, text="Clear Logs", command=self.clear_logs).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Copy All", command=self.copy_logs).pack(side='left', padx=5)

    def select_excel_file(self):
        """Select Excel file."""
        file = filedialog.askopenfilename(
            initialdir=self.config.input_dir,
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if file:
            self.selected_excel = file
            self.excel_label.config(text=Path(file).name, foreground="black")
            self.log_to_gui(f"Selected: {file}")

    def select_template_file(self):
        """Select template file."""
        file = filedialog.askopenfilename(
            initialdir=self.config.templates_dir,
            filetypes=[("PowerPoint files", "*.pptx"), ("All files", "*.*")]
        )
        if file:
            self.selected_template = file
            self.template_label.config(text=Path(file).name, foreground="black")
            self.log_to_gui(f"Template selected: {file}")

    def run_automation(self):
        """Run automation workflow."""
        if not self.selected_excel:
            messagebox.showerror("Error", "Please select an Excel file first")
            return

        if self.is_running:
            messagebox.showwarning("Warning", "Automation is already running")
            return

        output_name = self.output_entry.get() or "report.pptx"

        thread = threading.Thread(
            target=self._run_automation_thread,
            args=(self.selected_excel, self.selected_template, output_name)
        )
        thread.start()

    def _run_automation_thread(self, excel_file, template_file, output_name):
        """Run automation in separate thread."""
        try:
            self.is_running = True
            self.run_button.config(state='disabled')
            self.progress.start()
            self.log_to_gui("Starting automation...")

            success = self.app.run_full_workflow(excel_file, template_file, output_name)

            if success:
                self.result_label.config(text="✓ Automation completed successfully!", foreground="green")
                self.log_to_gui("✓ Automation completed!")
                messagebox.showinfo("Success", "Report generated successfully!")
            else:
                self.result_label.config(text="✗ Automation failed", foreground="red")
                self.log_to_gui("✗ Automation failed!")
                messagebox.showerror("Error", "Automation failed. Check logs for details.")

        except Exception as e:
            self.result_label.config(text=f"✗ Error: {str(e)}", foreground="red")
            self.log_to_gui(f"✗ Error: {str(e)}")
            messagebox.showerror("Error", str(e))
        finally:
            self.is_running = False
            self.run_button.config(state='normal')
            self.progress.stop()

    def run_test(self):
        """Run test."""
        thread = threading.Thread(target=self._run_test_thread)
        thread.start()

    def _run_test_thread(self):
        """Run test in separate thread."""
        try:
            self.progress.start()
            self.log_to_gui("Running module test...")

            if self.app.run_minimal_test():
                self.result_label.config(text="✓ All modules functional!", foreground="green")
                messagebox.showinfo("Test Passed", "All modules are working correctly!")
            else:
                self.result_label.config(text="✗ Test failed", foreground="red")
                messagebox.showerror("Test Failed", "Module test failed!")

        except Exception as e:
            self.log_to_gui(f"✗ Test error: {str(e)}")
        finally:
            self.progress.stop()

    def open_output_folder(self):
        """Open output folder."""
        import subprocess
        import sys
        try:
            if sys.platform == 'win32':
                subprocess.Popen(f'explorer {self.config.output_dir}')
            else:
                subprocess.Popen(['open', str(self.config.output_dir)])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open folder: {str(e)}")

    def log_to_gui(self, message):
        """Add message to logs display."""
        self.logs_text.insert('end', f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
        self.logs_text.see('end')
        self.root.update()

    def clear_logs(self):
        """Clear log display."""
        self.logs_text.delete('1.0', 'end')

    def copy_logs(self):
        """Copy all logs to clipboard."""
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.logs_text.get('1.0', 'end'))
            messagebox.showinfo("Success", "Logs copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", str(e))


def main():
    """Main entry point for GUI."""
    root = tk.Tk()
    gui = ReportAutomationGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
