---
name: new-project
description: Set up a project's brain folder from the templates, link it into the repo as docs/, and add a stub CLAUDE.md. Use when starting a new project or moving an existing one onto the harness.
---

# Put a project on the harness

Templates: `../../templates/` (relative to this skill's folder).

1. Ask the project type (general or ml-cv) and any learning areas. Add the project to `<brain>/projects.toml`:
   ```toml
   [<name>]
   repo = "C:/path/to/repo"
   type = "ml-cv"   # omit for general
   ```
   ml-cv: also ask the scope (off-the-shelf model only / a fine-tuning proposal / fine-tuning / from scratch) and
   record it in the project's decisions file; `/harness:ml-cv` lists the other setup questions.
2. Create `<brain>/<name>/docs/` with: `CLAUDE.md` (from `project-CLAUDE.md`), `handoff.md`, `owner-queue.md`,
   `decisions.md`, and `plans/`.
3. Existing project: move its `docs/` contents and `CLAUDE.md` into `<brain>/<name>/docs/` first. Trim the moved
   CLAUDE.md to project content only: the harness carries the workflow.
4. Run `py -3 <harness>/tools/install.py`. It makes the `docs` junction.
5. Write the repo's `CLAUDE.md` as one line: `@docs/CLAUDE.md`. Keep `docs`, `CLAUDE.md` and `.claude` out of the
   project's git (`.gitignore` or `.git/info/exclude`).
6. Commit the brain.
