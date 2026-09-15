---
name: pr-description
description: Write or revise a pull request or merge request description, or a commit message body. Load before drafting any PR/MR body, when rewriting one that reads as padded or unclear, and when a reviewer calls a description slop. Covers what to lead with, what to cut, and how to frame severity honestly. For voice (British English, no em-dashes, no bold-heading bullets) load writing-style as well.
---

How to write a pull request description someone can review from.

The audience is a reviewer deciding what to look at and what to trust. Everything in the description either helps them do that or is padding. This is a different job from a blog post or an outreach message, so voice rules live in `writing-style` and the repository's own conventions live in `AGENTS.md`; both still apply on top of this.

Read the project `AGENTS.md` first. It carries the non-negotiables: lead with the functional change, no ceremonial section headers, name the file or command on first mention, plain English over shorthand, no invented bracket prefixes in the title, and do not restate a scope decision that was settled earlier. What follows are the failure modes that survive all of that and still read as slop.

### Open on the human consequence, never on commit accounting

The first paragraph must say what stopped working for a person and what it cost. Counting commits, listing filenames, and classifying which commits are tests are all orientation for the author, not the reader, and they push the point below the fold.

**Before:**
> Issue #64 stopped invite links losing their referral credit at the members-only gate, and shipped no tests. Its verification table came from curling the production domain, so nothing in `tests/` stops the next edit to `middleware.ts` or to `PUBLIC_PATHS` in `lib/publicRoutes.ts` from putting the bug straight back. Four of the six commits here are tests only...

**After:**
> Members invite people with a link like `example.com/join?ref=member`. The referral parameter credits the referring member when someone signs up.

**Rule:** if the opening paragraph contains a commit count, a test-versus-code split, or more than one file path, it is the wrong opening. Rewrite until a reader outside the codebase knows what broke and why it mattered.

### Cut the bug's triage history

How a bug was first reported, who misdiagnosed it, and why it looked like something else belong in the issue. A pull request that fixes or tests the thing does not need the story. It reads as narrative padding because it changes nothing about how to review the diff.

Keep only the part that justifies the work, usually the blast radius, and keep it as a clause rather than a paragraph.

**Before:** a paragraph explaining the bug was reported as working on a laptop but not a phone, that this made it sound like a mobile problem, and that the real difference was the session cookie.

**After:** "That was everyone an invite is aimed at, since nobody following one has an account yet."

**Rule:** no paragraph about how a bug was discovered, reported, or misread. If severity needs establishing, one clause does it.

### Never explain framework mechanics before the consequence

Naming the language or framework behaviour behind a bug (`String()` on an array, how the router hands over a repeated parameter) explains the how to someone who has not yet been told the what. Usually the mechanics can be cut entirely; the diff shows them.

**Before:**
> `/join?ref=a&ref=b` forwarded `ref=a,b`, which is not a call-sign anybody holds, so that sign-up credited nobody. Next hands a repeated query parameter over as an array and `app/join/page.tsx` called `String()` on it.

**After:**
> `/join?ref=a&ref=b`, carrying the referrer twice, forwarded the two joined together as `ref=a,b` rather than picking one, so neither got the credit.

**Rule:** describe the observable wrong outcome. Mention the mechanism only if a reviewer cannot evaluate the fix without it.

### Say when an edge case actually fires, without inflating or dismissing it

Two opposite errors, and correcting the first tends to cause the second.

Inflating: writing up an input nothing in the product can produce as though it were live, which oversells the work and misleads whoever is judging priority.

Dismissing: over-correcting into "this guards a malformed input rather than a fault anyone is known to have hit", which reads as admitting the change is pointless. If a reader's response is "then why are we doing this?", the framing has failed even when every word is true.

The escape is to frame by what was wrong in the code, not by whether a user hit it. Unreachable-today and wrong-anyway are both true at once, and the second is the reason the change exists.

**Before (dismissive):**
> `/join?ref=a&ref=b` forwarded `ref=a,b`, so neither got the credit. Nothing the app builds produces a link like that, so this guards a hand-edited or mangled one rather than a fault anyone is known to have hit.

**After (frames the defect, keeps the honesty):**
> `app/join/page.tsx` declared its parameters as `{ ref?: string; c?: string }`, but Next hands a repeated parameter over as an array, so the route claimed a guarantee the framework does not make... No invite the app builds carries a duplicate parameter, so no member is known to have lost credit this way; the route was still asserting something untrue about its own inputs.

**Rule:** answer "what produces this input?" for every defect claimed, and pair it with what was actually incorrect (an unsound type, a duplicated rule, a broken invariant). Reachability goes in a trailing clause, never in the topic sentence. Before calling any of your own work merely defensive, check whether it is really a soundness fix described badly.

### Put the reviewer's orienting fact first, not last

