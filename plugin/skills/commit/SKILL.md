---
name: commit
description: Commit in a project repo safely - check the branch and every staged file so only the project reaches git. Use before any git commit in a project repo (not the brain).
---

# Commit a project

1. `git branch --show-current`. On `main`: switch to `dev`. Merging into `main` and tagging only when the owner asks.
2. `git status --short`. Stage files by name. Never `git add -A` or `git add .` blind.
3. Check each staged path. Only the project belongs in git:
   - Not docs, CLAUDE.md or `.claude/` (they live in the brain).
   - Not the owner's own tooling or personal data (those go in `.git/info/exclude`, never in `.gitignore`,
     `pyproject.toml` or lock files).
   - Not big generated media (a release asset instead).
4. Any non-code file staged: name it and ask the owner first.
5. Checks that fail: report them with a suggested fix. Commit only if the owner says so. Sonnet and Haiku do not fix
   code during a commit job.
6. Message: what changed and why, then the attribution lines the session asks for.
7. Never rewrite history without the owner's explicit yes.
