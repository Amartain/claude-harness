---
name: library-check
description: Check a library call's contract (expected inputs, defaults, argument order, edge cases, deprecations) against the installed version's source, docs and changelog, and record it next to the call. Use when wiring model outputs to losses or metrics, loading pretrained weights, on a deprecation warning or a new major version, for an API not verified this session, or when memory and docs disagree.
---

# Library check

Libraries change after Claude's training cutoff. The installed version is the truth; memory is a guess.

## When

- Wiring a model's output into a loss, a metric or a pretrained head.
- Loading pretrained weights and their preprocessing.
- A deprecation warning, or a new major version of a dependency.
- An API not verified in this session that the code relies on.
- Memory and the docs disagree, or the docs are thin.

## How

1. **Find the installed version.** The lock file, or `py -3 -m uv pip show <package>`.
2. **Read the installed source first.** It is exactly the version in use, and needs no network:
   `py -3 -c "import inspect, monai.losses as m; print(inspect.getsourcefile(m.DiceCELoss))"`, then read it.
3. **Then that version's docs.** If the docs site fails, the source at the matching release tag on GitHub
   (`raw.githubusercontent.com/<org>/<repo>/<tag>/...`) is the fallback.
4. **Check what changed** in newer releases: the changelog, deprecation notes. Say so if the project's version is
   behind and the behaviour differs.
5. **Write the contract down** where the next reader needs it: a comment at the call, or the project's docs.
   Include the source and version:
   `# DiceCELoss expects logits: one channel uses BCEWithLogitsLoss (monai 1.5.0, losses/dice.py)`.

Report what was checked and from where. If nothing could be read, say so rather than filling the gap from memory.
