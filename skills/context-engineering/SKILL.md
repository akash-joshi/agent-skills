---
name: context-engineering
description: The new rules of context engineering for Claude 5 generation models. Anthropic removed ~80% of Claude Code's system prompt with no eval loss because judgement replaces rules. Load when writing or auditing system prompts, CLAUDE.md, AGENTS.md, or skills for a modern coding agent; when a prompt or skill feels bloated; when the agent seems to be waffling instead of acting; when you're tempted to add "ALWAYS do X" / "NEVER do Y" rules; or when consolidating scattered instructions into a coherent context tree.
---

# Context Engineering for Claude 5 Generation Models

Source: [Thariq (Anthropic, Claude Code) - Jul 2026](https://x.com/trq212/status/2080710971228918066) · Full blog: [The new rules of context engineering for Claude 5 generation models](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models)

Anthropic removed **~80% of Claude Code's system prompt** for the Claude 5 generation (Opus 5, Fable 5) and saw **no measurable loss on coding evals**. The old rules were guardrails for older, weaker models. Newer models have judgement and don't need them. This skill encodes what was learned so you can apply the same discipline to your own system prompts, CLAUDE.md / AGENTS.md files, and skills.

## Core diagnosis: over-constraining is the failure mode

The team found transcripts where a single request contained conflicting instructions:

- System prompt: "leave documentation as appropriate"
- A skill: "DO NOT add comments"
- The user's own request: something different again

The model can resolve the conflict, but it wastes cycles thinking about the meta-problem instead of the actual task. The cost of a rule is not only the tokens it consumes - it's the attention it steals from the work.

**Rule of thumb.** Before writing or keeping any instruction, ask: *"Could the model figure this out from context and judgement?"* If yes, cut it. If no (product context, personal preference, non-obvious gotcha), keep it.

## The seven shifts

### 1. Rules → Judgement

- **Then:** "In code: default to writing no comments. Never write multi-paragraph docstrings..."
- **Now:** "Write code that reads like the surrounding code: match its comment density, naming, and idiom."

Rules that are true 80% of the time become wrong in the 20%. Newer models can read the surrounding context and pick the right behaviour. Give them the goal, not the recipe.

### 2. Examples → Interface design

- **Then:** three worked examples showing how to use a tool.
- **Now:** a tool whose parameters make correct usage obvious.

The Todo tool uses a status enum (`pending` / `in_progress` / `completed`) - the type tells the model what to write. Instructions like "only one in_progress at a time" define behaviour without an example needed. For skills, this means: stop over-teaching with examples; make the workflow steps expressive enough that the model can generalise.

### 3. Everything upfront → Progressive disclosure

Don't load context that isn't needed. Applies to:

- **Skills:** split long skills into a lean `SKILL.md` + `references/` subfiles the model loads on demand.
- **Tools:** deferred loading (the ToolSearch pattern - list tools by capability, load the schema when picked).
- **CLAUDE.md / AGENTS.md:** a tree of files, not one giant blob. The root file points at the topic-specific file.

**Common myth called out in the post:** "make CLAUDE.md a central repository for every known practice." Wrong. It should be a router, not an encyclopedia.

### 4. Repetition → Single source of truth for tool descriptions

Old models needed repeated instructions - once in the system prompt, once in the tool description. New models don't. Put tool instructions in the tool description only. If a system prompt duplicates something a tool description already says, cut the system prompt version.

### 5. Manual memory → Auto-memory

Users used to write to `CLAUDE.md` manually after every session. Now the model auto-saves memories that are actually relevant to future turns. Don't over-curate memory manually; trust the model to record what matters and prune what doesn't.

### 6. Simple specs → Rich references

Beyond markdown plans, the model can consume:

- HTML artifacts (design mockups as HTML beat screenshots or descriptions)
- Test suites as executable specs
- Reference implementations in other codebases
- **Rubrics** - encoded taste, e.g. "what does a good API look like"; especially useful when a verifier agent reviews another agent's output in a dynamic workflow.

If you can point the model at a rich reference, that beats writing prose about the reference.

### 7. Skills as encyclopedias → Skills as opinionated guides

Skills work best when they encode *particular opinions, knowledge, or best practices particular to you, your team, or your product*. Not general advice the model already knows. If a skill's contents could have been written by someone who has never seen your codebase, it's not a skill - it's a Wikipedia article.

## Applying it: an audit checklist

Point this checklist at any system prompt, CLAUDE.md, AGENTS.md, or skill you own.

For each rule / section / instruction, ask:

1. **Is it opinionated, product-specific, or a real gotcha?** Generic web search or terminal usage doesn't need to be in your context. Cut.
2. **Are examples doing work that expressive step names could do?** If steps are named clearly, cut half the examples.
3. **Is it one giant SKILL.md that could be a lean index + `references/` subfiles?** Split it.
4. **Are there guardrails that were true for older models but redundant for a Claude 5 generation model?** Cut them.
5. **Does it repeat something the model would infer from context or from another skill?** Delete the duplicate.

### Anti-patterns to cut

- "ALWAYS do X" / "NEVER do Y" when the model can read context and decide
- Long example sections that could be replaced by named steps
- Duplicate constraints stated in two or more places
- Meta-instructions about how to use the skill (should live in the framework, not each skill)
- "Rules" that are actually 80% heuristics

### What to keep

- Real gotchas ("Tailscale is at `/home/linuxbrew/.linuxbrew/bin/`, not in `PATH`")
- Non-obvious workflows (which subsystem does what)
- Files or references pointing to fuller context
- Rubrics (e.g. an anti-patterns section in a writing-style skill - that IS a rubric, keep it)
- User preferences that override defaults

## When editing existing docs

1. **Delete first, add second.** The instinct on hitting a failure mode is to write a comprehensive rule. Comprehensive rules bloat base context - which makes the model waffle across the whole session, not just the one it was written for.
2. **If a section reads like a lecture** ("here's how to think about X"), it's probably slop - cut it.
3. **If a section is a checklist of concrete preferences or gotchas**, keep it.
4. **Prefer one link to a fuller reference** over ten lines of inline detail.

## Meta-lesson on writing rules

When you encounter a failure mode, the temptation is to write a paragraph explaining it into the top-level system prompt so the model "learns" not to do it again. That's usually the wrong response for three reasons:

1. **Base context bloat.** Everything in the top-level context runs on every turn, even turns that have nothing to do with the failure mode. You're paying attention tokens forever to prevent one class of bug.
2. **Lost-in-the-middle.** The longer the base context, the more likely important instructions get under-weighted (Liu et al., Stanford 2023). Ironically, more rules make the model *worse* at following rules.
3. **Premature termination.** Models can give up or provide uncertain answers long before exhausting the context window (arxiv 2606.29718, Xia et al., Jun 2026). Bloated preambles make this worse.

**Better shape:**

- Short trigger in the top-level file (one line: when this comes up, load the deeper doc).
- Full detail in a linked reference document.
- Structural enforcement in a skill or script where the failure actually happens (verification step, pre-commit hook, output check).

Base context grows by tens of characters, not thousands.
