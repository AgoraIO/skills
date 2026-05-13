# Agora RTC — React

Uses the `agora-rtc-react` package, which wraps `agora-rtc-sdk-ng` with React hooks and components.

## Installation

```bash
npm install agora-rtc-react
# Since agora-rtc-react 2.x, you do not need to add agora-rtc-sdk-ng
# to your app's package.json manually.
# agora-rtc-react re-exports all agora-rtc-sdk-ng types and classes,
# so you can import AgoraRTC and its types from either package.
```

## Setup

Create the client once outside your component tree, then wrap with `AgoraRTCProvider`:

```tsx
import AgoraRTC, { AgoraRTCProvider } from 'agora-rtc-react';
import { useMemo } from 'react';

const client = AgoraRTC.createClient({ mode: 'rtc', codec: 'vp8' });

function App() {
  return (
    <AgoraRTCProvider client={client}>
      <VideoCall channel="test" token={null} />
    </AgoraRTCProvider>
  );
}
```

> For live streaming (host/audience), use `mode: "live"` instead.

> **Codec interop**: `'vp8'` and `'vp9'` scale better in multi-user calls. `'h264'` does not scale well beyond small groups. If codecs differ between Web and native clients, Agora's server transcodes transparently (works but adds latency). See [cross-platform-coordination.md](cross-platform-coordination.md) for full interop notes.

> **UID constraints**: If you pass `uid` into `useJoin`, numeric UIDs must be `0` to `2^32 - 1`; string UIDs must be ASCII and at most `255` characters. Keep UID type consistent per channel.

## Video Call Component

```tsx
import {
  LocalUser,
  RemoteUser,
  useIsConnected,
  useJoin,
  useLocalCameraTrack,
  useLocalMicrophoneTrack,
  usePublish,
  useRemoteUsers,
} from 'agora-rtc-react';
import { useState } from 'react';

function VideoCall({
  appId,
  channel,
  token,
}: {
  appId: string;
  channel: string;
  token: string | null;
}) {
  const [calling, setCalling] = useState(false);
  const isConnected = useIsConnected();

  const [micOn, setMicOn] = useState(true);
  const [cameraOn, setCameraOn] = useState(true);

  const { localMicrophoneTrack } = useLocalMicrophoneTrack(micOn);
  const { localCameraTrack } = useLocalCameraTrack(cameraOn);

  useJoin({ appid: appId, channel, token: token ?? null }, calling);
  usePublish([localMicrophoneTrack, localCameraTrack]);

  const remoteUsers = useRemoteUsers();

  return (
    <div>
      {isConnected ? (
        <>
          <LocalUser
            audioTrack={localMicrophoneTrack}
            videoTrack={localCameraTrack}
            cameraOn={cameraOn}
            micOn={micOn}
            playAudio={false}
          />
          {remoteUsers.map((user) => (
            <RemoteUser key={user.uid} user={user} />
          ))}
          <button onClick={() => setMicOn((v) => !v)}>
            {micOn ? 'Mute' : 'Unmute'}
          </button>
          <button onClick={() => setCameraOn((v) => !v)}>
            {cameraOn ? 'Hide camera' : 'Show camera'}
          </button>
          <button onClick={() => setCalling(false)}>Leave</button>
        </>
      ) : (
        <button onClick={() => setCalling(true)}>Join</button>
      )}
    </div>
  );
}
```

## Voice-Only (Audio Call)

Drop `useLocalCameraTrack` and remove `videoTrack` / `cameraOn` props:

```tsx
import {
  LocalUser,
  RemoteUser,
  useIsConnected,
  useJoin,
  useLocalMicrophoneTrack,
  usePublish,
  useRemoteUsers,
} from 'agora-rtc-react';

function VoiceCall({
  appId,
  channel,
  token,
}: {
  appId: string;
  channel: string;
  token: string | null;
}) {
  const [calling, setCalling] = useState(false);
  const isConnected = useIsConnected();
  const [micOn, setMicOn] = useState(true);

  const { localMicrophoneTrack } = useLocalMicrophoneTrack(micOn);
  useJoin({ appid: appId, channel, token: token ?? null }, calling);
  usePublish([localMicrophoneTrack]);

  const remoteUsers = useRemoteUsers();

  return (
    <div>
      {isConnected ? (
        <>
          <LocalUser
            audioTrack={localMicrophoneTrack}
            micOn={micOn}
            playAudio={false}
          />
          {remoteUsers.map((user) => (
            <RemoteUser key={user.uid} user={user} />
          ))}
          <button onClick={() => setMicOn((v) => !v)}>
            {micOn ? 'Mute' : 'Unmute'}
          </button>
          <button onClick={() => setCalling(false)}>Leave</button>
        </>
      ) : (
        <button onClick={() => setCalling(true)}>Join</button>
      )}
    </div>
  );
}
```

## Next.js / SSR

`agora-rtc-react` is browser-only. See **[nextjs.md](nextjs.md)** for the required dynamic import pattern — `next/dynamic` with `ssr: false` does not work in Next.js 14+ Server Components without extra steps.

## How the React SDK Differs from the Web SDK

The React SDK builds on `agora-rtc-sdk-ng` and handles several things automatically that require manual management in the raw Web SDK:

- **Track cleanup** — `useLocalMicrophoneTrack` and `useLocalCameraTrack` call `stop()` and `close()` automatically when the component unmounts or the track is disabled. No manual cleanup needed.
- **Channel leave** — `useJoin` leaves the channel when the second argument (`calling`) becomes `false` or the component unmounts.
- **Publish/unpublish** — `usePublish` publishes tracks when they become ready and unpublishes when they are disabled or null.
- **Remote audio playback** — `RemoteUser` plays remote audio automatically. No need to call `user.audioTrack.play()` manually.
- **Mute without stopping device** — pass `micOn={false}` / `cameraOn={false}` to `useLocalMicrophoneTrack` / `useLocalCameraTrack` to mute while keeping the device active. The hooks handle `setEnabled()` internally.

Prefer hooks and components over direct `client.*` calls in React. Drop down to the underlying `agora-rtc-sdk-ng` client (via `useRTCClient()`) only for advanced operations not exposed by the React layer.

## Official Documentation

- React Quickstart: <https://docs.agora.io/en/video-calling/get-started/get-started-sdk?platform=react-js>
- API Reference: <https://api-ref.agora.io/en/video-sdk/reactjs/2.x/>
