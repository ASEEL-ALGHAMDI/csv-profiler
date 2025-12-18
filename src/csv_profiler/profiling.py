from collections import defaultdict

from csv_profiler.models import ColumnProfile


MISSING = {"", "na", "n/a", "null", "none", "nan"}


def is_missing(value: str | None) -> bool:
    if value is None:
        return True
    return value.strip().casefold() in MISSING


def try_float(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None


def infer_type(values: list[str]) -> str:
    usable = [v for v in values if not is_missing(v)]
    if not usable:
        return "text"

    for v in usable:
        if try_float(v) is None:
            return "text"

    return "number"


def profile_columns(rows: list[dict[str, str]]) -> list[ColumnProfile]:
    columns: dict[str, list[str]] = defaultdict(list)

    for row in rows:
        for col, val in row.items():
            columns[col].append(val)

    profiles: list[ColumnProfile] = []

    for name, values in columns.items():
        total = len(values)
        missing = sum(1 for v in values if is_missing(v))
        unique = len({v for v in values if not is_missing(v)})
        inferred_type = infer_type(values)

        profiles.append(
            ColumnProfile(
                name=name,
                inferred_type=inferred_type,
                total=total,
                missing=missing,
                unique=unique,
            )
        )

    return profiles