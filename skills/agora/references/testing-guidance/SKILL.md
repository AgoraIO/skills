---
name: agora-testing-guidance
description: |
  Mocking patterns and testing requirements for Agora SDK integration code.
  Covers RTC Web, RTC React, RTC iOS, RTC Android, RTC React Native, RTC Flutter,
  RTM Web, RTM iOS, RTM Android, and ConvoAI REST API.
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

### RTC React Native (`react-native-agora`)

Mock at the module boundary using `jest.mock`. The engine is created via `createAgoraRtcEngine()` — mock the factory and capture the registered event handler so tests can fire callbacks.

```javascript
// __mocks__/react-native-agora.js
const mockEngine = {
  initialize: jest.fn().mockResolvedValue(undefined),
  enableVideo: jest.fn().mockResolvedValue(undefined),
  startPreview: jest.fn().mockResolvedValue(undefined),
  joinChannel: jest.fn().mockResolvedValue(undefined),
  leaveChannel: jest.fn().mockResolvedValue(undefined),
  registerEventHandler: jest.fn(),
  unregisterEventHandler: jest.fn(),
  release: jest.fn().mockResolvedValue(undefined),
};

module.exports = {
  createAgoraRtcEngine: jest.fn().mockReturnValue(mockEngine),
  ChannelProfileType: { ChannelProfileCommunication: 1 },
  ClientRoleType: { ClientRoleBroadcaster: 1, ClientRoleAudience: 2 },
  RtcSurfaceView: 'RtcSurfaceView', // React Native components mock as strings
};
```

In tests, capture the event handler to simulate callbacks:

```javascript
import { createAgoraRtcEngine } from 'react-native-agora'

test('fires onUserJoined and renders remote view', async () => {
  const engine = createAgoraRtcEngine()
  // ... component renders, engine.registerEventHandler is called

  // Get the handler the component registered
  const handler = engine.registerEventHandler.mock.calls[0][0]

  // Simulate a remote user joining
  act(() => {
    handler.onUserJoined({ channelId: 'test', localUid: 0 }, 42, 0)
  })

  expect(screen.getByTestId('remote-video-42')).toBeTruthy()
})
```

`RtcSurfaceView` is a native component — render it as a string stub in Jest config (`moduleNameMapper`) or via the manual mock above.

### RTC Flutter (`agora_rtc_engine`)

Use the `mockito` package with `build_runner` to generate mocks. Inject the engine via constructor rather than calling `createAgoraRtcEngine()` directly — the factory cannot be mocked without injection.

```yaml
# pubspec.yaml
dev_dependencies:
  mockito: ^5.4.0
  build_runner: ^2.4.0
```

```dart
// test/mocks.dart
import 'package:agora_rtc_engine/agora_rtc_engine.dart';
import 'package:mockito/annotations.dart';

@GenerateMocks([RtcEngine])
void main() {}
// Run: flutter pub run build_runner build
```

```dart
// test/video_call_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'mocks.mocks.dart';

void main() {
  late MockRtcEngine mockEngine;

  setUp(() {
    mockEngine = MockRtcEngine();
    // Stub async methods
    when(mockEngine.initialize(any)).thenAnswer((_) async {});
    when(mockEngine.enableVideo()).thenAnswer((_) async {});
    when(mockEngine.joinChannel(
      token: anyNamed('token'),
      channelId: anyNamed('channelId'),
      uid: anyNamed('uid'),
      options: anyNamed('options'),
    )).thenAnswer((_) async {});
    when(mockEngine.leaveChannel(options: anyNamed('options')))
        .thenAnswer((_) async {});
    when(mockEngine.release()).thenAnswer((_) async {});
    when(mockEngine.registerEventHandler(any)).thenReturn(null);
  });

  test('joins channel with correct parameters', () async {
    // Inject mockEngine into your widget/service under test
    await myService.join(engine: mockEngine, channel: 'test', token: null);

    verify(mockEngine.joinChannel(
      token: null,
      channelId: 'test',
      uid: 0,
      options: anyNamed('options'),
    )).called(1);
  });
}
```

To simulate event callbacks, capture the `RtcEngineEventHandler` passed to `registerEventHandler` and call its methods directly in tests.

`AgoraVideoView` is a platform widget — wrap your widget under test in a `MaterialApp` and stub the view, or test logic separately from rendering.

### RTM Web (`agora-rtm`)

Mock at the module boundary. The `RTM` constructor can throw — the mock should reflect that. Capture `addEventListener` calls so tests can simulate incoming events.

```javascript
// __mocks__/agora-rtm.js
const mockRtmClient = {
  login: jest.fn().mockResolvedValue({}),
  logout: jest.fn().mockResolvedValue({}),
  subscribe: jest.fn().mockResolvedValue({}),
  unsubscribe: jest.fn().mockResolvedValue({}),
  publish: jest.fn().mockResolvedValue({}),
  addEventListener: jest.fn(),
};

const AgoraRTM = {
  RTM: jest.fn().mockImplementation(() => mockRtmClient),
};

module.exports = AgoraRTM;
module.exports.default = AgoraRTM;
```

