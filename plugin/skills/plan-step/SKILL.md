---
name: plan-step
description: Write a build plan for the next step - an owner brief, then closed cards with calibrated time estimates. Use in plan mode (Opus) before building anything larger than a small fix.
---

# Plan a step

Template: `../../templates/plan.md` (relative to this skill's folder).

1. Read CLAUDE.md, the baton, and only the doc sections the step touches. Read the decisions file before asking
   anything: settled is settled.
2. Ask the owner only big-picture questions (what gets built, how it behaves or looks, what it locks in). Decide
   small details yourself.
3. Write the brief (up to 15 lines): Why, You'll see, You decided, Assumed, Out of scope, Estimate.
4. Write closed cards. Anything undecided goes to the project's owner-queue as a `- [ ]` item, not into a card.
5. **Estimate.** Read the brain's `estimates.csv` and run `py -3 <harness>/tools/calibrate.py` when it exists.
   Show the calibrated number per card and in total. Total over 2 h calibrated: suggest a split; the owner decides.
6. Name every decision the owner might want to change, so they can comment on it in plan mode.
7. The first build action saves the plan to `docs/plans/step-NN.md` (the brain, through the junction).
