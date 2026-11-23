"""SessionStart hook: the owner's start-up.

Harness inbox: shown in the owner's first session of the day, in any project.
A project's owner-queue: shown in the first session of the day in that project.
Prints a note for Claude (stdout becomes session context) only when something is open and not yet shown today.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

from day import count_open, is_new_day
from store import (
    STATE_PATH,
    Brain,
    load_brain,
    load_state,
    match_project,
    read_text,
    read_time,
    report_error,
    save_state,
)

SKIP_SOURCES = {"compact"}


def run(payload: dict[str, object], brain: Brain, state_path: Path, now: datetime) -> str:
    if payload.get("source") in SKIP_SOURCES:
        return ""
    state = load_state(state_path)
    day_started = read_time(state, "day_started_at")
    if is_new_day(day_started, read_time(state, "last_activity"), now, brain.settings()):
        day_started = now
        state["day_started_at"] = now.isoformat()
    shown = dict(state.get("shown", {}))  # type: ignore[call-overload]

    def due(key: str) -> bool:
        stamp = shown.get(key)
        return day_started is not None and (stamp is None or datetime.fromisoformat(stamp) < day_started)

    lines = []
    inbox_open = count_open(read_text(brain.inbox))
    if inbox_open and due("_harness"):
        lines.append(f"- {inbox_open} open in the harness inbox: {brain.inbox.as_posix()}")
        shown["_harness"] = now.isoformat()
    project = match_project(Path(str(payload.get("cwd", "."))), brain.projects())
    if project is not None:
        queue_open = count_open(read_text(project.queue))
        if queue_open and due(project.name):
            lines.append(f"- {queue_open} open in {project.name}'s owner-queue: {project.queue.as_posix()}")
            shown[project.name] = now.isoformat()

    state["shown"] = shown
    state["last_activity"] = now.isoformat()
    save_state(state, state_path)
    if not lines:
        return ""
    return "\n".join(
        [
            "Owner start-up: the owner has open items not yet shown today.",
            *lines,
            "Before anything else, run the harness:startup skill and walk the owner through them, one at a time.",
        ]
    )


def main() -> None:
    now = datetime.now()
    brain = None
    try:
        payload = json.loads(sys.stdin.read() or "{}")
        brain = load_brain()
        message = run(payload, brain, STATE_PATH, now)
        if message:
            print(message)
    except Exception as error:  # a hook must never block a session
        report_error(brain.root if brain else None, "startup.py", error, now)


if __name__ == "__main__":
    main()