In tests, capture event listeners to simulate incoming messages:

```javascript
import AgoraRTM from 'agora-rtm'

test('displays message when RTM message event fires', async () => {
  const client = new AgoraRTM.RTM('app-id', 'user-1')

  // ... component mounts, addEventListener is registered
  const listeners = {}
  client.addEventListener.mockImplementation((type, cb) => {
    listeners[type] = cb
  })

  // Re-render to pick up the mock
  render(<ChatComponent client={client} />)

  // Simulate incoming message
  const messageEvent = {
    publisher: 'user-2',
    channelName: 'test',
    message: 'Hello!',
    customType: 'chat.message',
  }
  act(() => {
    listeners.message(messageEvent)
  })

  expect(screen.getByText('Hello!')).toBeInTheDocument()
})
```

Test that `login` is awaited before `subscribe`:

```javascript
test('subscribes only after login resolves', async () => {
  let resolveLogin
  client.login.mockReturnValue(new Promise(r => { resolveLogin = r }))

  render(<ChatComponent />)
  expect(client.subscribe).not.toHaveBeenCalled()

  resolveLogin({})
  await waitFor(() => expect(client.subscribe).toHaveBeenCalledWith('test-channel', expect.any(Object)))
})
```

### RTM iOS / Signaling (`AgoraRtmKit`)

Use protocol-based injection. `AgoraRtmClientKit` is initialized with a delegate — define a protocol wrapping its interface and inject a mock in tests.

```swift
// RtmClientProtocol.swift
protocol RtmClientProtocol: AnyObject {
    func login(_ token: String?, completion: ((AgoraRtmErrorInfo?) -> Void)?)
    func logout()
    func subscribe(channelName: String, option: AgoraRtmSubscribeOptions?,
                   completion: ((AgoraRtmErrorInfo?) -> Void)?)
    func unsubscribe(_ channelName: String, completion: ((AgoraRtmErrorInfo?) -> Void)?)
    func publish(channelName: String, message: String,
                 option: AgoraRtmPublishOptions?,
                 completion: ((AgoraRtmErrorInfo?) -> Void)?)
    func destroy()
}

// Make real client conform
extension AgoraRtmClientKit: RtmClientProtocol {}
```

```swift
// MockRtmClient.swift (XCTest)
class MockRtmClient: RtmClientProtocol {
    var loginCallCount = 0
    var subscribeCallCount = 0
    var publishedMessages: [(channel: String, message: String)] = []
    var loginShouldSucceed = true

    func login(_ token: String?, completion: ((AgoraRtmErrorInfo?) -> Void)?) {
        loginCallCount += 1
        completion?(loginShouldSucceed ? nil : AgoraRtmErrorInfo())
    }

    func subscribe(channelName: String, option: AgoraRtmSubscribeOptions?,
                   completion: ((AgoraRtmErrorInfo?) -> Void)?) {
        subscribeCallCount += 1
        completion?(nil)
    }

    func publish(channelName: String, message: String,
                 option: AgoraRtmPublishOptions?,
                 completion: ((AgoraRtmErrorInfo?) -> Void)?) {
        publishedMessages.append((channel: channelName, message: message))
        completion?(nil)
    }

    func unsubscribe(_ channelName: String, completion: ((AgoraRtmErrorInfo?) -> Void)?) {
        completion?(nil)
    }

    func destroy() {}
}
```

```swift
// SignalingManagerTests.swift
class SignalingManagerTests: XCTestCase {
    func testSubscribesAfterLogin() {
        let mock = MockRtmClient()
        let manager = SignalingManager(rtmClient: mock)

        manager.connect(token: "token", channel: "test")

        XCTAssertEqual(mock.loginCallCount, 1)
        XCTAssertEqual(mock.subscribeCallCount, 1)
    }

    func testPublishSendsToCorrectChannel() {
        let mock = MockRtmClient()
        let manager = SignalingManager(rtmClient: mock)

        manager.sendMessage("Hello", to: "room-1")

        XCTAssertEqual(mock.publishedMessages.first?.channel, "room-1")
        XCTAssertEqual(mock.publishedMessages.first?.message, "Hello")
    }
}
```

Simulate delegate callbacks by calling them directly in tests — your `SignalingManager` should expose or accept a delegate reference for injection.

### RTM Android / Signaling (`io.agora:agora-rtm`)

Use Mockito. `RtmClient.create(config)` is a static factory — wrap it behind an interface to enable injection. Capture `ResultCallback` arguments to simulate async success/failure.

