import json

import pytest
from guard import answer, verdict

ASKED = [
    "git stash",
    "git -C ../brain stash pop",
    "git add -A",
    "git add .",
    "git add --all && git commit -m x",
    "git push --force origin dev",
    "git push -f",
    "git push --force-with-lease",
    "sed -i 's/a/b/' file.py",
    "sed -E -i.bak 's/a/b/' f",
    "node -e \"require('fs').writeFileSync('a.ts', s)\"",
    "cat ~/.ssh/id_ed25519",
    "Get-Content C:\\Users\\x\\.aws\\credentials",
    "cat .env",
    "type backend\\.env.local",
]
PASSED = [
    "git status --short",
    "git add src/app.py tests/test_app.py",
    "git push origin dev",
    "git log --oneline | grep stash-fix",
    "sed -n '1,40p' file.py",
    'node -e "console.log(process.version)"',
    ".venv/Scripts/python -m pytest",
    "ls .venv",
    "npm run build",
]


@pytest.mark.parametrize("command", ASKED)
def test_guarded_commands_ask(command: str) -> None:
    assert verdict("Bash", {"command": command}) is not None
    assert verdict("PowerShell", {"command": command}) is not None


@pytest.mark.parametrize("command", PASSED)
def test_normal_commands_pass(command: str) -> None:
    assert verdict("Bash", {"command": command}) is None


def test_file_tools_ask_on_credential_paths_only() -> None:
    assert verdict("Read", {"file_path": "C:\\Users\\x\\.ssh\\config"}) is not None
    assert verdict("Edit", {"file_path": "/repo/.env"}) is not None
    assert verdict("Grep", {"pattern": "key", "path": "/home/x/.aws"}) is not None
    assert verdict("Read", {"file_path": "/repo/src/env.py"}) is None
    assert verdict("Read", {"file_path": "/repo/.venv/lib/site.py"}) is None


def test_the_answer_is_a_pre_tool_use_ask() -> None:
    output = json.loads(answer("why"))["hookSpecificOutput"]
    assert output["hookEventName"] == "PreToolUse"
    assert output["permissionDecision"] == "ask"
    assert output["permissionDecisionReason"] == "Guard: why."
