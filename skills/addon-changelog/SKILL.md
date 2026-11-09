---
name: addon-changelog
description: Bump a Blender extension version and write a plain changelog entry from the git diff. Use when releasing a new addon version.
---
# Version bump and changelog

1. Read `git diff <last tag>..HEAD -- <addon folder>`.
2. Pick the bump: fix only = patch, new operator or option = minor, removed or renamed operator or property = major.
3. Update `version` in blender_manifest.toml.
4. Add to CHANGELOG.md, newest first: `## <version>, <date>` then one line per user-visible change, in plain words a Blender user understands. No internal refactors, no filler.
5. Tag `v<version>` only after the addon-package skill printed REGISTER_OK.
