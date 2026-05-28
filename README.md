# claude-code-ticket-agent

A custom Claude Code agent that turns a Jira ticket ID into a reviewable merge request, one TDD commit at a time.

You give it a ticket ID:

```
/ticket ABC-123
```

The agent reads the Jira ticket, follows linked Figma designs and Confluence pages, explores the codebase, creates a worktree, writes a TDD-driven plan, executes it commit by commit, pushes the branch, and opens an MR. Your only job is to review the final diff.

Full writeup: [Hand Claude a Jira ID, Get Back a Merge Request](https://thewriting.dev)

## Install

```sh
# 1. Drop AGENTS.md at the root of your repo (or at ~/AGENTS.md for global rules)
cp AGENTS.md ~/AGENTS.md

# 2. Drop the agent definition into Claude Code's agents folder
mkdir -p ~/.claude/agents
cp agents/ticket.md ~/.claude/agents/ticket.md

# 3. (Optional) Drop the discuss skill for tickets that aren't fully scoped
mkdir -p ~/.claude/skills/discuss
cp skills/discuss/SKILL.md ~/.claude/skills/discuss/SKILL.md

# 4. (Optional) Drop the cc-to-linear skill to post agent run timelines to Linear
mkdir -p ~/.claude/skills/cc-to-linear
cp -R skills/cc-to-linear/* ~/.claude/skills/cc-to-linear/
```

Then in any Claude Code session inside a git repo:

```
/ticket ABC-123
```

For tickets that aren't fully scoped, talk through the implementation decisions first:

```
/discuss ABC-123 - short description of what needs deciding
```

To post the agent's tool-by-tool timeline as a comment on a Linear issue once the run finishes:

```
/cc-to-linear LIN-123
```

## Prerequisites

- [Claude Code](https://www.anthropic.com/claude-code)
- Atlassian MCP server configured in Claude Code (for reading Jira and Confluence)
- Figma MCP server configured in Claude Code (for reading design files)
- A CLI tool to open merge requests: [`glab`](https://gitlab.com/gitlab-org/cli) for GitLab or [`gh`](https://cli.github.com/) for GitHub
- `git worktree` (built into git)

## Files

- [`AGENTS.md`](./AGENTS.md) - Engineering rules the agent follows. TDD enforcement, commit format, plan structure, code-style guidance. This is the source of truth for how the agent works.
- [`agents/ticket.md`](./agents/ticket.md) - The agent definition. Four-phase workflow: gather context, set up worktree and plan, execute with TDD, push and open MR.
- [`skills/discuss/SKILL.md`](./skills/discuss/SKILL.md) - Optional companion skill. Run `/discuss` before `/ticket` to clarify gray-area implementation decisions and write them to a context file the ticket agent can consume.
- [`skills/cc-to-linear/`](./skills/cc-to-linear/) - Optional companion skill. After the agent finishes a ticket, run `/cc-to-linear LIN-123` to post a structured timeline of the run (prompt, tools used, files touched, errors handled, final message) as a comment on the Linear issue. Gives reviewers an auditable trail alongside the diff. Requires the [Linear MCP server](https://linear.app/docs/mcp).

## How it works

The whole thing is two markdown files.

**`AGENTS.md`** is the agent's engineering handbook. Every rule you'd enforce in a code review goes here. The two bits that matter most are the **plan-mode instructions** (commit groups with red/green phases, status indicators, verification commands) and the **TDD enforcement** ("NEVER write implementation code before writing a failing test"). Without these, agents skip tests or dump unreviewable walls of code.

**`agents/ticket.md`** is the agent definition. A custom agent in Claude Code is a markdown file in `~/.claude/agents/` that describes a workflow. When invoked, the agent gets all the tools of a normal session but follows whatever you've written.

The ticket agent runs in four phases:

1. **Gather context.** Reads the ticket via Atlassian MCP, fetches design screenshots from Figma links, pulls Confluence content, and explores the codebase to understand existing patterns.
2. **Set up worktree and plan.** Creates a worktree, switches into it, and writes a structured `plan.md` following the format from `AGENTS.md`.
3. **Execute with TDD.** Works through the plan one commit at a time. Failing tests first, minimum implementation to pass them, commit with a `[TICKET-ID]` prefix, mark it ✅ in the plan.
4. **Push and open MR.** Runs the full test suite, pushes the branch, opens an MR with a structured description.

## When this doesn't work

- Ambiguous tickets. If you're still exploring approaches or having design conversations, don't hand it to the agent. Ambiguity makes it guess, and its guesses add scope you didn't ask for.
- Large cross-cutting refactors that touch dozens of files. These need judgment calls about what to touch and what to leave alone, which are hard to encode in rules.

Sweet spot: CRUD features, UI changes with clear designs, contained bug fixes.

## Make it yours

Both files are tuned to a specific workflow. Fork, rip out what doesn't fit, and add rules for whatever your team cares about. The agent is only as good as your `AGENTS.md`. Be highly prescriptive.

## License

MIT
