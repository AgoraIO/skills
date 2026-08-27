# Quickstart Prompts and Output

User-facing prompts and the normalized output contract for the state machine in
[quickstarts.md](quickstarts.md). Load this file only when the current state
requires a user prompt or the resolved quickstart spec.

## Product Intro

Explain briefly that ConvoAI is a server-managed voice agent that joins an RTC
channel and usually pairs an RTC client with a backend that starts the agent.

Use a natural transition:

```text
Before we jump into custom code, let's first use the official sample to get the
whole flow working once. Once the agent can join the channel and finish one real
conversation, we can turn that working version into your demo.
```

Avoid internal phrases such as "baseline flow" or "policy violation."

## Intake

Use this only when stack preference or setup permission is unresolved:

```text
Which official quickstart should we use first: Python or Node/TypeScript?
I can check your environment and handle normal quickstart setup in one approved
scope. I will ask again before creating a project, overwriting files, exposing
secrets, installing a system runtime, or changing anything outside the selected
quickstart.
```

## Environment Check

Read the cloned sample's runtime declarations before deciding whether a runtime
or package manager is current enough. Check only the selected baseline plus the
Agora CLI.

- Node/TypeScript: `node --version`, then the package manager declared by the
  sample; use an npm fallback only when its README supports one.
- Python baseline: `python3 --version` and `bun --version`, checked against the
  sample's current declarations.
- Agora CLI: follow [CLI readiness](../cli/README.md#cli-readiness-agents),
  including its explicitly verified version floor and upgrade procedure.

Do not install or upgrade Node.js or Python automatically. Install non-system
quickstart tools only inside the user's approved setup scope.

## Project Readiness

Before the CLI sequence, tell the user:

```text
I will check Agora login, project selection, App ID, App Certificate, required
features, and the sample env file. Read-only checks come first; setup fixes stay
inside the approved scope.
```

Execute [the CLI-driven readiness check](quickstarts.md#cli-driven-readiness-check)
instead of duplicating its commands here. A healthy doctor result proves only
control-plane readiness. Continue through the sample-ready gate before claiming
the integration works.

## Vendor Defaults

Skip this prompt unless the user mentions BYOK, vendor API keys, a specific
provider, MLLM, or a Studio Agent ID.

```text
The official quickstart works with Agora credentials alone. Its checked-in
configuration defines the current default STT → LLM → TTS pipeline.

A. Use the sample defaults
B. Use my own vendor keys (BYOK)
C. Show the current official provider list
D. Choose a documented non-default cascading or MLLM path
E. Reuse an Agora Studio Agent ID
```

Never fill this prompt with model identifiers cached in the skill.

## Custom Provider

After fetching the current official provider docs, ask the user to choose only
from the provider modes and vendors documented there.

```text
Choose a documented provider path:
- Cascading: STT + LLM + TTS
- MLLM: a provider currently listed in the official docs

Reply with the provider choice for each required stage.
```

If a named provider is absent from the current docs, use:

```text
That provider is not in the current official Agora ConvoAI provider docs, so I
should not proceed as if it is supported.

A. Use the official sample defaults
B. Show the current official provider list
C. Re-check the latest docs before deciding
```

## Studio Agent ID

Use only when the user wants an existing Studio-managed agent:

```text
Open https://console.agora.io/studio/agents and copy the Agent ID for the agent
you want to reuse.

This Studio Agent ID identifies saved configuration and maps to `pipeline_id`.
It is different from the runtime `agent_id` returned when a session starts.

A. I have the Studio Agent ID
B. I need to look it up
C. Return to the sample-default/provider path
```

Do not ask the user to rebuild provider configuration that Studio already owns.

## Structured Quickstart Spec

After all gates resolve, normalize the result and continue only within the
approved setup scope:

```yaml
use_case: <summary>
mode: quickstart
official_template: <python | nextjs | go>
baseline_gate:
  quickstart_repo_cloned: true
  official_start_command_run: true
  agent_join_verified: true
  rtc_client_connected: true
project_readiness:
  app_id: <ready | missing | unknown>
  app_certificate: <ready | missing | unknown>
  convoai_activation: <ready | missing | unknown>
provider_config:
  mode: <sample-default | byok | studio | unknown>
  pipeline: <cascading | mllm | studio-managed | unknown>
  stt: <sample-default | documented-provider | not-applicable | unknown>
  llm: <sample-default | documented-provider | not-applicable | unknown>
  tts: <sample-default | documented-provider | not-applicable | unknown>
studio_agent:
  use_existing_agent_id: <yes | no>
  agent_id: <value | missing | not-applicable>
```

`studio_agent.agent_id` is the Studio Agent ID, not the runtime session ID.

## After Collection

Execute and verify the selected official quickstart. After first success, route
by the user's next request:

- Studio-managed agent → [conversational-ai-studio.md](conversational-ai-studio.md)
- provider parameters → current official provider docs
- custom LLM backend → [server-custom-llm.md](server-custom-llm.md)
- direct REST integration → [auth-flow.md](auth-flow.md)
- existing application → [integration-from-quickstart.md](integration-from-quickstart.md)
