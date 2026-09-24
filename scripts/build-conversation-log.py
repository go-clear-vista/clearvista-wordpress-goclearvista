#!/usr/bin/env python3
"""Rebuild docs/conversation-log.md from a Claude Code transcript (.jsonl)."""
import json, re, sys
from datetime import datetime

src, out = sys.argv[1], sys.argv[2]
HEADER = """# ClearVista website redesign — conversation log

Chronological record of the Claude Code session that redesigned goclearvista.com (Sept 23–24, 2026).
Includes every user message and Claude's written replies. Tool calls, raw tool output and screenshots are omitted; see `notes/previews/` for the screenshots.
"""
SKIP = ("<local-command", "<command-name>", "<system-reminder>", "This session is being continued",
        "Stop hook feedback", "<task-notification>", "Caveat:")

def ts(e):
    t = e.get("timestamp", "")
    try:
        return datetime.fromisoformat(t.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M UTC")
    except Exception:
        return t

def clean(s):
    s = re.sub(r"<system-reminder>.*?</system-reminder>", "", s, flags=re.S)
    return s.strip()

parts, seen = [HEADER], set()
for line in open(src):
    try:
        e = json.loads(line)
    except Exception:
        continue
    if e.get("isMeta") or e.get("isCompactSummary") or e.get("isSidechain"):
        continue
    a = e.get("attachment") or {}
    if e.get("type") == "attachment" and a.get("type") == "queued_command" and isinstance(a.get("prompt"), str):
        c = clean(a["prompt"])
        if c and ("u", c) not in seen:
            seen.add(("u", c))
            parts.append(f"---\n\n### 🧑 User (sent mid-turn) — {ts(e)}\n\n{c}\n")
        continue
    m = e.get("message") or {}
    c = m.get("content")
    if e.get("type") == "user":
        if isinstance(c, list):
            if any(b.get("type") == "tool_result" for b in c if isinstance(b, dict)):
                continue
            c = "\n".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text")
        if not isinstance(c, str):
            continue
        c = clean(c)
        if not c or c.startswith(SKIP):
            continue
        key = ("u", c)
        if key in seen:
            continue
        seen.add(key)
        parts.append(f"---\n\n### 🧑 User — {ts(e)}\n\n{c}\n")
    elif e.get("type") == "assistant" and isinstance(c, list):
        txt = "\n\n".join(b["text"].strip() for b in c if b.get("type") == "text" and b.get("text", "").strip())
        if not txt:
            continue
        key = ("a", e.get("uuid"), txt)
        if key in seen:
            continue
        seen.add(key)
        parts.append(f"**🤖 Claude — {ts(e)}**\n\n{txt}\n")

open(out, "w").write("\n".join(parts))
