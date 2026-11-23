---
name: retro
description: Close a finished plan - fill its "As built" with real times, log the estimates, and route what was learned. Use when the last card of a plan is done.
---

# Close a plan

1. Fill the plan's **As built**: real minutes per card and in total, against the estimate. Say what surprised.
2. Every card has a row in `<brain>/estimates.csv` (`tools/log_estimate.py`); add the missing ones.
3. Ask: what went wrong, what was slow, what did the owner correct? Run `/harness:learn` on each answer.
4. Close the count: "N lessons: X to the project, Y harness proposals in the inbox."
5. `/harness:baton`.
