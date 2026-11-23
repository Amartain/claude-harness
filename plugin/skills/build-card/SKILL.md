---
name: build-card
description: Build one card of an approved plan - fast checks, tick the box, log the estimate. Use for each card in docs/plans/step-NN.md while building.
---

# Build a card

1. Note the start time (`date +%H:%M`).
2. Read only what the card's Why/Read lines name. Reuse what its Reuse line names.
3. Build it: rule, API, UI and tests as one vertical slice. Edit files with the edit tool.
4. **Fast checks** while building: the linters, type checks and the tests the card touches.
5. Visual card: `/harness:visual-check` before it is done.
6. A test for a found bug: run it once against the old code; it must fail there.
7. Tick the card's boxes in the plan. Log the time:
   `py -3 <harness>/tools/log_estimate.py <project> <plan> <card> <model> <estimate_min> <actual_min>`
   (when the tool exists; otherwise note the minutes in the plan's "As built").
8. Next card. Between cards: fast checks plus the e2e specs the card touched. The full check suite runs before the
   commit that ends the session or the plan.
