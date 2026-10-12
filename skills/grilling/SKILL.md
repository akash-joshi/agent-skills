---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases. Covers multi-round decision analysis - external-model question formation, persistent decision logs, devil's-advocate checks, and standing values instruments (values card sort, Moving Motivators).
source: https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md
---

**Canonical home:** `akash-joshi/agent-skills` repo (`skills/grilling/SKILL.md`). After updating the installed copy, sync the public copy too: clone to `/tmp`, apply the same patch, commit and push.

## Core workflow

Treat grilling as collaborative decision analysis, not a survey. Build a decision tree, identify only questions whose prerequisites are settled, and work through them in dependency order. Find facts from records or tools yourself; ask the user for decisions and experiences that only they can provide. Do not act on a proposed plan until shared understanding is confirmed.

For interpretive questions, make a concise, evidence-grounded claim with a clear point of view for the user to confirm, correct, or refine. Ask foundational factual questions without guessing the answer. Ground claims in sources you have actually read, and do not turn an inference into a fact. Keep questions compact and concrete; avoid bare menus, stale shorthand, and direct introspection questions that ask the user to do the analysis. If the user wants the verdict, stop grilling and give it.

Maintain a separate decision log for each distinct decision, appending confirmed decisions in the same turn. Keep the user's actual answer distinct from your recommendation. Resolve the deliverable itself, not only its surrounding process: do not mark it complete before the user has reviewed its actual content.

## Deck discussions

Agree the high-level message and actual beats of one slide before expanding copy or moving on. A yes to a framing or one bullet is not acceptance of the whole slide. If asked where an example belongs, answer placement without treating later slides as approved; advance on explicit acceptance or a direction such as “next slide”. Ground examples in the user's real work or an accepted hypothetical. For example, do not introduce an arbitrary report/payment scenario and let it define the talk.

When the shared deck is the decision log, apply approved content in place and append a separate Decision log section in native notes. Preserve spoken commentary and sources, mark unresolved copy provisional, and change only agreed slides. Use `collaborative-slide-editing` for native editing and verification.

## Load relevant detail on demand

Read only the references relevant to the current task. These retain specific failure examples, recovery steps, and detailed practices; do not load the entire set for unrelated work.

- `references/cost-detail-01.md` - External question formation, prompt neutrality, and incremental decision logs.
- `references/cost-detail-02.md` - Devil's advocate, values instruments, stale framings, and decision-log scope.
- `references/cost-detail-03.md` - Bias checks, grounding, factual versus interpretive questions, and review-before-completion.
- `references/cost-detail-04.md` - Evidence updates, user-state claims, data interpretation, and shared-fact verification.
- `references/cost-detail-05.md` - Delegated verdict caveats, fatigue decisions, and shifting out of grilling mode.
- `references/cost-detail-06.md` - Retiring dropped follow-ups and ending recommendations cleanly.
- `references/cost-detail-07.md` - One-at-a-time decisions, readable turns, log recovery, and testing replacements for subtractions.
- `references/cost-detail-08.md` - Carrying new signal forward without prematurely resolving open questions.

