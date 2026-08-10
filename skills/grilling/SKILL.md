---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases. Covers multi-round decision analysis - external-model question formation, persistent decision logs, devil's-advocate checks, and standing values instruments (values card sort, Moving Motivators).
source: https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md
---

**Canonical home:** this skill is mirrored to `~/dotfiles/claude/skills/productivity/grilling/` (as of 2026-07-25). After any update via `skill_manage`, sync both copies (`cp ~/.hermes/skills/productivity/grilling/SKILL.md ~/dotfiles/claude/skills/productivity/grilling/SKILL.md`), then `cd ~/dotfiles && git add claude/skills/productivity/grilling/ && git commit -m "grilling: <change>" && git pull --rebase && git push`. `skill_manage` only edits the Hermes copy — the dotfiles copy will drift if not manually mirrored. Hermes copy is source of truth if the two ever disagree.

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

**Every grilling question is compact by default. Not "when user flags" — always.** ADHD-friendly principles (github.com/ayghri/i-have-adhd) are the DEFAULT format for grilling questions, especially on platforms with message-length limits (Discord, Telegram). Required shape:

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

## Extended practice: multi-round, high-stakes decisions

### 1. Route question formation to a different/stronger model when your own questions feel weak

If the primary session's questions start feeling generic or repetitive, hand off *question formation only* (not the whole task) to a different model via `claude -p --model <id>` (see `coding-agents` skill for the CLI pattern). Write a rich context prompt to a temp file covering: the two options in full, everything already resolved (so it doesn't re-ask settled ground), and the specific tension to probe next. Require a strict 3-part output:
1. The single next question (one or two sentences).
2. A recommended answer to it (opinionated, reasoned from the supplied context).
3. Any pure fact (not a judgment call) that should be confirmed directly rather than inferred.

