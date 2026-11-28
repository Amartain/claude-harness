# claude-harness

A Claude Code harness: how one person works with Claude across every project, kept in one place.

- **Rules** (`CLAUDE.md`): working agreements and a plain-writing style, imported into the global `~/.claude/CLAUDE.md`.
- **Skills** (`/harness:<name>`), 18 in all:
  - Workflow: `plan-step`, `build-card`, `baton`, `commit`, `retro`, `startup`, `learn`, `new-project`,
    `new-rule`, `doc-edits`.
  - Quality: `visual-check`, `licence-check` (assets, code, datasets, model weights), `library-check` (a library
    call's contract against the installed version's source and docs), `python-conventions`,
    `python-design-patterns`.
  - ML/CV: `ml-cv`, defaults for data, models (custom or pretrained), training and evaluation. Used by projects
    whose CLAUDE.md says `Project type: ml-cv`.
  - Research and notes: `research-step` (literature research), `dev-journal` (learnings into the owner's own notes).
- **Hooks**: the owner's start-up (open items once a day), an activity stamp, and a guard that asks before risky
  commands (`git stash`, `git add -A`, force pushes, `sed -i`) and before touching credentials.
- **Tools**: code map, file-length check, estimate log and calibration. Standard library only.

It pairs with a private **brain** repo: one folder per project (its docs, decisions, plans and baton), the harness
inbox, and the logs. The harness is read-only for Claude (an `ask` permission guards it); the brain is free to edit.

## Install in three steps

Needs Python 3.12+ (`py -3` on Windows) and Claude Code.

1. Clone this repo, and make a brain folder (or clone yours) with `_harness/inbox.md` and `projects.toml`:

   ```toml
   [myproject]
   repo = "C:/path/to/myproject"
   type = "ml-cv"   # optional: only for ML/CV projects
   ```

2. Run the installer. It is safe to run again, and `--dry-run` shows what it would change.

   ```
   py -3 tools/install.py --brain C:/path/to/brain
   ```

   It writes `~/.claude/harness.toml`, imports the rules into `~/.claude/CLAUDE.md`, adds the permissions to
   `~/.claude/settings.json` (a `.bak` copy is kept), and links each project's `docs/` to its brain folder.

3. Paste the two `/plugin` commands it prints into Claude Code, then open a new session.

New project: `/harness:new-project`. Tests: `py -3 -m pytest`.

Optional: for `dev-journal`, run the installer with `--journal C:/path/to/notes` (a rerun keeps it), and keep a
style guide in the brain at `_owner/journal-style.md`.

Bigger harness changes (more than ~3 new files) arrive as a bundle in `<brain>/_harness/staged/<version>/`: read
it, then run its `apply.py` (`--dry-run` first). It copies new files only and never overwrites.

`plugin/skills/python-design-patterns` is third-party, under the MIT licence in its `SOURCE.md`.

No licence: this is a personal harness, shared as an example. Ask me if you want to reuse part of it.
