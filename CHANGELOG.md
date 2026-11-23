# Changelog

The plugin's version is in `plugin/.claude-plugin/plugin.json`. After a bump, run `/plugin update` in Claude Code.

## 0.2.0 · 2026-11-23

- New guard hook (`hooks/guard.py`): asks the owner before `git stash`, `git add -A` / `.`, force pushes, `sed -i`,
  `node -e` file writes, and anything touching `.ssh`, `.aws` or `.env`.
- `build-card` and `plan-step`: estimates carry a kind (app, ui, docs, tooling, harness) and are logged with
  `tools/log_estimate.py`, then calibrated with `tools/calibrate.py`.
- Rules: numbers a user would notice are proposals; unsure whether something is public-safe goes under "Ask me";
  bump the plugin version with each change to `plugin/`.

## 0.1.0 · 2026-11-23

- First release: global rules, 13 skills, templates, the start-up and activity hooks, the installer.
