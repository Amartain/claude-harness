"""Fail when a hand-written code file is longer than the project's limit (200 lines by default).

    py -3 <harness>/tools/check_file_length.py        run from inside the project

Settings, all optional, in the brain's projects.toml under [<project>.file_length]:
limit, extensions, skip (folder names), generated (file names).
"""

import sys
from pathlib import Path
from typing import Any

from project import find_project, strings

LIMIT = 200
EXTENSIONS = (".py", ".ts", ".tsx", ".js", ".svelte", ".css")
SKIP = (
    ".venv", "venv", "node_modules", ".git", "docs", "static", "dist", "build", "__pycache__",
    ".mypy_cache", ".ruff_cache", ".pytest_cache", ".claude", "test-results", "playwright-report",
)  # fmt: skip


def code_files(repo: Path, settings: dict[str, Any]) -> list[Path]:
    extensions = set(strings(settings, "extensions", EXTENSIONS))
    skip = set(strings(settings, "skip", SKIP))
    generated = set(strings(settings, "generated", ()))
    return sorted(
        path
        for path in repo.rglob("*")
        if path.suffix in extensions
        and path.name not in generated
        and not skip.intersection(path.relative_to(repo).parts[:-1])
        and path.is_file()
    )


def too_long(repo: Path, settings: dict[str, Any]) -> list[str]:
    limit = int(settings.get("limit", LIMIT))
    found = []
    for path in code_files(repo, settings):
        count = len(path.read_text(encoding="utf-8", errors="replace").splitlines())
        if count > limit:
            found.append(f"{path.relative_to(repo).as_posix()}: {count} lines (max {limit})")
    return found


def main() -> int:
    project = find_project(Path.cwd())
    settings = project.tool("file_length")
    found = too_long(project.repo, settings)
    print("\n".join(found) or f"All code files are within {settings.get('limit', LIMIT)} lines.")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
