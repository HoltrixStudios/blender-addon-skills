---
name: addon-lint
description: Check a Blender addon folder or zip for the errors that break install or registration, with addon_lint.py, then fix every finding. Use before packaging or after any addon edit.
---
# Lint a Blender addon

1. Run `python3 <skill_dir>/../../mcp/addon_lint.py <addon folder or zip>`. It prints one line per finding and `LINT_OK` when clean.
2. Fix every ERROR. Fix WARN unless the user wants it kept, then say why.
3. If Blender is installed, also run `blender --background --factory-startup --command extension validate <folder>` and fix what it reports.
4. Re-run until `LINT_OK`. Report the final line, never "should work".
