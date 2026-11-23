---
name: learn
description: Route one lesson (a mistake, a surprise, an owner correction) to where it belongs - the project's brain folder, a skill, or the global rules - and log it. Use whenever something is learned that a later session should know.
---

# Route a lesson

Ask: who needs this next time?

| The lesson is about | Do |
|---|---|
| This project only | Edit the right doc in `docs/` (the brain) directly. No ask needed. |
| One workflow | Harness proposal for that skill (below). |
| Every project | Harness proposal for the harness `CLAUDE.md` (below). Keep it lean: is it really global? |

**Harness proposal** (the harness is read-only for Claude):
1. Say it in chat in one line: `Harness proposal: <exact wording> → <file>`.
2. Append it to `<brain>/_harness/inbox.md`: `- [ ] <date> · <project> · <file>: "<exact wording>". Why: <reason>.`
3. Keep working. The owner's next start-up shows it.

**Then log it:** one line in `<brain>/learnings.md`:
`<date> · <project> · <what happened> · <lesson> · went to: <file or inbox>`.

New Claude memories (in `~/.claude/projects/.../memory/`) count as lessons too: route them the same way, then delete
the memory file.
