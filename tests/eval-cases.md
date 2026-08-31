# Agora Skills — Eval Cases

Evaluation-driven regression testing. Run these cases after every skill change.

## Evaluation Method

For each case:

1. Send "User Input" to the model with skills loaded
2. Check if model behavior matches "Expected Behavior"
3. Mark PASS / FAIL
4. Failed cases drive skill modifications

---

## 1. Routing Accuracy (R-series)

### R-01: RTC Web

- User Input: "How do I implement a video call on Web?"
- Expected Behavior: Routes to `references/rtc/web.md`, provides initialization and track management guidance
- Pass Criteria: References `AgoraRTC.createClient`; does not route through intake
- Result: ___

### R-02: RTC iOS

- User Input: "RTC on iOS Swift"
- Expected Behavior: Routes to `references/rtc/ios.md`
- Pass Criteria: References `AgoraRtcEngineKit`; not Android or Web SDK
- Result: ___

### R-03: RTC Android

- User Input: "RTC Android Kotlin"
- Expected Behavior: Routes to `references/rtc/android.md`
- Pass Criteria: References `RtcEngine`; Kotlin syntax
- Result: ___

### R-04: RTC React

- User Input: "Agora React hooks"
- Expected Behavior: Routes to `references/rtc/react.md`
- Pass Criteria: References `agora-rtc-react` or `AgoraRTCProvider`
- Result: ___

### R-05: ConvoAI Python without a proven baseline

- User Input: "ConvoAI agent in Python"
- Expected Behavior: Routes to `references/conversational-ai/README.md`, classifies the request as quickstart/integration, and enters `quickstarts.md`
- Pass Criteria: Does not jump straight to `/join` or SDK code; asks for the next quickstart decision or anchors on an official baseline first
- Result: ___

### R-06: Server-side token generation

- User Input: "Generate an RTC token in Go"
- Expected Behavior: Routes to `references/server/tokens.md`
- Pass Criteria: Provides token generation guidance; references Go SDK
- Result: ___

### R-07: RTM Web

- User Input: "RTM messaging on Web"
- Expected Behavior: Routes to `references/rtm/web.md`
- Pass Criteria: References `agora-rtm`; not `agora-rtc-sdk-ng`
- Result: ___

### R-08: Cloud Recording

- User Input: "Record my RTC session"
- Expected Behavior: Routes to `references/cloud-recording/README.md`; presents acquire/start/stop lifecycle
- Pass Criteria: Does not confuse Cloud Recording with RTC local recording; references REST API pattern
- Result: ___

### R-09: Working baseline skips quickstart

- User Input: "My ConvoAI agent already starts successfully; now help me add transcript rendering in React"
- Expected Behavior: Skips `quickstarts.md` and routes to the relevant React client reference
- Pass Criteria: Does not re-ask baseline or readiness questions; references `agent-toolkit.md` or `agent-client-toolkit-react.md`
- Result: ___

### R-10: Supported vendor query routes to provider reference

- User Input: "What providers does Agora ConvoAI support for STT, LLM, and TTS?"
- Expected Behavior: Routes to `references/conversational-ai/README.md`, then uses the official current provider docs as the source of truth
- Pass Criteria: Starts from the local ConvoAI module, but uses live docs for the current provider matrix instead of inventing or relying on a stale local copy
- Result: ___

### R-11: MLLM request routes to ConvoAI before intake

- User Input: "I want MLLM with Gemini"
- Expected Behavior: Routes directly to `references/conversational-ai/README.md`
- Pass Criteria: Does not add an extra routing hop before going to the ConvoAI module when the request is already clearly ConvoAI-specific
- Result: ___

### R-12: Studio Agent ID request routes to ConvoAI before intake

- User Input: "I already have an Agent ID from Agora Studio Agents"
- Expected Behavior: Routes directly to `references/conversational-ai/README.md`, then into the ConvoAI quickstart Studio Agent ID branch
- Pass Criteria: Does not add an extra routing hop before going to the ConvoAI module when the request is already clearly ConvoAI-specific
- Result: ___

### R-13: Mixed CLI + ConvoAI onboarding request stays ConvoAI-first

- User Input: "Help me use the CLI to fast onboard ConvoAI"
- Expected Behavior: Routes to `references/conversational-ai/README.md` first, then uses the CLI references as a supporting readiness path
- Pass Criteria: Does not route the whole request to the standalone CLI module first; keeps the conversation in the ConvoAI onboarding flow
- Result: ___

### R-14: Existing app routes to ConvoAI integration

- User Input: "Add ConvoAI to my existing Next.js app"
- Expected Behavior: Routes to `references/conversational-ai/README.md`, classifies the request as `integration`, clones or inspects the official quickstart source in a separate folder or branch, then routes to `references/conversational-ai/integration-from-quickstart.md`
- Pass Criteria: Does not scaffold a replacement standalone app in the user's repo; does not edit the existing app before quickstart source inspection and copy map
- Result: ___

### R-15: ConvoAI architecture question routes to architecture.md

- User Input: "How does the ConvoAI call sequence work between my server, the agent, and the client?"
- Expected Behavior: Routes to `references/conversational-ai/architecture.md` (via README or directly) and explains server `/join`, client RTC/RTM join order, and agent lifecycle at a high level
- Pass Criteria: References the architecture topic file; does not invent a custom architecture or skip the server-start / client-join distinction
- Result: ___

---

## 2. Code Generation Quality (C-series)

### C-01: agent_rtc_uid type

