---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases. Covers multi-round decision analysis - external-model question formation, persistent decision logs, devil's-advocate checks, and standing values instruments (values card sort, Moving Motivators).
source: https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md
---

**Canonical home:** `akash-joshi/agent-skills` repo (`skills/grilling/SKILL.md`). After any update via `skill_manage`, sync the public copy too: clone to `/tmp`, apply the same patch, commit and push.

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled — the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Each question should be formatted like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each round the user answers reshapes the tree — settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it — don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report — ask the rest of the frontier now. The _decisions_ are the user's — put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.

**Keep each question compact, especially on platforms with message-length limits (Discord, Telegram).**

```
Q — <opinionated claim in one line>
Grounding: <up to 5 short bullets, one clause each, evidence from files>
<bare question, one line>?
```

Hard rules for EVERY grilling question:
- Lead with the claim. No preamble ("Fair.", "Right.", "Locked.", "Reread.").
- No recap of prior rounds — the decision log is the recap.
- No closing softener ("Confirm or push back?", "Correct or wrong?", "Ship as this?" — pick zero or one, ideally none, the bare `?` on the question is enough).
- Cap grounding at 5 bullets. If you need more, dispatch to Opus per §1 for a sharper question — the sprawl is a signal the question isn't tight enough yet.
- Menu shape (A vs B, "which of these") is BANNED. Section 12 requires an opinionated claim, not a comparison table. If you're about to type "Option A does X, Option B does Y" — stop, pick one, present as the claim.

**Anti-pattern warning: over-explaining is the default failure mode.** The "opinionated answer" rule (§12) fights the compact-format rule and the session drifts toward long menus of reasoning. When they conflict, compact wins — the opinion still lives inside the one-line claim. Long explanations are laundered menus. If a question is over ~10 lines, it's wrong-shaped, not thorough.

Signal you've violated this: user responds with "what's the fucking question?", "i-have-adhd?", "such a bad question", or asks you to reload the skill. When any of those fire, don't apologise in prose — re-ask the SAME question in the correct format immediately.

**Never anchor a question on prior-session or file-based shorthand without checking it's still live.** If a question depends on a framing that came from an old interview review, a prep doc, or a decision log the user hasn't referenced in the current conversation (e.g. a "three-lane career filter" invented in a past session), state the framing plainly and explicitly flag its source before asking the user to react to it. Don't assume shared context persists just because it lives in a file. Ask "is this still how you think about X" as its own opening move, not baked silently into a bigger question.

**Recognise when the user is asking for the verdict, not another round.** After a devil's-advocate pass (per section 3 below) has run once and the user pushes back with something like "isn't this what we're trying to resolve" or otherwise signals impatience with further questioning, that is the cue to actually deliver the recommendation — not to layer in yet another clarifying question. One devil's-advocate round per convergence is the ceiling; a second hedge after the user has explicitly asked for the call reads as avoidance, not rigour.




## Load only the relevant detail

The full instructions are preserved verbatim in these references. Before acting, load the files matching the current task and relevant pitfalls. Do not load every file for unrelated work. If a workflow spans adjacent files, read both. Relative links retain their original skill-root meaning.

- `references/cost-detail-01.md`: Extended practice: multi-round, high-stakes decisions; 1. Route question formation to a different/stronger model when your own questions feel weak; 2. Keep a running decision log, appended incrementally, not written once at the end
- `references/cost-detail-02.md`: 3. When the scorecard converges suspiciously cleanly, run a devil's-advocate pass before presenting a verdict; 4. Personal-values instruments (values card sort, Moving Motivators) are a standing lens, not a one-off question; 4b. Once you've started routing question formation to Opus, don't revert to asking flat/direct questions yourself mid-session; 5. Before asking a "new axis" question, verify it's actually new — not a restatement of an already-resolved comparison; 6. A genuinely separate decision thread gets its own log doc — don't auto-append to whatever's open; 7. Before presenting a "new axis" as distinct from the main A-vs-B comparison, check whether it actually is one; 8. Decision-log scoping — one log per decision, not one log per session; 9. Verify stated preferences and framings are CURRENT, not stale
- `references/cost-detail-03.md`: 8a. Don't dispatch a "next question" without checking your own prompt for injected bias; 8b. Don't dump prior-session shorthand on the user without checking they have the context; 11. A well-defined task can still hide an unresolved decision — don't let file-writing substitute for grilling; 12a. Don't use the literal phrase "Recommended answer:" — it signals the direct-question antipattern; 12b. When grilling content structure (article sections, doc beats, deck slides), show the actual beats, not the meta-framing; 12. Every grilling question ships with a recommended, opinionated answer — never a bare menu; 12a. Sequence foundational fact-gathering BEFORE interpretive claims
- `references/cost-detail-04.md`: 12b. Recommended answers are for interpretive questions, not bare factual ones; 13. Do not close or mark-done the underlying task until the user has reviewed the actual deliverable content — not just a sub-decision surfaced during grilling; 14. When the user references "the recent call" or a conversation not on file, check Voicenotes before trusting the written decision log; 9. Don't close/finalize a task on process resolution alone — the actual content still has to be walked through; 10. When the user says "that's what we grill for, don't just ask directly" — the fix is ONE opinionated question, not a menu; 14b. Check local source-of-truth files before reaching for external APIs; 15. Never launder your own paraphrase through an "independent" external model dispatch
- `references/cost-detail-05.md`: 17. Don't narrate the user's mind, and don't ask the surface question you already suspect the answer to; 15b. Direct introspection questions ("what changed?") don't work — ground the grill in evidence, not self-analysis; 17. Direct introspection questions ("what changed?", "why do you feel X?") are anti-grills — reframe as concrete claims to react to; 18. Don't invent structure in the user's own data — check what the source actually claims; 18b. Don't fabricate grounding — if you cite source files as evidence, you must have actually read them
- `references/cost-detail-06.md`: 19. Verify shared session facts before building a reading on top of them; 20. Don't relay a delegated model's verdict without applying its own caveats; 21. When the user declares themselves "locked in" on an irreversible decision late at night or under fatigue, install a daylight-test frame — don't accept the declaration at face value; 24b. When the user signals resolution-readiness, drop the grilling FORMAT — verdict shape, not framed-question shape; 27. When the user structurally removes a path to closing a follow-up, retire the follow-up — don't re-surface it dressed differently; 25. State the recommendation, then stop — no trailing "Applying?" / "Confirm?" / "Or push back?"
- `references/cost-detail-07.md`: 26. In multi-question grills, grill ONE question at a time — don't dump N cut proposals in one message; 22. ADHD-friendly formatting — apply the 10 rules from `ayghri/i-have-adhd` to every grilling turn; 23a. Cross-session recovery — when picking up a decision thread with no log, reconstruct BEFORE continuing; 23. Write to the decision log same-turn, not at session end — and confirm the write in the message; 24. Don't passively accept a subtraction — stress-test the replacement before closing the round
- `references/cost-detail-08.md`: 16. Don't mark an open follow-up "resolved" when the user gives you rich new signal — carry it forward for grilling
