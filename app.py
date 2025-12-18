import io
import csv
import json
from datetime import datetime

import pandas as pd
import streamlit as st

from csv_profiler.profiling import profile_columns
from csv_profiler.render import render_markdown


# ---------- Helpers ----------
def read_csv_from_uploaded_file(uploaded_file) -> list[dict]:
    """
    Read a Streamlit UploadedFile and return rows as list[dict[str, str]].
    Keeps compatibility with csv_profiler.profile_columns(rows).
    """
    raw = uploaded_file.getvalue()
    text = raw.decode("utf-8-sig", errors="replace")
    f = io.StringIO(text)
    reader = csv.DictReader(f)
    return list(reader)


def build_report(filename: str, rows: list[dict], profiles) -> tuple[dict, str]:
    report_dict = {
        "source": filename,
        "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "rows": len(rows),
        "columns": [p.to_dict() for p in profiles],
    }
    md = render_markdown(filename, len(rows), profiles)
    return report_dict, md


def profiles_to_df(profiles) -> pd.DataFrame:
    data = [p.to_dict() for p in profiles]
    df = pd.DataFrame(data)

    for col in ["total", "missing", "unique"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    if "missing_pct" in df.columns:
        df["missing_pct"] = pd.to_numeric(df["missing_pct"], errors="coerce").fillna(0.0)

    if "type" in df.columns:
        df["type"] = df["type"].fillna("unknown").astype(str)

    if "name" in df.columns:
        df["name"] = df["name"].fillna("unknown").astype(str)

    return df


# ---------- UI ----------
st.set_page_config(page_title="CSV Profiler", page_icon="📄", layout="wide")

st.title("CSV Profiler")
st.caption("Upload a CSV to instantly analyze columns, types, and data quality.")

with st.sidebar:
    st.header("Upload")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    st.divider()
    st.header("Display")
    show_table = st.toggle("Show raw table preview", value=True)
    max_rows_preview = st.slider("Preview rows", 5, 200, 25)

    st.divider()
    st.header("Downloads")
    st.caption("After processing, download JSON / Markdown here.")


if not uploaded_file:
    st.info("Upload a CSV file from the sidebar to start.")
    st.stop()

# ---------- Processing ----------
try:
    rows = read_csv_from_uploaded_file(uploaded_file)
    if not rows:
        st.warning("The uploaded CSV appears to be empty (no rows).")
        st.stop()

    profiles = profile_columns(rows)
    report_dict, report_md = build_report(uploaded_file.name, rows, profiles)

    df_profiles = profiles_to_df(profiles)
    df_data = pd.DataFrame(rows)

except Exception as e:
    st.error(f"Failed to process CSV: {e}")
    st.stop()


# ---------- Top Metrics ----------
total_rows = len(rows)
total_cols = len(df_data.columns)
total_missing = int(df_profiles["missing"].sum()) if "missing" in df_profiles.columns else 0
missing_rate = (total_missing / (total_rows * max(total_cols, 1))) * 100 if total_rows else 0

num_cols = int((df_profiles["type"] == "number").sum()) if "type" in df_profiles.columns else 0
text_cols = int((df_profiles["type"] == "text").sum()) if "type" in df_profiles.columns else 0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Rows", f"{total_rows:,}")
c2.metric("Columns", f"{total_cols:,}")
c3.metric("Total Missing", f"{total_missing:,}")
c4.metric("Missing Rate", f"{missing_rate:.2f}%")
c5.metric("Types", f"{num_cols} number • {text_cols} text")

st.divider()


# ---------- Downloads ----------
json_bytes = json.dumps(report_dict, indent=2, ensure_ascii=False).encode("utf-8")
md_bytes = report_md.encode("utf-8")

with st.sidebar:
    st.download_button(
        label="⬇️ Download report.json",
        data=json_bytes,
        file_name="report.json",
        mime="application/json",
        use_container_width=True,
    )
    st.download_button(
        label="⬇️ Download report.md",
        data=md_bytes,
        file_name="report.md",
        mime="text/markdown",
        use_container_width=True,
    )


# ---------- Layout: Preview + Insights ----------
left, right = st.columns([1.1, 0.9], gap="large")

with left:
    st.subheader("Preview")
    if show_table:
        st.dataframe(df_data.head(max_rows_preview), use_container_width=True)
    else:
        st.caption("Preview is turned off from the sidebar.")

    st.subheader("Columns Summary")
    summary_cols = [c for c in ["name", "type", "total", "missing", "missing_pct", "unique"] if c in df_profiles.columns]
    st.dataframe(
        df_profiles[summary_cols].sort_values(by="missing_pct", ascending=False) if "missing_pct" in df_profiles.columns else df_profiles[summary_cols],
        use_container_width=True,
        height=360,
    )


with right:
    st.subheader("Insights")

    if "missing_pct" in df_profiles.columns:
        st.markdown("*Missing % by column*")
        miss_df = df_profiles[["name", "missing_pct"]].sort_values("missing_pct", ascending=False).head(20)
        st.bar_chart(miss_df.set_index("name"))

    if "unique" in df_profiles.columns:
        st.markdown("*Top unique counts (first 20)*")
        uniq_df = df_profiles[["name", "unique"]].sort_values("unique", ascending=False).head(20)
        st.bar_chart(uniq_df.set_index("name"))

    if "type" in df_profiles.columns:
        st.markdown("*Type distribution*")
        type_counts = df_profiles["type"].value_counts().rename_axis("type").reset_index(name="count")
        st.dataframe(type_counts, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("Per-column Details")
    st.caption("Open a column to view its full JSON profile.")

    for _, row in df_profiles.sort_values(by="missing_pct", ascending=False).iterrows() if "missing_pct" in df_profiles.columns else df_profiles.iterrows():
        col_name = row.get("name", "unknown")
        with st.expander(f"{col_name}"):
            prof = next((p for p in profiles if getattr(p, "name", None) == col_name), None)
            if prof:
                st.json(prof.to_dict())
            else:
                st.json(dict(row))


st.divider()
st.subheader("Markdown Report Preview")
st.code(report_md, language="markdown")