- User Input: "Create a ConvoAI agent in Python"
- Expected Behavior: `agent_rtc_uid` is string `"0"`
- Pass Criteria: Not int `0`
- Result: ___

### C-02: remote_rtc_uids type

- User Input: Same as C-01
- Expected Behavior: `remote_rtc_uids` is `["*"]`
- Pass Criteria: Not string `"*"`
- Result: ___

### C-03: Agent name uniqueness

- User Input: Same as C-01
- Expected Behavior: Agent `name` includes a random suffix (e.g., `agent_{uuid[:8]}`)
- Pass Criteria: Not a fixed string like `"my_agent"`
- Result: ___

### C-04: Credentials not hardcoded

- User Input: Same as C-01
- Expected Behavior: AppID, Customer Key/Secret read from environment variables
- Pass Criteria: No hardcoded credential values in generated code
- Result: ___

### C-05: RTC Web autoplay restriction

- User Input: "Play audio track in RTC on Web"
- Expected Behavior: Skill reminds to call `track.play()` after a user gesture
- Pass Criteria: References autoplay restriction; does not generate code that calls `play()` without user interaction context
- Result: ___

### C-06: Next.js SSR pattern

- User Input: "Agora RTC in Next.js"
- Expected Behavior: Uses `"use client"` directive and dynamic import pattern
- Pass Criteria: Generated code matches the Web Framework Notes pattern in the skill; does not use `next/dynamic` with `ssr: false` as the recommended approach
- Result: ___

### C-07: MCP server features

- User Input: "What features could we add to an MCP server with ConvoAI?"
- Expected Behavior: Describes MCP tool patterns (`save_memory`, `search_memory`, etc.); references `server-mcp` recipe
- Pass Criteria: Does not fabricate non-existent Agora APIs
- Result: ___

### C-08: Cloud Recording acquire/start sequence

- User Input: "Show me how to start Cloud Recording"
- Expected Behavior: Presents acquire → start sequence with TTL warning
- Pass Criteria: `acquire` is called before `start`; response notes the 5-minute `resourceId` TTL; credentials sourced from environment variables
- Result: ___

### C-09: ConvoAI join request — token auth option presented

- User Input: "Generate a ConvoAI join request in Node.js"
- Expected Behavior: Presents token-based auth (`Authorization: agora token=<token>` via `buildTokenWithRtm`) as the recommended option; Basic Auth is acceptable as an alternative
- Pass Criteria: Token auth option is mentioned and explained; if token auth is used, imports `agora-token` and calls `buildTokenWithRtm`; does not present Basic Auth as the only option
- Result: ___

### C-10: ConvoAI `/update` — full params object required

- User Input: "Update the max tokens for my ConvoAI agent's LLM"
- Expected Behavior: Generated code sends the full `params` object in the update payload, not just the changed field
- Pass Criteria: Update body includes `model` alongside `max_tokens` (or notes that omitting `model` will erase it); references the "overwrites entirely" gotcha

### C-11: RTM + RTC UID consistency

- User Input: "I'm building an app with both RTC and RTM — how do I join both?"
- Expected Behavior: Uses `String(rtcUid)` as the RTM user ID after RTC join resolves
- Pass Criteria: RTM login receives `String(rtcUid)`; does not use a separate hardcoded string or numeric UID for RTM

### C-12: ConvoAI token auth is the default

- User Input: "Show me a ConvoAI join request"
- Expected Behavior: Presents token-based auth as the default; does not default to Basic Auth (Customer ID + Secret) without being asked
- Pass Criteria: `Authorization: agora token=<token>` pattern appears in the primary example; Basic Auth shown as an alternative only

### C-13: Quickstart vendor defaults come from the official sample

- User Input: "I want the fastest way to get ConvoAI working"
- Expected Behavior: Quickstart uses the provider and model values in the cloned official sample's current config.
- Pass Criteria: Does not substitute cached provider model IDs from the skill; preserves the sample's env names and inspects current sample config before describing the default pipeline.

### C-14: Sample-aligned env names are preserved

- User Input: "Use the official full-stack Next.js quickstart"
- Expected Behavior: Keeps the official sample env names instead of inventing provider-placeholder env vars
- Pass Criteria: Uses `LLM_API_KEY` / `LLM_URL` for the sample-aligned path; does not replace them with `OPENAI_API_KEY` / `OPENAI_BASE_URL`

---

## 3. Failure Paths (F-series)

### F-01: Vague request — no product specified

- User Input: "Build me an AI assistant for my app"
- Expected Behavior: Does not generate code immediately; infers ConvoAI as the primary route or asks one focused clarification if the target is still genuinely unclear
- Pass Criteria: Does not force a separate intake flow or a rigid needs-analysis template; keeps the ambiguity handling natural and minimal
- Result: ___

### F-02: MCP server unreachable

- Scenario: MCP server unreachable
- User Input: "Integrate ConvoAI in Python"
- Expected Behavior: Informs user MCP is unavailable; falls back to local references and provides fallback URL
- Pass Criteria: Does not fabricate REST API parameters; notifies user to verify against official docs
- Result: ___

### F-03: Non-existent "create channel" API

- User Input: "Create an RTC channel on Web"
- Expected Behavior: Explains that channels auto-create when the first user joins via `client.join()`
- Pass Criteria: Does not generate a fabricated "create channel" API call
- Result: ___

### F-04: No App Certificate — token security disabled

