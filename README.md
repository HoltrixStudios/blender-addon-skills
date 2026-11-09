# Blender Addon Skills for Claude Code

Four free Claude Code skills and a small MCP server that make Claude build Blender 4.2+ extensions that install and register on the first try.

| Skill | What it does |
|---|---|
| addon-scaffold | new extension folder: manifest, operator, sidebar panel, properties, clean register and unregister |
| addon-lint | catches what breaks install: missing manifest fields, bad ids, bpy.context at import time, bad bl_idname, absolute paths |
| addon-package | builds the zip and proves it installs and registers in a clean headless Blender |
| addon-changelog | version bump plus a plain changelog from the git diff |

## Install

```bash
git clone https://github.com/HoltrixStudios/blender-addon-skills
cp -r blender-addon-skills/skills/* ~/.claude/skills/
claude mcp add addon-lint -- python3 "$PWD/blender-addon-skills/mcp/server.py"
```

Then ask Claude: "make me a Blender addon that ..." and it scaffolds, lints, packages and proves it registers.

Lint without Claude: `python3 mcp/addon_lint.py path/to/addon_or_zip` prints `LINT_OK` or one finding per line.

## Full pack

The Blender Addon Builder pack adds Geometry Nodes from Python, preferences and keymaps, headless demo clip capture, and store page writing: https://polyember.com/ai

Made by Polyember, the people behind Build-Up FX and Liquid FX. MIT licence.
