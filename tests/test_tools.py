from pathlib import Path

import check_file_length
import code_map
import pytest
from project import find_project


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_a_201_line_file_fails_and_200_passes(tmp_path: Path) -> None:
    write(tmp_path / "src" / "long.py", "x = 1\n" * 201)
    write(tmp_path / "src" / "fine.py", "x = 1\n" * 200)
    assert check_file_length.too_long(tmp_path, {}) == ["src/long.py: 201 lines (max 200)"]


def test_generated_files_and_skipped_folders_are_ignored(tmp_path: Path) -> None:
    write(tmp_path / "src" / "api-types.ts", "x\n" * 500)
    write(tmp_path / "node_modules" / "lib.js", "x\n" * 500)
    assert check_file_length.too_long(tmp_path, {"generated": ["api-types.ts"]}) == []


def test_the_limit_comes_from_settings(tmp_path: Path) -> None:
    write(tmp_path / "a.ts", "x\n" * 51)
    assert check_file_length.too_long(tmp_path, {"limit": 50}) == ["a.ts: 51 lines (max 50)"]


def test_the_map_lists_each_module_by_its_first_comment_line(tmp_path: Path) -> None:
    write(tmp_path / "app" / "clock.py", '"""Tells the time.\n\nMore detail."""\n')
    write(tmp_path / "app" / "bare.py", "def tick():\n    pass\n\ndef _hidden():\n    pass\n")
    write(tmp_path / "web" / "store.ts", "/** Keeps the state. */\nexport const a = 1\n")
    write(tmp_path / "web" / "Card.svelte", "<script>import Row from './Row.svelte'</script>\n")
    text = code_map.build_map(tmp_path, {"roots": ["app", "web"]})
    assert "- `clock.py` — Tells the time." in text
    assert "- `bare.py` — tick" in text
    assert "- `store.ts` — Keeps the state." in text
    assert "- `Card.svelte` — uses Row" in text
    assert text.index("## app/") < text.index("## web/")


def test_the_map_survives_a_syntax_error(tmp_path: Path) -> None:
    write(tmp_path / "broken.py", "def (:\n")
    assert "- `broken.py`\n" in code_map.build_map(tmp_path, {})


def test_find_project_reads_its_tool_settings(tmp_path: Path) -> None:
    brain, repo = tmp_path / "brain", tmp_path / "proj"
    (repo / "sub").mkdir(parents=True)
    write(brain / "projects.toml", f'[proj]\nrepo = "{repo.as_posix()}"\n\n[proj.file_length]\nlimit = 120\n')
    config = tmp_path / "harness.toml"
    write(config, f'brain = "{brain.as_posix()}"\n')
    project = find_project(repo / "sub", config)
    assert project.name == "proj"
    assert project.docs == brain / "proj" / "docs"
    assert project.tool("file_length") == {"limit": 120}
    with pytest.raises(SystemExit):
        find_project(tmp_path, config)