- User Input: "I don't have an App Certificate, just an App ID. Here's my code: [RTC join without token]"
- Expected Behavior: Warns the user that their project has no token security enabled; any channel can be joined by anyone without authentication; advises enabling App Certificate in Agora Console before proceeding
- Pass Criteria: Warning is issued before or instead of generating code; includes advice to enable App Certificate; does not silently generate code that passes `null` as token without the warning
- Result: ___

### F-05: Hardcoded credentials in user code

- User Input: "Here's my code: `const client = AgoraRTC.createClient(...); await client.join('my-app-id', channel, 'my-app-certificate', uid)`"
- Expected Behavior: Warns that App Certificate must never appear in client-side code; explains the token generation flow
- Pass Criteria: Warning is issued before or instead of continuing with the code; advises moving App Certificate to a server-side token generator; does not silently continue with the insecure pattern

### F-06: Non-existent product asked about

- User Input: "How do I use Agora's Cloud Recording SDK?"
- Expected Behavior: Clarifies that Cloud Recording is REST API only — there is no client SDK; describes the acquire/start/stop REST API pattern
- Pass Criteria: Does not fabricate a "Cloud Recording SDK" package or import; routes to `references/cloud-recording/README.md`

### F-07: No quickstart bypass into `/join` payload generation

- User Input: "Generate the ConvoAI /join payload for my new project"
- Expected Behavior: Enters the ConvoAI quickstart flow unless a working baseline is already confirmed
- Pass Criteria: Does not generate a `/join` payload before the baseline path and readiness gates are resolved

### F-08: No scaffold before baseline

- User Input: "Scaffold a ConvoAI backend for me"
- Expected Behavior: Explains in natural language that custom scaffolding is blocked until the official quickstart source is inspected, then gives the next official quickstart step
- Pass Criteria: Does not generate `package.json`, backend routes, UI code, SDK files, or a `/join` payload from memory; includes source/baseline status and the next official quickstart command when action is blocked

### F-09: Existing app edit is blocked before baseline

- User Input: "Add the ConvoAI route directly to my app now"
- Expected Behavior: Refuses the edit in natural language if the quickstart source has not been inspected or no copy map exists, then gives the step that unblocks it
- Pass Criteria: Does not use "policy violation" or "Track A/B" in user-visible wording; does not edit the user's app before source inspection and copy map

---

## 4. Intake Accuracy (I-series)

### I-01: AI customer service bot

- User Input: "I want to build an AI customer service bot where users call in and an AI answers"
- Expected Behavior: Enter intake; identify ConvoAI (primary) + RTC SDK (client-side companion)
- Pass Criteria: Does not generate code directly; outputs needs analysis first; explicitly notes client needs RTC SDK
- Result: ___

### I-02: Education platform with session replay

- User Input: "I want to build an online education platform with video classes and session replay"
- Expected Behavior: Identify RTC SDK (video) + Cloud Recording (replay)
- Pass Criteria: Needs analysis includes both products
- Result: ___

### I-03: Partial ConvoAI context still stays in quickstart

- User Input: "Help me integrate ConvoAI with OpenAI, Python backend, I have my credentials"
- Expected Behavior: Enters the ConvoAI quickstart flow, skips already-known fields, and asks only the next unresolved quickstart decision
- Pass Criteria: Does not generate code; does not ask a long multi-step interview; asks only for the baseline path or equivalent next gate
- Result: ___

### I-04: Clear RTC request — no intake

- User Input: "RTC Web video call"
- Expected Behavior: Routes DIRECTLY to `references/rtc/web.md`; does NOT go through intake
- Pass Criteria: Intake flow is not entered; confirms the routing non-regression for experienced developers
- Result: ___

### I-05: Cloned repo is not a working baseline

- User Input: "I cloned agent-quickstart-nextjs, but the ConvoAI agent has never connected"
- Expected Behavior: Treats this as `quickstart`, not a completed baseline
- Pass Criteria: Stays in the ConvoAI quickstart flow; does not skip directly to advanced implementation guidance
- Result: ___

### I-06: Working baseline can skip quickstart

- User Input: "Our ConvoAI baseline already works; help me add useTranscript in React"
- Expected Behavior: Skips quickstart and routes directly to React client references
- Pass Criteria: Does not ask baseline-path or readiness questions; references the client toolkit or React hooks docs
- Result: ___

### I-07: Quickstart recaps the default vendor combo

- User Input: "I want to start a new ConvoAI project with the safest default path"
- Expected Behavior: Quickstart includes the documented default provider combo instead of inventing one
- Pass Criteria: Uses the Python SDK-backed default combo; does not invent unsupported vendors or omit the key default parameters
- Result: ___

### I-08: Vendor-list question uses the dedicated file

- User Input: "Before we write code, tell me which providers are supported right now"
- Expected Behavior: Uses the local ConvoAI module first, then answers from the official current provider docs
- Pass Criteria: Does not invent a local-only provider list when the user is explicitly asking what is supported right now
- Result: ___

### I-09: Vendor gate uses explicit branching

- User Input: "I have the credentials. What provider path should I take?"
- Expected Behavior: The vendor step offers a clear default / show-list / choose-custom branch
- Pass Criteria: The prompt includes A/B/C-style branching for default combo, current official provider list, and non-default provider choice
- Result: ___

### I-10: Vendor gate distinguishes cascading vs MLLM

- User Input: "I want MLLM with Gemini"
- Expected Behavior: The vendor-selection step treats this as an MLLM path, not just a non-default TTS/LLM tweak
- Pass Criteria: The flow records or acknowledges the `mllm` mode explicitly instead of forcing the user back into the cascading default combo
- Result: ___

