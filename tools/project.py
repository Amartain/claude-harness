"""Find the project a tool runs in, from the brain's projects.toml, and read its per-tool settings.

A project's settings live under its table, one sub-table per tool:

    [scrolly.file_length]
    limit = 200
"""

import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "plugin" / "hooks"))

from store import CONFIG_PATH, load_brain, match_project

__all__ = ["CONFIG_PATH", "ProjectTools", "find_project", "load_brain", "strings"]


@dataclass(frozen=True)
class ProjectTools:
    name: str
    repo: Path
    docs: Path
    settings: dict[str, Any] = field(default_factory=dict)

    def tool(self, name: str) -> dict[str, Any]:
        return dict(self.settings.get(name, {}))


def find_project(cwd: Path, config_path: Path = CONFIG_PATH) -> ProjectTools:
    brain = load_brain(config_path)
    project = match_project(cwd, brain.projects())
    if project is None:
        raise SystemExit(f"{cwd} is not a project in {brain.root / 'projects.toml'}.")
    data = tomllib.loads((brain.root / "projects.toml").read_text(encoding="utf-8"))
    return ProjectTools(
        name=project.name,
        repo=project.repo,
        docs=brain.root / project.name / "docs",
        settings=dict(data[project.name]),
    )


def strings(settings: dict[str, Any], key: str, default: tuple[str, ...]) -> tuple[str, ...]:
    value = settings.get(key)
    return tuple(str(item) for item in value) if isinstance(value, list) else default
