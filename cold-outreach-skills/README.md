# Cold Outreach Skills for AI Agents

A collection of AI agent skills for client acquisition through cold outreach, social selling, and content-led growth. Built for solo consultants, freelancers, and agency founders who want AI coding agents to help with prospecting, outreach, follow-ups, and closing.

Works with Claude Code, Cursor, Windsurf, and any agent that supports markdown skills.

Built by [Akash Joshi](https://thewriting.dev) and [Madhavi Swamy](https://github.com/madhaviswamy). Informed by [Talha Asif's](https://talhaasiif.substack.com/) playbook for scaling an agency to $1M ARR through cold outreach, and [Corey Haines'](https://github.com/coreyhaines31/marketingskills) marketing skills format.

## What are Skills?

Skills are markdown files that give AI agents specialised knowledge and workflows for specific tasks. When you add these to your project, your agent can recognise when you're working on an outreach task and apply the right frameworks, templates, and best practices.

## How Skills Work Together

Skills reference each other and build on a natural outreach workflow. Start with finding prospects, write the message, follow up, create content, and close the deal.

```
                        ┌─────────────────────────────┐
                        │     prospecting-lists        │
                        │  (systematic list-building)  │
                        └─────────────┬───────────────┘
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         ▼                            ▼                            ▼
┌─────────────────┐        ┌──────────────────┐        ┌───────────────────┐
│  keyword-search │        │  profile-         │        │  content-selling  │
│  (find people   │        │  optimization     │        │  (long-term       │
│   who need help │        │  (convert profile │        │   inbound play)   │
│   right now)    │        │   visitors)       │        │                   │
└────────┬────────┘        └──────────────────┘        └───────────────────┘
         │
         ▼
┌─────────────────┐
│    cold-dm      │
│  (write the     │
│   message)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  follow-up-     │
│  sequences      │
│  (don't give up │
│   after one)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  discovery-     │
│  calls          │
│  (close the     │
│   deal)         │
└─────────────────┘
```

See each skill's **Related Skills** section for the full dependency map.

## Available Skills

| Skill | Description |
|-------|-------------|
| [keyword-search](skills/keyword-search/) | Find people actively looking for your service right now using platform search on Twitter/X, LinkedIn, and Telegram. The fastest path to first clients. |
| [cold-dm](skills/cold-dm/) | Write cold DMs on Twitter/X, LinkedIn, and Telegram that get replies. Message structure, personalisation, platform-specific formatting, and volume targets. |
| [follow-up-sequences](skills/follow-up-sequences/) | Build multi-channel follow-up sequences that close deals. Most deals close on the 3rd-5th touch, not the first. |
| [content-selling](skills/content-selling/) | Use content to attract inbound clients without direct selling. Show don't sell. The long-term compounding play to layer on top of outreach. |
| [profile-optimization](skills/profile-optimization/) | Optimise your Twitter/X, LinkedIn, and Telegram profiles to convert visitors into clients. Your profile is your landing page. |
| [prospecting-lists](skills/prospecting-lists/) | Build qualified prospect lists from directories, databases, and community research. ICP definition, source hierarchy, and list management. |
| [discovery-calls](skills/discovery-calls/) | Run discovery calls that close deals. Call prep, the 4-phase framework (understand → prove → propose → close), pricing conversations, and follow-up. |

## Installation

### Option 1: Clone and Copy

```bash
git clone https://github.com/akash-joshi/agent-skills.git
cp -r agent-skills/cold-outreach-skills/skills/* .agents/skills/
```

### Option 2: Git Submodule

```bash
git submodule add https://github.com/akash-joshi/agent-skills.git .agents/cold-outreach
```

### Option 3: Cherry-pick Individual Skills

```bash
# Just copy the skills you need
cp -r agent-skills/cold-outreach-skills/skills/cold-dm .agents/skills/
cp -r agent-skills/cold-outreach-skills/skills/keyword-search .agents/skills/
```

## Recommended Order

If you're just starting out and need clients:

1. **profile-optimization** — fix your profile first (takes 30 minutes, pays dividends forever)
2. **keyword-search** — find people who need help right now
3. **cold-dm** — write the outreach message
4. **follow-up-sequences** — don't give up after one message
5. **discovery-calls** — close the deal when they respond
6. **prospecting-lists** — build a systematic pipeline (once manual outreach is working)
7. **content-selling** — add content as a long-term layer (once you have recurring revenue)

## Attribution

These skills are distilled from real-world outreach that generated $1M+ ARR:

- [Talha's Digest](https://talhaasiif.substack.com/) — 20 articles on cold outreach, Telegram/X/LinkedIn client acquisition, agency scaling
- [Dan Gwalter / Think Fractional](https://think-fractional.com) — fractional consulting frameworks
- Format inspired by [Marketing Skills](https://github.com/coreyhaines31/marketingskills) by Corey Haines

## Contributing

Found a way to improve a skill or have a new one to add? Open a PR. The best skills come from people who've actually done the outreach and closed the deals.

## License

MIT
