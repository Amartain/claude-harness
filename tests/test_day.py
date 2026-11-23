from datetime import datetime

from day import DaySettings, count_open, is_new_day

S = DaySettings(break_hours=6, boundary_hour=4)


def at(day: int, hour: int, minute: int = 0) -> datetime:
    return datetime(2026, 11, day, hour, minute)


def test_first_session_ever_is_a_new_day() -> None:
    assert is_new_day(None, None, at(23, 10), S)


def test_five_hour_break_is_the_same_day() -> None:
    assert not is_new_day(at(23, 9), at(23, 10), at(23, 15), S)


def test_seven_hour_break_before_the_boundary_is_the_same_day() -> None:
    # Worked 17:00-18:00, back at 01:00: 04:00 has not passed yet.
    assert not is_new_day(at(23, 17), at(23, 18), at(24, 1), S)


def test_seven_hour_break_across_the_boundary_is_a_new_day() -> None:
    assert is_new_day(at(23, 18), at(23, 23), at(24, 6), S)


def test_night_owl_at_half_past_one_is_still_today() -> None:
    # Working since 20:00, last reply at 01:20.
    assert not is_new_day(at(23, 20), at(24, 1, 20), at(24, 1, 30), S)


def test_worked_until_five_back_at_one_pm_is_a_new_day() -> None:
    # The boundary counts from the day's start (20:00), not from the last activity (05:00).
    assert is_new_day(at(23, 20), at(24, 5), at(24, 13), S)


def test_long_afternoon_break_is_the_same_day() -> None:
    # 08:00-09:00, back at 16:00: a 7 h break, but no 04:00 since the day began.
    assert not is_new_day(at(23, 8), at(23, 9), at(23, 16), S)


def test_count_open_counts_only_unchecked_boxes() -> None:
    text = "# Queue\n- [ ] one\n- [x] done\n  - [ ] nested\nprose - [ ] not at line start\n"
    assert count_open(text) == 2