### I-11: Path B warns about private repo access

- User Input: "I want a separate backend and frontend baseline"
- Expected Behavior: The baseline step mentions that the preferred Python repo is private and may fall back to the public decomposed sample
- Pass Criteria: The prompt does not present Path B as if it were guaranteed-public access
- Result: ___

### I-12: Quickstart opening uses natural wording

- User Input: "I want to build a demo that talks to an agent. Help me implement it."
- Expected Behavior: The quickstart opening explains the "official sample first" idea in natural product language
- Pass Criteria: Does not use stiff phrasing like "run the baseline flow" or "anchor on a proven baseline"; instead says to first run the official sample through once and then customize the demo
- Result: ___

### I-13: Unsupported provider is stated explicitly

- User Input: "I want to use a provider that is not in the current official provider docs"
- Expected Behavior: The quickstart flow states clearly that this provider is not in the current official support list
- Pass Criteria: Explicitly says the provider is not currently documented as supported; does not continue as if it were supported
- Result: ___

### I-14: Studio Agent ID path skips provider re-entry

- User Input: "I already configured my agent in Agora Studio and I have the Agent ID"
- Expected Behavior: Quickstart switches to the Studio Agent ID branch instead of re-asking STT / LLM / TTS provider choices
- Pass Criteria: Explains the Studio Agent ID path, asks for the Agent ID or confirms the user has it, and does not reopen the default-provider prompt
- Result: ___

### I-15: Studio Agent ID is distinguished from runtime agent_id

- User Input: "I have an Agent ID from Studio"
- Expected Behavior: Quickstart clarifies that the Studio Agent ID is not the same as the runtime `agent_id` returned by `/join`
- Pass Criteria: Explicitly distinguishes the Studio Agent ID from the runtime `agent_id`
- Result: ___

### I-16: Studio Agent ID maps to pipeline_id

- User Input: "I already have the Agent ID from Agora Studio"
- Expected Behavior: Quickstart explains that the Studio Agent ID is passed using the request field `pipeline_id`
- Pass Criteria: Explicitly states `Agent ID` from Studio maps to `pipeline_id` in the request body
- Result: ___

### I-17: Studio path preserves the fixed request shape

- User Input: "Use my Agora Studio Agent ID in the start request"
- Expected Behavior: The Studio path keeps the fixed request shape with `name`, `pipeline_id`, and `properties`
- Pass Criteria: Does not replace `pipeline_id` with `agent_id`; preserves separate header token and `properties.token`
- Result: ___

### I-18: Fastest onboarding path can recommend CLI-assisted readiness

- User Input: "I want the fastest way to get ConvoAI working"
- Expected Behavior: Quickstart stays in the ConvoAI flow, but can recommend the Agora CLI as the fastest way to confirm login, project selection, feature enablement, and readiness before sample setup
- Pass Criteria: Mentions the CLI-assisted readiness shortcut before code generation; still keeps the official sample as the first end-to-end baseline
- Result: ___

### I-19: CLI-assisted readiness does not replace the working baseline

- User Input: "If `agora project doctor` is healthy, am I done with ConvoAI onboarding?"
- Expected Behavior: Clarifies that CLI readiness is only preflight and does not replace the first successful end-to-end ConvoAI session
- Pass Criteria: Explicitly says the CLI can verify readiness but cannot by itself prove the agent joins the RTC channel and completes a real conversation
- Result: ___

### I-20: Quickstart can spell out the full CLI + sample combo

- User Input: "Give me the full fastest ConvoAI onboarding flow with CLI"
- Expected Behavior: Quickstart provides a complete combined path rather than only linking out to CLI docs
- Pass Criteria: Lists an ordered CLI preflight plus sample-run sequence such as login, project create or use, `feature enable convoai`, `project doctor`, then sample clone/env/run/verify
- Result: ___

### I-21: Full-flow combo still respects baseline-path gating

- User Input: "Give me the full fastest onboarding flow"
- Expected Behavior: If the baseline path is not already obvious, quickstart asks for the baseline path first instead of dumping every full-flow combination
- Pass Criteria: Does not emit all path combinations when the request has not yet implied full-stack, separate backend/frontend, or existing-app integration
- Result: ___

### I-22: CLI shortcut does not overclaim App Certificate verification

- User Input: "Can the CLI confirm my ConvoAI project is fully ready, including App Certificate?"
- Expected Behavior: Clarifies the exact boundary of the CLI-assisted readiness step
- Pass Criteria: Says the CLI can verify login, project context, feature readiness, App ID presence, and App Certificate presence at the control-plane layer, but cannot by itself prove RTM runtime readiness or sample-ready status
- Result: ___

### I-23: Unspecified project prefers current project only if it is directly usable

- User Input: "Use the CLI to get ConvoAI working for me. I didn't specify a project."
- Expected Behavior: Quickstart checks the current selected project first, but only keeps it if it satisfies the first-success conditions
- Pass Criteria: Does not blindly continue with the current project when it lacks the required certificate / token-ready path / features
- Result: ___

### I-24: Unspecified project avoids retrofitting arbitrary old projects

- User Input: "I didn't name a project. Just get me to the fastest first-success path."
- Expected Behavior: Quickstart prefers a directly usable project or creates a dedicated new one
- Pass Criteria: Does not default to repairing arbitrary historical projects when the user did not ask for a specific one
- Result: ___

### I-25: Specified project is repaired first, then can fall back to a new project

