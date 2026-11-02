# Handwritten Generator

[![Tests](https://github.com/esteban-dlp/Handwritten-Generator/actions/workflows/tests.yml/badge.svg)](https://github.com/esteban-dlp/Handwritten-Generator/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](pyproject.toml)

### Your handwriting. Your settings. Your agent.

A **local-first, MIT-licensed** toolkit for building handwriting libraries from your notes, reviewing individual samples, and rendering text as HTML and PDF with the help of your preferred AI agent.

[Quick start](#quick-start) · [Use with an agent](#bring-your-agent) · [Compatibility](docs/AGENT_COMPATIBILITY.md) · [Generation](docs/GENERATION.md) · [Extraction](docs/EXTRACTION.md)

**Your notes → candidate samples → human review → approved library → handwritten pages**

## Features

- **Review before approval** — inspect samples, uncheck unwanted variants, and download the approved library from a standalone HTML page
- **Reproducible variation** — seeded shuffle bags visit every alternative before repeating a cycle
- **Controlled geometry** — configurable spacing, single-axis microdeformation and punctuation placement
- **Configurable pages** — grid, ruled or blank paper, page dimensions, cell size and margins
- **Versioned outputs** — each render gets its own directory and SHA-256 manifest
- **Private by default** — no telemetry, accounts or uploads; no personal notes, identities or libraries bundled
- **Agent-ready** — three documented skills and an AGENTS.md that put the current user in control

> This portable public edition is separate from the author's private legacy scripts. It does not include personal handwriting or coursework. The demo uses a generic system font, not anyone's handwriting.

## Quick start

Requires **Python 3.10+** and WeasyPrint's native dependencies. On macOS, start with `brew install pango`; see [setup](docs/SETUP.md) for platform notes.

```sh
git clone https://github.com/esteban-dlp/Handwritten-Generator.git
cd Handwritten-Generator
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
manuscrito setup --config private/config.json
manuscrito render examples/text.txt --library examples/font-library.json \
  --config private/config.json --output outputs/demo
```

Open `outputs/demo/v0001/document.html` or `document.pdf`. This tests installation in explicit **font mode**. To use your real handwriting, build a library with the extraction workflow below.

## Bring your agent

Ask your agent:

> Read AGENTS.md and the setup skill. Configure my preferred page size and paper. Then use my notes to build a candidate handwriting library and show me counts, all samples and new-only samples before approval.

| Skill | Purpose |
| --- | --- |
| [Setup](.agents/skills/manuscript-setup/SKILL.md) | Page size, paper, letter scale, margins, spacing and seed |
| [Generate](.agents/skills/manuscript-generate/SKILL.md) | Prepare content, check coverage, render and inspect |
| [Extract characters](.agents/skills/manuscript-extract-characters/SKILL.md) | Segment general notes, label crops, review and approve |

**Discovery depends on the agent.** Codex discovers the checked-in `.agents/skills/` directory when run inside this repository. Claude Code uses `.claude/skills/`; install the same workflows locally with:

```sh
mkdir -p .claude/skills
cp -R .agents/skills/manuscript-* .claude/skills/
```

The included `CLAUDE.md` also points Claude Code to `AGENTS.md`. For other agents, explicitly ask them to read `AGENTS.md` and the relevant `SKILL.md`. Giving an agent a repository URL alone does **not** guarantee skill installation, execution permissions, dependencies or successful extraction. See the [compatibility guide](docs/AGENT_COMPATIBILITY.md) for verified conventions and a smoke test.

User identity, language, colors and document conventions belong in local configuration/content, not hard-coded rules inherited from the author.

## Extract → review → approve → render

```sh
manuscrito extract private/notes.pdf --regions private/regions.json \
  --output private/candidates.json
manuscrito review private/candidates.json --output outputs/new-samples.html
manuscrito counts private/candidates.json
```

The agent or human supplies labels and crop coordinates after inspecting the PDF. Open the review HTML, uncheck unwanted samples, and download the approved JSON. Existing libraries should be backed up and merged by stable ID, not overwritten with a new-only batch. See [the complete extraction guide](docs/EXTRACTION.md).

**General notes are sufficient to start.** Isolated-character sheets are optional and can improve difficult cases. This is not universal OCR: touching cursive, ambiguous characters and noisy scans still need human review.

## Layout

```text
src/manuscrito/       portable CLI and engine
.agents/skills/       discoverable skills for Codex; portable SKILL.md workflows
docs/                 setup, generation, extraction, contribution guides
examples/             non-personal demonstration inputs
tests/                synthetic fixtures and regression tests
private/              local settings, PDFs and libraries (ignored)
outputs/              versioned renders and review files (ignored)
```

## Test

```sh
python -m unittest discover -s tests -v
```

Always inspect the actual PDF as well as test results. This is a character renderer, not a proof checker or complete mathematical typesetter. Complex fractions, matrices, diagrams and multi-column exercises need explicit layout work. Raster crops may include paper backgrounds; private legacy formats are not imported automatically. See [generation limitations](docs/GENERATION.md).

## Privacy, permission and license

Use handwriting samples with permission. Do not forge signatures, impersonate others, or misrepresent authorship where disclosure is required. Your files remain yours; local input does not license them to this project. Repository code is available under the [MIT License](LICENSE). Contributions are welcome: [contribution guide](docs/CONTRIBUTING.md).
