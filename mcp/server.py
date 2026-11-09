#!/usr/bin/env python3
"""Minimal stdio MCP server with one tool, lint_addon, so Claude Code can lint a Blender addon.
Add it with: claude mcp add addon-lint -- python3 /path/to/mcp/server.py"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from addon_lint import lint, load

TOOL = {"name": "lint_addon", "description": "Lint a Blender 4.2+ extension folder or zip, returns findings or LINT_OK",
        "inputSchema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}


def reply(i, result):
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": i, "result": result}) + "\n"); sys.stdout.flush()


for line in sys.stdin:
    msg = json.loads(line); m = msg.get("method"); i = msg.get("id")
    if m == "initialize":
        reply(i, {"protocolVersion": msg["params"].get("protocolVersion", "2025-06-18"), "capabilities": {"tools": {}},
                  "serverInfo": {"name": "addon-lint", "version": "0.1.0"}})
    elif m == "tools/list":
        reply(i, {"tools": [TOOL]})
    elif m == "tools/call":
        try:
            res = lint(load(msg["params"]["arguments"]["path"])); text = "\n".join(res) or "LINT_OK"
        except Exception as e:
            text = f"ERROR {e}"
        reply(i, {"content": [{"type": "text", "text": text}]})
    elif i is not None:
        sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": i, "error": {"code": -32601, "message": "unknown method"}}) + "\n"); sys.stdout.flush()
