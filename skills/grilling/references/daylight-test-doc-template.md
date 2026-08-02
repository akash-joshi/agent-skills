# Daylight-test decision frame — template

Use this when the user declares "locked in" on a high-stakes irreversible decision late at night or under fatigue, and the declaration contradicts the option their own prior grilling / stated filter favours. Purpose: capture the frame so it survives to daylight and can be re-run when the fatigue clears.

Save as: `~/.cache/feedback-mirror/<decision-slug>-final-decision-frame-YYYY-MM-DD.md` (or wherever the user's decision-log home is). Sync to Dropbox. Set a Taskwarrior task for tomorrow pointing at it.

## Structure

```markdown
# <Option A> vs <Option B> — final decision frame (YYYY-MM-DD)

**State at time of writing:**
- Current status of each option (signed offer, pending, expected paperwork, etc.)
- The specific trigger that produced the "locked in" declaration (email received, hard conversation, deadline pressure, time of day)
- Explicit acknowledgement: user is currently in a fatigue window (late night / hungry / stressed). This doc exists so the decision can be re-run in daylight.

## Withdrawal / execution mechanics (already confirmed)

- List the specific mechanical facts that make it clear neither option has an artificially compressed window:
  - Notice periods, clawback clauses, financial exposure
  - Whether there are any true deadlines that force a tonight decision (there usually aren't)
- End with: "same-day rule — send withdrawal/execution the day the counter-signal arrives, not tonight, not tomorrow."

## Where <pull-option> genuinely wins

Real signals that support the current pull. Be honest and specific. Include:
- Culture / health / sustainability signals that are objectively true
- Any interview signal that specifically validated this option
- Structural advantages (stability, cross-portfolio scope, promotion cadence, etc.)
- Anything from prior grilling logs that pointed here

## Where the user's own stated filter (from prior grilling / values sort) contradicts the pull

Cite the specific filter doc by path. Walk each filter axis:
- BRAND — how do the options compare on this axis? Which one does the filter point to?
- COMP — cash-heavy floor, ideal number, actual comparison
- OPTIONALITY / recovery — which option scores better on the axis the user actually stated?

If all three axes point away from the current pull, name that explicitly. This is the point of the daylight test.

## Yellow flags the warmth is masking

Cite the specific interview review file for the pull-option. Walk the red-flags section. Include:
- Specific admissions the interviewer made that are structural risks
- Firing rates, PIP process gaps, sponsor stability, mandate durability
- Any thesis-contradicting data from the same round (e.g. cadence data contradicting the flywheel thesis)
- Modernisation-vs-greenfield split
- Reactive-vs-strategic origins of the program/team

## The daylight test

Before executing on the declaration, run this sequence in order:

1. Sleep, eat, walk before opening the decision at all.
2. Re-read the pull-option's red-flags file line by line.
3. Re-read the alternative's most honest interview (typically the offer call or a peer round).
4. Check the counter-signal paper (Volaris written offer, contract terms, etc.) against what must be true for the decision to hold — see next section.
5. If the pull still holds after all four steps, execute. Same day the counter-signal is countersigned, not later.

If any step shifts the read, don't execute. Reopen the frame instead of forcing the decision through.

## What must be true in the counter-signal for the pull to hold

List the specific things that must appear in writing / verbally / on paper for the decision to be safe:
- Comp figures matching prior verbal anchors, not the opening lowball
- Bonus formula documented, not "at discretion"
- Any moonlighting/consulting consent needed for the user's live side income
- Remote status confirmed
- Start date compatible with other commitments
- Notice period documented

If any come back weaker than expected, the "locked in" declaration is not durable — the option is worse than what tonight's Akash thinks it is.

## Sources

- List every prior grilling log, interview review, values sort, filter doc, offer letter, contract, and memory file that fed this frame
- Include specific paths so the daylight-test re-read is easy
```

## When to install this doc

Trigger signals from the user:
- "I'm locked in on X" / "I've decided X" / "I'm going with X" declared:
  - Late night (after 9pm) OR
  - Right after a rejection/counter-offer/hard-conversation trigger OR
  - Contradicting the option their own prior grilling favoured
- Combined with: no daylight decision-frame doc already exists for this pair

## What to do in the chat when the trigger fires

1. Push back explicitly with the fatigue-state observation. Name the bias vectors (certainty-over-optionality, loss aversion, recency, social-cost aversion).
2. Propose the daylight test as a concrete sequence, not vague "sleep on it."
3. Offer to write the frame doc same turn. Do it — this is a safe/reversible action, act-first-ask-after applies.
4. Set a Taskwarrior task for tomorrow so it surfaces when the actual trigger (paper offer, morning) arrives.
5. Do NOT validate the declaration ("that makes sense given the culture-fit"). Push back honestly.
6. End the session on "stop deciding tonight. Eat something and sleep."

## Anti-patterns

- Writing the frame doc but then still sending the withdrawal/execution email in the same turn "just to have it ready." No. Nothing gets sent tonight.
- Framing the daylight test as "if you still want to X tomorrow" — that's a hedge. It's "if all four steps pass tomorrow." Different rule.
- Skipping the "what must be true in the counter-signal" section. This is often the specific gate that catches the decision — the paper offer comes back weaker than the verbal anchor, and the whole calculus changes.
- Not setting a Taskwarrior task. Without it, morning-Akash forgets tonight-Akash flagged this, and the frame doc silently rots in the cache folder.
