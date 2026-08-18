# Startup Idea Skills for AI Agents

A collection of AI agent skills for finding bootstrapped startup ideas with real, visible demand and building them. Built for solo founders, indie hackers, and bootstrappers who want AI coding agents to help them go from "I can't find an idea" to a validated shortlist and a shipped v1.

Optimised for bootstrapped, one-person-friendly ideas with a realistic path to roughly $10k MRR in 12 months. Not for VC moonshots or five-year builds with unclear demand.

Works with Claude Code, Cursor, Windsurf, and any agent that supports markdown skills.

Distilled from [Charlie Ward's](https://x.com/charlierward) Bootstrapped Startup Idea Playbook and the B.R.O.T.H. framework, built from thousands of idea conversations in his founder communities [Ramen Space](https://ramenspace.com) and IndieBeers. Structure inspired by [Corey Haines'](https://github.com/coreyhaines31/marketingskills) marketing skills format.

## What are Skills?

Skills are markdown files that give AI agents specialised knowledge and workflows for specific tasks. When you add these to your project, your agent recognises when you're working on idea generation, validation, or launch and applies the right frameworks.

## The core belief: demand first

Building in a market with no demand is like pushing water uphill. Market research decides **what** to build; user research decides **how**. Finding a competitor already building your idea is good news, it proves demand. The job is to enter a proven market from a better angle, not to invent an untouched one.

## How Skills Work Together

These skills follow the **B.R.O.T.H. framework**: Begin with yourself, Research widely, Order & cull, Tactics time, Heat & ship. Start with your own founder-market fit, research demand, rank the shortlist, pick an entry angle, and ship.

```
                    ┌──────────────────────────────┐
                    │      founder-market-fit       │
                    │   (Begin: skills, scars,      │
                    │    network → ICP + keywords)  │
                    └───────────────┬──────────────┘
                                    │
                                    ▼
                    ┌──────────────────────────────┐
                    │        trend-research         │
                    │  (Research: trends, search    │
                    │   volume → competitor list)   │
                    └───────────────┬──────────────┘
                                    │
                                    ▼
                    ┌──────────────────────────────┐
                    │         idea-scoring          │
                    │  (Order & Cull: score 1-5,    │
                    │   commit to one idea)         │
                    └───────────────┬──────────────┘
                                    │
                                    ▼
                    ┌──────────────────────────────┐
                    │   market-entry-strategies     │
                    │  (Tactics: downmarket,        │
                    │   upmarket, repurpose, early) │
                    └───────────────┬──────────────┘
                                    │
                                    ▼
                    ┌──────────────────────────────┐
                    │           ship-v1             │
                    │  (Heat & Ship: study, build   │
                    │   v1, interview users)        │
                    └──────────────────────────────┘

     demand-first-validation underpins every stage (the mindset check)
```

See each skill's **Related Skills** section for the full dependency map.

## Available Skills

| Skill | B.R.O.T.H. stage | Description |
|-------|------------------|-------------|
| [demand-first-validation](demand-first-validation/) | Mindset | The demand-first principle, the four failure modes that kill bootstrapped ideas, and the competitor reality check. Why an existing competitor is a green light. |
| [founder-market-fit](founder-market-fit/) | Begin With Yourself | Generate candidate ideas from your own skills, experience, scars, and network. Produces an ICP you can reach in a week plus a keyword list. |
| [trend-research](trend-research/) | Research Widely | Turn keywords into demand evidence using Google Trends, Ahrefs, Exploding Topics, and more. Output: a competitor list with real search volume. |
| [idea-scoring](idea-scoring/) | Order & Cull | Score a shortlist 1-5 on market size, competition, interest, and buildability. Weigh validation difficulty against execution difficulty. |
| [market-entry-strategies](market-entry-strategies/) | Tactics Time | The only four ways to enter a proven market: downmarket, upmarket, repurpose to an adjacent market, or be early to a trend. |
| [ship-v1](ship-v1/) | Heat & Ship | Study what works, build a simple v1 fast, then interview users to refine. The next-7-days checklist. |

## Installation

### npx skills (Recommended)

```bash
# Install all startup idea skills
npx skills add akash-joshi/agent-skills --skill demand-first-validation founder-market-fit trend-research idea-scoring market-entry-strategies ship-v1

# Install specific skills
npx skills add akash-joshi/agent-skills --skill founder-market-fit trend-research

# List available skills
npx skills add akash-joshi/agent-skills --list
```

Works with Claude Code, Cursor, Codex CLI, and Gemini CLI.

### Clone and Copy

```bash
git clone https://github.com/akash-joshi/agent-skills.git
cp -r agent-skills/skills/startup-ideas/*/ .agents/skills/
```

### Cherry-pick Individual Skills

```bash
cp -r agent-skills/skills/startup-ideas/founder-market-fit .agents/skills/
cp -r agent-skills/skills/startup-ideas/trend-research .agents/skills/
```

## Recommended Order

Follow B.R.O.T.H. end to end:

1. **demand-first-validation** - internalise the mindset before anything else
2. **founder-market-fit** - find the ideas only you can win (Begin With Yourself)
3. **trend-research** - prove demand and list competitors (Research Widely)
4. **idea-scoring** - rank and commit to one (Order & Cull)
5. **market-entry-strategies** - pick your winning angle (Tactics Time)
6. **ship-v1** - build it and talk to users (Heat & Ship)

## Attribution

Distilled from Charlie Ward's Bootstrapped Startup Idea Playbook, presented via [Ascend Circle](https://ascendcircle.org). Charlie runs [Ramen Space](https://ramenspace.com) (a founder coworking community, 100+ members) and IndieBeers (a 5,000-member founder meetup). Real examples referenced: Tiiny Host, Data Fetcher, and Hovercode.

- Charlie Ward on [X](https://x.com/charlierward) and [LinkedIn](https://linkedin.com/in/charlierward)
- Format inspired by [Marketing Skills](https://github.com/coreyhaines31/marketingskills) by Corey Haines

## Contributing

Found a way to improve a skill or have a new one to add? Open a PR. The best skills come from people who have actually found ideas, validated them, and shipped.

## License

MIT
