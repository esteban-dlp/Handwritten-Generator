# Generation guide

## Prepare the content

Use UTF-8 plain text, with explicit newlines where a paragraph or step must end. Confirm the user's title, optional identification, language and style. Do not apply any original-author-specific header, color or punctuation rules. Check mathematics separately from the rendering.

## Render

```sh
manuscrito render private/text.txt --library private/approved-library.json \
  --config private/config.json --output outputs/notes
```

Each run creates a fresh directory (`v0001`, `v0002`, …) with HTML, PDF and a manifest containing the configuration and file SHA-256 values. Avoid concurrent writers to the same output folder. HTML and PDF are generated from the same layout. Missing characters stop handwritten rendering with an explicit error. Font mode is opt-in and is not a personal handwriting substitute.

## Algorithm

Each character has an independent shuffle bag. All alternatives are used before refilling it. The first alternative in a new cycle cannot equal the previous last alternative when at least two exist. With at least three alternatives, consecutive cycle orders also differ. With two alternatives, alternating them necessarily repeats the cycle order. A seed makes the process reproducible within the same software/library version.

For each glyph, only width or height receives a randomly selected scale within the configured bounds; the other remains exactly 1.0. Spacing is sampled from the configured gap range. Widths are measured after deformation, and overflowing words/characters move to the next row. The public engine wraps at character boundaries, not whole-word boundaries. Vertical centers vary per character, with special lower/upper anchors for punctuation.

## Inspect before delivery

1. Confirm dimensions and page count in the PDF
2. Inspect first, middle and final pages at normal size
3. Zoom in on punctuation, repeated letters and dense formulas
4. Check no crop or glyph crosses the content boundary
5. Review HTML at narrow width; generated fixed-page documents may require zooming, whereas the review gallery wraps responsively
6. Report coverage gaps and supply only the file formats requested by the user

## Current boundaries

No automatic theorem solving, formula parsing, PDF signature preservation, complex diagrams, color-by-role or variable-height math layout is included. Multi-column exercises require explicit future layout development. Do not claim a private legacy feature exists in the public CLI. PDF metadata is left to the export library; this public edition does not promise anonymous documents. Examine metadata separately when privacy matters.
