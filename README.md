# agent-skills

A collection of AI agent skills, custom agents, and workflows for Claude Code. Built for engineers, consultants, and founders who want AI agents that actually do useful work.

By [Akash Joshi](https://thewriting.dev).

## What's in here

### 🎯 [Cold Outreach Skills](skills/cold-outreach/)

7 skills for client acquisition through cold outreach, social selling, and content-led growth. Built for solo consultants and freelancers.

| Skill | Description |
|-------|-------------|
| [keyword-search](skills/cold-outreach/keyword-search/) | Find people actively looking for your service on X/LinkedIn/Telegram |
| [cold-dm](skills/cold-outreach/cold-dm/) | Write outreach messages that get replies |
| [follow-up-sequences](skills/cold-outreach/follow-up-sequences/) | Multi-channel follow-up cadences (most deals close on touch 3-5) |
| [content-selling](skills/cold-outreach/content-selling/) | Inbound content strategy for client leads |
| [profile-optimization](skills/cold-outreach/profile-optimization/) | Convert profile visitors into clients |
| [prospecting-lists](skills/cold-outreach/prospecting-lists/) | ICP-based systematic list building |
| [discovery-calls](skills/cold-outreach/discovery-calls/) | Run calls that close deals |

### 🎫 [Ticket Agent](agents/ticket.md)

A custom Claude Code agent that turns a ticket ID into a reviewable merge request, one TDD commit at a time.

```
/ticket ABC-123
```

The agent reads the ticket from your project tracker, follows linked designs and docs, explores the codebase, creates a worktree, writes a TDD-driven plan, executes it commit by commit, pushes the branch, and opens an MR. Your only job is to review the final diff.

Full writeup: [Hand Claude a Ticket, Get Back a Merge Request](https://thewriting.dev)

**Prerequisites:** Project tracker MCP server (Jira, Linear, GitHub Issues, etc.), `glab` or `gh` CLI for merge requests, Figma MCP server (optional).

### 💬 [Discuss](skills/discuss/)

Clarify gray areas in proposed work before planning. Surfaces implementation choices that would change the outcome, walks through them with concrete options, and produces a context file that plan mode or downstream agents can consume.

```
/discuss ABC-123 - should we use WebSockets or SSE for the streaming endpoint?
```

Use before `/ticket` on any non-trivial feature where multiple reasonable implementations exist.

### 🐯 [Tiger-Style Coding](skills/tiger-style-coding/)

Apply TigerBeetle's [TIGER_STYLE.md](https://github.com/tigerbeetle/tigerbeetle/blob/main/docs/TIGER_STYLE.md) principles to any language and project. Enforces safety > performance > developer experience: 70-line function cap, runtime assertions, bounded loops and retries, explicit library options, zero-dependency bias.

Load when writing, reviewing, or refactoring code — or when configuring AI coding agents on how to write code for your codebase. Includes a review checklist that catches sprawl, unbounded work, and undocumented dependencies in agent-generated PRs.

### 🎙️ [Voicenotes](skills/voicenotes-skill/)

Connect AI agents to the [Voicenotes](https://voicenotes.com) API. Semantic search across notes, retrieve full transcripts, filter by tags or date range, and create text notes through natural conversation.

```
"pull my meeting notes from last Tuesday about the API redesign"
```

Requires a `VOICENOTES_API_KEY` - grab one from https://voicenotes.com/app?open-claw=true#settings.

### 🎭 [Playwright CLI](skills/playwright-cli/)

Drive a real browser from the command line with `playwright-cli`. Navigate, click, fill forms, and read accessibility snapshots that give the agent stable element refs instead of brittle selectors.

```
"log into the staging dashboard and check the settings page renders"
```

Nine reference guides cover the parts agents usually get wrong: reusing an authenticated session across runs, saving and loading storage state, mocking network requests, recording video and traces, and generating Playwright tests from a live session.

Requires `npm install -g @playwright/cli`, and `ffmpeg` if you want video.

### 📐 [AGENTS.md](./AGENTS.md)

Engineering rules the agent follows. TDD enforcement, commit format, plan structure, code-style guidance. Drop this at the root of your repo (or `~/AGENTS.md` for global rules) — it's the source of truth for how all agents in this repo behave.

## Install

### npx skills (Recommended)

```sh
# Install all skills
npx skills add akash-joshi/agent-skills

# Install just cold outreach skills
npx skills add akash-joshi/agent-skills --skill cold-dm keyword-search follow-up-sequences

# List available skills
npx skills add akash-joshi/agent-skills --list
```

Works with Claude Code, Cursor, Codex CLI, and Gemini CLI. Auto-detects your agent and installs to the right directory.

### Manual

```sh
# Everything
git clone https://github.com/akash-joshi/agent-skills.git

# Just cold outreach skills
cp -r agent-skills/skills/cold-outreach/*/ .agents/skills/

# Ticket agent + engineering rules
cp agent-skills/AGENTS.md ~/AGENTS.md
mkdir -p ~/.claude/agents && cp agents/ticket.md ~/.claude/agents/ticket.md

# Individual skills
mkdir -p ~/.claude/skills/discuss && cp skills/discuss/SKILL.md ~/.claude/skills/discuss/SKILL.md
```

## License

MIT