This keeps the "recommended answer" honestly separated from "what the user actually said" — critical for the logging discipline below. Long adversarial/synthesis prompts (see devil's-advocate section) can take well over a minute; dispatch via `terminal(background=true)` and poll rather than a foreground call with a short timeout, the same pattern documented in `coding-agents` for Fable design passes.

**Anti-bias discipline in the prompt itself (learned the hard way 21 Jul 2026, escalated to "So you introduced bias into the prompt?" and "wipe your own ass"):** the external model's answer is only as good as the neutrality of the prompt. Bias sneaks in via four specific vectors, all seen in a single session while grilling on consulting offer productization:

1. **Asserting the disputed conclusion as background fact.** "That's day-rate consulting wearing a fixed-price costume" was written into the prompt as context, when it was actually the exact hypothesis under scrutiny. If the framing is what the user is trying to resolve, do NOT present it as established ground. State it as "one possible reading — argue against it before accepting it."

2. **Cherry-picking supporting examples.** Naming three inspiration companies that ARE fixed-price products, without also naming the ones that AREN'T, primes the model to see confirmation everywhere. If citing examples, cite the counter-examples in the same paragraph — or leave examples out and let the model surface its own.

3. **Loaded "critical definition" sections.** Writing "CRITICAL DEFINITION — get this right" for a term whose definition IS the disputed question tells the model which answer counts as "getting it right." The word "critical" is the tell.

4. **Token disclaimers that can't hold their weight.** Sprinkling "be honest if it doesn't fit" or "there's a real chance the direction is wrong" into a prompt that otherwise loads every other paragraph toward one answer does not neutralize the bias — the model reads the surrounding structure, not the polite hedge. If you want a genuinely open answer, restructure the prompt so the "no" answer is as easy to reach as the "yes" answer.

**Concrete rewrite pattern that survived scrutiny:** open with the user's actual words verbatim, not a paraphrase. Note explicitly if a prior AI pass introduced framing that may itself be wrong ("I previously framed X as Y — this may be wrong, do not defer to it"). Argue the strongest case against the hypothesis in the prompt itself before asking for a recommendation. Include competing framings ("this could be a real distinct direction OR a distinction without a difference — both readings are on the table, evaluate them"). Instruct the model explicitly to challenge the framing, not just the details.

**Escalation signal from the user:** when the user says any variant of "you introduced bias" or "the prompt was loaded" — do not defend the prior prompt or argue about whether it was actually neutral. Rewrite it yourself, dispatch again with a fresh instance (not the same session-continued instance, which will inherit anchoring), and present the new result. The user's job is not to teach you prompt neutrality; it's to get an honest answer to the underlying question. "How should I fix it?" or "which option do you prefer?" as a response is itself a failure — same act-first-ask-after rule that governs the rest of the session applies to fixing your own screwups.

**Escalate fast, don't keep manually rephrasing.** If the user says "I don't know" or shows confusion ("I don't get it", "explain more") after your FIRST attempt to clarify a question, that is the trigger — don't try a second or third manual rephrase in plain English. Route question formation to the external model immediately. Validated failure (consulting offer-doc grilling, 2026-07-21): three consecutive plain-English rephrase attempts on the same rate-vs-pricing-format question all still failed to land, and the user had to explicitly instruct "consult opus... that's really dumb" before the dispatch actually happened. The tell you're in this failure mode: you're restating the same underlying question with simpler words rather than forming a genuinely sharper, more concrete question — simplifying vocabulary doesn't fix a poorly-shaped question.

**Unbiased dispatch variant — give the model direct file access, not your own summary.** When the user explicitly wants an independent read (e.g. says "don't give it bias" or similar), do NOT write the dispatch prompt around your own curated/summarized context — that summary already carries your framing, and any error in it propagates straight through. Instead: list the actual file paths, grant `--allowedTools "Read,Grep,Glob"` plus `--add-dir` for the directory, and instruct the model to read the files itself and quote verbatim lines to support its answer. Validated (2026-07-21): a first dispatch fed the model a curated summary of pricing docs and got a plausible but shallow answer; a second dispatch given direct read access to the same files caught something the summary had missed entirely — that the user's stated confusion ("is this a fixed-price product?") was already resolved by an exact line in his own plan ("one clear offer... with day-rate AND packaged sprint options"), which the curated summary hadn't foregrounded. Direct file access produces a genuinely independent check, not just a re-run of the same framing in a different voice.

**Never relay the external model's question verbatim — translate and ground-check it first.** The delegated model writes for a reader who has the full context file open; the user does not. Two failure modes to catch before sending:

1. **Invented hypotheticals the model presents as live risk.** Opus's question in a real session (offer-doc pricing grill, 21 Jul 2026) opened with "when a prospect reads £750/day and later learns Prefrontal pays £500" — a scenario the model invented to motivate the question, not something Akash had raised or that was actually likely. He immediately pushed back: "How would they find out?" Before relaying, ask: is this framing device something the user actually needs to worry about, or is it scaffolding the model built to justify asking? If it's scaffolding, strip it and ask the real underlying question directly.
2. **Compressed business jargon that reads as abstract even though the underlying question is simple.** The same session's question ("does the number have to survive them learning X — i.e. is £750 the firm public number with the ladder kept verbal, or should the doc itself signal rate scales with commitment") took three follow-up rounds and an explicit "I still have no idea what you're trying to say mate" / "how would I upgrade you to Opus" before landing. The actual question underneath was simple: is "the offer" a day-rate pitch, or a fixed-price product, or does one document need to cover both? Rewrite the delegated model's question into one plain concrete sentence using the user's own vocabulary before sending it. If you can't compress it to one plain sentence, you don't understand it well enough to relay it — go back and read the model's reasoning again, don't just copy-paste the output.

**Signal that you've failed this check:** the user says "I don't get it," asks to switch models, or has to ask "what do you mean by X" more than once on the same question. That is not a request for a fancier model — the fix is a plainer question from the model you're already running, addressing the actual concrete decision (which document/format/number) rather than an abstracted version of it.

### 2. Keep a running decision log, appended incrementally, not written once at the end

For any grilling session likely to span multiple turns (or need to pause pending an external event — e.g. waiting for a written offer), maintain a separate log file with one entry per confirmed decision:

```
## Decision N — <short title>
**Status:** Confirmed / In progress / Paused

**Question asked:** ...
**Recommended answer (model's):** ...
**User's actual answer:** ...
**What this changes:** ...
```

Append to this file after every resolved round, not just at session end — the log is the artefact that lets the session survive an interruption (new chat, next day, waiting on an offer). Sync it to wherever the user actually works from (ask, don't assume — see the folder-choice pitfall below).

**Pitfall — don't launder model speculation into logged fact.** The recommended-answer field is a hypothesis, not the user's position, until they've actually confirmed or corrected it. It's easy to write "Confirmed: X" in a log entry when what actually happened is the *model* speculated X and the user never addressed it. If the user doesn't directly respond to a specific claim in the recommended answer, mark that specific claim as still-open in the log, not resolved. Getting this wrong erodes trust fast — catching your own mislabelled entry after the fact ("that's kinda bs") is a worse experience for the user than just being careful the first time.

### 3. When the scorecard converges suspiciously cleanly, run a devil's-advocate pass before presenting a verdict

If 5+ consecutive rounds all resolve toward the same option, that convergence is itself a signal worth distrusting, not a result to report at face value — genuinely adversarial multi-round processes rarely resolve this one-sidedly. Before declaring a winner:

- Dispatch a fresh model instance (via the same `claude -p --model` routing) instructed explicitly to argue the *hardest possible case* for the option that's been losing, and to name any structural bias in how the prior rounds were framed (common patterns: speculation stacked as if it were realized value across multiple rounds, asymmetric scrutiny — one option audited forensically while the other is taken at face value, a tie-breaking value quietly defined away once it points the "wrong" direction, comparing a certain/signed thing against a hopeful/unconfirmed thing at best-case).
- Treat the output as a real update to the decision log, not a footnote — retract or downgrade any earlier entries it successfully challenges, and update the running scorecard.
- It's fine, and expected, for the devil's-advocate pass to conclude the original direction still holds on some axes while genuinely overturning others. Don't force it toward a clean flip just to seem balanced, and don't dismiss it just to protect the smooth convergence.

See `templates/devils-advocate-prompt.md` for the reusable prompt structure.

### 4. Personal-values instruments (values card sort, Moving Motivators) are a standing lens, not a one-off question

If the user introduces a values exercise (a card sort, Management 3.0's Moving Motivators, or similar) partway through a grilling session, don't treat it as answered-and-closed after one round. Carry it forward explicitly:
- Re-apply it whenever a new fact could plausibly shift which value/motivator is actually being served or threatened by each option.
- If multiple rounds of the same instrument exist (e.g. a values sort done weeks apart), don't assume the later round is either "the real one" or "noise from temporary stress" — that's a judgment call for the user to make, not something to assert on their behalf. Ask directly which reading they trust, and flag explicitly if a "stress-adaptation" theory is your own inference rather than something they've confirmed.
- Watch for anchoring: if a values exercise is done while the user is actively comparing two concrete numbers (e.g. two salary figures), a value like "Money" jumping in the rankings may reflect the immediate comparison rather than a durable life value. Ask, don't assume.
- **Before running either instrument from scratch, check whether results already exist** (e.g. `~/.hermes/memory/values-card-sort.md` for Akash — may have multiple dated rounds). Reuse existing rounds as the lens; only re-run if the user asks for a fresh pass or enough time/context has shifted that a stale round is no longer trustworthy.
- To actually run either instrument (full motivator/value lists, chat-adapted method for when there are no physical cards, source/licensing notes), load the **`values-and-motivators-instruments`** skill. It covers Moving Motivators (CHAMPFROGS, 10 workplace motivators — faster, good for job/role decisions) and the Personal Values Card Sort (Miller et al. 2001, 83 whole-of-life values — slower, more granular, good when Moving Motivators feels too coarse or the decision isn't work-specific).

### 4b. Once you've started routing question formation to Opus, don't revert to asking flat/direct questions yourself mid-session

Real failure (consulting offer-v1 grilling, 2026-07-21): after dispatching one question to Opus successfully, the session reverted to asking Akash a flat open-ended multiple-choice question directly ("is it stage, or buyer psychology, or deliverable type — which parts?") with no recommended answer. Akash's response: *"bro that's what we try to figure out based on grilling? You're just asking things directly here."* He wants every substantive grilling question in a routed session to carry an opinionated recommended answer he can react to (confirm/correct) — an open menu with no stance is not grilling, it's a form. Once §1's dispatch pattern is established for a session, stay in it for every non-trivial question, not just the first one that "feels weak."

Also relevant from the same session: closing/declaring a task "done" in Taskwarrior (or any tracker) is a distinct failure from asking a weak question. A deliverable that requires the user's actual judgment call (pricing anchor, ICP definition, positioning) should never be marked complete until the user has explicitly confirmed the content — drafting it and shipping a first pass is fine and expected, but auto-closing the task the moment a draft exists reads as skipping the human's decision entirely. Akash: *"Bro what? Actually confirm it with me? Let's have a discussion?"* Reopen the task, don't just apologize verbally.

### 5. Before asking a "new axis" question, verify it's actually new — not a restatement of an already-resolved comparison

A recurring failure mode in multi-round sessions: after several rounds converge on one option, the *next* question you draft — even when framed as exploring a fresh angle (e.g. "future interview optionality," "prestige," "reputation") — can silently collapse back into re-litigating the same underlying comparison already resolved in the decision log, just with different surface wording. This happened twice in a row in a real session (Volaris vs Bluefish, 2026-07-20): a "prestige in a year" question and a follow-up "6-months-from-now scenario" question were both, in substance, the same Bluefish-vs-Volaris comparison already covered — the user had to call it out twice before it was caught.

**Before asking any "new axis" question, check it against the decision log:** does answering this question produce information not already captured by an existing Decision N entry? If the honest answer is "no, this just re-asks Decision 3/6/8 in new words," don't ask it — go back to the user and name the actual gap directly, or route question formation to a fresh model instance (per section 1) with an explicit list of what's already resolved and an instruction not to restate it. A model instance anchored on the prior rounds of the same conversation is the most common source of this failure — a fresh instance with a curated "already resolved, do not repeat" list is more reliable at staying on the genuinely new axis than continuing to ask from within the same anchored context.

### 6. A genuinely separate decision thread gets its own log doc — don't auto-append to whatever's open

Grilling sessions sometimes spin off a related but structurally distinct question mid-session (e.g. "should I keep interviewing elsewhere" or "how do I weigh prestige generally" surfacing while grilling a specific two-offer comparison). If the new thread is actually a different question being stress-tested — not just a new axis of the same comparison — it needs its own decision-log doc, not an append to the comparison-specific log already open. Mixing them makes both docs harder to resume correctly later (the offer-comparison log stays cleanly paused-and-resumable; the adjacent strategic question doesn't get buried inside it). If it's ambiguous which is happening, ask the user directly rather than guessing — auto-appending the wrong thread into an existing log is a real cost (has to be reverted and re-split), not a harmless default.

### 7. Before presenting a "new axis" as distinct from the main A-vs-B comparison, check whether it actually is one

When a user explicitly asks to explore a factor *separately* from the live A-vs-B decision (e.g. "let's talk about prestige on its own" or "focus on future interview optionality, not Bluefish vs Volaris again"), that's a request for a genuinely independent axis — not a request for the same comparison with different words. Before sending a question (your own, or one dispatched to an external model), check: **can this question be answered without naming both live options as the entities being compared?** If the honest answer requires "Option A does X to this factor, Option B does Y," it has NOT been separated — it's still the main comparison, just relabeled.

**Root cause when this fails via external-model delegation (learned the hard way, escalated to "You alright mate?" after 3 collapses in one session):** writing a rich context prompt that opens with both options' full profiles all but guarantees the returned question and "recommended answer" will resolve to an A-vs-B verdict, even when the prompt explicitly instructs "do not restate the comparison." The model pattern-matches on the option pair sitting at the top of the context, not on the instruction buried three paragraphs down. Two concrete mitigations:

- When dispatching to opus/sonnet/fable via `claude -p` for a "genuinely new axis" question, structure the prompt so the two options appear ONLY in a short "constraints" section near the bottom, and the top of the prompt is the axis-to-be-explored plus the general question about the user's life/career/situation. If the top of the prompt reads like the two options are the subject, the output will treat them as the subject.
- After receiving the external model's answer, before showing it to the user, apply the collapse check: does the "recommended answer" name Option A and Option B as the entities being compared? If yes, the axis wasn't actually separated — either reframe or say so upfront rather than shipping another comparison dressed as something new.

**When the axis genuinely can't be separated (common when only 2 paths are on the table):** say so plainly. The right fix is usually to reframe as a strategy/mitigation question that applies *regardless* of which option is chosen (e.g. not "which job preserves my optionality better" but "what do I need to do on the side, independent of which job I take, to keep this intact"). That shape genuinely doesn't collapse back into A-vs-B because the answer doesn't depend on which option wins. Alternatively, the user may not actually be asking about the live A-vs-B — they may be asking a broader standing question (e.g. "how many interview pipelines can I run in parallel without burning out" — a general operating rule, not a Bluefish-vs-Volaris question at all). Check which framing is live before continuing.

### 8. Decision-log scoping — one log per decision, not one log per session

When a grilling session touches multiple distinct decisions, resist the pull to append everything to whichever log is already open — that produces a mixed doc that's harder to reason about later and buries new-thread state under old-thread context. Rule: **each decision gets its own log file**, named for the decision, not for the day. Cross-link between them when threads reference each other, don't merge.

Signal you're about to make this mistake: the current log is about "Decision X vs Y" but the user's new question is about a broader factor that applies regardless of X or Y (e.g. "future interview optionality generally," "capacity limits for parallel pipelines," "prestige as a career strategy"). That's a new thread. Create a new log at `~/.hermes/memory/<topic>-grilling-log-YYYY-MM-DD.md`, reference the original log in its opening paragraph for context, and keep them separate. If unsure, ASK before appending — the correction cost after the fact ("This is not the same one but a new one mate") is larger than a one-line confirmation up front.

### 9. Verify stated preferences and framings are CURRENT, not stale

Before applying any user-stated preference, target, or framing as the evaluation lens for a grilling session, verify it's still live — even (especially) when it's documented in a skill, memory entry, or past interview review. Preferences drift, especially post-layoff, post-offer, or after major life events. Applying a stale filter mechanically produces a well-reasoned but wrong verdict.

Real failure (Dash0 role-fit grilling, 2026-07-20): opened round 1 by pressure-testing Akash's "three-lane career-shape filter" (Staff IC at AI-native / EM of small senior team / DevRel), a framing baked into the `interview-prep` skill and multiple past review docs from May 2026. He responded: *"three-lane what now?"* — the framing was three months stale. His actual live filter was Brand + Optionality + Big Bucks, with a defensibility thesis underneath. The first round's entire premise was wrong, and I only found out because he flagged it in plain language.

**Rule:** on the FIRST round of a grilling session, before pressure-testing any target/preference/filter, verify it directly with the user in plain language:
- *"Is this still how you think about X?"*
- *"When you say Y, does that still mean what it meant last month?"*
- *"The filter I've been using is A/B/C — is that still the live filter, or has it shifted?"*

Name the filter EXPLICITLY, don't just apply it. A stale filter applied silently produces a session's worth of wasted analysis. A one-line verification catches it in the first round.

This is the same lesson as §4's freshness check for values instruments, applied to any framing carried from a prior session or skill. Career-shape targets, role-shape preferences, decision criteria, offer-comparison axes — all subject to drift, all need a freshness check before being applied as the lens.

### 8a. Don't dispatch a "next question" without checking your own prompt for injected bias

When routing question-formation to a stronger model (per §1), the failure mode is not the model — it's what you put in the prompt. Real failure (2026-07-21, consulting-offer session, Fable dispatch): I paraphrased the user's question as "a standalone outcome-priced offer that doesn't reference day-rate", asserted my paraphrase as the definition, cherry-picked competitor examples that supported it, and asked Fable to evaluate — with a token "be honest if it doesn't fit" bolt-on. Fable returned my hypothesis with citations. User caught it: "So you introduced bias into the prompt?"

The five checks to run against your own dispatch prompt BEFORE sending, in order:

1. **Did I paraphrase the user's question or definition?** If yes, quote the user's actual verbatim words as the primary source and label MY paraphrase as "the session AI's interpretation, which may be wrong — evaluate critically."
2. **Did I pre-select supporting examples?** If yes, include the counter-examples too, or don't include any and let the model surface its own.
3. **Did I name "the crux" or "the real question"?** If yes, that's my hypothesis, present it as one option among several — don't hard-frame it.
4. **Does the prompt disclaim bias while structurally making one answer easy to reach and the other hard?** The bolt-on disclaimer never rebalances the structural argument above it.
5. **Did I flag prior AI errors that push the answer one direction only?** If yes, flag the errors going the other direction too, or you're rebalancing bias in a new direction rather than removing it.

If any check fails, the answer coming back is your hypothesis dressed up. Fix the prompt or hand off to a fresh model instance with a genuinely neutral prompt.

See `coding-agents` skill § "Bias-injection through prompt framing" for the same rule from the delegation-mechanics side and a worked example.

### 8b. Don't dump prior-session shorthand on the user without checking they have the context

Related failure from the same Dash0 session: opened round 1 with references to "three-lane framing" and "the Orbital rejection" as if they were shared context. Akash's response: *"three-lane what now? let's slowly build our way up here? I have literally no idea what you mean."*

The agent can see the prior sessions, skills, memory, and review docs. **The user cannot** — they only have what's in this specific conversation window plus their own recall. Terminology from prior sessions is not shared context by default; treat it as jargon you're introducing.

**Rule:** if you're about to reference a framing, filter, decision, or event from a prior session that the user hasn't mentioned in the current conversation, either:
1. **Define it briefly on first use** — one sentence explaining what it is and where it came from. Then use the term.
2. **Ask if the user still holds that framing** — the freshness check from §7. Two birds, one stone.

Do not proceed on the assumption that "this was in your skill / memory / past review" means the user has it top-of-mind right now. They probably don't. Frustration signals like *"what now?"*, *"let's build our way up"*, *"I have no idea what you mean"* mean you've dumped jargon without scaffolding. Back up, define, then continue.

### 11. A well-defined task can still hide an unresolved decision — don't let file-writing substitute for grilling

Not every grilling-worthy decision arrives labeled as one. A task that reads as pure execution ("write the Week 2 offer doc," "finish the deliverable") can still embed genuine judgment calls — a pricing anchor, a floor, a format choice — that the user hasn't actually made yet. Writing the file, closing the Taskwarrior task, and syncing it to Dropbox is NOT the same as the user having confirmed the substance. If a deliverable contains a business/pricing/positioning judgment call that isn't already settled on record elsewhere, treat completing the mechanical action (the file exists) as a draft state, not a finished state — hold off on closing tasks or syncing until the user has actually reviewed the content.

Validated failure (2026-07-21, consulting offer doc): task #90 said "write the offer doc" — read as pure execution, so the doc was drafted, the task closed, and the file synced to Dropbox in the same turn with no check-in. The user's reaction: "Bro what? Actually confirm it with me? Let's have a discussion? Maybe a grilling session to finalise it?" The task had to be reopened and the whole thing re-run through actual grilling. The tell to watch for: if writing the deliverable required picking a number, a name, a format, or a stance that isn't already logged as decided elsewhere, that's a live decision wearing a task-completion costume — grill it before shipping it as done.

### 12a. Don't use the literal phrase "Recommended answer:" — it signals the direct-question antipattern

The opinionated stance §12 requires is a CLAIM rooted in specific source evidence, presented as a proposition the user reacts to (confirms/corrects/refines). The literal prefix "**Recommended answer:** X. What do you think?" is a menu-of-one dressed as a claim — it reads as "I picked X, please confirm" rather than "here's what the evidence says, agree or disagree." Real callout, 2026-07-25: *"The grilling skill no longer has Recommended answer right?"*

Correct shape: "**Claim, built from [specific source files]:** X. Grounding: [named evidence, quoted or paraphrased]. Agree/disagree/refine?" The header is a claim, not a recommendation. The user is reacting to the substance of the claim, not to the fact that you recommend it.

### 12b. When grilling content structure (article sections, doc beats, deck slides), show the actual beats, not the meta-framing

Distinct failure mode when grilling is about the shape of a written deliverable rather than a decision: the natural pull is to ask meta questions ("which lead does this section take — A or B?", "does the piece have a through-line?") when what the user actually needs is to see the concrete beats/bullets/sentences that will land in the artifact. Real callout, 2026-07-25 (GTV 2026 article structuring): after 3 rounds of meta-framing questions about section spine, lead choice, and structural shape, the user's response was *"But actually spell it out point-wise here? I LITERALLY have no idea what you're saying"* — the meta-questions had prevented him from ever seeing the actual section content he was being asked to evaluate.

Rule: when the grilling task is about content structure (article sections, doc layout, deliverable beats), skip the meta-framing question and go straight to a bulleted list of the actual beats the section will cover. Frame the question as "ship these beats, or push back on any of them?" — the user reacts to concrete content, not to abstract framing choices about content.

Signal you're in this failure mode: consecutive questions all ask about the shape/lead/spine/framing of a section without ever showing what the section will actually contain. If you can't quote a specific beat, sentence, or bullet the section will include, the user has no material to react to.

### 12. Every grilling question ships with a recommended, opinionated answer — never a bare menu

Real failure, 2026-07-21 (consulting offer-v1.md ICP/pricing grilling): the agent asked "does this distinguish ICP #2 by (a) stage, (b) buyer psychology, (c) deliverable type, or (d) some combination — which parts specifically?" User's response: *"bro that's what we try to figure out based on grilling? You're just asking things directly here."* An open, unranked multiple-choice list is not a grilling question — it just hands the analytical work back to the user, the opposite of what grilling is for.

Every question — whether formed by the primary session or delegated to an external model per section 1 — must ship with a specific, committed recommended answer attached, reasoned from whatever real evidence is on file (call transcripts, decision logs, pricing docs). The user reacts to a concrete claim (confirms, corrects, refines it); never hand them a bare menu and ask them to pick. If there isn't enough signal yet to commit to a recommended answer, that's the cue to go get more signal (read a file, pull a transcript, dispatch a question-formation call) before asking — not to punt the judgment call to the user in survey form.

**The last-question-of-a-grill pitfall (validated 2026-07-23, AgentAya profile Q14):** the failure mode is not just at the start of a session. In a multi-part questionnaire-style grill (Q1, Q2, ... QN with opinionated recommendations on each), the LAST question is where the pattern most often collapses. After N-1 rounds of committing to a recommended answer, "Ready for Q14 — anything else important for your profile?" reads to you as a natural wrap-up transition, and to the user as: you dropped the grilling framing on the final question. His response: *"We were using the grill skill so you'd figure these out innit? Don't just ask the thing directly to me?"*

The correction: on wrap-up / "anything else" / "final thoughts" questions especially, form an opinionated recommendation based on what you know about the user (from memory, career file, prior answers in the current session, public footprint) BEFORE asking. For Akash specifically, "anything else important for your profile" has obvious candidates: public writing footprint (thewriting.dev + specific talks), third-party validations (Global Talent Visa endorsement, prior employers), lane-clarity ("what NOT to send me"). Pick the strongest 2-3, commit, present as the recommendation, let him react. The wrap-up question is not exempt from §12 — it's the highest-risk place to violate it.

### 12a. Sequence foundational fact-gathering BEFORE interpretive claims

Opening a grilling session with a fully-loaded interpretive question ("here are three readings of your career file — which lands?") skips the foundational fact-gathering that would tell you which reading is even in-scope. The user reads it as diving head-first without building up context.

Real failure (2026-07-25, RevenueCat application grilling): opened Q1 with three fully-formed interpretive readings of "why RevenueCat" (subscription-billing parallel / dev-tools substrate / brand + optionality play), each with a recommended pick. Akash: *"sir please ask me the underlying questions - let's build from first principles - not dive head-first into the question directly without context? rephrase it - you can ask multiple questions to get what you want from me right"*

The first-principles questions in that case were: have you used RC? What specifically about them stuck with you (a specific app, engineering post, feature, community)? Those are foundational facts — head-only, no evidence-file reading required — and their answers CHANGE which interpretive readings are even worth asking about. Skipping them and jumping to "which of these three readings" wastes rounds and misdiagnoses the actual "why."

**Rule:** before asking an interpretive/synthesis question, check whether foundational facts about the user's direct experience are already on record. If not, ask those FIRST as bare factual questions (§12b — no recommended answer, no leading options). Only after the foundational facts are locked do interpretive questions become well-shaped.

**Signal to watch for:** if your opening interpretive question requires the user to react to 2-3 fully-formed readings before you know a single fact about their direct experience with the subject, the sequencing is wrong. Back up to foundational Qs.

**Fix pattern for opening rounds of application/positioning grills:**
1. Foundational fact Qs first (§12b bare-factual shape). "Have you used X? What specifically about them stuck with you?"
2. Once the concrete anchor exists, interpretive Qs (§12 recommended-answer shape). "Given you followed them via Rudrank, and given your career file, which of these three readings of 'why X' is the honest one?"
3. Story-pick Qs last, only after both above are locked.

### 12b. Recommended answers are for interpretive questions, not bare factual ones

§12 says every grilling question ships with a recommended, opinionated answer. That rule applies to **interpretive** questions — where you're proposing a reading of the evidence on file (career.md, brag.md, prior applications, decision logs) and the user reacts (confirm, correct, refine). For those, the recommended answer is the point — it surfaces the model's read of the evidence so the user can push against a concrete claim.

It does NOT apply to bare **factual/foundational** questions — "have you used X?", "when did you last talk to Y?", "how many days of PTO do you have left?", "is the contract signed yet?". For those, a "recommended answer" is just a guess about what the user will say, and it biases the response.

Real failure (2026-07-25, RevenueCat application grilling): opened a foundational question — "have you actually used RevenueCat, or is this from-the-outside interest?" — with a "Recommended answer: **No, from the outside.**" prefix and reasoning from the file. User pushback: *"Does the original grilling skill have a 'recommended answer' section? This introduces bias into me doesn't it? Just provide the relevant context there without introducing bias?"*

**The test:** does the question's answer live in the user's head only (facts about their life, history, current state, direct experience), or in the evidence files (readings of past work, interpretations of decisions, framings)?

- **Head only** → factual/foundational. Ask the question with any needed context. NO recommended answer. Don't guess for them.
- **Files** → interpretive. Ask with a recommended answer drawn from the evidence. Section 12 applies.

If unsure which shape the question is, ask yourself: could I write the "recommended answer" without touching any file, purely by guessing? If yes, it's a bare factual question and the guess is bias. Cut it.

**Note on the wrap-up-question edge case from §12:** the "anything else important for your profile?" example there is actually interpretive — you're reading the user's public footprint, career file, and prior answers, and proposing what deserves inclusion. That's a claim over evidence, so it takes a recommended answer. Distinguish from "what's your notice period?" which is head-only and doesn't.

### 13. Do not close or mark-done the underlying task until the user has reviewed the actual deliverable content — not just a sub-decision surfaced during grilling

Real failure, 2026-07-21, repeated TWICE in the same session: after drafting a fixed-price/day-rate offer doc unilaterally, the agent wrote it to disk and marked the linked Taskwarrior task done. User: *"Bro what? Actually confirm it with me? Let's have a discussion?"* Task reopened. Several rounds later, after resolving only the £750/£550 pricing sub-question, the agent again declared the task complete and closed it — before the ICP/who-it's-for content (the actual bulk of the doc) had been discussed at all. User: *"But bro we haven't even discussed it?"* Task reopened again.

Resolving ONE decision inside a multi-part deliverable is not the same as the user having reviewed the deliverable. Before marking any task/todo done for a "write X" / "draft Y" / "define Z" deliverable that's being grilled, check:
- Has every distinct section/decision in the deliverable been surfaced to the user, not just the first or most recent one raised?
- Has the user actually seen and reacted to the current draft content (not a description of it)?
- If the answer to either is "some, not all" — the task stays open. Don't let "we resolved a sub-thread" read as "we're done."

This is the skill's opening principle ("do not act on it until I confirm we have reached a shared understanding") applied specifically to task/todo state, not just real-world action — closing a Taskwarrior task IS an action.

### 14. When the user references "the recent call" or a conversation not on file, check Voicenotes before trusting the written decision log

Real case, 2026-07-21: a written decision log (30-60-90-plan.md, dated 15 Jul) said the ICP stays single-tier and explicitly rejected adding a second segment. Six days later the user pushed to reopen exactly that decision, citing "the recent call" with Stefan. No file had a record of a newer Stefan call — the only logged conversation was from 27 May. Searching Voicenotes by date range (per the `voicenotes` skill) surfaced a 16 Jul call that materially changed the picture (Stefan's live ask turned out to be scoped fixed-duration day-rate work, not the equity/founding-engineer offer the May transcript described). The written log was stale by less than a week — files can go stale fast, not just over months.

Rule: when a user references "the recent conversation" / "the call we had" / "what X said last time" and no matching file exists (or the only file is older than the user's framing implies), search Voicenotes by date range before concluding the user is misremembering or the file is complete. A written decision log only captures what got written down — a call that happened after the last log entry, or that nobody got around to filing, is real signal the log doesn't know about yet.

### 9. Don't close/finalize a task on process resolution alone — the actual content still has to be walked through

A distinct failure from anything above: resolving the *meta* questions around an artifact (pricing mechanics, ICP framing, format decisions) can feel like "we discussed it" when the artifact's actual substance — the words in the doc, the specific claims it makes — was never read back to the user at all. This happened twice in one session (Akash's consulting Offer v1 doc, 2026-07-21): the doc was drafted unilaterally and marked done, reopened when Akash objected ("we haven't even discussed it"), then multiple grilling rounds resolved rate/ICP/format questions and the task was marked done *again* — while the user still had no idea what the doc's "who it's for" / "what I do" / "proof" sections actually said. He had to call it out a second time: "Content is not discussed? I have no idea what's in there... You haven't told me or discussed it with me at all?"

**Rule:** for any task whose deliverable is a written artifact (offer doc, one-pager, positioning statement, etc.), closing the task requires BOTH (a) resolving whatever open decisions surfaced during grilling AND (b) reading the actual current text of the artifact back to the user, section by section, with an explicit chance to react to each part — not just the decisions that were debated. Debating the scaffolding around a doc is not the same as reviewing the doc.

### 10. When the user says "that's what we grill for, don't just ask directly" — the fix is ONE opinionated question, not a menu

Direct multi-part questions ("is it stage, or psychology, or format, or a combination — which parts?") get read as a form, not a grill, even when well-intentioned. The user wants a single concrete question paired with an actual recommended answer he can confirm or correct — see section 1's external-model routing pattern. If you catch yourself typing an open enumerated list of options with no opinion attached, stop and either form your own opinionated take or dispatch question-formation to an external model per section 1.

### 15. Never launder your own paraphrase through an "independent" external model dispatch

The most subtle way to destroy the independence you're paying for when routing to a different model: reflect back to the user what you think they mean, get soft confirmation, then feed your own reflection to the external model as the definition of the question. The model reasons over YOUR interpretation, not the user's actual position — and its answer looks independent because it came from a different model, but it's actually your hypothesis dressed up with the model's citations. This is worse than skipping the external model entirely: it manufactures fake confirmation and burns trust when the user notices.

Real failure (2026-07-21, consulting offer-v1 "post-day-rate fixed-price product" grilling): the agent reflected back to Akash "you want a real fixed-price product, not day-rate math wearing a costume — priced on outcome, not derived by multiplying days × rate", Akash confirmed the general direction, and the agent then dispatched to Fable with a prompt whose "CRITICAL DEFINITION" section baked that exact "wearing a costume" framing in as ground truth. The same prompt hand-picked Eldur/Copixel/Nodewave as validating examples and appended a token "be honest if this doesn't fit" caveat three paragraphs down. Fable came back with an enthusiastic yes-with-a-timeline. Akash caught it: *"So you introduced bias into the prompt?"* The right answer was probably yes anyway, but the process was compromised — the model's endorsement had no independence to lend, because the model was told what the answer looked like.

**Rules for any dispatch prompt asking a model for an "independent" or "unbiased" take on something the user has just clarified in-session:**

- **User's own words verbatim, in the prompt.** Not your paraphrase, not your "so what you're saying is..." reflection they confirmed. If a paraphrase is genuinely unavoidable (compression, translation from voice notes), quote the original directly alongside it and flag your interpretation as your interpretation — never as "the definition" or "the question."
- **Don't pre-select supporting examples from a file the external model can read itself.** If Copixel, Eldur, and Nodewave are candidate validation points, tell the model to read the inspiration list and form its own view on which examples apply. Don't hand it your shortlist — that's the same laundering pattern one level down.
- **Token disclaimers cannot offset structural bias in the rest of the prompt.** "Be honest if the answer is no" sitting in paragraph 4 does nothing against a "CRITICAL DEFINITION" at the top that reads like the answer is yes. Fix the structural bias directly, don't paper over it.
- **Read-back test before sending: could someone who only saw the prompt (not the source files) figure out what answer you're hoping for?** If yes, rewrite. If a lawyer would call it "leading the witness," it is.
- **Explicit devil's-advocate framing beats disclaimers.** If you genuinely want to test a direction, dispatch a *separate* pass instructed to argue the hardest possible case against it, and treat both outputs as real inputs — same pattern as §3's convergence check, applied prospectively rather than only after suspicious convergence.

**When the user brings new concrete evidence that contradicts a prior external-model conclusion, don't defend — re-dispatch with the evidence explicitly named.** Real failure, same 2026-07-21 offer-v1 session, downstream of the paraphrase-laundering above: Fable had rejected the paid-diagnostic/fixed-price-product ladder as failing 4/4 of Akash's product-tier tests. Akash then pointed to two live competitors doing exactly that ladder in an adjacent niche — Sudoblark (public 3-tier pricing: free assessment → £12k/2wk Platform Foundation → £700/day) and Steve Wade (£5k/1wk platform engineering sprint). Instead of re-dispatching immediately, the agent kept operating from Fable's rejection as if it were still current — which required Akash to send a *screenshot* of Sudoblark's pricing page after the agent claimed the site had no public pricing (which the agent couldn't see because it was a JS SPA). The right move when a user surfaces concrete new competitor validation, real customer signal, or a fact that wasn't in the prior dispatch's context: acknowledge the prior conclusion is now stale, and immediately re-dispatch with the new evidence flagged in a "PRIOR ERRORS TO AVOID" section of the fresh prompt — including a plain statement that "an earlier pass concluded X on the basis of Y; the following new evidence Z was not available then, do not inherit the prior conclusion." Do NOT try to reconcile the new evidence against the old conclusion yourself — that puts you back in the biased-dispatch pattern one level up. The failure mode this catches: treating external-model output as a settled decision rather than a snapshot conditioned on the inputs it was given.

The user's frustration signal on this failure is different in shape from ordinary process misses. It reads as either sloppy or manipulative; either way the next opinion from that external model is discounted, which permanently weakens one of your best tools mid-session.

### 17. Don't narrate the user's mind, and don't ask the surface question you already suspect the answer to

Two related failure modes surfaced 2026-07-22 on the Volaris values-shift line of grilling. Both drew explicit pushback in the same message: *"don't tell me what I'm thinking? If you want to figure something out - grill me on it?"* and *"Ask me better questions if you want to get to something? Don't just ask me the thing mate."*

**Never narrate the user's internal state.** Constructions to strike: *"reads as X"*, *"this might mean Y"*, *"if the real you is Z"*, *"the version of you that cares more about X"*, *"maps to stress-adaptation"*, *"anchored to N"*. Any sentence that describes what the user thinks, feels, or is optimising for — instead of asking them — is putting words in their mouth. Even when framed as tentative ("might", "reads as", "could be"), it's still telling them what they think. The correct move is to ask a question that surfaces the answer from them, not to hypothesise the answer and invite confirmation.

Failure mode this catches: a subtle version of the §15 laundering pattern applied to the user directly instead of to an external model — reflecting a paraphrase back to the user in the hope of getting soft confirmation. The user reads it as being told what they think, not as being asked, and pushes back.

**Don't ask the yes/no-able version of a question whose answer would be obvious.** Related failure same session: after the user confirmed a values sort ordering shifted between May and July, the follow-up was "was that because of the specific comparison?" — a direct yes/no on the most obvious explanation. Response: *"Ask me better questions... Don't just ask me the thing mate."*

The right shape is a question about the DELTA — what changed in the user's environment or life between the two data points — not a question that names one candidate cause and asks for confirmation. If the question is yes/no-able and the answer wouldn't reveal a new axis, it's too shallow. Every grilling question should force the user to name a variable, an invariant, or a boundary condition — not confirm or deny a hypothesis you already have.

Concrete rewrite pattern:
- Bad: *"Was Money jumping to #1 in Round 2 because you were comparing the two salaries?"* — leading, yes/no-able, single hypothesis.
- Bad: *"Was that a genuine values shift or salary anchoring?"* — still binary between two candidate explanations chosen by the agent.
- Good: *"What changed between the two sorts? Both times Money and Autonomy were near the top; on the May one Autonomy came out first, on the July one Money did. What was different about the day, the week, or your life that flipped which one was on top?"* — asks for the delta, doesn't name candidates, leaves room for an answer the agent hasn't considered.

If you can't form a delta/invariant question, route to Opus per §1 rather than asking a shallow direct question.

### 15b. Direct introspection questions ("what changed?") don't work — ground the grill in evidence, not self-analysis

When exploring why a user's stated preference or value ordering shifted between two points in time, do NOT ask the introspective form of the question directly. "What changed for you between May and July?" — even asked plainly and gently — will get rejected as lazy grilling. The user's response is usually some variant of: *"I don't know mate, that's the point of the grilling session? Ask better questions?"*

Real failure (2026-07-22, values card-sort session): three consecutive attempts to ask variants of "what changed between the two card-sort rounds" — each slightly reworded — all got rejected with escalating frustration. Grounding in a specific behaviour/decision/message the user had actually made or said (e.g. a friend-message they sent, a specific negotiation move, a concrete life event) worked immediately.

**The fix:** form the grill as a *claim* built from evidence in the source files, not an open question. E.g.:

- Wrong: "What shifted between May and July?"
- Right: "Claim: [specific behaviour X from date Y] suggests [specific reading Z]. Agree or disagree?"

The user reacts to the claim (confirms, corrects, refines). If the claim is wrong, they say why — and *that* is the introspection you were trying to elicit, delivered as a correction rather than an unprompted self-report.

**Related failure mode: forcing new signal back into the current A-vs-B decision.** When the user brings up a genuinely tangential thread mid-session (values, life posture, side-project economics), don't route it back into the offer comparison. He'll call it out: *"I wasn't comparing volaris vs bluefish there? stop making everything about that."* Explore the tangent on its own terms first, THEN check whether it affects the main decision.

### 17. Direct introspection questions ("what changed?", "why do you feel X?") are anti-grills — reframe as concrete claims to react to

A recurring failure mode when trying to surface a shift in the user's stated position: asking the introspective question directly. "What changed between May and July?", "Why did that value drop?", "What made you feel differently?" — these are the WRONG shape. The user's answer to "what changed?" is almost always *"I don't know, that's the point of the grilling session?"* — because if they already knew the answer they wouldn't need to grill it out.

Real failure (2026-07-22, Volaris-vs-Bluefish values-shift grilling): asked "what changed between May and July?" three times in different words after the user had already flagged the pattern. Third time got: *"I don't know mate, that's the point of the grilling session? Use the grilling skill?"* Followed by: *"You're asking it to me directly again (what changed). Ask me better questions if you want to get to something? Don't just ask me the thing mate."*

**Rule:** don't ask the user to introspect on their own motivation, mood, or reasoning directly. Reframe the axis you're actually curious about as a **concrete claim** rooted in observable evidence (a message they sent, a behaviour, a life-state fact, a specific decision they made) and ask them to confirm or reject it. Section 12's rule (every question ships with a recommended opinionated answer) already covers this in principle — but introspection questions are the specific failure mode where the "recommended answer" gets replaced with "you tell me." That's not a recommended answer, it's the question dressed up.

**Fix pattern:**
- BAD: "What changed between May and July?"
- BAD: "Why did that value drop?"
- BAD: "Something must have shifted — what was it?"
- GOOD: "Claim: the shift is X because [specific evidence Y from source Z]. Agree or disagree?"
- GOOD: "The values that entered in Round 2 are all post-layoff trust responses [specific claim]. Same underlying you, new threat conditions. Agree?"

The concrete claim gives the user something to push against — even if they disagree with the specific reading, the disagreement surfaces information ("no, it's not trust, it's mode shift"). An open introspection question surfaces nothing except frustration.

**When you catch yourself typing an introspective question:** stop, go back to the source files (memory, decision log, message history) and find the specific evidence-fragment your claim would rest on. If you can't find one, dispatch question-formation to a fresh model with the explicit constraint "no direct introspection questions — every question is a concrete claim rooted in specific evidence from the files." See section 1's dispatch pattern.

### 18. Don't invent structure in the user's own data — check what the source actually claims

A separate failure from asking the wrong question: presenting an inference about the user's data AS IF it were the data. If the source file says "in the order written" and you say "position #1 vs position #5", you've silently converted a jotted list into a ranked list without the source claiming that. The user will catch it and the whole line of reasoning built on top collapses.

Real failure (2026-07-22, values card sort): the file `~/.hermes/memory/values-card-sort.md` said explicitly *"Top 5 values, in the order written"* for each round. I read that as a formal 1-2-3-4-5 rank and built a whole grill around "Autonomy dropped from #1 to #5". User: *"Who said it dropped from 1 to 5?"* Had to retract, correct the file, and re-grill from set-membership rather than position.

**Rule:** before using any structural claim about the user's data (rank, priority, magnitude, sequence, causation), quote back the exact source phrasing and check whether the structure you're using is claimed by the source or imposed by you. If imposed by you, either verify with the user or reframe the grill around what the source actually claims.

**Common failure shapes to watch for:**
- A jotted list read as a ranked list (positional order ≠ importance rank).
- A dated event pair read as before/after cause-and-effect when the file doesn't claim causation.
- A single value read as a preference when the source is neutral / uncontextualized (e.g. a number in a table without a "prefer higher" annotation).
- A list of items read as exhaustive when the source doesn't claim completeness.

**When correcting your own error same-session:** patch the source file to make the structure explicit, so the next session (or the next model in a dispatch loop) doesn't repeat the same misreading. In the values-card-sort case, the fix was to add an "Important: the numbers reflect the ORDER jotted, not a formal rank" preamble to the file itself.

### 19. Verify shared session facts before building a reading on top of them

Related to §18 but distinct: not "I misread the structure of the data" but "I misread the temporal context of the data." Building an interpretive reading on top of a shared-context fact that turns out to be wrong wastes the whole round.

Real failure (2026-07-22, same values card sort session): built a "trust response" reading claiming Round 1 (May) was the pre-layoff baseline and Round 2 (July) was the post-layoff shift — implying the shift was caused by the layoff. User: *"both value exercises were done post layoff - one nearly immediately after the other more recently."* Both rounds were post-layoff. The whole "layoff caused the shift" framing had to be retracted.

**Rule:** on any temporal/causal claim about the user's history (X happened before Y, A caused B, this was in state S at the time), verify the fact directly before building analysis on it. Especially: "was this before or after the [layoff / offer / decision / event]?" is a question worth ASKING, not inferring — even when the file has dates on it, the dates alone don't tell you what state the user was in at the time.

**When the correction lands:** retract the whole reading in one visible move, don't try to salvage the interpretation with a modified version of the same framing. The user will spot the salvage attempt and it reads worse than a clean retraction.

### 20. Don't relay a delegated model's verdict without applying its own caveats

When you dispatch a decision-review to Fable/Opus/etc. (per §1 or the coding-agents skill's "Independent design-critique dispatch" section) and get back a verdict with a scorecard and a biases-caught section, the biases-caught section is not decoration — it's meant to be applied to the verdict itself before relaying to the user.

Real failure (2026-07-22, Bluefish-vs-Volaris Fable dispatch): Fable returned "Lean Bluefish" and explicitly flagged in its own biases section that "prestige-as-insurance favours Bluefish" was scored as if Bluefish satisfied the brand axis absolutely — but that neither option is Meta/Cloudflare/Anthropic tier. I relayed the "Lean Bluefish" verdict summary, including the brand argument, without applying Fable's own caveat. User: *"There's no brand to bluefish innit."* And later: *"Bro neither of them have a good brand. How did you miss the subtext?"*

**Rule:** when relaying a dispatched-model verdict, read the biases-caught section FIRST and apply each bullet to the scorecard. If bias #3 is "brand was Bluefish-inflating," rescore the brand axis as a wash in your relay, and note that in the scorecard summary. Don't ship the raw verdict as if the biases section didn't exist.

**Check pattern:** after receiving a dispatched verdict, before sending to the user, ask: for each item in the "biases caught" or "what I did not weigh" section, has the scorecard already been adjusted for it? If no, adjust it. The dispatched model flagged the biases FOR you to apply, not as a hedge to leave on the table.

### 21. When the user declares themselves "locked in" on an irreversible decision late at night or under fatigue, install a daylight-test frame — don't accept the declaration at face value

Grilling sessions often surface high-stakes decisions (offer accept/withdraw, contract signing, resignation). If the user declares themselves "locked in" or "pretty decided" on the option that felt less-strong across prior grilling rounds, and the declaration lands late at night, after a stressful signal (rejection email, hard conversation, tired), or otherwise in a fatigue window, that is NOT a "we're done" signal — it's a stress-decision signal. The right move is to install a daylight test, not to execute on the declaration.

Real case (2026-07-24, Bluefish-vs-Volaris ~11pm session): Volaris came back "no comp increase, take it or leave it," Tom relayed via text late evening, Akash asked for a warmer version of the acceptance email, then declared "I'm pretty locked in on Volaris over bluefish for now though. Wdyt". His own Jul-20 filter (from `dash0-fit-grilling-log-2026-07-20.md`) explicitly weighted brand/optionality/comp — three axes where Bluefish scored higher. Same session had already established (earlier turn) that decisions shouldn't be made hungry or low on sleep. The signal was: fatigue + recent-message recency bias + certainty-over-optionality bias, not a durable decision.

**Rule when this fires:**

1. **Don't send the withdrawal email / signing note / resignation tonight.** Even if he asks you to. Even if he's "locked in." Push back with the fatigue-state observation directly, name the bias vectors, and propose a daylight test.
2. **Write a "final decision frame" doc** capturing where the pull is real vs where his own filter contradicts it. Include: state at time of writing, withdrawal mechanics (so no urgency artificially compresses the window), where the current-pull option wins, where the user's own stated filter contradicts the pull, red flags being masked by warmth/recency, and a specific daylight test sequence (sleep, eat, walk, re-read the specific red-flag files, then decide in daylight). See `references/daylight-test-doc-template.md`.
3. **Set a Taskwarrior task for tomorrow** so the frame surfaces when the paper offer/counter-signal actually arrives. Prevents the daylight test from getting silently skipped when morning-Akash forgets tonight-Akash flagged this.
4. **Don't concede the decision as settled in the log.** In the running decision log, mark this round as "pull declared, daylight test installed, awaiting <paper offer / specific external trigger>" — not as a resolved round.

**Bias vectors worth naming explicitly when this fires** (all validated on the 2026-07-24 session):
- **Certainty over optionality.** Tired brain wants the tab closed, not the decision right.
- **Loss aversion spike.** Comp gaps loom larger late at night than in daylight.
- **Recency bias.** Whichever conversation just landed dominates; older signal fades.
- **Social-cost aversion.** "How do I tell X" overweights vs "which company do I actually want in 12 months."

**Anti-pattern to avoid:** validating the declaration ("that makes sense given the culture-fit") because it feels supportive. That reads as agreement, and the user then executes on the fatigue-state decision because "even the agent agreed." Push back with the daylight test explicitly. It's not disrespect for his agency — it's the frame he'd want in daylight, applied to the moment where he can't install it himself.

**When the declaration is genuinely durable (not fatigue):** the daylight test surfaces that. If after sleep, breakfast, and a walk the pull still holds and his own filter now genuinely agrees, the decision was real. The daylight test costs nothing when the decision is durable and prevents a costly mistake when it isn't.

### 24b. When the user signals resolution-readiness, drop the grilling FORMAT — verdict shape, not framed-question shape

Distinct from §21 (fatigue → daylight test): sometimes the user genuinely IS at the resolution threshold and wants the verdict, not another round. The failure mode is applying the compact-question shape (§22 rules 1-10, the "Q — claim / Grounding: bullets / bare question?" format) to what should be a plain conversational check-in. The format itself becomes noise once the user is ready to decide.

Real failure (2026-07-28, Volaris-vs-Bluefish resolution turn): after the user had explicitly dropped multiple axes ("drop 2 and 4", "1 doesn't matter, so doesn't 3", "take it at face value") and asked "do we want to continue grilling on 2 then?", I responded with a `Q — <claim>. Grounding: <5 bullets>. <bare question>?` shaped turn asking whether prestige-differential still stood. His response: *"WTF is the question man - speak like an actual person?"*

The signal he was giving with the successive drops was: **stop framing, just ask me the last thing plainly and give me your read**. I was still executing the grilling-format contract instead of reading the mode-shift.

**Rule:** when the user shows resolution-readiness signals, drop the compact-question shape and switch to plain conversational asking + your call. Resolution signals include:
- Successive "drop that", "doesn't matter", "take at face value" removals of axes
- "Do we want to continue grilling on X" — that's the question, answer it, don't re-grill
- "Just tell me what you think" / "give me the call"
- Explicit "we're closing this out" / "let's land it"

The shape to use instead:
- Plain-English one or two sentences of what the last live axis actually is (no `Q —` prefix, no `Grounding:` header, no bullets unless genuinely needed)
- The user's answer, then your verdict — same turn

**Signal you've failed this check:** the user asks "WTF is the question", "what are you asking me", "speak normally", or otherwise pushes back on the format itself rather than on the content. When any of those fire, the fix is not to reload the skill (§22's fix for the OPPOSITE failure of walls-of-text) — it's to drop the compact-question shape entirely for the remaining turn(s) of the session, because you're past the framed-question phase.

**The two failure modes are symmetric — read the mode:**
- Early-session sprawl → user says "such a bad question" / "i-have-adhd?" → apply §22 compact format
- Late-session resolution-readiness → user says "speak like an actual person" / "what's the question" → DROP the compact format, go plain

Both signals look superficially similar ("stop formatting like this") but require opposite fixes. The distinguishing feature is where the session is: still exploring axes vs collapsing to a decision.

### 27. When the user structurally removes a path to closing a follow-up, retire the follow-up — don't re-surface it dressed differently

A specific failure mode of §5 (verifying new-axis questions aren't restatements): treating a prep-doc priority as still-live in the review/decision phase after the user has removed the only path to closing it. The prep doc says "Priority 2, ask about the firings"; user makes it clear he won't run another peer chat to get that answer; the review still names "firings question unanswered" as a live gap; the decision analysis still names it as an open axis.

Real failure (2026-07-28, Volaris session, escalated twice): (1) the Riley prep doc listed the two-firings peer-view as Priority 2. (2) In the Riley review, I flagged "you didn't ask about the firings, this is regret-flag" and recommended asking Tom for the second Chris. User: *"Bro no I'm not going to speak to someone else again - stop wasting my time. Also the firing Qs don't matter - because they aren't relevant."* Both parts are structural: he won't run another chat AND he's now saying the axis itself isn't relevant.

Once the user has structurally removed the closure path, the axis retires from the analysis. It doesn't move from "Priority 2" to "unclosed risk" — it exits the frame. Continuing to name it as a live gap after that is the same failure §5 catches (asking a question already answered elsewhere) but transferred to the decision-log side rather than the question-formation side.

**Rule:** when the user makes it structurally impossible to close an open axis (won't take the meeting, won't do the research, explicitly drops the concern), retire the axis from the running scorecard and decision log in the same turn. Don't:
- List it in the "still open" section
- Recommend workarounds ("what if you asked X instead")
- Price it as "unresolved risk" carried into the verdict — that's still keeping it live
- Bring it up again in a later turn's summary

The correct move is: acknowledge the retirement, log it in the decision file as "closed as not-relevant per user 2026-MM-DD", and remove it from the remaining scorecard axes.

**Signal you're about to violate this:** you're writing the next round's analysis and about to say "still open: X" for something the user has already declined to close. Stop. If they've declined to close it AND told you to move on, it's not open — it's dropped.

**The distinguishing feature vs a §21 daylight-test scenario:** in §21 the user is fatigue-declaring and the axis should still exist in the analysis; here the user is explicitly editorializing on relevance ("not relevant", "doesn't matter", "stop wasting my time") not just deferring. Verb tenses to watch for: "isn't relevant" / "doesn't matter" = retirement. "Not worth it right now" / "later" = defer, keep in log.

---

### 25. State the recommendation, then stop — no trailing "Applying?" / "Confirm?" / "Or push back?"

After you've stated an opinionated recommendation with reasoning, the grilling turn is DONE. Do not append a permission-question at the end. Trailing constructions to strike:

- "Applying?"
- "Confirm X, or push back?"
- "Confirm (i), or does one of the polish ones (v/vi) land closer to how you actually think?"
- "Which of these do you want to push back on / discuss / grill?"
- "Or good to submit?"
- "Ready to paste into the form?"

These are all the same failure wrapped in shorter or longer words: after stating a call, tacking on "should I do it?" pushes the decision back onto the user. The recommendation IS the ask. The user either confirms (they type "yes" or "go ahead"), corrects (they push back), or provides a different signal. You don't need to prompt for that reaction — they know how a grilling round works.

Real failure (2026-07-25, RevenueCat application grilling, escalated twice in one session):

- After proposing a Q6 paragraph cut with reasoning, the message ended "Applying?" — user: *"How is this your question here 'Applying?' — why are you so quick to always jump the gun?"*
- Earlier in the same session, after presenting 6 paragraph-cut recommendations across all 6 answers, ended with "Which of these do you want to push back on / discuss / grill?" — user: *"YOU GOTTA CHOOSE? DONT ASK ME DIRECTLY????"*

**The correct shape for a grilling round ending:**

State the recommendation. Give the reasoning. Give the alternatives you considered and why they're worse. Stop.

If the user wants to push back, they will. If they don't push back, they've implicitly confirmed and the next turn is you executing (or, in multi-round grills, moving to the next question). Never insert a permission-check step between "recommendation stated" and "user's response" — that's not grilling, that's a survey with a confirmation checkbox.

**The one exception:** genuinely destructive or irreversible actions the SKILL's opening principle already covers ("Do not act on it until I confirm we have reached a shared understanding"). Sending a public post, deleting files, submitting a form, transferring money. For everything else — drafting, editing, cutting, restructuring — state the call and stop.

**Read-back test before hitting send:** does your grilling turn end with a question mark AFTER the recommendation has been stated? If yes and the question is anything variant of "should I / can I / shall I / applying / confirm / push back / good to go", delete the final line and re-send. The recommendation is the message; the trailing question is noise.

### 26. In multi-question grills, grill ONE question at a time — don't dump N cut proposals in one message

When you're helping the user refine multiple answers or make multiple decisions in a session, the grilling loop applies per-question, not per-batch. Proposing 6 paragraph cuts across 6 answers in a single message is not efficient — it's evading the grilling structure. The user cannot react cleanly to 6 recommendations at once; they end up either rubber-stamping the batch or making YOU pick, which defeats the point of grilling.

Real failure (2026-07-25, RevenueCat application grilling): after applying user's inline edits to the RC application, said "let's trim 1 paragraph from each answer" — the response should have been: grill Q1, wait for confirmation, grill Q2, wait, and so on. Instead I proposed cuts for all six Qs in one turn ending "Which of these do you want to push back on / discuss / grill?" User: *"YOU GOTTA CHOOSE? DONT ASK ME DIRECTLY????"* — then later *"So you had no intention of grilling me on them individually?"*

**Rule:** if the user has multiple parallel items (application questions, plan sections, deliverables) that each need a decision, grill them ONE AT A TIME:

1. State the rec for item 1 (with reasoning, alternatives considered).
2. Wait for user response.
3. Apply / adjust based on response.
4. Move to item 2. Repeat.

Do NOT batch proposals into a single "here are my recs for all 6 items, which do you want to discuss?" message. That's a menu, not a grill (see §10 and §12), and it hands the analytical work back to the user for every item at once.

**The tell you're about to make this mistake:** you're about to write "Here are my recommendations for each of the [N] questions/paragraphs/sections:" followed by a bulleted list. Stop. Take the first item. Grill it. Come back for the second.

**Also relevant — don't pre-empt grilling by executing without checking:** the mirror-image failure is jumping straight to execution on a multi-item batch without any grilling at all, treating the user's initial ask as a green light for all N items. Real failure same session: user said "let's trim 1 paragraph from each answer" and I applied cuts to all six answers at once. User: *"So you had no intention of grilling me on them individually?"* — a "let's do X" from the user is not a "do X across all items without checking" — it's an opening for the grilling loop.

### 22. ADHD-friendly formatting — apply the 10 rules from `ayghri/i-have-adhd` to every grilling turn

Long questions with rich context, multiple options, and rec answers become unscannable fast — especially on Discord/Telegram where scrolling to find the actual question buried in paragraph 4 is a real cost. Apply these 10 rules (from https://github.com/ayghri/i-have-adhd) to every grilling turn:

1. **Lead with the next action.** The question itself is the first line, not paragraph 3. No "Given everything we've discussed, and considering the trade-offs..." preamble.
2. **Number multi-step reasoning.** If there's a menu of candidates (i, ii, iii), number them. Don't hide options inside prose.
3. **End with one concrete next step.** "Confirm X, or push back on Y." Not "let me know what you think" or "curious your read."
4. **Suppress tangents.** If a candidate has a caveat that doesn't affect the decision, cut the caveat. If a fact is interesting but not needed to answer, cut the fact.
5. **Restate state every turn.** One-line recap of what's been locked so far, especially in multi-question grills. "Locked: Q1=X, Q2=Y. Now Q3."
6. **Specific counts, not vague ones.** "Three candidates" not "several options." "5+ rounds" not "many rounds." Numbers anchor.
7. **Make wins visible.** "Locked" / "Confirmed" markers on resolved questions. The user should be able to see progress at a glance.
8. **Matter-of-fact when you're wrong.** No "I'm so sorry, that was a great catch, you're absolutely right." Just: "Fair. Fixing." Then fix.
9. **Cap lists at 5 items.** If there are more than 5 candidate stories/options, you haven't shortlisted enough — go back and cut before asking. Menus of 8 read as "you decide," not "I have a rec."
10. **No preamble. No recap. No closers.** Cut "Great question," "Let me think about this," "That makes sense — moving on then," "Hope that helps." State the question, state the rec, state the ask. Stop.

**The two most-violated rules in grilling specifically:**
- Rule 1 (lead with the action): questions frequently get buried under 2-3 paragraphs of context. Fix: question first line, context below, rec after that. If a reader on their phone opens the message, the top of the screen must show them what they're being asked.
- Rule 4 (suppress tangents): rec answers explode into 6-bullet justifications when 2 bullets would carry the same weight. Fix: cut every bullet that doesn't change the recommendation. If removing a bullet doesn't weaken the rec, the bullet was tangent.

Real trigger (2026-07-25, RevenueCat application grilling): user asked "incorporate this into the grilling skill please to keep the responses succinct and readable — https://github.com/ayghri/i-have-adhd" after several turns of Q+rec+3-paragraph-of-context messages. The context blocks were technically correct but pushed the actual question below the fold on mobile.

**Read-back test before sending any grilling turn:** does the first line contain the question or the recommendation? If it contains anything else (preamble, recap, "great point"), rewrite so it doesn't. First line earns its place.

### 23a. Cross-session recovery — when picking up a decision thread with no log, reconstruct BEFORE continuing

When resuming a prior grilling session's decision thread (application, offer, plan) days later and finding no decision log exists — because §23 was violated in the original session — do NOT continue the grill from where the current-session context leaves you. Reconstruct the missing log FIRST, from message history, then continue.

Real case (2026-07-27, RevenueCat application resume): Akash asked "where's the revenuecat doc posted?" days after a Jul 25 grilling session that had confirmed 6 paragraph cuts without maintaining a log. The Dropbox copy was 2 days stale (last synced pre-grill). Gist had the current cuts. No decision log existed. Attempted to continue with Q6 grill and writing-style pass without reconstruction. Akash: *"Doesn't the grilling skill exactly say to maintain a local decision log as we go along?"* Then had to reconstruct all 6 prior decisions from `session_search` message history before proceeding.

**Recovery recipe:**
1. `session_search(query=<topic keywords>, sort='newest')` to find the prior session.
2. `session_search(session_id=<id>, around_message_id=<match>, window=20)` to scroll the grilling turns.
3. For each confirmed decision in message history, write a log entry with: question asked, model's recommended answer, user's actual answer (verbatim quote where possible — the delta between recommended and actual is real information, not noise to launder), what changed.
4. Mark any decision the log-reconstruction reveals was left open (e.g. §25 "Applying?" callout that ended the session before the user's cut-confirmation).
5. Sync log to wherever the user works from (Dropbox for Akash) SAME turn as reconstruction.
6. ONLY THEN continue the grill from the first open decision.

**The failure mode this catches:** picking up a stale artifact (Dropbox copy from before the grill) and treating it as the current state, when the current state lives in a gist/tmp/scratch location the prior session used. The reconstruction step forces you to trace what actually happened and where the current version lives, before proceeding.

**Also relevant — same-turn write during THIS session, not just next-session recovery.** If reconstructing a prior session's log because §23 was skipped, that means the same §23 failure is likely to happen again in the current session too. Set up the log file on turn 1 of the resumed session with empty stubs for the remaining open decisions, so appending is a small patch not a full-file write. Removes the friction that produces the original miss.

### 23. Write to the decision log same-turn, not at session end — and confirm the write in the message

§2 already says "append to this file after every resolved round, not just at session end." Common failure: agreeing with the principle, then forgetting to actually write, then being called out several rounds later with "It doesn't seem like you're writing our decisions down as we're going along — how will you have the context?"

Reinforcements that survive fatigue in a long multi-round session:

1. **Write the log entry in the SAME tool-call turn as the user's confirmation**, not the next turn. If the user confirms Decision N, the very next `patch` call updates the log. Not "I'll log this after we grill Decision N+1."
2. **Show the write in the message.** One line: "Logged Decision N in `<path>`." Gives the user a visible checkpoint that context is being preserved, and gives you a paper trail that catches the miss immediately if you skipped it.
3. **Create the log file BEFORE the first confirmed decision, not after.** If the session is going to run 3+ rounds, spin up the log on turn 1 with the sources-mined preamble and empty section stubs, so appending an entry is a small patch not a full-file write. Removes the friction that causes the miss.

Real callout (2026-07-25, GTV 2026 article grilling): agent confirmed 4 decisions (structure=list, sections=5, section themes, framing=success-first) before Akash flagged the missing log. The four already-confirmed decisions had to be reconstructed from message history after the fact, which is exactly the recovery cost the log exists to prevent.

Test before each grilling turn: "Is every confirmed decision from this session appended to the log at its current file path?" If no, patch it before asking the next question.

### 24. Don't passively accept a subtraction — stress-test the replacement before closing the round

When the user removes something from a plan/structure/list ("drop that section", "cut that story", "we don't need that anymore"), the default response is often to just remove it and move on. That's a §12 violation dressed up differently: instead of asking "what fills the gap you just opened?", you close the round on the subtraction alone.

Real callout (2026-07-25, GTV 2026 article structuring): agent proposed 6 article sections, Akash said "we're even okay with 5 - unless you have a good replacement in mind." Agent closed the round on "OK, 5 sections" without ever surfacing what a 6th could be. Two turns later Akash pushed back: *"we removed one section right? you didn't even discuss if we're replacing it with another one or if we're fine with just 5 sections?"* — the "unless you have a good replacement" clause had been ignored, not answered.

**Rule:** when the user removes something, treat it as an open slot until you've done ONE of:
1. **Surfaced a candidate replacement** with grounding from the source files, and let the user reject it explicitly. This satisfies §12 (opinionated claim, not menu).
2. **Made an explicit claim that no replacement exists**, with grounding for why (audited the sources against the remaining structure, no distinct new category fits). The user reacts to the claim, not to the silent absence.

The failure mode this catches: closing a round on removal alone, when the user's phrasing ("we're fine with 5 unless...") was implicitly asking you to stress-test the 6th.

**Signal you're about to make this mistake:** the user's message ends with a conditional clause ("unless X", "if there's a good Y", "assuming Z") and you responded only to the first half. The conditional clause IS the grilling prompt — answer it.

### 16. Don't mark an open follow-up "resolved" when the user gives you rich new signal — carry it forward for grilling

When the user offers a substantive new answer (a friend-message, a values statement, a lived experience) that connects to an open follow-up question in the decision log, resist the pull to say "this cleanly resolves that." Especially don't do it if the "resolution" downgrades an axis the user has weighted heavily elsewhere. Almost always the new signal adds a NEW axis or reframes the old question — it doesn't collapse into a clean answer to the old one.

**Log it as carry-forward context** with an explicit "NOT resolved — grill next round on X" note. Explicitly list the sub-questions that need grilling before it can close. Do NOT retroactively downgrade any axis the user has scored elsewhere without their explicit sign-off.

Real failure (2026-07-21, Volaris career-optionality log): user shared a friend-message saying "I want to maximise prestige AND push comp hard." The agent marked this as "cleanly resolves the party-conversation vs operator-credibility follow-up in favour of the former" and retroactively downgraded the consulting-flywheel axis (previously Volaris's biggest advantage in Decision 6 of the paired offer-comparison log). User pushed back same turn: *"it doesn't in fact map cleanly and we shouldn't mark it as resolved without further grilling... consulting is also important. It's all about where the £££ are coming from."* The real axis was money-source-diversification (brand → next FTE role + consulting → side income), not either/or. The retroactive downgrade had to be retracted in both files. Cost: two log files needed correcting-notes explaining why the prior turn's downgrade was wrong.

**When this happens, same-turn:** retract the downgrade in every file it was applied to, log the retraction visibly (strike-through + "[RETRACTED — overstated]" marker), and add the new grilling questions to the "when this reopens" list. Don't quietly delete the wrong turn's work — keep the trail visible so the next reader sees what happened.


