---
name: design-doc
description: Write a design doc for a proposed change, following the team's established format. Covers scoping, drafting, iteration, and publishing to Notion.
---

# Design Doc Skill

Write a design doc at `docs/proposals/<slug>.md` for a proposed change to the
codebase.

## Process

1. **Scope first.** Before writing the doc, understand what's changing and why.
   Explore the relevant code paths. If the change was motivated by a comparison
   (e.g. against an external API), capture the gap analysis in a separate
   scoping file (e.g. `<topic>-tasks.md` in the repo root) so the design doc
   itself stays focused.

2. **Draft the doc locally.** Write to `docs/proposals/<slug>.md`. Iterate with
   the user until they're happy with the content.

3. **Publish to Notion.** Create a page under the target engineering teamspace,
   under the appropriate category page. Use `notion-create-pages` with the
   teamspace or category page as parent. Read
   `notion://docs/enhanced-markdown-spec` before converting content. Use
   Notion `<table>` syntax for tables, not markdown pipes.

4. **Create tickets.** If the user asks, break the doc into tickets in the
   project sprint tracker. Use the schema from the tracker: Task name,
   Status, Priority, Effort level, Task type, Description.

## Doc structure

Follow this section order exactly. Every section is required unless marked
optional.

### Requirement

What problem does this solve, and for whom? State the gaps or needs clearly.
If something was considered and deliberately excluded, say so here with the
reasoning (e.g. "We're deliberately not implementing X because Y").

Keep it concise. A reader should understand the scope in under 30 seconds.

### How Things Work Right Now

Only describe the parts of the current system that the proposed changes will
touch. Do not rehash the full architecture. Each subsection should explain
one thing that matters for understanding a proposed change.

