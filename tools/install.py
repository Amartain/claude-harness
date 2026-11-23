"""Install the harness on this machine. Safe to run again: every step checks before it changes anything.

    py -3 tools/install.py [--brain PATH] [--dry-run]

1. ~/.claude/harness.toml       where the harness and the brain are (the hooks read it)
2. ~/.claude/CLAUDE.md          imports the harness rules and the brain's machine notes
3. ~/.claude/settings.json      ask before editing the harness; the brain is free to edit
4. <project>/docs junctions     one per project in the brain's projects.toml
Then it prints the two /plugin commands to paste into Claude Code.
"""

import argparse
import json
import os
import shutil
import subprocess
import tomllib
from pathlib import Path
from typing import Any

HARNESS = Path(__file__).resolve().parent.parent
CLAUDE_HOME = Path.home() / ".claude"
MARKER = "<!-- managed by claude-harness tools/install.py -->"


def permission_path(path: Path) -> str:
    """Claude Code permission rules want POSIX form with `//` for absolute: C:\\x\\y -> //c/x/y."""
    posix = path.resolve().as_posix()
    if len(posix) > 1 and posix[1] == ":":
        posix = "/" + posix[0].lower() + posix[2:]
    return "/" + posix


def import_path(path: Path) -> str:
    """CLAUDE.md import, home-relative when possible (`@~/...`)."""
    try:
        return "@~/" + path.resolve().relative_to(Path.home()).as_posix()
    except ValueError:
        return "@" + path.resolve().as_posix()


def global_claude_md(brain: Path) -> str:
    return "\n".join(
        [
            MARKER,
            import_path(HARNESS / "CLAUDE.md"),
            import_path(brain / "_owner" / "machine.md"),
            "",
        ]
    )


def merge_permissions(settings: dict[str, Any], brain: Path) -> dict[str, Any]:
    perms = settings.setdefault("permissions", {})
    wanted = {
        "ask": [f"Edit({permission_path(HARNESS)}/**)"],
        "allow": [f"Edit({permission_path(brain)}/**)"],
        "additionalDirectories": [brain.resolve().as_posix()],
    }
    for key, values in wanted.items():
        current = perms.setdefault(key, [])
        current.extend(v for v in values if v not in current)
    return settings


def write(path: Path, text: str, dry: bool) -> None:
    print(f"  write {path}")
    if not dry:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def install_claude_md(brain: Path, dry: bool) -> None:
    target = CLAUDE_HOME / "CLAUDE.md"
    if target.exists() and MARKER not in target.read_text(encoding="utf-8"):
        print(f"  SKIP {target}: it exists and was not written by this script. Add these two lines yourself:")
        print("  " + global_claude_md(brain).replace("\n", "\n  "))
        return
    write(target, global_claude_md(brain), dry)


def install_settings(brain: Path, dry: bool) -> None:
    path = CLAUDE_HOME / "settings.json"
    settings = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    merged = merge_permissions(json.loads(json.dumps(settings)), brain)
    if merged == settings:
        print(f"  ok    {path} already has the permissions")
        return
    if not dry and path.exists():
        shutil.copy2(path, path.with_suffix(".json.bak"))
    write(path, json.dumps(merged, indent=2) + "\n", dry)


def install_junctions(brain: Path, dry: bool) -> None:
    projects_file = brain / "projects.toml"
    if not projects_file.exists():
        print(f"  none  {projects_file} not found, no junctions to make")
        return
    for name, entry in tomllib.loads(projects_file.read_text(encoding="utf-8")).items():
        link, target = Path(entry["repo"]) / "docs", brain / name / "docs"
        if link.is_junction() or link.is_symlink():
            print(f"  ok    {link} -> {os.readlink(link)}")
        elif link.exists():
            print(f"  SKIP  {link} is a real folder. Move its contents to {target} first.")
        elif not target.exists():
            print(f"  SKIP  {target} does not exist yet.")
        else:
            print(f"  link  {link} -> {target}")
            if not dry:
                subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)], check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--brain", type=Path, default=HARNESS.parent / "brain")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    brain: Path = args.brain.resolve()
    dry: bool = args.dry_run

    print("1. harness.toml")
    toml = f'harness = "{HARNESS.as_posix()}"\nbrain = "{brain.as_posix()}"\n'
    write(CLAUDE_HOME / "harness.toml", toml, dry)
    print("2. global CLAUDE.md")
    install_claude_md(brain, dry)
    print("3. permissions")
    install_settings(brain, dry)
    print("4. junctions")
    install_junctions(brain, dry)
    print("5. paste these into Claude Code:")
    print(f"  /plugin marketplace add {HARNESS.as_posix()}")
    print("  /plugin install harness@claude-harness")


if __name__ == "__main__":
    main()
