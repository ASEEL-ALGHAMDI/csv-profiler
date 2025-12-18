from datetime import datetime

from csv_profiler.models import ColumnProfile


def md_header(source: str) -> list[str]:
    ts = datetime.now().isoformat(timespec="seconds")
    return [
        "# CSV Profiling Report",
        "",
        f"- Source: {source}",
        f"- Generated: {ts}",
        "",
    ]


def md_table_header() -> list[str]:
    return [
        "| Column | Type | Missing | Unique |",
        "|---|---:|---:|---:|",
    ]


def md_col_row(p: ColumnProfile) -> str:
    return f"| {p.name} | {p.inferred_type} | {p.missing} ({p.missing_pct/100:.1%}) | {p.unique} |"


def render_markdown(source: str, n_rows: int, profiles: list[ColumnProfile]) -> str:
    lines: list[str] = []
    lines += md_header(source)

    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Rows: {n_rows:,}")
    lines.append(f"- Columns: {len(profiles):,}")
    lines.append("")

    lines.append("## Columns")
    lines.append("")
    lines += md_table_header()
    for p in profiles:
        lines.append(md_col_row(p))
    lines.append("")

    return "\n".join(lines) + "\n"