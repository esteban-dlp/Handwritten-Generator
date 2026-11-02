---
name: manuscript-generate
description: Prepare and render user-controlled handwritten-style text with an approved local character library
---

# Generate a document

1. Read AGENTS.md and docs/GENERATION.md, then inspect the active config and approved library. Respect the user's language, content and format. Do not inherit personal conventions from another user.
2. Prepare accurate UTF-8 text. Verify mathematical content independently. Explicitly mark paragraph/step breaks; this CLI does not parse LaTeX or infer proof structure.
3. Check coverage before rendering. If a glyph is missing, ask for a sample or propose an explicit alternative. Never silently replace handwriting with a font.
4. Run `manuscrito render private/text.txt --library private/approved-library.json --config private/config.json --output outputs/notes`. Preserve previous versions and inspect the manifest.
5. Check the exported PDF, not just HTML: dimensions, pagination, wrapping, punctuation, dense formulas and first/last page content. Inspect a close-up and normal reading size. Run tests after code changes.
6. Deliver only requested formats. Report real checks and limitations. Do not claim perfect recognition, mathematical correctness or automatic complex layout from rendering alone.
