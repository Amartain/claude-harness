from datetime import datetime
from pathlib import Path

import pytest
import startup
from store import Brain, load_state, report_error


@pytest.fixture
def brain(tmp_path: Path) -> Brain:
    root = tmp_path / "brain"
    (root / "_harness").mkdir(parents=True)
    (root / "_harness" / "inbox.md").write_text("- [ ] a harness proposal\n", encoding="utf-8")
    for name in ("scrolly", "site"):
        (tmp_path / name).mkdir()
        (root / name / "docs").mkdir(parents=True)
        (root / name / "docs" / "owner-queue.md").write_text(f"- [ ] {name} question\n", encoding="utf-8")
    entries = [f'[{name}]\nrepo = "{(tmp_path / name).as_posix()}"\n' for name in ("scrolly", "site")]
    (root / "projects.toml").write_text("".join(entries), encoding="utf-8")
    return Brain(root=root)


def start(brain: Brain, state: Path, project: str, when: datetime, source: str = "startup") -> str:
    cwd = brain.root.parent / project
    return startup.run({"source": source, "cwd": str(cwd)}, brain, state, when)


def test_first_session_shows_inbox_and_its_project_queue(brain: Brain, tmp_path: Path) -> None:
    message = start(brain, tmp_path / "s.json", "scrolly", datetime(2026, 11, 23, 10))
    assert "harness inbox" in message
    assert "scrolly's owner-queue" in message
    assert "site" not in message


def test_later_session_in_another_project_shows_only_its_queue(brain: Brain, tmp_path: Path) -> None:
    state = tmp_path / "s.json"
    start(brain, state, "scrolly", datetime(2026, 11, 23, 10))
    message = start(brain, state, "site", datetime(2026, 11, 23, 15))
    assert "site's owner-queue" in message
    assert "harness inbox" not in message


def test_second_session_in_the_same_project_is_silent(brain: Brain, tmp_path: Path) -> None:
    state = tmp_path / "s.json"
    start(brain, state, "scrolly", datetime(2026, 11, 23, 10))
    assert start(brain, state, "scrolly", datetime(2026, 11, 23, 11)) == ""


def test_next_day_shows_everything_again(brain: Brain, tmp_path: Path) -> None:
    state = tmp_path / "s.json"
    start(brain, state, "scrolly", datetime(2026, 11, 23, 10))
    assert "harness inbox" in start(brain, state, "scrolly", datetime(2026, 11, 24, 10))


def test_nothing_open_is_silent(brain: Brain, tmp_path: Path) -> None:
    brain.inbox.write_text("- [x] done\n", encoding="utf-8")
    (brain.root / "scrolly" / "docs" / "owner-queue.md").write_text("No open questions.\n", encoding="utf-8")
    assert start(brain, tmp_path / "s.json", "scrolly", datetime(2026, 11, 23, 10)) == ""


def test_compaction_does_not_trigger_or_stamp(brain: Brain, tmp_path: Path) -> None:
    state = tmp_path / "s.json"
    assert start(brain, state, "scrolly", datetime(2026, 11, 23, 10), source="compact") == ""
    assert load_state(state) == {}


def test_a_crash_becomes_an_open_inbox_item(brain: Brain) -> None:
    report_error(brain.root, "startup.py", ValueError("bad toml"), datetime(2026, 11, 23, 10))
    assert "- [ ] Hook error in startup.py" in brain.inbox.read_text(encoding="utf-8")
