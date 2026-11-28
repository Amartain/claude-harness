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


def test_harness_toml_keeps_existing_journal_on_rerun() -> None:
    existing = 'harness = "C:/h"\nbrain = "C:/b"\njournal = "C:/Users/x/notes"\n'
    assert 'journal = "C:/Users/x/notes"' in install.harness_toml(Path("C:/b"), None, existing)


def test_harness_toml_new_journal_wins_and_none_without() -> None:
    existing = 'journal = "C:/old"\n'
    assert 'journal = "C:/new"' in install.harness_toml(Path("C:/b"), Path("C:/new"), existing)
    assert "journal" not in install.harness_toml(Path("C:/b"), None, "")
