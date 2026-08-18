---
name: idea-scoring
description: Score and rank a shortlist of startup ideas to decide which one to build. Use when the user has several candidate ideas and asks "which idea should I pick," "how do I prioritise these," "how do I choose between ideas," or mentions scoring, ranking, or culling a list. This is the "Order & Cull" stage of the B.R.O.T.H. framework. For generating the shortlist, see founder-market-fit and trend-research. For picking the entry angle once an idea is chosen, see market-entry-strategies.
metadata:
  version: 1.0.0
---

# Idea Scoring (Order & Cull)

You help the user go from a long list of researched ideas down to the one worth building. Good techniques make finding ideas easy, sometimes too easy. This stage is the discipline that whittles the pile down to a single committed direction.

## The scoring model

Score each candidate idea from 1 to 5 on four questions. Higher is better.

1. **Biggest market size?** Is there enough demand and enough addressable spend to reach roughly $10k MRR?
2. **Lowest competition?** Is the market proven but not saturated, with a visible gap to enter through? (Some competition is good; a crowded field with no gap is not.)
3. **Most interesting?** Will you still care in 12 months? Boredom kills bootstrapped projects as reliably as no demand.
4. **Can I build it?** Does it fit your skills and constraints, or can you realistically learn what's missing?

Total the four scores per idea. Rank the list. The top one or two graduate to strategy.

## How to expand before you cull

Before scoring, widen the field so you are choosing from the best options, not the first few. Use Deep Research (or your LLM's equivalent) with the keywords and competitor list from earlier stages.

Prompt shape:
> "Here are my target market, the problems, and a list of competitors: [paste]. Do deep research to expand this into a fuller set of opportunities. For each: estimate market size and demand signals, list direct and indirect competitors, note how saturated it is and where the gaps are, and flag how hard it would be to validate and to build. End with an opinionated view of the two or three biggest opportunities and why."

Expected outputs from that research:
- Deeper competitor analysis per direction
- An opinionated view of the biggest opportunities

Then you score the expanded set, not just your original hunches.

## Validation difficulty vs execution difficulty

When ranking, weigh two different kinds of hard. An idea can be easy to validate but hard to build, or vice versa. The three archetypes:

| Entry type | Validation difficulty | Execution difficulty |
|---|---|---|
| Direct competitor (go at a proven market) | Easiest | Hardest (you must be genuinely better or cheaper) |
| Indirect competitor (adjacent market) | Medium | Medium |
| Growing trend (early mover) | Hardest (demand not yet proven) | Easiest, and first-mover advantage if you are right |

There is no free lunch: the easier something is to validate, the harder it usually is to execute against entrenched players, and vice versa. Pick the trade-off that matches your strengths, then confirm the specific angle in market-entry-strategies.

## Workflow

1. Gather surviving candidates from research.
2. Run a Deep Research expansion to widen and deepen the field.
3. Score every candidate 1 to 5 on market size, competition, interest, and buildability.
4. Overlay the validation-vs-execution trade-off.
5. Commit to the top one or two. Cull the rest without regret.

## What NOT to do

- Do not skip the expansion and score only your first three ideas. You will miss better ones.
- Do not ignore "most interesting." An idea you find dull will die of neglect.
- Do not chase the highest market-size score alone. A huge market you cannot enter or cannot stand is worthless.
- Do not keep everything. The output of this stage is a decision, not a longer list.

## Related skills

- **founder-market-fit** and **trend-research** - produce the candidates this stage ranks
- **market-entry-strategies** - choose the angle for the idea you commit to
- **ship-v1** - build the winner
- **demand-first-validation** - the mindset check underlying every score
