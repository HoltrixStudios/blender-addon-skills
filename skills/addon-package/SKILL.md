---
name: addon-package
description: Build an installable extension zip for a Blender addon and prove it installs and registers in a clean headless Blender. Use when the user wants to ship or test an addon.
---
# Package and prove a Blender addon

1. Lint first (addon-lint skill) until `LINT_OK`.
2. Build (the output folder must exist first, Blender does not create it): `mkdir -p dist && blender --background --factory-startup --command extension build --source-dir <folder> --output-dir dist`.
3. Prove it installs in a throwaway profile:
   `export BLENDER_USER_RESOURCES=$(mktemp -d)` then
   `blender --background --factory-startup --command extension install-file -r user_default -e dist/<zip>` (must print `Installed "<id>"`),
   then, WITHOUT --factory-startup so the throwaway profile loads: `blender --background --python-expr "import bpy; assert 'bl_ext.user_default.<id>' in bpy.context.preferences.addons; bpy.ops.<category>.<op>(); print('REGISTER_OK')"`.
4. Done only when the output shows `REGISTER_OK` and no Traceback. Give the user the zip path and its sha256.
