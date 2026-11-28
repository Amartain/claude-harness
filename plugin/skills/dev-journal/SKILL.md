---
name: dev-journal
description: Write a learning into the owner's dev journal (notes) in the owner's own style - file name, note type, frontmatter and voice from the style file. Use when the owner asks for a note, or offer it once at the end of a session that taught the owner something reusable (a tool, a fix, a concept).
---

# Dev journal

The journal is the owner's own reference, in the owner's voice. It is not Claude's memory: lessons about how to
work still go through `/harness:learn`.

1. **Offer, don't assume.** At the end of a session that taught something reusable, offer once in one line:
   "Journal note on <topic>?". Write only on a yes, or when the owner asks.
2. **Read the style first:** `<brain>/_owner/journal-style.md` (name format, prefixes, types, voice, per-type
   layout). The journal folder is `journal` in `~/.claude/harness.toml`.
3. **Pick the name** per the style file (index, prefix, type). A new prefix is a proposal: ask.
4. **Write it in the type's layout and voice** from the style file, with the owner's own context (past notes, past
   pain). Mark anything not verified this session.
5. **Don't commit** the journal unless the owner asks. Say the file name in one line.
6. **When the owner corrects a note** (renames it, rewrites the style), update `journal-style.md` and its
   corrections log in the brain, and commit the brain.
