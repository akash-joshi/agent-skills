# voicenotes-skill

A skill that connects AI agents to the [Voicenotes](https://voicenotes.com) API — search semantically, retrieve transcripts, filter by tags or date range, and create text notes through natural conversation.

Works with any AI agent that can read markdown and execute curl commands (Claude Code, OpenClaw, custom agents, etc.). 

## Install

```bash
npx skills add akash-joshi/voicenotes-skill
```

Or manually copy `SKILL.md` into your agent's skills directory.

## Setup

1. Create an integration at https://voicenotes.com/app?open-claw=true#settings
2. Copy the API key
3. Set the `VOICENOTES_API_KEY` environment variable:

```bash
export VOICENOTES_API_KEY="your_key_here"
```

## What it can do

- Semantic search across your notes
- Retrieve full transcripts for any note
- Filter notes by tags and/or date range
- Create new text notes

See [SKILL.md](SKILL.md) for full API details and response formats.
