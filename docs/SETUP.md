# Setup and configuration

## Install

Use Python 3.10 or later in a virtual environment, then `python -m pip install -e .`.

WeasyPrint depends on native libraries. On macOS, install Pango with `brew install pango`. On Linux, follow the current WeasyPrint distribution instructions for your OS. On Windows, use the WeasyPrint-supported native library setup or WSL. Troubleshoot native dependencies before changing rendering logic.

Run `manuscrito setup --config private/config.json`. This refuses to overwrite an existing config. Edit the resulting JSON to match the user's preferences.

| Setting | Meaning |
| --- | --- |
| width, height | Page dimensions in points, 72 points per inch |
| cell | Row/grid spacing in points; currently use integer points for grid alignment |
| margin_cells | Margin in grid units, including the bottom |
| paper | grid, ruled or blank |
| font_size | Demo-font size only; sample size is controlled by cell/source_cell |
| seed | Reproducible variant order, deformation and spacing |
| deformation | Minimum and maximum axis scale; one axis changes per glyph |
| gap | Character gap range in cell units |
| word_space | Word spacing in cell units |
| ink | Demo-font color; raster samples preserve their source ink |

For A4 use 595.28 × 841.89; for US Letter use 612 × 792. This project does not mandate either. Header text, numbering style and language are supplied by the user in the input text, not injected automatically.

Start with a small sample and inspect at 100% before producing a long document. Large crops, noise and poor segmentation cannot be repaired by changing the page size. For disabling deformation set `[1, 1]`.
