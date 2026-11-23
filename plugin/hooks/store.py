"""File access for the hooks: the harness config, the brain's settings and project list, and the state file."""

import json
import tomllib
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from day import DaySettings

HOME_CLAUDE = Path.home() / ".claude"
CONFIG_PATH = HOME_CLAUDE / "harness.toml"
STATE_PATH = HOME_CLAUDE / "harness-state.json"


@dataclass(frozen=True)
class Project:
    name: str
    repo: Path
    queue: Path


@dataclass(frozen=True)
class Brain:
    root: Path

    @property
    def inbox(self) -> Path:
        return self.root / "_harness" / "inbox.md"

    def settings(self) -> DaySettings:
        path = self.root / "_owner" / "startup.toml"
        if not path.exists():
            return DaySettings()
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        return DaySettings(
            break_hours=float(data.get("break_hours", 6)),
            boundary_hour=int(data.get("boundary_hour", 4)),
        )

    def projects(self) -> list[Project]:
        path = self.root / "projects.toml"
        if not path.exists():
            return []
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        return [
            Project(
                name=name,
                repo=Path(entry["repo"]),
                queue=self.root / name / entry.get("queue", "docs/owner-queue.md"),
            )
            for name, entry in data.items()
        ]


def load_brain(config_path: Path = CONFIG_PATH) -> Brain:
    data = tomllib.loads(config_path.read_text(encoding="utf-8"))
    return Brain(root=Path(data["brain"]))


def match_project(cwd: Path, projects: list[Project]) -> Project | None:
    """The project whose repo folder contains `cwd` (case-insensitive, for Windows)."""
    here = str(cwd.resolve()).lower()
    for project in projects:
        repo = str(project.repo.resolve()).lower()
        if here == repo or here.startswith((repo + "\\", repo + "/")):
            return project
    return None


def load_state(path: Path = STATE_PATH) -> dict[str, object]:
    if not path.exists():
        return {}
    return dict(json.loads(path.read_text(encoding="utf-8")))


def save_state(state: dict[str, object], path: Path = STATE_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2), encoding="utf-8")


def read_time(state: dict[str, object], key: str) -> datetime | None:
    value = state.get(key)
    return datetime.fromisoformat(value) if isinstance(value, str) else None


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def report_error(brain_root: Path | None, hook: str, error: BaseException, now: datetime) -> None:
    """A hook never blocks a session: its error becomes an open inbox item for the owner's start-up."""
    if brain_root is None:
        return
    inbox = brain_root / "_harness" / "inbox.md"
    inbox.parent.mkdir(parents=True, exist_ok=True)
    line = f"- [ ] Hook error in {hook} ({now:%Y-%m-%d %H:%M}): {type(error).__name__}: {error}\n"
    with inbox.open("a", encoding="utf-8") as handle:
        handle.write(line)