- User Input: "Use project `my-old-project` if possible."
- Expected Behavior: Quickstart inspects and repairs the named project first, then falls back to a dedicated new project only if it still cannot satisfy first-success requirements
- Pass Criteria: Preserves the repair-first behavior for user-specified projects instead of immediately abandoning them
- Result: ___

### I-26: RTM enablement delay is treated as runtime readiness, not instant failure

- User Input: "I just enabled RTM and the first run still fails."
- Expected Behavior: Quickstart distinguishes control-plane enablement from runtime usability
- Pass Criteria: Mentions bounded wait/retry for RTM availability instead of treating the first failed run as proof of permanent misconfiguration
- Result: ___

### I-27: Proven sample bug allows minimal upstream workaround

- User Input: "The official sample starts but a bug inside the sample itself blocks first success."
- Expected Behavior: Quickstart stays on the official sample path but allows a minimal upstream-shaped workaround
- Pass Criteria: Does not jump to a self-built replacement implementation; allows only the minimal fix needed to restore the official path
- Result: ___

### I-28: First ConvoAI reply includes full baseline status

- User Input: "Help me build a ConvoAI voice agent"
- Expected Behavior: First ConvoAI reply includes the official template, exact next command or next setup step, full `baseline_gate`, and `blocked` status
- Pass Criteria: Uses checkmark glyphs for baseline status instead of raw booleans; does not generate custom code or app scaffolding
- Result: ___

### I-40: Starting from scratch customizes agent prompt in quickstart

- User Input: "Start from the official quickstart and make the agent a Spanish-speaking sales coach with this prompt: ..."
- Expected Behavior: Clones or opens the official quickstart, then updates the documented agent prompt/greeting/persona or join/config details inside the quickstart source
- Pass Criteria: Preserves the sample architecture, env names, token flow, lifecycle, and documented commands; does not self-build a replacement app
- Result: ___

### I-41: ERR_PNPM_IGNORED_BUILDS falls back without changing the quickstart

- User Input: "`pnpm install` finished adding packages but exited 1 with `[ERR_PNPM_IGNORED_BUILDS]` for esbuild, sharp, and unrs-resolver. What next?"
- Expected Behavior: Runs `pnpm dev` once, then switches to the standard npm scripts only if pnpm prevents Next.js from starting with the same error
- Pass Criteria: Uses `npm install --package-lock=false` followed by `npm run dev` when fallback is needed; does not run `pnpm approve-builds`, edit `package.json`, create `pnpm-workspace.yaml`/`pnpm.yaml`, or change global pnpm build settings; verifies the local page with a real GET
- Result: ___

### I-42: Expand exported Agora credentials into quickstart env file

- User Input: "AGORA_APP_ID and AGORA_APP_CERTIFICATE are already in my shell. Write the Node quickstart `.env.local` and start the dev server."
- Expected Behavior: Writes `.env.local` with resolved `NEXT_PUBLIC_AGORA_APP_ID` and `NEXT_AGORA_APP_CERTIFICATE` values (not literal `$AGORA_APP_ID` placeholders), then runs the documented start command
- Pass Criteria: Env file contains non-empty concrete values; does not leave shell-variable names as literal text in the file; starts with `pnpm dev` and uses the I-41 npm fallback only if pnpm prevents Next.js from starting
- Result: ___

### I-29: Recovery after custom-server deviation

- User Input: "You already built me a custom ConvoAI server, but the official sample never worked"
- Expected Behavior: Acknowledges the deviation in natural language, stops the custom path, emits current `baseline_gate`, and proposes the next official sample command
- Pass Criteria: Does not continue editing the custom server; does not use "policy violation" phrasing in the user-visible response
- Result: ___

### I-30: Copy map before existing-app edits

- User Input: "The quickstart works now; integrate it into my existing app"
- Expected Behavior: Produces a copy map with source quickstart files, destination app files, and adaptation notes before editing the user repo
- Pass Criteria: Does not edit the existing app until the copy map exists and is approved or the user explicitly says to proceed
- Result: ___

### I-31: Routine quickstart reply has no footer

- User Input: "What does the baseline prove?"
- Expected Behavior: Answers the question naturally
- Pass Criteria: Does not include a full status footer because no state changed and the user did not ask for status
- Result: ___

### I-32: Gate flip emits one-line status

- User Input: "The quickstart repo is cloned now"
- Expected Behavior: Marks the relevant baseline gate as advanced and emits a one-line status such as `baseline_gate: 0/4 -> 1/4; next: <command>`
- Pass Criteria: Does not dump the full footer for a simple gate flip
- Result: ___

### I-33: Status request emits full footer

- User Input: "Where are we with the ConvoAI setup?"
- Expected Behavior: Emits the full status footer on demand
- Pass Criteria: Includes official template, next command or step, all four baseline gate fields, and blocked status
- Result: ___

### I-34: Do-not-re-ask uses session memory

- User Input: In turn 1 the user says "I'm using FastAPI with Next.js"; later the agent needs the backend language
- Expected Behavior: Uses the prior user statement before workspace detection or asking
- Pass Criteria: Does not ask again for the backend or frontend stack unless the user later changed it
- Result: ___

### I-35: Conflicting frontend frameworks produce medium confidence

- User Input: "Add ConvoAI to this app" with `package.json` containing both `next` and `vite`
- Expected Behavior: Emits `app_inventory` with `detection_confidence: medium`, names both detected frontend candidates, and asks one focused question about the active app
- Pass Criteria: Does not silently choose Next.js or Vite; does not ask a broad intake questionnaire
- Result: ___

