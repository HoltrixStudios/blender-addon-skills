#!/usr/bin/env python3
"""Static checks for a Blender 4.2+ extension folder or zip. Prints one finding per line, LINT_OK when clean."""
import ast, re, sys, zipfile
try:
    import tomllib
except ImportError:  # Python before 3.11: the manifest only needs flat key = value lines
    tomllib = None
from pathlib import Path

def parse_toml(text):
    if tomllib:
        return tomllib.loads(text)
    out = {}
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if "=" in line and not line.startswith("["):
            k, v = (s.strip() for s in line.split("=", 1))
            out[k] = ast.literal_eval(v)
    return out


REQ = ["schema_version", "id", "version", "name", "tagline", "maintainer", "type", "blender_version_min", "license"]


def load(target):
    p = Path(target)
    if p.suffix == ".zip":
        z = zipfile.ZipFile(p)
        return {n: z.read(n) for n in z.namelist() if not n.endswith("/")}
    return {str(f.relative_to(p)): f.read_bytes() for f in p.rglob("*") if f.is_file() and "__pycache__" not in f.parts}


def lint(files):
    out = []
    if "blender_manifest.toml" not in files:
        return ["ERROR blender_manifest.toml missing at the root (zip it from inside the addon folder)"]
    try:
        m = parse_toml(files["blender_manifest.toml"].decode())
    except Exception as e:
        return [f"ERROR manifest does not parse: {e}"]
    out += [f"ERROR manifest field missing: {k}" for k in REQ if k not in m]
    if "id" in m and not re.fullmatch(r"[a-z][a-z0-9_]*", m["id"]):
        out.append("ERROR id must be lowercase letters, digits and underscores")
    if len(m.get("tagline", "")) > 64 or m.get("tagline", "").endswith("."):
        out.append("ERROR tagline must be 64 chars max with no trailing period")
    if m.get("type") not in ("add-on", "theme"):
        out.append("ERROR type must be add-on or theme")
    init = files.get("__init__.py")
    if init is None:
        return out + ["ERROR __init__.py missing at the root"]
    tree = ast.parse(init)
    names = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
    out += [f"ERROR {f}() missing in __init__.py" for f in ("register", "unregister") if f not in names]
    if any(isinstance(n, ast.Assign) and any(getattr(t, "id", "") == "bl_info" for t in n.targets) for n in tree.body):
        out.append("WARN bl_info is ignored by extensions, the manifest wins; remove it to avoid drift")
    for n in tree.body:  # module level code that touches context or data at import breaks install
        if isinstance(n, (ast.Expr, ast.Assign)) and re.search(r"bpy\.(context|data)\.", ast.unparse(n)):
            out.append(f"ERROR line {n.lineno}: bpy.context or bpy.data used at import time")
    for name, src in files.items():
        if not name.endswith(".py"):
            continue
        t = ast.parse(src)
        for c in [n for n in ast.walk(t) if isinstance(n, ast.ClassDef)]:
            kinds = [b.attr if isinstance(b, ast.Attribute) else getattr(b, "id", "") for b in c.bases]
            for kind, tag in (("Operator", "_OT_"), ("Panel", "_PT_"), ("Menu", "_MT_")):
                if kind in kinds and tag not in c.name:
                    out.append(f"WARN {name}: class {c.name} should contain {tag}")
            for s in c.body:
                if isinstance(s, ast.Assign) and any(getattr(x, "id", "") == "bl_idname" for x in s.targets) and "Operator" in kinds:
                    v = getattr(s.value, "value", "")
                    if not re.fullmatch(r"[a-z0-9_]+\.[a-z0-9_]+", str(v)):
                        out.append(f"ERROR {name}: operator bl_idname '{v}' must look like category.name in lowercase")
        if re.search(rb"[\"'](/Users/|/home/|[A-Z]:\\\\)", src):
            out.append(f"ERROR {name}: absolute path in code")
    return out


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: addon_lint.py <addon folder or zip>")
    res = lint(load(sys.argv[1]))
    print("\n".join(res) if res else "LINT_OK")
    sys.exit(1 if any(r.startswith("ERROR") for r in res) else 0)


if __name__ == "__main__":
    main()
