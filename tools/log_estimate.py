"""Append one row to the brain's estimates.csv: what a card was estimated at, and what it took.

    py -3 <harness>/tools/log_estimate.py <project> <plan> <card> <kind> <model> <estimate_min> <actual_min>

estimate_min is the first-instinct (nominal) estimate, before calibration: calibrate.py turns these rows into the
factor to divide by. kind groups cards that run alike: app, ui, docs, tooling, harness. Wall-clock minutes.
"""

import csv
import sys
from datetime import date
from pathlib import Path

from project import CONFIG_PATH, load_brain

FIELDS = ("date", "project", "plan", "card", "kind", "model", "estimate_min", "actual_min")


def estimates_path(config_path: Path = CONFIG_PATH) -> Path:
    return load_brain(config_path).root / "estimates.csv"


def append(path: Path, row: dict[str, str]) -> None:
    for key in ("estimate_min", "actual_min"):
        if not row[key].isdigit() or int(row[key]) == 0:
            raise ValueError(f"{key} must be a whole number of minutes above 0, not {row[key]!r}")
    new = not path.exists() or path.stat().st_size == 0
    with path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        if new:
            writer.writeheader()
        writer.writerow({field: row.get(field, "") for field in FIELDS})


def main(argv: list[str]) -> int:
    if len(argv) != len(FIELDS) - 1:
        print(__doc__)
        return 2
    row = dict(zip(FIELDS, [date.today().isoformat(), *argv], strict=True))
    append(estimates_path(), row)
    print(f"Logged {row['project']} {row['plan']} card {row['card']}: {row['estimate_min']} → {row['actual_min']} min")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