### I-36: Scan error produces low confidence

- User Input: "Add ConvoAI to this app" when a candidate config file cannot be read
- Expected Behavior: Reports which file could not be read, degrades to `detection_confidence: low`, and asks one focused question
- Pass Criteria: Does not fabricate `baseline_track` or silently guess the project structure
- Result: ___

### I-37: Multi-project workspace lists candidates before asking

- User Input: "Add ConvoAI to this repo" with `apps/web` (Next.js), `apps/api` (FastAPI), and `apps/mobile` (React Native)
- Expected Behavior: Emits `app_inventory` listing all three projects, explains that ConvoAI needs a backend plus at least one client, and asks whether to wire web+api or include mobile too
- Pass Criteria: Does not silently pick a target; does not scan or modify projects outside chosen targets
- Result: ___

### I-38: Client/backend split confirms both targets

- User Input: "Add ConvoAI to this app" with `client/` (Next.js) and `server/` (Express)
- Expected Behavior: Detects a client/backend split, explains that the backend starts the agent and the client joins RTC, then asks one question to confirm both are integration targets
- Pass Criteria: Does not ask blind "which project?"; lists detected paths and stacks before asking
- Result: ___

### I-39: Unsupported backend still uses official source first

- User Input: "Add ConvoAI to my Rails app"
- Expected Behavior: Detects Rails as an unsupported direct quickstart target, offers Python or Node as the official source/first-success baseline, then routes to `auth-flow.md` for the Rails REST integration
- Pass Criteria: Does not pretend there is an official Rails quickstart; does not generate Rails ConvoAI code from memory before inspecting the official quickstart/API source
- Result: ___

---

## 5. CLI Skill Coverage (CLI-series)

### CLI-01: Root routing for install and login

- User Input: "How do I install the Agora CLI and log in?"
- Expected Behavior: Routes to the top-level CLI module rather than RTC / ConvoAI / intake
- Pass Criteria: Uses the CLI references, recommends `curl -fsSL https://dl.agora.io/cli/install.sh | sh`, names the installed `agora` command, and includes `agora login`; does not recommend npm
- Result: ___

### CLI-02: Deprecated preview package migration

- User Input: "I still have agora-cli-preview installed. What should I do?"
- Expected Behavior: Explains the stable package migration path
- Pass Criteria: Tells the user not to use `agora-cli-preview`; routes to the current `agora` install path via the `dl.agora.io` installer; does not present the preview package as current; does not recommend `npm install -g agoraio-cli` as the replacement
- Result: ___

### CLI-03: Version-aware minimum support

- User Input: "What CLI version should I use for this skill?"
- Expected Behavior: Anchors guidance on the verified minimum version
- Pass Criteria: States Minimum CLI `0.2.1`, and that install/auth guidance was last verified against `0.2.7`; does not hand-wave with "latest"
- Result: ___

### CLI-04: Project creation guidance stays within real command surface

- User Input: "Create an Agora project for RTC and ConvoAI with the CLI"
- Expected Behavior: Uses the documented project workflow
- Pass Criteria: References `agora project create <name> --feature rtc --feature convoai` for low-level project creation, or `agora init <name> --template <template>` for full demo onboarding; does not invent unsupported flags or subcommands
- Result: ___

### CLI-05: Feature enable guidance uses real feature values

- User Input: "How do I enable ConvoAI in the CLI?"
- Expected Behavior: Uses the project feature subcommands
- Pass Criteria: Uses `agora project feature enable convoai`; only references valid features `rtc`, `rtm`, or `convoai`
- Result: ___

### CLI-06: Doctor guidance includes actual recovery commands

- User Input: "agora project doctor says my project is not ready. What next?"
- Expected Behavior: Uses the CLI doctor workflow and suggested remediations
- Pass Criteria: Mentions `agora login`, `agora project use <project>`, or `agora project feature enable convoai` where applicable; does not invent automatic healing behavior
- Result: ___

### CLI-07: Doctor deep mode is version-aware

- User Input: "What does `agora project doctor --deep` do?"
- Expected Behavior: Describes the currently verified behavior instead of promising future runtime checks
- Pass Criteria: States that deep mode runs repo-local checks such as `.agora` metadata and quickstart env consistency where applicable; does not claim it proves RTC/RTM runtime connectivity or sample-ready status
- Result: ___

### CLI-08: Agent automation prefers JSON output

- User Input: "I want an agent to call the CLI safely from scripts"
- Expected Behavior: Recommends machine-readable output and stable parsing boundaries
- Pass Criteria: Recommends `--json`, `agora introspect --json` for command discovery, `AGORA_HOME` isolation for CI/multi-agent runs, CLI readiness before mutating commands, and `agora init` examples that always include `--template`; does not tell agents to parse pretty output by default
- Result: ___

### CLI-09: Config defaults and override locations are accurate

- User Input: "Where does the Agora CLI keep its config, and can I override it?"
- Expected Behavior: Explains the config directory and override mechanism
- Pass Criteria: References the default Agora CLI config directory and `AGORA_HOME`; does not invent unrelated env vars
- Result: ___

### CLI-10: Failure path does not hallucinate missing commands

- User Input: "Can I run `agora convoai init`?"
- Expected Behavior: Rejects the invented command and routes to the real command set
- Pass Criteria: Explicitly says this is not part of the verified CLI surface; redirects to actual `agora init`, `agora quickstart`, `auth`, `config`, `project`, `project feature`, or `project doctor` commands
- Result: ___

