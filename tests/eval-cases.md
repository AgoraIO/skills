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
- Pass Criteria: Does not go through `intake/SKILL.md` first when the request is already clearly ConvoAI-specific
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

### C-13: Quickstart vendor defaults come from the Python SDK

- User Input: "I want the fastest way to get ConvoAI working"
- Expected Behavior: Quickstart anchors on the documented Python SDK first-success combo
- Pass Criteria: Mentions Deepgram STT with `language=\"en-US\"`, OpenAI LLM with `model=\"gpt-4o-mini\"`, and ElevenLabs TTS with `model_id=\"eleven_flash_v2_5\"` plus `sample_rate=24000`

### C-14: Sample-aligned env names are preserved

- User Input: "Use the official full-stack Next.js quickstart"
- Expected Behavior: Keeps the official sample env names instead of inventing provider-placeholder env vars
- Pass Criteria: Uses `LLM_API_KEY` / `LLM_URL` for the sample-aligned path; does not replace them with `OPENAI_API_KEY` / `OPENAI_BASE_URL`

---

## 3. Failure Paths (F-series)

### F-01: Vague request — no product specified

- User Input: "Build me an AI assistant for my app"
- Expected Behavior: Does not generate code immediately; routes through `skills/agora/intake/SKILL.md` for needs analysis
- Pass Criteria: Does not fabricate an Agora product choice; acknowledges ambiguity
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
- Expected Behavior: Treats this as `integration`, not a completed baseline
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

---

## Evaluation Log

| Date | Skill Version | Pass | Fail | Failed Cases | Fix Actions |
|------|--------------|------|------|-------------|-------------|
| | | | | | |
