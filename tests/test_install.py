from pathlib import Path

import install


def test_permission_path_uses_posix_double_slash() -> None:
    assert install.permission_path(Path("C:/Users/x/claude-harness")) == "//c/Users/x/claude-harness"


def test_merge_permissions_adds_once_and_keeps_existing() -> None:
    settings = {"model": "opus", "permissions": {"allow": ["Bash(ls)"]}}
    brain = Path("C:/Users/x/brain")
    once = install.merge_permissions(settings, brain)
    twice = install.merge_permissions(once, brain)
    assert twice["model"] == "opus"
    assert twice["permissions"]["allow"] == ["Bash(ls)", "Edit(//c/Users/x/brain/**)"]
    assert len(twice["permissions"]["ask"]) == 1
    assert twice["permissions"]["ask"][0].endswith("/claude-harness/**)")
