---
name: manuscript-setup
description: Configure page size, paper, handwriting scale and local paths for a user's manuscript workflow
---

# Setup a manuscript workspace

1. Read AGENTS.md and docs/SETUP.md. Inspect Python and native WeasyPrint dependencies before installing anything. Use a project virtual environment.
2. Ask only for preferences not already provided: page dimensions, grid/ruled/blank paper, cell/letter size, margins, spacing and optional seed. Do not assume the original author's preferences or inject a name/course.
3. Run `manuscrito setup --config private/config.json` for a new workspace. For an existing file, read and patch only requested fields. Keep inputs and approved libraries under private/ and outputs under outputs/.
4. Explain that sample scale follows cell/source_cell; font_size only affects explicit demonstration font mode. Deformation may change one axis only and must preserve legibility.
5. Install with `python -m pip install -e .`, run the synthetic tests, and render the generic example. Check PDF dimensions and view the real result before declaring setup complete.
6. Record the user's configuration locally. Never commit identities, personal notes or libraries. Show the user how to request later changes without editing program source.
