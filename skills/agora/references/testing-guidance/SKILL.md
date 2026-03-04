---
name: agora-testing-guidance
description: |
  Mocking patterns and testing requirements for Agora SDK integration code.
  Covers RTC Web, RTC React, RTC iOS, RTC Android, and ConvoAI REST API.
  Use when generating tests for any Agora integration, or when reminding the user
  to add tests to an implementation.
license: MIT
metadata:
  author: agora
  version: '1.0.0'
---

# Agora Testing Guidance

Mocking patterns and completeness requirements for Agora SDK integration code.

## When to Generate Tests

Every code generation task that produces implementation code must include test stubs.
If the user asks to "implement" something, remind them to generate tests before the
task is complete. Do not mark an implementation task as done until tests are addressed.

See the [Completeness Gate](#completeness-gate) section for the reminder template.

## Mocking Patterns

### RTC Web (`agora-rtc-sdk-ng`)

Mock at the module boundary. The key interfaces to mock:

- `AgoraRTC.createClient()` → mock client with `join`, `leave`, `publish`, `subscribe`
- `AgoraRTC.createMicrophoneAudioTrack()` / `createCameraVideoTrack()` → mock tracks
- `client.on(event, handler)` → capture event handlers for test assertions

Pattern: use Jest's `jest.mock` with a manual mock file.

```javascript
// __mocks__/agora-rtc-sdk-ng.js
const mockClient = {
  join: jest.fn().mockResolvedValue(undefined),
  leave: jest.fn().mockResolvedValue(undefined),
  publish: jest.fn().mockResolvedValue(undefined),
  subscribe: jest.fn().mockResolvedValue(undefined),
  on: jest.fn(),
  off: jest.fn(),
};

const mockTrack = {
  play: jest.fn(),
  stop: jest.fn(),
  close: jest.fn(),
  setEnabled: jest.fn().mockResolvedValue(undefined),
};

const AgoraRTC = {
  createClient: jest.fn().mockReturnValue(mockClient),
  createMicrophoneAudioTrack: jest.fn().mockResolvedValue({ ...mockTrack }),
  createCameraVideoTrack: jest.fn().mockResolvedValue({ ...mockTrack }),
};

module.exports = AgoraRTC;
module.exports.default = AgoraRTC;
```

In tests, call `jest.mock('agora-rtc-sdk-ng')` at the top of the file to activate the
manual mock automatically.

### RTC React (`agora-rtc-react`)

Mock at the hooks boundary. `agora-rtc-react` wraps `agora-rtc-sdk-ng` — mock the
hooks directly rather than re-mocking the underlying SDK.

Pattern: mock the `agora-rtc-react` module and wrap components under a mock provider.

```javascript
// In your test file
jest.mock('agora-rtc-react', () => ({
  AgoraRTCProvider: ({ children }) => children,
  useLocalMicrophoneTrack: jest.fn().mockReturnValue({
    localMicrophoneTrack: null,
    isLoading: false,
    error: null,
  }),
  useLocalCameraTrack: jest.fn().mockReturnValue({
    localCameraTrack: null,
    isLoading: false,
    error: null,
  }),
  useRemoteUsers: jest.fn().mockReturnValue([]),
  useJoin: jest.fn().mockReturnValue({ isConnected: false, isLoading: false }),
  usePublish: jest.fn(),
}));
```

For integration tests that need real hook behavior, wrap the component under a real
`AgoraRTCProvider` with a mocked `IAgoraRTCClient` injected as the `client` prop.

### RTC iOS (Swift)

Use protocol-based injection. `AgoraRtcEngineKit.sharedEngine(withAppId:delegate:)`
is a singleton — wrap it behind a protocol to enable mocking.

Pattern:

```swift
// Define the protocol
protocol RtcEngineProtocol: AnyObject {
    func joinChannel(byToken token: String?,
                     channelId: String,
                     uid: UInt,
                     mediaOptions: AgoraRtcChannelMediaOptions) -> Int32
    func leaveChannel(_ leaveChannelBlock: ((AgoraChannelStats) -> Void)?) -> Int32
    func enableVideo() -> Int32
    func muteLocalAudioStream(_ mute: Bool) -> Int32
}

// Make the real engine conform
extension AgoraRtcEngineKit: RtcEngineProtocol {}

// In your class, inject via initializer
class RtcManager {
    private let engine: RtcEngineProtocol
    init(engine: RtcEngineProtocol = AgoraRtcEngineKit.sharedEngine(
        withAppId: Config.appId, delegate: nil)) {
        self.engine = engine
    }
}

// In tests
class MockRtcEngine: RtcEngineProtocol {
    var joinChannelCallCount = 0
    func joinChannel(byToken token: String?, channelId: String,
                     uid: UInt,
                     mediaOptions: AgoraRtcChannelMediaOptions) -> Int32 {
        joinChannelCallCount += 1
        return 0
    }
    // ... implement remaining protocol methods
}
```

### RTC Android (Kotlin)

Use interface extraction with Mockito. `RtcEngine.create(context, appId, handler)`
is a factory method — wrap it behind an interface to enable mocking.

Pattern:

```kotlin
// Define the interface
interface RtcEngineInterface {
    fun joinChannel(token: String?, channelName: String, uid: Int,
                    options: ChannelMediaOptions): Int
    fun leaveChannel(): Int
    fun enableVideo(): Int
    fun muteLocalAudioStream(mute: Boolean): Int
}

// Adapter wrapping the real engine
class RtcEngineAdapter(private val engine: RtcEngine) : RtcEngineInterface {
    override fun joinChannel(token: String?, channelName: String,
                              uid: Int, options: ChannelMediaOptions) =
        engine.joinChannel(token, channelName, uid, options)
    // ... delegate remaining methods
}

// In tests (using Mockito)
val mockEngine = mock(RtcEngineInterface::class.java)
`when`(mockEngine.joinChannel(any(), any(), any(), any())).thenReturn(0)
```

Add `testImplementation 'org.mockito:mockito-kotlin:5.+'` to `build.gradle`.

### ConvoAI REST API

Mock at the HTTP client layer. ConvoAI integration generates REST calls — mock the
HTTP client, not the Agora SDK.

**Python** — use `unittest.mock.patch`:

```python
from unittest.mock import patch, MagicMock
import pytest

@patch('requests.post')
def test_create_agent(mock_post):
    mock_post.return_value = MagicMock(
        status_code=200,
        json=lambda: {"agent_id": "agent_abc123", "status": "STARTING"}
    )

    from your_module import create_agent
    result = create_agent(channel="test-channel", uid="42")

    assert result["agent_id"] == "agent_abc123"
    mock_post.assert_called_once()
    call_kwargs = mock_post.call_args
    assert "Authorization" in call_kwargs.kwargs.get("headers", {})
```

**JavaScript/TypeScript** — use `jest.spyOn` on `global.fetch`:

```javascript
beforeEach(() => {
  jest.spyOn(global, 'fetch').mockResolvedValue({
    ok: true,
    json: async () => ({ agent_id: 'agent_abc123', status: 'STARTING' }),
  });
});

afterEach(() => jest.restoreAllMocks());

test('createAgent sends correct request', async () => {
  await createAgent({ channel: 'test-channel', uid: '42' });
  expect(fetch).toHaveBeenCalledWith(
    expect.stringContaining('/agents/join'),
    expect.objectContaining({ method: 'POST' }),
  );
});
```

If using `axios` instead of `fetch`, use `axios-mock-adapter` or mock `axios.post`
with `jest.spyOn(axios, 'post')`.

## Completeness Gate

When generating an implementation, append the following reminder after the code block:

```text
> **Testing:** The above implementation is not complete without tests.
> Generate unit tests that verify: [list specific behaviors from the implementation].
> See `references/testing-guidance/SKILL.md` for mocking patterns.
```

Substitute `[list specific behaviors]` with the concrete behaviors the tests should
cover — for example:

- "join is called with the correct channel name and UID"
- "agent_rtc_uid is passed as string, not integer"
- "acquire is called before start; start is not called if acquire fails"

Do not leave the completeness gate as a generic reminder. Make it specific to the
implementation just generated.
