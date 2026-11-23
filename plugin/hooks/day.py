"""Pure rules for the owner's start-up: when a new day begins, and how many items are open."""

import re
from dataclasses import dataclass
from datetime import datetime, timedelta

OPEN_ITEM = re.compile(r"^\s*- \[ \] ", re.MULTILINE)


@dataclass(frozen=True)
class DaySettings:
    break_hours: float = 6
    boundary_hour: int = 4


def is_new_day(
    day_started_at: datetime | None,
    last_activity: datetime | None,
    now: datetime,
    settings: DaySettings,
) -> bool:
    """A new day needs both: a long break since the last activity, and the boundary hour passed since the
    current day began. Counting the boundary from the day's start (not the last activity) keeps a night owl
    who works until 05:00 and returns at 13:00 on a new day."""
    if day_started_at is None or last_activity is None:
        return True
    if now - last_activity < timedelta(hours=settings.break_hours):
        return False
    return boundary_passed(day_started_at, now, settings.boundary_hour)


def boundary_passed(start: datetime, end: datetime, hour: int) -> bool:
    """True when the clock reached `hour`:00 at some moment after `start` and no later than `end`."""
    first = start.replace(hour=hour, minute=0, second=0, microsecond=0)
    if first <= start:
        first += timedelta(days=1)
    return first <= end


def count_open(text: str) -> int:
    """Open items are Markdown checkbox lines: `- [ ] ...`."""
    return len(OPEN_ITEM.findall(text))
