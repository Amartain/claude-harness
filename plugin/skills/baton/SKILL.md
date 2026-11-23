---
name: baton
description: Overwrite the project's baton (docs/handoff.md) for the next session, then commit the brain. Use at the end of every session.
---

# Write the baton

Template: `../../templates/handoff.md` (relative to this skill's folder).

1. **Overwrite** `docs/handoff.md`. Never append. Keep it under 25 lines.
2. NOW: where the work stands, with the plan file. GREEN: which checks last passed, at which commit. DO: the one next
   action. WAIT: open owner items (count + the one that matters). DON'T: up to 3 live hazards.
3. History goes to git. Decisions go to the doc that governs them. Questions go to the owner-queue as `- [ ]` items.
4. Commit the brain: `git -C <brain> add -A && git -C <brain> commit -m "<project>: <what changed>"`. No ask needed:
   the brain is free rein.