### CLI-11: Root routing bypasses intake for clear CLI requests

- User Input: "Help me use `agora project doctor`"
- Expected Behavior: Routes directly to the CLI module
- Pass Criteria: Does not add an unnecessary routing detour; treats the request as a CLI usage question first
- Result: ___

### CLI-12: ConvoAI onboarding prep points to CLI doctor without pretending onboarding is complete

- User Input: "Before I integrate Conversational AI, what can the CLI verify for me?"
- Expected Behavior: Positions the CLI as a readiness tool, not as the whole ConvoAI workflow
- Pass Criteria: Mentions login, project selection, feature status, and `project doctor`; does not claim the CLI alone completes end-to-end ConvoAI onboarding
- Result: ___

### CLI-13: Project env is export-first

- User Input: "How do I get dotenv-style env vars from the Agora CLI?"
- Expected Behavior: Routes to the dedicated CLI env workflow and uses `agora project env` as the primary command
- Pass Criteria: Says `agora project env` prints dotenv lines to `stdout` by default and does not claim it writes `.env.local`
- Result: ___

### CLI-14: Secrets require explicit opt-in

- User Input: "How do I get the app certificate from `agora project env`?"
- Expected Behavior: Explains the secret boundary for env export
- Pass Criteria: Requires `--with-secrets` before `AGORA_APP_CERTIFICATE` is exported; does not imply secrets are included by default
- Result: ___

### CLI-15: Env write chooses safe default targets

- User Input: "What's the difference between `agora project env write` and `agora quickstart env write`?"
- Expected Behavior: Distinguishes generic project dotenv writing from official quickstart template-aware env writing
- Pass Criteria: Says `project env write` writes generic `AGORA_APP_ID` / `AGORA_APP_CERTIFICATE`, while `quickstart env write` writes runtime-specific files and variable names such as Next.js `NEXT_PUBLIC_AGORA_APP_ID` / `NEXT_AGORA_APP_CERTIFICATE` or Python `server/.env` with `APP_ID` / `APP_CERTIFICATE`
- Result: ___

### CLI-16: OAuth loopback redirect mismatch guidance is host-aware

- User Input: "Agora CLI login fails with `redirect_uri mismatch`. What should I check?"
- Expected Behavior: Uses the verified loopback OAuth rule
- Pass Criteria: Mentions exact `redirect_uri` matching across authorize and token exchange, and warns not to mix `localhost` with `127.0.0.1`
- Result: ___

### CLI-17: CLI doctor is framed as control-plane readiness only

- User Input: "If `agora project doctor` is healthy, can I assume the sample will work now?"
- Expected Behavior: Keeps the CLI doctor boundary narrow
- Pass Criteria: Says `doctor` proves control-plane readiness only, not RTM runtime availability or sample-ready status
- Result: ___

### CLI-18: Undocumented CLI bootstrap shortcuts are rejected

- User Input: "Can I use `agora convoai quickstart init` or `agora project doctor all`?"
- Expected Behavior: Rejects invented CLI shortcuts
- Pass Criteria: Explicitly says these are not part of the verified CLI surface and routes the user back to real `agora init`, `agora quickstart`, `auth`, `project`, `project env`, `project feature`, and `project doctor --feature <feature>` commands
- Result: ___

### CLI-19: Repo README teaches explicit skill prompting

- User Input: "How do I tell my agent to use the Agora skill and not self-build?"
- Expected Behavior: Points to explicit prompt templates or gives equivalent wording
- Pass Criteria: Tells the user to explicitly instruct the agent to use the Agora skill, follow the official sample-first path, and avoid undocumented CLI commands or self-built first-success flows
- Result: ___

### CLI-20: Command tree discovery uses introspect

- User Input: "How can an agent discover the full Agora CLI command tree?"
- Expected Behavior: Uses the v0.2.1 machine-readable discovery path
- Pass Criteria: Recommends `agora introspect --json` for agents, mentions filtering on `headlessSafe` for non-interactive runs, and `agora --help --all` / `agora --help --all --json` for help output; does not suggest scraping pretty help as the default
- Result: ___

### CLI-21: Telemetry controls are documented

- User Input: "How do I turn off Agora CLI telemetry in automation?"
- Expected Behavior: Routes to CLI automation guidance
- Pass Criteria: Mentions `agora telemetry disable`, `agora telemetry status`, and `DO_NOT_TRACK=1`; does not invent unrelated env vars
- Result: ___

### CLI-22: Auth JSON unauthenticated state is recoverable

- User Input: "`agora auth status --json` exits 3 with AUTH_UNAUTHENTICATED. Is that fatal?"
- Expected Behavior: Interprets the documented auth state correctly
- Pass Criteria: Says this is a recoverable unauthenticated state and the next step is `agora login` or `agora login --no-browser`, not a generic CLI crash
- Result: ___

### CLI-23: Installed CLI examples do not use local binary notation

- User Input: "Show me commands for the installed Agora CLI"
- Expected Behavior: Uses installed-command examples
- Pass Criteria: Uses `agora ...` in examples, and reserves `./agora` only for a locally built binary from the CLI repository
- Result: ___

### CLI-24: CLI-only token-server setup stays out of ConvoAI routing

- User Input: "Use the Agora CLI to export env vars for my RTC token server."
- Expected Behavior: Routes to the CLI env workflow and server token reference, not the ConvoAI quickstart
- Pass Criteria: Uses `references/cli/env.md` for env export/write and `references/server/tokens.md` for token generation; does not route into ConvoAI onboarding
- Result: ___

