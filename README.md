CSV Profiler

CSV Profiler is a lightweight command-line tool for profiling CSV files.
It reads a CSV file and generates simple profiling reports in JSON and Markdown formats.

The CLI is built with Typer, which allows the entire project to be executed using a single command-line entry point.
More about Typer: https://typer.tiangolo.com/

⸻

Installation

pipx install csv-profiler

⸻

Usage

Run the profiler with a single command:

csv-profiler path/to/file.csv

Example:

csv-profiler data/sample.csv –out-dir outputs –report-name report

⸻

Output

The command generates two files:

report.json
report.md

⸻

Requirements

Python 3.9+