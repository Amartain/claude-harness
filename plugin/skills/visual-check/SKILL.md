---
name: visual-check
description: Take screenshots of every screen state a card touches (each theme, width and mode the project names) and look at them before calling the card done. Use for any card that changes what the screen shows.
---

# Look at visual work

Green tests on data do not show a broken screen.

1. List the states the card touches. The project's CLAUDE.md or design doc names its axes (themes, times of day,
   widths such as 390 px and 1440 px, reduced motion on and off).
2. Take a screenshot of each (Playwright, or the project's screenshot script).
3. Look at every one. Check: overflow and clipping, contrast, alignment, scrollbars, focus rings, empty states.
4. Fix what is wrong and shoot again. Name the screenshots you looked at in the report.