```kotlin
// RtmClientInterface.kt
interface RtmClientInterface {
    fun login(token: String, callback: ResultCallback<Void?>)
    fun logout(callback: ResultCallback<Void?>)
    fun subscribe(channelName: String, options: SubscribeOptions, callback: ResultCallback<Void?>)
    fun unsubscribe(channelName: String, callback: ResultCallback<Void?>)
    fun publish(channelName: String, message: String, options: PublishOptions, callback: ResultCallback<Void?>)
    fun release()
}

// Adapter wrapping real RtmClient
class RtmClientAdapter(private val client: RtmClient) : RtmClientInterface {
    override fun login(token: String, callback: ResultCallback<Void?>) =
        client.login(token, callback)
    // ... delegate remaining methods
}
```

```kotlin
// SignalingManagerTest.kt
@RunWith(MockitoJUnitRunner::class)
class SignalingManagerTest {
    @Mock lateinit var mockRtmClient: RtmClientInterface
    @Mock lateinit var mockEventListener: RtmEventListener

    private lateinit var manager: SignalingManager

    @Before
    fun setUp() {
        manager = SignalingManager(rtmClient = mockRtmClient)
    }

    @Test
    fun `subscribes only after login succeeds`() {
        // Capture the ResultCallback passed to login
        val callbackCaptor = argumentCaptor<ResultCallback<Void?>>()
        manager.connect(token = "token", channel = "test")

        verify(mockRtmClient).login(eq("token"), callbackCaptor.capture())
        verify(mockRtmClient, never()).subscribe(any(), any(), any())

        // Simulate login success
        callbackCaptor.firstValue.onSuccess(null)

        verify(mockRtmClient).subscribe(eq("test"), any(), any())
    }

    @Test
    fun `publishes message to correct channel`() {
        manager.sendMessage("Hello", channel = "room-1")

        verify(mockRtmClient).publish(
            eq("room-1"),
            eq("Hello"),
            any(),
            any()
        )
    }
}
```

Simulate `RtmEventListener` callbacks by calling them directly on the listener reference your manager holds:

```kotlin
@Test
fun `updates UI when message event fires`() {
    // Get the listener your manager registered
    val listener = manager.getEventListener() // expose for testing

    listener.onMessageEvent(MessageEvent().apply {
        publisherId = "user-2"
        // set message data
    })

    // Assert UI state updated
}
```

Add to `build.gradle`:
```groovy
testImplementation 'org.mockito:mockito-kotlin:5.+'
testImplementation 'org.mockito:mockito-core:5.+'
```

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

## Token Renewal

Token renewal is a required production behavior on every platform. The event fires ~30 seconds before expiry.

### Web (`token-privilege-will-expire`)

```javascript
test('renews token before expiry', async () => {
  global.fetch = jest.fn().mockResolvedValue({
    ok: true,
    json: async () => ({ token: 'new-token-xyz' }),
  })

  // Trigger the expiry event
  const handler = client.on.mock.calls.find(([e]) => e === 'token-privilege-will-expire')[1]
  await handler()

  expect(fetch).toHaveBeenCalledWith(expect.stringContaining('/token'))
  expect(client.renewToken).toHaveBeenCalledWith('new-token-xyz')
})
```

### iOS (`onTokenPrivilegeWillExpire`)

```swift
func testRenewsTokenBeforeExpiry() {
    let expectation = XCTestExpectation(description: "renewToken called")
    mockEngine.renewTokenHandler = { token in
        XCTAssertFalse(token.isEmpty)
        expectation.fulfill()
    }

    // Call the delegate method directly
    manager.rtcEngine(mockEngine, tokenPrivilegeWillExpire: "expiring-token")

    wait(for: [expectation], timeout: 1.0)
}
```

### Android (`onTokenPrivilegeWillExpire`)

```kotlin
@Test
fun `renews token when privilege will expire`() {
    val renewCaptor = argumentCaptor<String>()

    // Trigger expiry via the event handler
    val handler = manager.getRtcEventHandler()
    handler.onTokenPrivilegeWillExpire("expiring-token")

    verify(mockEngine, timeout(500)).renewToken(renewCaptor.capture())
    assertThat(renewCaptor.firstValue).isNotEmpty()
}
```

### RTM (`token-privilege-will-expire` / `onTokenPrivilegeWillExpire`)

RTM tokens expire independently from RTC tokens. Both need renewal handlers:

```javascript
// Web RTM — status event carries token expiry
test('handles RTM token expiry', async () => {
  global.fetch = jest.fn().mockResolvedValue({
    ok: true,
    json: async () => ({ rtmToken: 'new-rtm-token' }),
  })

  const statusHandler = rtmClient.addEventListener.mock.calls
    .find(([e]) => e === 'status')[1]

  await statusHandler({ state: 'TOKEN_EXPIRED', reason: 'token expired' })

  expect(rtmClient.login).toHaveBeenCalledWith({ token: 'new-rtm-token' })
})
```

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
