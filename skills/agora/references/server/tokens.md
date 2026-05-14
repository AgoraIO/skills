# Agora Server-Side: Token Generation

## Overview

Tokens authenticate users before joining channels. Generated server-side from App ID + App Certificate + channel + UID + expiration.

## Quick Reference

- `onTokenPrivilegeWillExpire` fires **30 seconds** before expiry — renew proactively
- UID in token must match UID used to join
- Max token validity: 24 hours
- Use `RtcRole.SUBSCRIBER` for audience-only users (prevents stream bombing)

## UID / Account-Name Constraints (Token Gotcha)

- Numeric UID (`buildTokenWithUid` + RTC join with numeric uid): must be `0` to `2^32 - 1`.
- String UID/account name (`buildTokenWithUserAccount` or `buildTokenWithRtm` account): ASCII only, max `255` characters.
- **RTM / `buildTokenWithRtm` `account`**: the API expects a string. Prefer an integer user id encoded as a string of digits (for example `"12345"`), not an arbitrary alphanumeric handle, to avoid identity clashes with other services.
- Here, `account` means the user's RTC identity string (account name), not your Agora customer account.
- Identity and type must match end-to-end:
  - If the token is minted for numeric UID `123`, join RTC with numeric `123`.
  - If the token is minted for account `"12345"` (string carrying a numeric id — preferred), join with that exact same string identity on the client; do not substitute a different handle or assume it interchangeably maps to a numeric uid unless your SDK documents that.

## Token Generation Guides

- **[Deploy a Token Server](https://docs.agora.io/en/video-calling/token-authentication/deploy-token-server)** — Express/Flask/Go server examples
- **[Use Tokens](https://docs.agora.io/en/video-calling/token-authentication/authentication-workflow)** — When and how tokens are used

## Token Libraries

All implementations are in [AgoraIO/Tools — DynamicKey/AgoraDynamicKey](https://github.com/AgoraIO/Tools/tree/master/DynamicKey/AgoraDynamicKey):

| Language | Notes                                                                               |
| -------- | ----------------------------------------------------------------------------------- |
| Node.js  | Also available as [`agora-token`](https://www.npmjs.com/package/agora-token) on npm |
| Python 3 | Use `python3/` directory                                                            |
| Go       |                                                                                     |
| Java     |                                                                                     |
| C#       |                                                                                     |
| Dart     |                                                                                     |
| Deno     | Native implementation — do NOT use the `agora-token` npm package in Deno            |
| Rust     |                                                                                     |
| PHP      |                                                                                     |
| Ruby     |                                                                                     |
| Lua      |                                                                                     |
| Perl     |                                                                                     |

## Token Types

- **RTC Token** — channel access for Video/Voice SDK
- **RTM Token** — access for Real-Time Messaging
- **Combined RTC + RTM Token** — bundles RTC + RTM privileges in one token via `buildTokenWithRtm`; also satisfies the `agora token=` auth header for ConvoAI REST API calls (see [conversational-ai/README.md](../conversational-ai/README.md#authentication))

> **[AccessToken2 Guide](https://docs.agora.io/en/video-calling/token-authentication/deploy-token-server)** — AccessToken2 with multi-service privileges

## buildTokenWithRtm (Node.js)

Generates a combined RTC + RTM token using `AccessToken2`. Use this when you need a single token that covers both channel access and RTM messaging — or to authenticate ConvoAI REST API calls.

```javascript
import { RtcTokenBuilder, RtcRole } from 'agora-token';

const token = RtcTokenBuilder.buildTokenWithRtm(
  appId, // string — your Agora App ID
  appCertificate, // string — your App Certificate
  channelName, // string — channel the user will join
  account, // string — prefer integer user id as a string of digits (e.g. "12345")
  RtcRole.PUBLISHER,
  tokenExpire, // number — seconds until token expires (e.g. 3600)
  privilegeExpire, // number — seconds until privileges expire (0 = same as tokenExpire)
);
```

> **`account` vs `uid`**: `buildTokenWithRtm` takes a string `account`, not an integer type. Prefer passing the user's numeric id as a numeric string, and have the client join with that exact same string identity. If the RTC client joins with a numeric uid type instead, use `buildTokenWithUid` for RTC-only tokens.