"This preserves behaviour" is the single most useful sentence for whoever reads the diff, because it tells them what not to look for. Tacked onto the end of a paragraph it arrives after they have already gone looking.

**Rule:** lead each section with its behavioural claim. "One is a deduplication, with no behaviour change" before the explanation, never after it.

### Focus on the conceptual shift, not code-level minutiae

For refactors, migrations, and infrastructure changes, the description must explain what the change fundamentally means for developers, CI, and the architecture (e.g. uniting three separate mini-repos under a single monorepo interface; replacing polling with reactive webhooks).

Do not drown the reviewer in a laundry list of line edits, deleted files, or bookkeeping details (e.g. detailing every line of `.dockerignore` changed or listing every regex tweak). The diff shows the code; the description explains the mental model and the functional impact.

**Before:**
> `server/Dockerfile` changes its context, copies `.npmrc`, runs `npm ci -w server`, and moves `WORKDIR`. Then `docker-compose.yml`, `staging.yml`, and `local.yml` update `context: .` with `dockerfile: server/Dockerfile`. Then `server/.dockerignore` is deleted and `.dockerignore` gains entries for `docs`, `adr`, `coverage`, and `logs`...

**After:**
> This unites the three separate mini-repos we previously maintained (frontend, backend, and Cloudflare Worker) under a single monorepo interface using npm workspaces. A single `npm i` or `npm ci` at the root now provisions all dependencies, while service boundaries remain intact: production Docker images use workspace-scoped installs (`npm ci -w server`) so worker tooling never leaks into backend images.

**Rule:** if a paragraph reads as a prose narrative of git diff chunks rather than an explanation of the architectural shift and its functional consequences, zoom out. Explain the model, not the bookkeeping.

### Never name the review tooling

No skill names, no slash commands, no reporting that a tool was unavailable or refused to load. Describe what the review looked for and what it found: "reviewing for tests that pass for the wrong reason found X". A note that some tool could not be loaded is the author's problem, not the reviewer's.

Do not create a `## Review` section in the description summarizing what `/code-review`, `jimi-review`, or automated reviewers found. Review findings are incorporated directly into the commits before opening the PR. The reviewer cares about the final state of the code, not a diary of the author's iterations with review tools.

### Do not publish a specific you could not verify

If a detail resisted checking, write only what is certainly true rather than the plausible version. "Neither `a` nor `b` gets the credit" is verifiable; naming the exact value that ends up stored, when the check kept failing, is a guess dressed as fact.

**Rule:** any precise value, count or identifier in a description must have been observed. Otherwise state the weaker claim that holds.

### Say what the tests cannot reach, then go and check it by hand

A test plan listing only the commands that ran invites the obvious question: does this hold in the real thing? Unit tests that call a route handler or a middleware function directly bypass the framework's routing, the real redirect, and the served markup, so a green suite is compatible with a broken page.

Name that boundary in the description, then close it yourself with curl or a browser against a built server and put the results in a table or concise bullet list. This is not padding, because each row covers something the suite provably cannot: the route matcher that decides whether middleware runs at all, the rendered HTML rather than a component prop, a real status code rather than an assertion about a mocked function.

State plainly whether the manual pass re-runs in CI. If there is no end-to-end harness, say so, so nobody reads the table as a standing guarantee.

**Rule:** before writing the test plan, ask what the tests stub or call directly, and treat every answer as something to verify by hand and report. Never claim end-to-end coverage that unit tests do not provide; equally, never leave the gap unchecked just because it is outside the diff.

### Verification belongs in the description, never as a separate PR comment

The description is the single permanent record for the reviewer. When proving a change against a real stack, a live database, or an emulator, put the commands and the observed output directly into the description's `## Verification` section.

Posting verification as an issue comment on the opened PR or MR fragments the record. Reviewers look at the description first to decide whether to trust the diff; scattering proof across the comment thread forces them to hunt through discussion to see if the branch was ever actually tested.

**Rule:** never post test plans, terminal outputs, or real-stack proof as a PR comment. Put them directly into `## Verification` in the PR body.

### One idea per clause

Compressing three ideas into a single subordinate clause reads as fluent and communicates nothing. "It was reported as working on a laptop but not a phone, because the laptop was signed in" carries the report, the misdiagnosis and the mechanism at once, and requires the reader to already know that being signed in bypasses the gate.

**Rule:** if a clause carries more than one idea, give each its own sentence or cut the ones that are not load-bearing. Usually cutting is right.

### The description is not addressed to the author

A description is the permanent record of what a change is, read later by whoever is reviewing or bisecting. A question aimed at the author does not belong in it. A section headed "A decision for you" turns the record into a message, and the moment the decision is taken the section is wrong rather than merely stale.

Open questions go to the person, in conversation. The description carries the decision and why it went that way.

