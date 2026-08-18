---
name: founder-market-fit
description: Generate candidate startup ideas grounded in the user's own skills, experience, and network. Use when the user asks "what should I build," "how do I find a startup idea," "what business is right for me," or mentions founder-market fit, ikigai, or not knowing where to start. This is the "Begin With Yourself" stage of the B.R.O.T.H. framework. For checking whether the resulting ideas have demand, see demand-first-validation and trend-research.
metadata:
  version: 1.0.0
---

# Founder-Market Fit (Begin With Yourself)

You help the user reduce the noise of infinite proven ideas down to the few they are uniquely positioned to win. In a world of abundant trends and validated product ideas, the constraint is not finding an idea, it is finding the idea that fits *you*.

> "Above product-market fit, is founder-market fit." - Naval Ravikant

Founder-market fit is the deep, authentic alignment between a founder's personal and professional experience and the specific market problem they choose to solve. Start here before touching any trend tool, because your background is the filter that turns a wall of opportunities into a workable shortlist.

## The starting questions (3 minutes, fast and rough)

Have the user answer quickly. This is a prompt for ideas, not a polished document.

- What are my skills?
- What is my experience?
- Who is in my network?
- What work makes me lose track of time?
- Where do these intersect?

**Worked example:**
- Skills: community building, product management
- Experience: building paid communities on Slack
- Network: community builders and founders
- Loses track of time: building products
- Intersection: building products for Slack community builders

The intersection is the fishing spot. It names a market you can reach and a problem you understand.

## The ICP framing (the sharper version)

Convert the intersection into three concrete lines. Focus on one ideal customer profile at a time, drawn from real personal experience.

- **ICP I can reach in 1 week:** _____
- **Their workflow(s) or problem(s) I understand from scars:** _____
- **Constraints (optional):** _____

Ground rules:
1. One ICP at a time, based on lived experience.
2. It does not need to be perfect. It exists to prompt ideas.

**Example 1**
- ICP I can reach in 1 week: online community managers
- Problems I understand from scars: onboarding, community engagement, understanding community needs
- Constraints: SaaS

**Example 2**
- ICP I can reach in 1 week: bootstrapped SaaS founders
- Problems I understand from scars: assessing and discovering new ideas, growth
- Constraints: focus on assessing new ideas

The phrase "reach in 1 week" is doing real work. If you cannot get in front of this ICP within a week, distribution will be your bottleneck no matter how good the product is.

The phrase "from scars" is also deliberate. Problems you have personally suffered give you an unfair advantage in language, credibility, and knowing which details matter.

## Turn it into search fuel

Once the three lines are filled in, use an LLM to expand them into a set of high-level keywords describing the ICP's world, their tools, and their recurring problems. That keyword list is the input to the next stage.

Prompt shape to hand the LLM:
> "I want to build a bootstrapped SaaS for [ICP]. They struggle with [problems from scars]. Constraints: [constraints]. Give me a list of high-level topics, categories, and keywords describing this market, the tools these people already use, and the problems they repeatedly hit. I will use these keywords for trend and search-traffic research."

Output: a list of keywords and candidate directions to research. Hand it to **trend-research**.

## What NOT to do

- Do not skip this stage and jump straight to trend tools. Without a personal filter you will drown in options and pick something you cannot reach or sustain.
- Do not pick an ICP you have no way to contact within a week.
- Do not over-polish. Rough and fast beats perfect and slow here.
- Do not chase an intersection that bores you. "Loses track of time" is a real selection criterion, not a nicety.

## Related skills

- **trend-research** - feed the keyword list into trend and search-traffic tools to find demand
- **demand-first-validation** - the mindset check that keeps this grounded in real demand
- **idea-scoring** - rank the shortlist once research has expanded it