### CLI-25: Init without template in agent mode

- User Input: "Run agora init my-demo --yes --json for me"
- Expected Behavior: Adds `--template` before running; explains non-interactive init requires an explicit template
- Pass Criteria: Does not run bare `agora init my-demo --yes --json`; includes `--template python` or `--template nextjs` (or asks which baseline applies); mentions `QUICKSTART_TEMPLATE_REQUIRED` if relevant
- Result: ___

### CLI-26: Stuck on CLI 0.1.6 upgrade path

- User Input: "agora version shows 0.1.6 and the skill says I need a newer CLI"
- Expected Behavior: Runs CLI readiness: `dl.agora.io` curl installer, then PATH re-check; does not use `--add-to-path`, invented `--force`, or npm
- Pass Criteria: Recommends `curl -fsSL https://dl.agora.io/cli/install.sh | sh`; re-verifies with `agora version` and `which -a agora`; does not offer `npm install -g agoraio-cli` as an alternate
- Result: ___

### CLI-27: PATH shadowing after install

- User Input: "I upgraded the CLI but agora version still shows 0.1.6"
- Expected Behavior: Diagnoses PATH shadowing and fixes before continuing
- Pass Criteria: Uses `which -a agora` or `where.exe agora`; references `agora doctor` PATH recovery or reordering PATH; does not uninstall automatically; uses `install.sh --uninstall` / `install.ps1 -Uninstall` or stale-binary removal only after user approval; does not continue ConvoAI/CLI workflows until version confirms the new binary
- Result: ___

### CLI-28: Python quickstart env writer

- User Input: "Seed credentials for agent-quickstart-python with the CLI"
- Expected Behavior: Uses template-aware env write
- Pass Criteria: Uses `agora quickstart env write` so `server/.env` gets `APP_ID` / `APP_CERTIFICATE`; does not use `agora project env write` alone (which writes generic `AGORA_APP_ID`)
- Result: ___

### CLI-29: Config version newer than CLI

- User Input: "agora project use fails: Config version 3 is newer than this CLI supports"
- Expected Behavior: Explains old binary vs newer config and routes through CLI upgrade
- Pass Criteria: Recognizes the `Config version N is newer than this CLI supports` error as caused by an old `agora` binary on PATH reading a config file written by a newer CLI; recommends resolving it by upgrading through the CLI readiness flow (curl install first); treats hand-editing the config file as a last resort only after backing it up; does not name a specific config schema version number
- Result: ___

### CLI-30: Upgrade in CI stays non-mutating

- User Input: "Should my GitHub Action run agora upgrade?"
- Expected Behavior: Recommends non-mutating check in CI
- Pass Criteria: Recommends `agora upgrade --check --json`; does not mutate the binary in CI unless `AGORA_ALLOW_UPGRADE_IN_CI=1` is explicitly justified
- Result: ___

### CLI-31: npm install path is declined

- User Input: "Should I install the Agora CLI with npm?"
- Expected Behavior: Declines npm and routes to the standalone installer
- Pass Criteria: Does not recommend `npm install -g agoraio-cli`; states that the published npm package is stale at `0.1.6` and below Minimum CLI `0.2.1`; recommends `curl -fsSL https://dl.agora.io/cli/install.sh | sh`; if the user already has an npm-managed install, offers `--replace-npm` on macOS/Linux or `npm uninstall -g agoraio-cli` followed by the PowerShell installer on Windows
- Result: ___

### CLI-32: Region is detected, never asked

- User Input: "Set up the Agora CLI for my project"
- Expected Behavior: Completes login without interrogating the user about regions
- Pass Criteria: Runs bare `agora login` when the repo has no `.agora/project.json` and no prior session region; does **not** ask the user to choose between `global` and `cn`; raises `--region` only when a repo binding, a prior session region, or a `PROJECT_REGION_MISMATCH` error indicates it. Scoped to *asking the user to choose* — a passing mention of regions is not a failure.
- Result: ___

### C-15: RTM token subject and RTM login identity stay aligned

- User Input: "Show me a ConvoAI browser/client setup with RTC + RTM."
- Expected Behavior: Keeps RTM login identity aligned with the RTM token subject
- Pass Criteria: Does not mint an RTM token for one identity and log RTM in as another random user ID; if the flow uses the RTC-resolved UID, the RTM identity uses `String(rtcUid)`
- Result: ___

### C-16: React RTC plus RTM uses the current public SDK surface

- User Input: "Build a React video call with RTM chat and consistent user identities."
- Expected Behavior: Routes to the React RTC and RTM Web v2 references and coordinates the resolved RTC UID with RTM login
- Pass Criteria: Uses `agora-rtc-react` and the RTM v2 surface; does not generate RTM v1 APIs; keeps the RTM token subject and login identity aligned with `String(rtcUid)`
- Result: ___

### C-17: RTC Web alternatives are not copied as duplicate declarations

- User Input: "Create an Agora RTC Web live-streaming client with screen sharing."
- Expected Behavior: Selects live mode, sets the host/audience role before joining, chooses one UID strategy, and loads the dedicated screen-sharing pattern
- Pass Criteria: Does not emit both `rtc` and `live` as duplicate `const client` declarations or both join examples as duplicate `const uid` declarations in one code path; screen sharing uses a separate client with its own matching UID and token
- Result: ___

---

## Evaluation Log

| Date | Skill Version | Pass | Fail | Failed Cases | Fix Actions |
|------|--------------|------|------|-------------|-------------|
| | | | | | |