**Before:**
> ## A decision for you
> The copy now matches the code. The other way to resolve it is to change the code instead. The difference is a payout, so I have not chosen.

**After, in prose, no section:**
> `components/CommunityRef.tsx` also told members a community link "does not earn personal referral credit", which was false, since the link has always carried `?ref=<member>`. It now says a join through it counts towards the community total and as one of the sharer's own referrals.

**Rule:** if a sentence asks the reader to decide something, cut it and ask them directly instead.

### Follow-ups are issue links, and only for what you did not cause

Prose follow-ups evaporate. When the description closes its issue, a paragraph of remaining work is the only place that work exists and nobody will ever find it. Open an issue and link it.

Before writing one, answer in a single word whether the thing is pre-existing or introduced. Anything the change introduced gets fixed in the branch. Only what the change did not cause earns a link.

Hedging that question is worse than answering it wrongly. "It does not make the script more dangerous per record, it routes more records into the dangerous path" answers nothing. The writes were byte-identical to the ones already on the default branch, so the answer was "pre-existing".

**Rule:** every follow-up is an issue link with a one-word verdict behind it. Confirm the issue number exists before writing it into the body rather than predicting it.

### A capability the change adds is a change, not a follow-up

Work the branch enables belongs in the list of changes. A repair script that now recognises a case it used to skip is something this change does. That nobody has run it yet is not outstanding work.

**Rule:** a follow-up is only work that outlives the merge. If the branch has already done it and somebody merely has to press the button, it is a change.

### Take severity from the source issue before amplifying it

The issue usually states its own consequence, and it is often smaller than it looks from inside the diff. "They point at no member so they count toward nobody, but they will show as ref: @join in admin" is the issue saying its own item is cosmetic. Writing that up as production work needing credentials, with a command to run, invents stakes the issue had already disclaimed.

Never put a destructive command in a description unless running it is the point of the change. It reads as an instruction and invites a copy-paste.

**Rule:** re-read the issue's own words on impact before describing what remains. If it says nothing counts those records, say nothing counts them.

### Third person, never "you"

`writing-style` makes second person the default, but that rule is for blog writing, where the reader is the person doing the thing. A description is read by a reviewer, and the person the change affects is a third party. "If you ever changed your call-sign, your profile forgot most of your friends" addresses the reviewer as though they were the member, which is both wrong and oddly chummy for a permanent record.

**Before:** "Invite 50 friends and you earn the badge. If you ever changed your call-sign, your profile forgot most of your friends, so you could have brought in 60 and be told 12."

**After:** "A member who brings in 50 verified friends earns the badge. A member who had changed their call-sign was shown fewer than they had brought in, so somebody who had brought in 60 could be shown 12."

**Rule:** write about "a member", "an operator", "a visitor". Reserve "you" for talking to the author in conversation, never in a body. Do not import `writing-style`'s second-person default into a description; take its spelling, its ban on em-dashes and its ban on bold-heading bullets, and leave the blog voice behind.

### Plain language still names the file

Cutting jargon means dropping field names, library calls and internal vocabulary a reviewer does not need (`referredByEmail`, `Promise.all`, "precedence", "surfaces"). It does not mean dropping the paths. Going plain by replacing the specifics with a summary produces something a reviewer cannot act on: "three bits of code were counting the same thing three different ways" says there is a problem somewhere and refuses to say where.

The two moves look similar and are opposites. Cut the mechanism, keep the location.

**Before (jargon):** "Both surfaces resolved `referredBy` against the member's current handle, so the resolution diverged from `/api/me`, which matches every key in `referralKeys`."

**Before (vague, over-corrected):** "Three bits of code were counting the same thing three different ways, and the two that hand out awards were getting it wrong."

**After:** "A member who had changed their call-sign was shown fewer friends than they had brought in, on their public profile (`app/profile/[handle]/page.tsx`) and on their certificate (`lib/certificateRecord.ts`). Their dashboard (`app/api/me/route.ts`) had always counted it correctly."

**Rule:** every claim about something being wrong names the file it was wrong in. Plain English describes the behaviour; the path tells the reviewer where to look. If a sentence could be about any codebase, it is too vague to be in this one's description.

### One cause is one section, and a heading names a thing

Two symptoms of one root cause make one section. Splitting them doubles the headings and leaves the reader to find the connection. A heading naming something that did not happen, such as "Route names already stored were left in place", is filler, because the absence of an event is not a finding. The cause is.

Headings also sit at one level. A `###` above the first `##` nests the most important content deeper than the sections that follow it.

**Rule:** group by cause and count the causes honestly. If merging two sections turns "three things were wrong" into two, the number was wrong. A heading names a specific thing, never a category: "Everything else preserves behaviour" is a sentence, not a section.