Use subsection headings (###) named after what the subsection establishes,
not after the component (e.g. "### Session tokens are cached in Redis" not
"### Session state storage").

Reference specific code: file paths, function names, line numbers where
helpful. But don't turn it into a code walkthrough.

### Proposed Changes

Number each change (### 1. Short title, ### 2. Short title, etc.).

For each change:
- Explain what it does and how it works mechanically.
- Reference the existing code it builds on or modifies.
- Include a mermaid sequence diagram when the change involves multiple
  services or a request flow that isn't obvious.
- State where the logic lives (which service, which layer) and why.

After the individual changes, include:

**Changes by endpoint** (table): every endpoint affected, its method, and
what changes (New, Modified, or No change with annotation note).

**Database changes** (table, optional): migration number and DDL statement
for each migration.

### Success Criteria

Bullet list of observable outcomes. Each criterion should be testable: "X
returns Y" or "Z is persisted in W", not vague goals.

Include a **Downstream changes** subsection listing other files or docs that
need updating as a consequence (client libraries, quickstart docs, etc.).

### Open Questions (optional)

Things the team should discuss before or during implementation. Frame each as
a concrete question, not a vague area. Include enough context that a reader
can form an opinion without re-reading the whole doc.

### Rollback Strategy

How to undo each change. Call out whether migrations are reversible, whether
env var gates are needed, and whether the changes are independent of each
other.

## Writing style

- British English spelling (colour, organisation, prioritise).
- No em-dashes. Use commas, full stops, colons, or parentheses.
- No "**Bold heading**: explanation" bullet format. Write natural sentences.
- Say "external users" not "non-staff callers" or "non-staff principals".
- Say "calling the underlying service" not "proxying".
- Don't leak implementation details into the Requirement section.
- Don't pad Success Criteria with items that aren't testable.
- Reference code paths with `file.go:lineNumber` or `file.py:functionName`,
  not full file paths (the reader is in the repo).
- When you call something documented, standard, recommended, or a known
  pattern ("the documented pattern", "vendor documentation states", "the
  recommended approach"), link to the real source doc. Never use "documented"
  or "standard" as a rhetorical intensifier without a citation. If you cannot
  find a source, state it as your own reasoning or flag it for verification,
  do not present an inference as documented fact.
- If the audience includes non-engineers (a PM, a designer, a founder), skip
  code paths entirely. Refer to a surface by its URL (linked, e.g.
  `[/info](https://example.com/info)`) or its user-facing name ("the
  Instructions modal"), not its template path (`external_info.html`) or its
  JS symbol (`showIntroModal`). Bites hardest in Requirement, How Things Work
  Right Now, and Success Criteria. The engineering rules above still apply to
  Open Questions and internal notes; those aren't the sections the PM reads.
- Don't wrap each Proposed Change in "why we chose X over Y" paragraphs. The
  Requirement section already owns "what we're deliberately not doing"; the
  Proposed Changes section owns what we ARE doing. If you find yourself
  writing "Why in this order:", "Why a range instead of a per-puzzle number:",
  or "Why not [obvious alternative]:" mid-change, cut them. State the change.
  Move on.
- The doc has no history. It is the only draft that exists to the reader.
  NEVER describe what an earlier version said or how the scope shifted. Every
  one of these is banned: "the earlier draft said...", "this now covers...",
  "the change grows from X into Y", "corrected section", "this is no longer
  copy-only", "previously we...", "so the doc now covers...". Describe the
  current proposal in the present tense as if it were always this way. A
  "corrected" or "new" section is just "a section"; a scope that grew is just
  the scope. If a sentence only makes sense to someone who saw a prior
  version, delete it. This applies to iterative edits too: when you revise the
  doc, rewrite the affected sentences to stand alone, don't layer "now/no
  longer" language on top of the old text.
- Never name internal teammates in the doc. Requirements, approvals, and
  conditions are stated impersonally ("a requirement", "still being
  confirmed", "as required"), not attributed ("the tech lead wants...", "the
  PM passed on..."). External user or tester names that are the literal source
  of feedback can stay if they add signal; internal people never do.
- Trim redundant middle clauses in bullets. If a three-sentence bullet's
  middle sentence restates the first, cut it. "There is no time limit.
  Nothing is counting down in the background. Take as long as you need." →
  "There is no time limit. Take as long as you need." The middle clause earns
  nothing.
- Trim FAQ / question lists to items that add distinct information. If two
  entries would be answered by pointing at the same sentence, one of them is
  redundant. Short list of load-bearing questions beats a padded one that
  repeats itself.
- Speculation about future features belongs in Open Questions, not Proposed
  Changes. If you find yourself writing "if we later want X, that'd live in
  Y" or "we deliberately do not add Z at this stage" in Proposed Changes,
  either delete it or rephrase as a concrete question in Open Questions.
  Proposed Changes only describes what this doc proposes building now.
- Don't reference other proposal files by filename (`other-doc.md`,
  `auth-api.md`, etc.). These docs publish to Notion, where a local filename
  is meaningless. Refer to other work by its concept or topic ("the
  integrity plan", "the access-control proposal"), not its file path. Code
  paths are fine; proposal-doc filenames are not.

## Notion publishing

- Read `notion://docs/enhanced-markdown-spec` via ReadMcpResourceTool before
  every publish. The spec changes; don't rely on memory.
- Use `<table>` elements for tables, not markdown pipe tables.
- Use ```` ```mermaid ```` for sequence diagrams.
- Do not escape underscores inside inline code. Notion italicises with `*`,
  not `_`, so underscores inside backticks render fine. Escaping them
  (e.g. `api\_endpoint`) leaves a literal backslash in the rendered output.
- Never use `replace_content` when updating existing Notion pages. It deletes
  inline comments and discussions. Use `update_content` with targeted
  find-and-replace operations instead.
- Specify category or parent page IDs when publishing to teamspaces.

## Reference docs

Good design doc proposals typically include:
- `docs/proposals/api-access-control.md` (mermaid diagrams, per-endpoint
  table, gateway enrichment approach, code references)
- `docs/proposals/operational-controls.md` (concise, focused "How Things
  Work Right Now", clear success criteria)
- `docs/proposals/session-management.md` (tight scoping, deliberate
  exclusions stated upfront, database migration table)
