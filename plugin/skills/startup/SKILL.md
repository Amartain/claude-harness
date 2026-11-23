---
name: startup
description: The owner's start-up. Walk the owner through open items in the harness inbox and in this project's owner-queue, one at a time. Run it when the start-up hook says items are open, or when the owner asks for their start-up.
---

# The owner's start-up

The hook (`hooks/startup.py`) has named the files with open items. Open items are `- [ ]` lines.

1. Say how many items there are in total, and where. Then take them one at a time, oldest first.
2. For each item: quote it, give a recommendation in one or two lines, and ask: yes, no, or reword.
3. Apply the answer:
   - **Harness inbox, yes:** make the edit in the harness (the permission prompt asks the owner once), then tick
     the item `- [x]` and add ` → applied <date>`.
   - **Harness inbox, no:** tick it and add ` → declined <date>`.
   - **Harness inbox, reword:** edit the item's wording, then ask again.
   - **Owner-queue answer:** move the answer into the doc that governs it (decisions file, features, design), then
     tick the item or delete it, per the queue's own header.
4. Commit the brain when done (`git -C <brain> commit`, no ask needed).
5. Close the count: "That was all N. Back to <the baton's DO line>."

The owner may stop at any point. Unanswered items stay open and come back at the next day's start-up.
