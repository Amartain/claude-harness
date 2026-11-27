---
name: licence-check
description: Before using any third-party icon, font, image, sound, vendored code, dataset, annotations or pretrained model weights, find its source and licence and record it in the project's notices file. Use whenever an outside asset, snippet, dataset or model enters a project.
---

# Licence check

1. Find the original source (a URL, a package and version, a commit).
2. Find the licence from the source itself, not from memory. AI-generated assets: say plainly that their licence
   status is unverified.
3. Does it allow this use (commercial, modification, redistribution in a release)? If unclear, ask the owner
   before using it.
4. Record it in the project's notices file (for example `THIRD_PARTY_NOTICES.md`): name, source, licence, where used.
   Vendored code also keeps a `SOURCE.md` with the licence text next to it.
5. **Datasets and model weights.** Record a dataset's licence (and its annotations', if separate) before the first
   training run. For pretrained weights, record their own licence and the data they were trained on. Terms such as
   non-commercial, research-only or copyleft decide whether the work can ship; if they're unclear, ask the owner.
