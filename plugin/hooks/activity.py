"""Stop hook: stamps the owner's last activity, which the start-up uses to tell when a new day begins."""

import sys
from datetime import datetime
from pathlib import Path

from store import STATE_PATH, load_brain, load_state, report_error, save_state


def run(state_path: Path, now: datetime) -> None:
    state = load_state(state_path)
    state["last_activity"] = now.isoformat()
    save_state(state, state_path)


def main() -> None:
    now = datetime.now()
    try:
        run(STATE_PATH, now)
    except Exception as error:  # a hook must never block a session
        try:
            report_error(load_brain().root, "activity.py", error, now)
        except Exception as nested:  # no brain to report to: stderr is all that is left
            print(f"harness activity hook: {error}; reporting failed: {nested}", file=sys.stderr)


if __name__ == "__main__":
    main()
