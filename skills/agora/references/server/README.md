# Agora Server-Side

Server-side utilities for Agora — primarily token generation for secure authentication.

## When Tokens Are Needed

- **Production**: Always. Tokens authenticate users before they join channels.
- **Testing/Development**: Technically optional — token auth can be disabled in [Agora Console](https://console.agora.io), allowing `null` to be passed as the token. **Warn the user if they attempt this**: any channel can be joined by anyone without authentication. This is never acceptable for production and should be avoided even in development unless strictly necessary.
- **No App Certificate provided**: If the user has no App Certificate, they cannot generate tokens. Warn them explicitly that their project has no token security enabled, advise them to enable it in [Agora Console](https://console.agora.io) → Project Management → Edit → App Certificate, and do not proceed to generate code that omits token auth without this warning.
- **Never expose App Certificate on client**. Token generation must happen server-side.

## Token Types

- **RTC Token**: Grants access to join a specific RTC channel with a specific UID. Required for Video/Voice SDK.
- **RTM Token**: Grants access to RTM services for a specific user ID.
- **AccessToken2**: Current token format. Supports privilege expiration per service and can bundle RTC + RTM privileges in a single token.

## ConvoAI Agent Server SDKs

The TypeScript, Go, and Python SDKs are convenience wrappers around the ConvoAI REST API.
For any other backend language, call the REST API directly — fetch the live OpenAPI spec
for the full schema: `https://docs-md.agora.io/api/conversational-ai-api-v2.x.yaml`

Use these SDKs when building with TypeScript, Go, or Python to avoid writing REST boilerplate:

### TypeScript — `agora-agent-server-sdk`

```bash
npm install agora-agent-server-sdk
```

Builder pattern — configure the AI pipeline then create sessions:

```typescript
import { AgoraClient, Agent, Area } from 'agora-agent-server-sdk';

const client = new AgoraClient({
  area: Area.US,
  appId: process.env.AGORA_APP_ID,
  appCertificate: process.env.AGORA_APP_CERTIFICATE,
});

const agent = new Agent({
  name: `agent_${crypto.randomUUID().slice(0, 8)}`, // must be unique per project
  instructions: 'You are a helpful voice assistant.',
  greeting: 'Hello! How can I help you today?',
})
  .withStt(new DeepgramSTT({ apiKey: process.env.DEEPGRAM_API_KEY }))
  .withLlm(new OpenAI({ apiKey: process.env.OPENAI_API_KEY }))
  .withTts(new ElevenLabsTTS({ apiKey: process.env.ELEVENLABS_API_KEY }));

// Start a session (joins the agent to a channel)
const session = agent.createSession({ channel: 'my-channel', agentUid: 0 });
const sessionId = await session.start();

// Stop from the same process
await session.stop();

// Stop from a stateless server (e.g. a different request handler)
await client.stopAgent(sessionId);
```

Token auth is handled automatically when `appCertificate` is provided. For vendor-specific STT/LLM/TTS import paths and MLLM (OpenAI Realtime, Gemini Live) config, see the [SDK README](https://github.com/AgoraIO-Conversational-AI/agent-server-sdk-ts).

### Go / Python

- [agent-server-sdk-go](https://github.com/AgoraIO-Conversational-AI/agent-server-sdk-go)
- [agent-server-sdk-python](https://github.com/AgoraIO-Conversational-AI/agent-server-sdk-python)

## Reference Files

- **[tokens.md](tokens.md)** — Token generation for Node.js, Python, and Go. Express server example, security best practices.
- **Full token auth guide** — <https://docs-md.agora.io/en/video-calling/token-authentication/deploy-token-server.md>
