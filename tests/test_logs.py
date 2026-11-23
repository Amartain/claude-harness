from pathlib import Path

import calibrate
import pytest
from log_estimate import append


def row(kind: str, estimate: int, actual: int, project: str = "p") -> dict[str, str]:
    return {
        "date": "2026-11-23",
        "project": project,
        "plan": "plan",
        "card": "1",
        "kind": kind,
        "model": "sonnet",
        "estimate_min": str(estimate),
        "actual_min": str(actual),
    }


def test_append_writes_the_header_once(tmp_path: Path) -> None:
    path = tmp_path / "estimates.csv"
    append(path, row("ui", 60, 10))
    append(path, row("ui", 30, 10))
    lines = path.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "date,project,plan,card,kind,model,estimate_min,actual_min"
    assert len(lines) == 3
    assert lines.count(lines[0]) == 1


@pytest.mark.parametrize("bad", ["", "abc", "0", "-5", "1.5"])
def test_append_refuses_minutes_that_are_not_whole_and_positive(tmp_path: Path, bad: str) -> None:
    with pytest.raises(ValueError):
        append(tmp_path / "e.csv", {**row("ui", 1, 1), "actual_min": bad})


def test_factor_by_kind_on_a_known_sample(tmp_path: Path) -> None:
    path = tmp_path / "estimates.csv"
    for sample in (row("ui", 60, 10), row("ui", 30, 10), row("app", 90, 30), row("app", 40, 10, project="q")):
        append(path, sample)
    results = {c.kind: c for c in calibrate.calibrate(calibrate.read_rows(path))}
    assert results["ui"].factor == pytest.approx(4.5)
    assert results["ui"].median_factor == pytest.approx(4.5)
    assert results["app"].factor == pytest.approx(130 / 40)
    assert results["all"].rows == 4
    only_p = {c.kind: c for c in calibrate.calibrate(calibrate.read_rows(path, "p"))}
    assert only_p["app"].rows == 1


def test_an_empty_log_says_so(tmp_path: Path) -> None:
    assert calibrate.report(calibrate.calibrate(calibrate.read_rows(tmp_path / "none.csv"))) == (
        "No estimates logged yet."
    )
