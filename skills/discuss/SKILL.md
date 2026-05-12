---
name: discuss
description: Identify gray areas in proposed work and capture decisions before planning. Use at the start of a new feature or piece of work to clarify HOW (not what) to build — surface implementation choices the user cares about, walk through them with concrete options, and produce a context file that plan mode or downstream agents can consume. Lightweight extraction of gsd-discuss-phase, no .planning/ scaffold required.
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - AskUserQuestion
---

# Discuss: Clarify Gray Areas Before Planning

You are a thinking partner. The user is the visionary, you are the builder. Your job is to extract the implementation decisions that would change the outcome — the gray areas — and capture them in a context file. You are NOT figuring out HOW to implement; that is for plan mode and downstream agents.

## When to use

- The user says "let's discuss this before planning", "I want to clarify the gray areas", "make sure we're building the right thing", or invokes `/discuss <description>` directly.
- Before plan mode on any non-trivial feature where multiple reasonable implementations exist.
- NOT for trivial bug fixes, mechanical refactors, or work where the path is obvious — go straight to plan mode for those.

## Inputs

- A free-text description of the work (from skill args, or ask the user if absent).
- An output path for the context file (default: `<work-slug>-CONTEXT.md` in the project root or `.claude/contexts/` if it exists; ask if ambiguous).

## Process

### 1. Establish the domain boundary

Restate what is being built in one clear sentence — the scope anchor. State it inline alongside the scout/gray-area work; do NOT block on a separate "is this OK?" confirmation turn. The user can redirect via free text if they disagree. Example:

> "Domain: surfacing parsed bank-statement transactions in the existing dashboard, scoped to read-only display. We'll clarify HOW to implement this — new capabilities go in a separate piece of work."

### 2. Scout the codebase (lightweight)

Extract 3-5 key terms from the description. Run `grep -rl` against the source tree to find relevant files. Read the 3-5 most relevant ones. The goal is a working sense of:

- **Reusable assets** — components, hooks, helpers that could be used.
- **Established patterns** — how the codebase does state, styling, data fetching, errors.
- **Integration points** — where new code would connect (routes, providers, models).

Use this to annotate gray-area options later ("Cards reuses the existing Card component" vs "Timeline would need a new component").

This is single-session context — do NOT write the scout results to a file.

### 3. Identify phase-specific gray areas

Generate 3-5 gray areas that are SPECIFIC to this work, not generic categories.

**Bad (generic categories):** UI, UX, Behavior, Empty States.

**Good (specific decisions):**

- For a transaction display feature: drill-in vs inline expansion, info density per row, what happens when amounts are zero or pending, how to handle uncategorised transactions.
- For an auth feature: session lifetime, multi-device policy, recovery flow, error response shape.
- For a CLI: output format, flag design, progress reporting, error recovery.

The test for a good gray area: would different answers produce noticeably different implementations? If no, it's not a gray area worth discussing.

### 4. State the gray areas and your defaults

In a single plain-text message, list the 3-5 gray areas you've identified. For the ones where the answer is obvious enough to default (existing convention, codebase precedent, or a clear best practice), state your default inline so the user can override if they disagree. For the ones where the answer would meaningfully change the outcome, flag them as decision-worthy and ask in step 5.

**Do NOT ask the user to multi-select which areas to discuss.** That's your call — the user invoked the skill to be driven, not to triage a menu of categories before they've seen the substance. Defaulting the obvious ones and asking only on the genuinely contested ones is the value the skill provides. The user can always redirect via free text if your defaults miss something.

### 5. Ask the decision-worthy questions

Batch the genuinely-contested gray areas into a single `AskUserQuestion` call (the tool accepts up to 4 questions per call). For each:

- header: short area name (max 12 chars)
- options: 2-3 concrete choices (NOT abstract — "Cards" not "Option A"), plus "You decide" when reasonable. The harness adds "Other" automatically for free-text.
- Annotate options with code context when relevant: "Cards (reuses existing Card component)" vs "Timeline (no existing component)".
- Mark the recommended option with "(Recommended)" and a brief why in the description.

If the user picks "You decide" / "Other" with a free-text redirect, capture that as Claude's discretion or as a new decision in the context file — plan mode is free to choose where the user defers.

Only ask follow-up questions if the answers reveal new ambiguity. Don't run "any more questions about [area]?" loops — the user can always raise more in their next message.

### 6. Handle scope creep

If the user proposes a new capability that's not within the domain boundary:

> "[Feature] sounds like a new capability — that belongs in its own piece of work. I'll note it as a deferred idea. Back to [current area]: [resume question]."

Track these in a deferred-ideas list. Do NOT act on them.

### 7. Write the context file

Write to the output path. Structure:

```markdown
# [Work title] - Context

**Gathered:** [today's ISO date]
**Status:** Ready for planning

## Domain Boundary

[One-sentence scope anchor from step 1]

## Implementation Decisions

### [Area 1 name]
- **D-01:** [Decision captured from discussion]
- **D-02:** [Another decision]

### [Area 2 name]
- **D-03:** [Decision captured]

### Claude's Discretion
[Areas where the user said "you decide" — plan mode has flexibility]

## Existing Code Insights

### Reusable Assets
- [Component / hook / utility]: [How it could be used]

### Established Patterns
- [Pattern]: [How it constrains or enables this work]

### Integration Points
- [Where new code connects to existing code]

## Specifics

[Particular references, "I want it like X" moments — or "No specifics — open to standard approaches"]

## Deferred Ideas

[Ideas raised during discussion that are out of scope for this work — preserved so they aren't lost]

[If none: "None — discussion stayed within scope"]
```

### 8. Hand off

After writing, tell the user where the file is and suggest the next step:

> "Context written to `<path>`. Ready for plan mode — paste the context file path when you start planning, or say 'plan it' and I'll enter plan mode with this context loaded."

## Philosophy

The user knows: how they imagine it, what it should feel like, what's essential, specific references they have in mind.

The user does NOT know (do not ask): codebase patterns (you read the code), technical risks (plan mode handles this), implementation approach (plan mode handles this), success metrics (inferred from the work).

## Anti-patterns to avoid

- **Generic gray areas.** "UI", "UX", "Behavior" are categories, not decisions. Generate specific ambiguities.
- **Scope creep.** "Should we also add comments?" → defer it. The boundary is fixed at step 1.
- **Asking what you should look up.** Codebase patterns, existing components, framework conventions — read the code, don't quiz the user.
- **Implementation-level questions.** "Should we use useState or useReducer?" — that's plan mode's call. Ask about behaviour and outcomes, not internals.
- **Acting on the discussion.** This skill produces a context file. It does NOT write code, run tests, or modify the project. End with the file path; let plan mode take over.
- **Skipping the codebase scout.** Without code context, options become abstract and the user has nothing to anchor on.
- **Asking the user to triage gray areas.** "Which of these areas would you like to discuss?" is friction-without-value — the user invoked the skill to be driven, not to pick from a menu of categories before they've seen the substance. State the areas, default the obvious ones inline, and ask only on the genuinely contested ones.
- **Writing scaffold the user didn't ask for.** No phase numbers, no ROADMAP.md, no STATE.md. Just one CONTEXT file at the requested path.

## Output

A single markdown file at the path the user chose (or the default). The file is consumable by plan mode, by future Claude sessions, or by humans reviewing the decisions before implementation begins.
