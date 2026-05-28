#!/usr/bin/env python3
"""Parse a Claude Code session JSONL and emit a Linear-ready markdown comment.

Usage:
    parse.py <session_jsonl_path>

Output: markdown on stdout, suitable for posting as a Linear issue comment.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


def _text(content: Any) -> str:
    """Pull plain text out of a Claude message content field."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
        return "\n".join(p for p in parts if p)
    return ""


def _tool_result_text(content: Any) -> str:
    """Best-effort string of a tool_result for stats only (not posted whole)."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        out = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                out.append(block.get("text", ""))
        return "\n".join(out)
    return str(content) if content else ""


def parse(path: Path) -> dict[str, Any]:
    session_id = None
    cwd = None
    git_branch = None
    first_user_text = None
    last_assistant_text = None
    started_at = None
    ended_at = None

    pending: dict[str, dict[str, Any]] = {}
    tool_pairs: list[dict[str, Any]] = []
    tool_counts: Counter[str] = Counter()
    files_touched: dict[str, set[str]] = defaultdict(set)  # path -> set of tool names
    models_used: Counter[str] = Counter()
    total_input_tokens = 0
    total_output_tokens = 0
    error_pairs: list[dict[str, Any]] = []

    with path.open() as fh:
        for raw in fh:
            raw = raw.strip()
            if not raw:
                continue
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                continue

            sid = data.get("sessionId")
            if not sid:
                continue
            if session_id is None:
                session_id = sid
                cwd = data.get("cwd")
                git_branch = data.get("gitBranch")

            ts = data.get("timestamp")
            if ts:
                if started_at is None:
                    started_at = ts
                ended_at = ts

            entry_type = data.get("type")
            if entry_type == "user":
                content = data.get("message", {}).get("content")
                if isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "tool_result":
                            tool_use_id = block.get("tool_use_id")
                            match = pending.pop(tool_use_id, None)
                            if not match:
                                continue
                            pair = {
                                "tool": match["name"],
                                "input": match["input"],
                                "is_error": block.get("is_error", False),
                                "start": match["ts"],
                                "end": ts,
                                "output_preview": _tool_result_text(block.get("content"))[:200],
                            }
                            tool_pairs.append(pair)
                            tool_counts[match["name"]] += 1
                            if pair["is_error"]:
                                error_pairs.append(pair)
                            _record_file(files_touched, match["name"], match["input"])

                text = _text(content) if isinstance(content, list) else (content if isinstance(content, str) else "")
                if text and first_user_text is None and not text.startswith("<"):
                    first_user_text = text

            elif entry_type == "assistant":
                msg = data.get("message", {})
                content = msg.get("content", [])
                text = _text(content)
                if text:
                    last_assistant_text = text

                model = msg.get("model")
                if model:
                    models_used[model] += 1
                usage = msg.get("usage") or {}
                total_input_tokens += usage.get("input_tokens", 0) + usage.get("cache_creation_input_tokens", 0) + usage.get("cache_read_input_tokens", 0)
                total_output_tokens += usage.get("output_tokens", 0)

                for block in content if isinstance(content, list) else []:
                    if isinstance(block, dict) and block.get("type") == "tool_use":
                        tool_use_id = block.get("id")
                        pending[tool_use_id] = {
                            "name": block.get("name"),
                            "input": block.get("input"),
                            "ts": ts,
                        }

    return {
        "session_id": session_id,
        "cwd": cwd,
        "git_branch": git_branch,
        "first_user_text": first_user_text,
        "last_assistant_text": last_assistant_text,
        "started_at": started_at,
        "ended_at": ended_at,
        "tool_pairs": tool_pairs,
        "tool_counts": dict(tool_counts),
        "files_touched": {p: sorted(t) for p, t in files_touched.items()},
        "models_used": dict(models_used),
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "error_pairs": error_pairs,
    }


def _record_file(store: dict[str, set[str]], tool_name: str, tool_input: Any) -> None:
    if not isinstance(tool_input, dict):
        return
    file_keys = ("file_path", "path", "notebook_path")
    for key in file_keys:
        value = tool_input.get(key)
        if isinstance(value, str):
            store[value].add(tool_name)


def _duration(start: str | None, end: str | None) -> str:
    if not start or not end:
        return "unknown"
    try:
        s = datetime.fromisoformat(start.replace("Z", "+00:00"))
        e = datetime.fromisoformat(end.replace("Z", "+00:00"))
    except ValueError:
        return "unknown"
    seconds = int((e - s).total_seconds())
    if seconds < 60:
        return f"{seconds}s"
    if seconds < 3600:
        return f"{seconds // 60}m {seconds % 60}s"
    return f"{seconds // 3600}h {(seconds % 3600) // 60}m"


def render_markdown(view: dict[str, Any]) -> str:
    lines: list[str] = []
    sid = view["session_id"] or "unknown"
    lines.append(f"### Claude Code agent run · `{sid[:8]}`")
    lines.append("")

    if view["first_user_text"]:
        prompt = view["first_user_text"].strip()
        if len(prompt) > 500:
            prompt = prompt[:500] + "…"
        lines.append("**Prompt**")
        lines.append("")
        for line in prompt.splitlines():
            lines.append(f"> {line}")
        lines.append("")

    duration = _duration(view["started_at"], view["ended_at"])
    total_tools = sum(view["tool_counts"].values())
    models = ", ".join(f"{m} ({n})" for m, n in view["models_used"].items()) or "unknown"

    lines.append("**Run stats**")
    lines.append("")
    lines.append(f"- Duration: {duration}")
    lines.append(f"- Tool calls: {total_tools}")
    lines.append(f"- Errors: {len(view['error_pairs'])}")
    lines.append(f"- Tokens: {view['total_input_tokens']:,} in / {view['total_output_tokens']:,} out")
    lines.append(f"- Models: {models}")
    if view["cwd"]:
        lines.append(f"- cwd: `{view['cwd']}`")
    if view["git_branch"]:
        lines.append(f"- branch: `{view['git_branch']}`")
    lines.append("")

    if view["tool_counts"]:
        lines.append("**Tools used**")
        lines.append("")
        for name, count in sorted(view["tool_counts"].items(), key=lambda kv: -kv[1]):
            lines.append(f"- `{name}` × {count}")
        lines.append("")

    if view["files_touched"]:
        lines.append("**Files touched**")
        lines.append("")
        for filepath, tools in sorted(view["files_touched"].items()):
            tool_list = ", ".join(tools)
            lines.append(f"- `{filepath}` ({tool_list})")
        lines.append("")

    if view["error_pairs"]:
        lines.append("**Errors**")
        lines.append("")
        for pair in view["error_pairs"][:5]:
            preview = pair["output_preview"].replace("\n", " ")
            lines.append(f"- `{pair['tool']}` — {preview[:150]}")
        lines.append("")

    if view["last_assistant_text"]:
        summary = view["last_assistant_text"].strip()
        if len(summary) > 1500:
            summary = summary[:1500] + "…"
        lines.append("**Final assistant message**")
        lines.append("")
        for line in summary.splitlines():
            lines.append(f"> {line}")
        lines.append("")

    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: parse.py <session_jsonl_path>", file=sys.stderr)
        return 2
    path = Path(argv[1]).expanduser()
    if not path.exists():
        print(f"not found: {path}", file=sys.stderr)
        return 1
    view = parse(path)
    sys.stdout.write(render_markdown(view))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
