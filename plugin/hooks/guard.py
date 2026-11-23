"""PreToolUse hook: ask the owner before commands that went wrong before, and before touching credentials.

The rules in CLAUDE.md are in the prompt, and the prompt does not stop anything. Claude Code does: an "ask" answer
here makes it prompt the owner, whatever the model thinks. Nothing is blocked outright; the owner can say yes.
"""

import contextlib
import json
import re
import sys
from datetime import datetime

from store import load_brain, report_error

SEGMENT = r"[^|;&\n]*"  # stays inside one command of a pipeline or chain
COMMAND_RULES = (
    (re.compile(rf"\bgit\b{SEGMENT}\bstash\b"), "git stash round-trips flipped line endings before"),
    (
        re.compile(rf"\bgit\b{SEGMENT}\badd\s+(?:-A\b|--all\b|\.(?=\s|$|[;&|]))"),
        "git add -A / . can stage private files: check the staged list first",
    ),
    (re.compile(rf"\bgit\b{SEGMENT}\bpush\b{SEGMENT}\s(?:--force\S*|-f)\b"), "a force push rewrites shared history"),
    (re.compile(rf"\bsed\b{SEGMENT}\s(?:-[a-zA-Z]*i|--in-place)"), "sed -i edits failed silently before: use Edit"),
    (re.compile(r"\bnode\s+(?:-e|--eval)\b.*writeFile", re.DOTALL), "node -e rewrites failed silently before"),
)
SECRET = re.compile(r"(?:^|[\s'\"/\\~=])(\.ssh|\.aws|\.env(?:\.[\w-]+)?)(?=$|[\s'\"/\\;&|)])")
FILE_KEYS = ("file_path", "path", "pattern", "notebook_path")


def secret_reason(text: str) -> str | None:
    found = SECRET.search(text)
    return f"it touches {found.group(1)}, which holds credentials" if found else None


def verdict(tool_name: str, tool_input: dict[str, object]) -> str | None:
    """The reason to ask the owner first, or None to let the call through."""
    command = tool_input.get("command")
    if tool_name in {"Bash", "PowerShell"} and isinstance(command, str):
        for pattern, reason in COMMAND_RULES:
            if pattern.search(command):
                return reason
        return secret_reason(command)
    for key in FILE_KEYS:
        value = tool_input.get(key)
        found = secret_reason(value) if isinstance(value, str) else None
        if found:
            return found
    return None


def answer(reason: str) -> str:
    output = {"hookEventName": "PreToolUse", "permissionDecision": "ask"}
    output["permissionDecisionReason"] = f"Guard: {reason}."
    return json.dumps({"hookSpecificOutput": output})


def main() -> None:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
        tool_input = payload.get("tool_input")
        reason = verdict(str(payload.get("tool_name", "")), tool_input if isinstance(tool_input, dict) else {})
        if reason:
            print(answer(reason))
    except Exception as error:  # a hook must never block a session
        with contextlib.suppress(Exception):
            report_error(load_brain().root, "guard.py", error, datetime.now())


if __name__ == "__main__":
    main()
