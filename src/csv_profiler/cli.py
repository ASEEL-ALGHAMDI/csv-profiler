import typer
from pathlib import Path

from csv_profiler.io import read_csv, write_json, write_text
from csv_profiler.profiling import profile_columns
from csv_profiler.render import render_markdown

app = typer.Typer()


@app.command()
def profile(
    csv_path: str,
    out_dir: str = "outputs",
    report_name: str = "report",
):
    rows = read_csv(csv_path)
    profiles = profile_columns(rows)

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    report_json = out / f"{report_name}.json"
    report_md = out / f"{report_name}.md"

    report_dict = {
        "source": csv_path,
        "rows": len(rows),
        "columns": [p.to_dict() for p in profiles],
    }

    md = render_markdown(csv_path, len(rows), profiles)

    write_json(str(report_json), report_dict)
    write_text(str(report_md), md)

    typer.echo(f"Wrote: {report_json}")
    typer.echo(f"Wrote: {report_md}")


def main():
    app()


if __name__ == "__main__":
    main()