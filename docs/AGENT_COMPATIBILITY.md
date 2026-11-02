# Agent compatibility

## What is portable, and what is not?

A skill is a directory with a SKILL.md containing YAML frontmatter (`name` and `description`) followed by workflow instructions. That format is portable; discovery paths, activation behavior, trust prompts and execution permissions depend on the host agent. A skill cannot grant tools or bypass approvals.

This repository stores its three canonical workflows in `.agents/skills/`, using directory names that match the frontmatter names. AGENTS.md contains project-wide guidance; it is not a substitute for skill discovery. `.agents` is a directory, whereas `AGENTS.md` is a Markdown file.

## Codex

Open or clone this repository and launch Codex inside it. Codex scans `.agents/skills` from the working directory up to the repository root. The three skills can be selected explicitly by name or matched to a task from their descriptions. Ask it to use `manuscript-setup` first. If discovery does not refresh, restart Codex.

## Claude Code

Claude Code's documented project location is `.claude/skills/<skill-name>/SKILL.md`, not `.agents/skills`. From the repository root:

```sh
mkdir -p .claude/skills
cp -R .agents/skills/manuscript-* .claude/skills/
```

The local copy is intentionally ignored by Git. Refresh it after updating canonical skills. The root CLAUDE.md directs Claude Code to AGENTS.md. Select `/manuscript-setup`, `/manuscript-generate` or `/manuscript-extract-characters`, or describe a matching task. Workspace trust and host permissions still apply.

## Other agents and chat interfaces

Do not promise automatic discovery. Ask the agent to read AGENTS.md and the relevant `.agents/skills/.../SKILL.md` directly, or install the skill using that product's documented import process. An agent with only chat access cannot install dependencies, inspect local PDFs or execute the renderer without suitable tools. A GitHub URL alone does not provide local file access or execute anything. Private repositories require authorization.

Example request:

> Open this project locally. Read AGENTS.md and .agents/skills/manuscript-setup/SKILL.md. Install it in a virtual environment, ask only for missing page preferences, run the tests and render the generic example. Do not use or publish my personal handwriting until I provide and approve a library.

## Verification checklist

1. Ask the agent to name the three discovered skills and their paths. If it cannot, explicitly load the files rather than guessing.
2. Follow README installation and native dependency instructions.
3. Run `python -m unittest discover -s tests -v`.
4. Render the generic font-mode example from README and inspect HTML and PDF.
5. Extract a small candidate batch, review its samples and counts, then approve it before rendering personal handwriting.

Repository tests check the Python workflow, not every vendor's skill selector. We have not performed an end-to-end interactive test inside Codex or Claude Code, so host-specific automatic activation is documented from official sources, not claimed as locally observed.

## Official references

- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills) — Codex discovery locations and activation
- [Claude Code: Extend Claude with skills](https://code.claude.com/docs/en/skills) — project/personal skill paths and invocation
- [Agent Skills specification](https://agentskills.io/specification) — directory structure and SKILL.md frontmatter

Consult the documentation for your installed agent version if its behavior differs. The current user's content and preferences drive the workflow, within the host's system rules and actual permissions.
