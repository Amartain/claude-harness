# Changelog

The plugin's version is in `plugin/.claude-plugin/plugin.json`. After a bump, run `/plugin update` in Claude Code.

## 0.3.3 · 2026-11-28

- `install.py --journal PATH` writes the `journal` key; a rerun keeps an existing one (it used to overwrite
  `harness.toml` and drop it). Tests added.
- `research-step`: check every link resolves before handing over a reading list; mark unchecked items (M).

## 0.3.2 · 2026-11-28

- Public harness holds generic direction only: owner-specific names (a model class, file names, note-naming scheme)
  removed from `ml-cv`, `research-step` and `dev-journal`; the details live in the brain's `_owner/` files.
- Rule: what the owner wants to learn goes to the owner's notes (`journal` in `~/.claude/harness.toml`), not the
  brain.

## 0.3.1 · 2026-11-27

- New skill `dev-journal`: writes learnings into the owner's dev journal (notes) in the owner's style, read
  from the brain's `_owner/journal-style.md`; offers a note at the end of a session that taught something; the
  journal folder is `journal` in `~/.claude/harness.toml`.

## 0.3.0 · 2026-11-27

From the ML/CV sweep (an earlier ML project's code and notes); every item walked with the owner.
- New skills (installed from the brain bundle with `apply.py`): `ml-cv` (gated by `Project type: ml-cv`),
  `python-conventions`, `library-check`, `research-step`.
- `licence-check` covers datasets, annotations and pretrained weights. `new-project` asks the project type, learning
  areas and, for ml-cv, the scope; the project template carries a `Project type:` line.
- `plan-step` and `build-card`: owner-builds cards for learning areas; GPU runs estimated with kind `experiment`,
  which `calibrate.py` keeps out of its `all` line.
- Rules: learning areas; a function table for explaining unfamiliar code; licences include datasets and weights;
  big harness changes arrive as a bundle.

## 0.2.0 · 2026-11-23

- New guard hook (`hooks/guard.py`): asks the owner before `git stash`, `git add -A` / `.`, force pushes, `sed -i`,
  `node -e` file writes, and anything touching `.ssh`, `.aws` or `.env`.
- `build-card` and `plan-step`: estimates carry a kind (app, ui, docs, tooling, harness) and are logged with
  `tools/log_estimate.py`, then calibrated with `tools/calibrate.py`.
- Rules: numbers a user would notice are proposals; unsure whether something is public-safe goes under "Ask me";
  bump the plugin version with each change to `plugin/`.

## 0.1.0 · 2026-11-23

- First release: global rules, 13 skills, templates, the start-up and activity hooks, the installer.
