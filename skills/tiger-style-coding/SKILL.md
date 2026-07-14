---
name: tiger-style-coding
description: Apply TigerBeetle's Tiger-Style rules to any codebase. Load when writing, reviewing, or refactoring code — or when instructing AI coding agents (Claude Code, Codex, subagents) on style. Enforces safety > performance > developer experience priority order, function-length caps, runtime assertions, bounded loops, and dependency discipline. Works across TypeScript, JavaScript, Python, Go, Rust, and any language with runtime assertions.
---

# Tiger-Style Coding

Source: [TigerBeetle's TIGER_STYLE.md](https://github.com/tigerbeetle/tigerbeetle/blob/main/docs/TIGER_STYLE.md) — Zig-focused. This skill translates the language-agnostic rules for broader use (TypeScript, JavaScript, Python, Go, Rust, and anywhere runtime assertions exist).

## When to load

- Writing new code where correctness matters more than velocity
- Reviewing agent-generated PRs / diffs
- Setting up rules for Claude Code, Codex, or delegated subagents
- Refactoring a file that's grown past 500 lines or has functions past 70 lines
- Answering "how should I structure X" style questions where multiple designs are viable

## The priority order

**Safety > Performance > Developer Experience.** In that order. Simplicity is the tool that lets you achieve all three at once — it's not a fourth axis, it's the multiplier that lets them coexist.

## Non-negotiable rules

### 1. Function length: 70-line hard cap

If a function doesn't fit on one screen, split it. When splitting:
- **Push `if`s up:** parent function owns all branching / control flow
- **Push `for`s down:** helper functions do pure computation, no branching
- Parent keeps state in local vars; helpers return values, don't mutate

Reference: [Push ifs up and fors down](https://matklad.github.io/2023/11/15/push-ifs-up-and-fors-down.html) — matklad

### 2. Assertions everywhere

Type systems are compile-time only. Runtime invariants catch drift the type system can't.

- **Two assertions per non-trivial function minimum:** pre-conditions on args, post-conditions on returns
- **Assert positive AND negative space:** what you expect to be true AND what you expect to NOT be true. Bugs live at the boundary.
- **Split compound:** `assert(a); assert(b);` beats `assert(a && b);` — the failure tells you which one broke
- **Assert relationships between compile-time constants** (e.g. `assert(BATCH_SIZE <= MAX_PAYLOAD_BYTES / RECORD_SIZE)`)
- **Assertions are not error handling.** Assertion failures = programmer errors → crash. User / operational errors → handled explicitly.

TypeScript helper pattern:
```ts
function assert(cond: unknown, msg?: string): asserts cond {
  if (!cond) throw new Error(`assertion failed${msg ? `: ${msg}` : ""}`);
}

function invariant<T>(value: T | null | undefined, msg: string): T {
  if (value == null) throw new Error(`invariant: ${msg}`);
  return value;
}
```

Python has `assert` built-in, but note it's stripped with `python -O`. For production invariants that must survive optimization, define your own:
```py
def invariant(cond: object, msg: str = "") -> None:
    if not cond:
        raise AssertionError(f"invariant failed: {msg}")
```

### 3. Bound every loop, queue, retry

Every loop, queue, retry, recursion depth, batch size — explicit upper bound.

- Scrapers: max pages per run, max records per page
- Retries: max attempts, max total time
- Queues: max depth, drop-or-crash on overflow
- Event loops that legitimately can't terminate: assert that fact explicitly

Unbounded `while (hasMore)` is where tail-latency, memory blowup, and cost spikes live.

### 4. Simpler return types win

Ordering (best to worst): `void > bool > T > T | null > Result<T, E> > Promise<Result<T, E>>`

Every layer of optionality is a branch every caller must handle. Prefer throwing at boundaries and returning plain `T` internally. Reserve `null` for genuine "not found" cases. Only use `Result`-style when the caller genuinely branches on error kind.

### 5. Explicit options at library call sites

Don't rely on library defaults. Defaults change in minor versions; explicit options are self-documenting and version-safe.

```ts
// Bad
await fetch(url);

// Good
await fetch(url, {
  method: "GET",
  headers: { "user-agent": UA },
  signal: AbortSignal.timeout(10_000),
  redirect: "follow",
});
```

### 6. Naming

- **Qualifiers last, descending significance:** `latency_ms_max` not `maxLatencyMs`. Groups related vars alphabetically in logs and grep.
- **Symmetric pairs:** `source`/`target` not `src`/`dest` — so `source_offset`/`target_offset` line up character-for-character in code
- **Prefix helper functions with parent name:** `read_sector` → `read_sector_callback` to show call history
- **Callbacks go last in parameter lists** — mirrors control flow (callbacks are invoked last)
- **Nouns over adjectives:** `replica.pipeline` beats `replica.preparing` — nouns compose better in derived identifiers (`config.pipeline_max`) and read cleanly in docs
- **Infuse names with meaning:** `gpa: Allocator` (general-purpose) beats `allocator: Allocator` — tells the reader whether `deinit` is needed
- **Match character counts** when related — makes code line up visually
- **Don't overload names.** If a term already has a specific meaning in one part of the system, don't reuse it for something else.

Language-specific idioms override where they conflict: use `camelCase` in TS/JS to match the ecosystem, `snake_case` in Python and Rust. Consistency with the ecosystem wins over the Zig source doc's `snake_case` preference.

### 7. Say why

- **Every commit message answers "why"**, not just "what". Code shows what; commits and comments explain why.
- **PR descriptions don't live in `git blame`.** Put the reasoning in the commit body, not just the PR.
- **Comments are prose:** capital letter, full stop, real sentences. Not marginal scribbles.
- **Test descriptions state the goal and methodology** at the top so a reader can skip or dive in.

### 8. Zero-dependency bias

Every dependency is:
- Supply-chain attack surface
- Maintenance tax (breaking changes, deprecations, security patches)
- Cold-start cost (especially on edge runtimes and serverless)

Ask "can I write 30 lines instead" before adding a dependency. Foundational infrastructure amplifies dep cost through everything downstream.

Reasonable exceptions: stdlib-equivalent tools (`zod`, `pino`, `pydantic`), test frameworks, build tooling. Everything else needs a real justification in the PR body.

### 9. Zero technical debt

Fix it while the iron's hot. The "clean it up later" pass:
- Usually doesn't happen
- Costs 10-100x more if it does
- Erodes momentum and confidence in the codebase

If you spot a design flaw mid-implementation, fix it before shipping. Don't ship known bugs and file tickets.

### 10. Batch, don't react

Whenever code interacts with external systems (webhooks, message queues, cron triggers):
- **Run at your own pace.** Don't context-switch per event.
- **Batch external events** into your own scheduled cycles.
- Cheaper (fewer transactions, better CPU cache), safer (bounded work per period), simpler (control flow stays yours).

### 11. Back-of-envelope before code

Before writing implementation:
- Four resources: network, disk, memory, CPU
- Two dimensions per resource: bandwidth, latency
- Sketch the numbers. Land within 90% of the global optimum.

Example (email digest system):
- N subscribers × M items per digest × K bytes per item = payload size
- Provider API rate limit ÷ send rate = time to complete
- If that's longer than the cron interval, you have a problem before you start

### 12. Split compound conditions

Compound booleans hide cases. Split into nested `if/else`:

```ts
// Bad
if (user.active && user.plan === "pro" && !user.suspended) { ... }

// Good
if (user.active) {
  if (user.plan === "pro") {
    if (!user.suspended) { ... }
    else { /* explicit: suspended pro user */ }
  }
}
```

For every `if`, ask whether the matching `else` needs handling or asserting.

### 13. State invariants positively

`if (index < length)` matches how humans read the constraint. Negations are harder to parse:

```ts
// Good
if (index < length) {
  // invariant holds
} else {
  // invariant doesn't hold
}

// Harder to reason about
if (index >= length) {
  // it's not true that the invariant holds
}
```

### 14. Layout

- Line length ≤ 100 columns (two copies fit side-by-side on a modern monitor)
- Consistent indentation — 4 spaces or 2, but pick one and stick to it
- Braces on all `if` unless single-line — guards against "goto fail;" bugs
- Order in files: top-down importance. `main` first. In classes / structs: fields → types → methods.

### 15. Cache invalidation / state hygiene

- **Don't duplicate variables or take aliases.** State gets out of sync.
- **Declare at smallest scope.** Minimize live variables to reduce misuse probability.
- **Calculate values close to their use.** Distance in time / space between check and use → bugs (POCPOU: place-of-check to place-of-use, cousin of TOCTOU).
- **Group resource allocation and cleanup with blank lines** so leaks are visually obvious:
  ```ts
  const conn = await pool.acquire();

  try {
    // use conn
  } finally {
    await conn.release();
  }
  ```

### 16. Off-by-one discipline

- `index`, `count`, `size` are conceptually different types even if they're all `number` / `int`
- `count = index + 1`, `size = count * unit`
- Include units in names: `latency_ms`, `payload_bytes`, `page_count`
- Be explicit about division rounding: `Math.floor`, `Math.ceil`, `//` (Python), or assert exactness

## What NOT to lift from the TigerBeetle source doc

- **Static memory allocation at startup:** irrelevant for GC'd runtimes (JS, Python, Go, Java)
- **Explicit `u32` sizing:** JS has one Number type; Python has arbitrary-precision ints
- **In-place struct init with out-pointers:** Zig-specific memory model
- **Rewriting shell scripts in Zig:** if your existing scripts work and are portable enough, don't churn for the sake of the rule
- **`snake_case` for TS/JS functions and variables:** ecosystem convention is `camelCase`; consistency with the surrounding ecosystem wins

## For AI coding agents

When delegating work to Claude Code, Codex, Cursor, or subagents, enforce these rules most aggressively on their output:

1. **70-line function cap** — agents love writing 200-line functions
2. **Assertions with rationale comments** — pre/postconditions, not just types
3. **Commit messages that answer "why"**
4. **No new dependency without justification in the PR body**
5. **Bounded loops and retries** — no naked `while (true)` or unbounded pagination
6. **Explicit options at every fetch / library call**
7. **Split compound conditions**

## Pitfalls

- **Don't cargo-cult `snake_case` into TS codebases** — ecosystem convention is `camelCase`; consistency wins
- **Don't add assertion overhead to hot paths without measuring** — but do keep them in non-hot code; the cost is usually negligible
- **Keep runtime assertions on in production.** They downgrade catastrophic correctness bugs (silent data corruption) into liveness bugs (crash + restart). Crashes are visible; corruption isn't.
- **Don't confuse assertions with error handling.** User input validation ≠ assertion. Assertion is "the caller violated the contract" — an internal bug, not an operational condition. Validate at the trust boundary, assert inside.
- **Don't skip Python's `-O` gotcha.** `python -O` strips `assert` statements. If you rely on assertions in production Python, use a custom `invariant()` function instead of the built-in `assert`.
