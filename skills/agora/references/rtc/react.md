# Agora RTC — React

Uses the `agora-rtc-react` package, which wraps `agora-rtc-sdk-ng` with React hooks and components.

## Installation

```bash
npm install agora-rtc-react
# agora-rtc-react bundles agora-rtc-sdk-ng internally — no separate install needed
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

## Official Documentation

- React Quickstart: <https://docs.agora.io/en/video-calling/get-started/get-started-sdk?platform=react-js>
- API Reference: <https://api-ref.agora.io/en/video-sdk/reactjs/2.x/>
