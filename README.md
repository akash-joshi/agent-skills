# agent-skills

A collection of AI agent skills, custom agents, and workflows for Claude Code. Built for engineers, consultants, and founders who want AI agents that actually do useful work.

By [Akash Joshi](https://thewriting.dev).

## What's in here

### 🎯 [Cold Outreach Skills](cold-outreach-skills/)

7 skills for client acquisition through cold outreach, social selling, and content-led growth. Built for solo consultants and freelancers.

| Skill | Description |
|-------|-------------|
| [keyword-search](cold-outreach-skills/skills/keyword-search/) | Find people actively looking for your service on X/LinkedIn/Telegram |
| [cold-dm](cold-outreach-skills/skills/cold-dm/) | Write outreach messages that get replies |
| [follow-up-sequences](cold-outreach-skills/skills/follow-up-sequences/) | Multi-channel follow-up cadences (most deals close on touch 3-5) |
| [content-selling](cold-outreach-skills/skills/content-selling/) | Inbound content strategy for client leads |
| [profile-optimization](cold-outreach-skills/skills/profile-optimization/) | Convert profile visitors into clients |
| [prospecting-lists](cold-outreach-skills/skills/prospecting-lists/) | ICP-based systematic list building |
| [discovery-calls](cold-outreach-skills/skills/discovery-calls/) | Run calls that close deals |

### 🎫 Ticket Agent

A custom Claude Code agent that turns a ticket ID into a reviewable merge request, one TDD commit at a time.

```
/ticket ABC-123
```

The agent reads the ticket from your project tracker, follows linked designs and docs, explores the codebase, creates a worktree, writes a TDD-driven plan, executes it commit by commit, pushes the branch, and opens an MR. Your only job is to review the final diff.

Full writeup: [Hand Claude a Ticket, Get Back a Merge Request](https://thewriting.dev)

**Files:**
- [`AGENTS.md`](./AGENTS.md) - Engineering rules the agent follows
- [`agents/ticket.md`](./agents/ticket.md) - The agent definition (4-phase workflow)
- [`skills/discuss/SKILL.md`](./skills/discuss/SKILL.md) - Clarify ambiguous tickets before executing
- [`skills/cc-to-linear/`](./skills/cc-to-linear/) - Post agent run timelines to Linear issues

**Install:**

```sh
# Agent + engineering rules
cp AGENTS.md ~/AGENTS.md
mkdir -p ~/.claude/agents && cp agents/ticket.md ~/.claude/agents/ticket.md

# Optional skills
mkdir -p ~/.claude/skills/discuss && cp skills/discuss/SKILL.md ~/.claude/skills/discuss/SKILL.md
mkdir -p ~/.claude/skills/cc-to-linear && cp -R skills/cc-to-linear/* ~/.claude/skills/cc-to-linear/
```

**Prerequisites:**
- [Claude Code](https://www.anthropic.com/claude-code)
- Project tracker MCP server (Jira, Linear, GitHub Issues, etc.)
- Figma MCP server (optional, for design files)
- `glab` or `gh` CLI for merge requests

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
cp -r agent-skills/cold-outreach-skills/skills/* .agents/skills/

# Just the ticket agent
cp agent-skills/AGENTS.md ~/AGENTS.md
cp agent-skills/agents/ticket.md ~/.claude/agents/ticket.md
```

## License

MIT
