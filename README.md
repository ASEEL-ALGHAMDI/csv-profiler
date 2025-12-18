CSV Profiler

CSV Profiler is a lightweight Python tool for quickly analyzing CSV files and generating clear data profiling reports.
It supports both a command-line interface (CLI) and an interactive Streamlit web UI.

The CLI is built with Typer, allowing the entire project to run from a single, clean command-line entry point.
Learn more about Typer: https://typer.tiangolo.com/

⸻⸻⸻

Features
	•	One-command CSV profiling via CLI
	•	Interactive Streamlit web interface
	•	Column-level statistics (type, missing values, uniqueness)
	•	Summary metrics and charts
	•	Export results as JSON and Markdown
	•	Clean project structure, ready for extension
⸻⸻⸻
Installation
pipx install csv-profiler

Or for local development:
pip install -e .
⸻⸻⸻
CLI Usage

Run the profiler with a single command:csv-profiler path/to/file.csv

Example: csv-profiler data/sample.csv --out-dir outputs --report-name report

This generates profiling reports in the specified output directory.
⸻⸻⸻
Streamlit UI

Launch the web interface: streamlit run app.py

From the UI you can:
	•	Upload a CSV file
	•	View metrics cards and charts
	•	Inspect column profiles
	•	Download reports as JSON or Markdown
⸻⸻⸻
Output

Each run generates:
	•	report.json — structured profiling data
	•	report.md — human-readable summary
⸻⸻⸻
Project Structure

csv-profiler/
├── app.py                 # Streamlit UI
├── main.py                # CLI entry point
├── pyproject.toml
├── data/
│   └── sample.csv
├── outputs/
├── src/csv_profiler/
│   ├── cli.py
│   ├── io.py
│   ├── models.py
│   ├── profiling.py
│   └── render.py
⸻⸻⸻
Requirements

Python 3.9+
