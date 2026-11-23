---
name: new-rule
description: The check before adding any absolute rule ("always", "never", "must", "must not") to any doc. Use whenever a rule like that is about to be written.
---

# Before an absolute rule

Absolute rules pile up, go stale, and quietly constrain later work. So:

1. Show the owner the **exact wording** and **where it goes**.
2. List its drawbacks:
   - what it blocks later;
   - cases where it would be wrong;
   - what it conflicts with (name the existing rules);
   - a softer alternative: a default with its reasoning.
3. Can it be enforced by structure (a permission rule, a hook, a check script) instead of a prompt? Say so.
4. Add it only after the owner explicitly confirms. Without that, write the default and its reasoning instead.

Never turn your own inference into an absolute rule.
