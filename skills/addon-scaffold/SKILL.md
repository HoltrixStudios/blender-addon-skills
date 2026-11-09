---
name: addon-scaffold
description: Create a new Blender 4.2+ extension (addon) folder with blender_manifest.toml, an operator, a sidebar panel and properties that register cleanly. Use when the user asks for a new Blender addon or extension.
---
# Scaffold a Blender extension

1. Ask nothing you can infer. Pick an id in snake_case from the addon name.
2. Create `<id>/blender_manifest.toml` with: schema_version = "1.0.0", id, version = "0.1.0", name, tagline (64 chars max, no trailing period), maintainer, type = "add-on", blender_version_min = "4.2.0", license = ["SPDX:GPL-3.0-or-later"], and permissions only if the addon really needs files or network.
3. Create `<id>/__init__.py` with no bl_info (extensions use the manifest). Structure:
   - one PropertyGroup on `bpy.types.Scene` via PointerProperty
   - operators named `<ID>_OT_<verb>` with `bl_idname = "<id>.<verb>"`, `bl_options = {"REGISTER", "UNDO"}`, a `poll` that checks context
   - a panel `<ID>_PT_main` in `VIEW_3D`, region `UI`, `bl_category` = the addon name
   - `classes = (...)`, `register()` loops `bpy.utils.register_class`, `unregister()` loops reversed and deletes the Scene pointer
4. Never touch `bpy.context` or `bpy.data` at import time. Never hardcode absolute paths.
5. Run the addon-lint skill on the folder before saying it is done.
