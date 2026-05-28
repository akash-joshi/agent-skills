---
name: cc-to-linear
description: Post a Claude Code session's agent activity timeline as a comment on a Linear issue. Use when the user asks to "send this session to Linear", "post the agent run to LIN-XYZ", "log this work on Linear", "drop a timeline on the ticket", or invokes /cc-to-linear with a Linear issue identifier. Reads the current Claude Code session JSONL (or a named one), summarises tool calls, files touched, models used, and the final assistant message, then posts a structured markdown comment via the Linear MCP server.
---

# cc-to-linear

Turn a Claude Code session into an agent-activity timeline comment on a Linear issue. Auditable trail of what the agent did, posted alongside the human-written discussion on the ticket, so reviewers can see which files were touched, which tools were called, and what the agent concluded — without having to re-read the entire session.

## Trigger

The user invokes this skill with one of:

- `/cc-to-linear LIN-123`
- "post this session to LIN-123"
- "send the agent run to Linear ticket ENG-42"
- "drop a timeline on LIN-7"

The argument is a Linear issue identifier (TEAM-NUMBER format).

## Prerequisites

- Linear MCP server must be authenticated. If the tools `mcp__linear-server__*` are not available in this session, tell the user: "Linear MCP isn't authenticated. Run `/mcp` to OAuth into Linear, then restart Claude Code."

## Workflow

### Step 1 — Resolve the session JSONL

Find which Claude Code session JSONL to summarise. Priority:

1. If the user named a specific session ID, find it at `~/.claude/projects/*/{session_id}.jsonl`.
2. Otherwise, use the MOST RECENT JSONL file in `~/.claude/projects/-{cwd-as-dashes}/`. The cwd-as-dashes mapping replaces `/` with `-` (e.g. `/Users/<you>/code/foo` → `-Users-<you>-code-foo`).
3. If the most-recent file is the in-progress session you're running inside, walk back to the second-most-recent so we summarise a completed session, not one we're inside. The user usually wants to log the run they just finished.

Use this to find candidates:

```bash
ls -t ~/.claude/projects/-{cwd-as-dashes}/*.jsonl 2>/dev/null | head -3
```

### Step 2 — Generate the markdown

Run the parser:

```bash
python3 ~/.claude/skills/cc-to-linear/parse.py <session_jsonl_path>
```

The script outputs a markdown block on stdout with:
- Prompt (truncated to 500 chars)
- Run stats (duration, tool calls, errors, tokens, models, cwd, branch)
- Tools used (count by name)
- Files touched (path + which tools touched it)
- Errors (first 5 tool errors)
- Final assistant message (truncated to 1500 chars)

Capture stdout. **Do not modify the markdown** — the parser owns the formatting contract. If you want a different format, adjust `parse.py`, not the comment body.

### Step 3 — Post to Linear

Use `mcp__linear-server__save_comment`. Linear's MCP unifies create and update behind one tool — pass `body` + `issueId` to create a new comment, or include `id` to edit an existing one.

The tool accepts the human identifier (e.g. `LIN-123`) directly as `issueId`; no UUID lookup needed.

Tool input:
- `issueId`: the identifier the user passed (e.g. `LIN-123`)
- `body`: the markdown captured from `parse.py`

Send the body as real markdown with literal newlines — do not escape `\n` into the string.

### Step 4 — Confirm

Report back with:
- A one-line confirmation: "Posted to LIN-123."
- The Linear URL of the issue if returned by the MCP response, otherwise just the identifier.

## Behavioural rules

**Never invent session content.** If the JSONL has no tool calls, post the comment anyway with the prompt + final message and note "no tool calls in this session". Don't fabricate stats.

**Don't include secrets.** The parser truncates tool outputs to 200 chars, but if you spot anything that looks like a credential (API key, token, JWT, password) in the prompt or final message, redact it before posting and warn the user.

**One comment per invocation.** Don't paginate across multiple comments. If the markdown exceeds Linear's comment limit (~65k chars), tell the user and ask whether to truncate more aggressively or split.

**Idempotency.** Running this skill twice on the same session posts two comments. That's intentional — Linear comments aren't keyed by source. If you want edit-in-place behaviour, capture the comment ID returned by the first post and pass it as `id` on the next run.

## Why this skill exists

There's a real gap on the issue view today: when an autonomous coding agent works a ticket, the human reviewer has no good way to audit what it did — which files it read, what it tried and rolled back, why it picked the approach it did. Reading the full session transcript is too much. Reading nothing means trusting the diff at face value.

This skill posts a compact, structured timeline as one comment, so the agent's work sits alongside the rest of the ticket discussion and stays reviewable in the same place humans already look.
