"""Print how far estimates ran over the real time, by card kind: the factor to divide a first instinct by.

    py -3 <harness>/tools/calibrate.py [project]

Reads the brain's estimates.csv (written by log_estimate.py). The factor is total estimated ÷ total actual
minutes, so long cards weigh more than short ones. The median per-row factor is shown beside it.
"""

import csv
import sys
from dataclasses import dataclass
from pathlib import Path
from statistics import median

from log_estimate import estimates_path


@dataclass(frozen=True)
class Calibration:
    kind: str
    rows: int
    estimate_min: int
    actual_min: int
    median_factor: float

    @property
    def factor(self) -> float:
        return self.estimate_min / self.actual_min


def read_rows(path: Path, project: str | None = None) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return [row for row in csv.DictReader(handle) if project is None or row["project"] == project]


def calibrate(rows: list[dict[str, str]]) -> list[Calibration]:
    groups: dict[str, list[tuple[int, int]]] = {}
    for row in rows:
        pair = (int(row["estimate_min"]), int(row["actual_min"]))
        groups.setdefault(row["kind"] or "other", []).append(pair)
        groups.setdefault("all", []).append(pair)
    return [
        Calibration(
            kind=kind,
            rows=len(pairs),
            estimate_min=sum(e for e, _ in pairs),
            actual_min=sum(a for _, a in pairs),
            median_factor=median(e / a for e, a in pairs),
        )
        for kind, pairs in sorted(groups.items(), key=lambda item: (item[0] == "all", item[0]))
    ]


def report(results: list[Calibration]) -> str:
    if not results:
        return "No estimates logged yet."
    lines = [f"{'kind':<10}{'rows':>5}{'estimated':>11}{'actual':>8}{'factor':>8}{'median':>8}"]
    for c in results:
        lines.append(
            f"{c.kind:<10}{c.rows:>5}{c.estimate_min:>9} m{c.actual_min:>6} m{c.factor:>7.1f}x{c.median_factor:>7.1f}x"
        )
    lines.append("Divide a first-instinct estimate by its kind's factor. Few rows: trust it less.")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    print(report(calibrate(read_rows(estimates_path(), argv[0] if argv else None))))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
