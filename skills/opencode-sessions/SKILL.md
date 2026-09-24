---
name: opencode-sessions
description: List, create, inspect, rename, and delete local OpenCode sessions, including model-pinned runs, plan-mode agents, and parallel ticket-agent sessions
---

Manage local OpenCode sessions through the background service HTTP API.
Source behaviour is defined at https://opencode.ai/v2/docs/api/ and https://opencode.ai/v2/docs/build/client/.

The service must be reachable. Check it first:

```sh
opencode service status
opencode api get /api/info
```

Use the session routes only. Verified working against opencode v2.0.12:

## List sessions

```sh
opencode api get /api/session
```

## Create a session

```sh
opencode api post /api/session --data '{"location":{"directory":"/absolute/workdir"},"title":"short-title"}'
```

The response contains `data.id` of the form `ses_...`. Keep it for later calls.

## Get one session

```sh
opencode api get /api/session/SESSION_ID
```

## List messages in a session

```sh
opencode api get /api/session/SESSION_ID/message
```

## Rename a session

```sh
opencode api patch /api/session/SESSION_ID --data '{"title":"new-title"}'
```

An empty response body with exit code 0 means success. Confirm with a get.

## Delete a session

```sh
opencode api delete /api/session/SESSION_ID
```

An empty response body with exit code 0 means success. A later get returns `SessionNotFoundError` with HTTP 404.

## Launch a plan-mode agent

Plan is a built-in primary agent that explores and plans without editing project files, per https://opencode.ai/v2/docs/agents/. To set one off, create a session with that agent selected and then prompt it.

```sh
opencode api post /api/session --data '{"location":{"directory":"/absolute/workdir"},"title":"plan-task","agent":"plan"}'
```

This returns a `ses_...` id. Send the planning task as a prompt, which requires a `text` field:

```sh
opencode api post /api/session/SESSION_ID/prompt --data '{"text":"Explore <topic> and write a step-by-step plan. Do not edit files."}'
```

To retarget an existing session at the plan agent instead:

```sh
opencode api post /api/session/SESSION_ID/agent --data '{"agent":"plan"}'
```

Wait for the run to finish before reading results:

```sh
opencode api post /api/experimental/session/SESSION_ID/wait --data '{}'
```

Then read the transcript and take the latest assistant text as the plan:

```sh
opencode api get /api/session/SESSION_ID/message
```

Delete the session when the plan has been copied elsewhere.

## Launch with a specific model

When the user names a model, create the session first, then start its run with the CLI `--model` flag. Do not rely on a `model` object sent to `/api/session/SESSION_ID/prompt`: OpenCode 2.0.12 can accept that payload while still running the configured fallback model.

```sh
SESSION_ID=$(opencode api post /api/session \
  --data '{"location":{"directory":"/absolute/workdir"},"title":"task-title","agent":"build"}' \
  | jq -r '.data.id')

opencode run \
  --session "$SESSION_ID" \
  --model claude-code/claude-opus-5-5 \
  --agent build \
  --auto \
  "Complete the task end to end."
```

After the first assistant message appears, verify its `model.providerID` and `model.id` through `/api/session/SESSION_ID/message`. If they do not match the requested model, interrupt and delete the session, then recreate it correctly. Do not continue a wrongly modelled session and present it as compliant.

## Launch independent ticket agents

For multiple tickets, create one session per ticket. Give each a distinct title and keep its ticket scope explicit. If the ticket workflow creates worktrees, let each ticket agent create its own isolated worktree; do not point two agents at one writable worktree.

Start the model-pinned `opencode run` commands independently so one ticket does not block launching the others. Each prompt should identify the ticket, the ticket-agent instruction file, the repository rules, and the authorised completion boundary such as commits, push, draft PR or MR, recursive review, browser evidence, and CI monitoring.

Track for every run:

- ticket key
- OpenCode session ID
- requested and verified model ID
- working directory or worktree
- completion state and final PR or MR URL

When replacing a misconfigured run, interrupt its process, launch a clean replacement, verify the replacement model, and only then delete the old session.

## Notes

- Fork with `opencode api post /api/session/SESSION_ID/fork` rejects empty sessions with `empty_session`. Only fork sessions that already hold messages.
- Sending a prompt with `opencode api post /api/session/SESSION_ID/prompt` starts real model work and may incur cost. Prefer create, get, patch, and delete for safe trials.
- Every call above was verified locally with create, rename, read, and delete round-trips.
