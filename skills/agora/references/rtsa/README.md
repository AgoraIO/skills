# Agora RTSA SDK

Real-Time Streaming Acceleration SDK. Foundation layer for most Agora products, designed for Linux or RTOS systems on ARM/AARCH64/MIPS/RISC-V architectures.

## What It Does

- 1v1 / group audio & video calls
- Live streaming (host publishes, audience subscribes)
- Audio-only or video+audio
- Cross-platform: Linux or RTOS system base on ARM/AARCH64/MIPS/RISC-V

## Critical Rules

1. **App ID is mandatory**: Initialize the engine with `AGORA_APP_ID`. Without it, the SDK cannot function.
2. **Token management in production**: If App Certificate is enabled, you must obtain an RTC token from your server before joining a channel.
3. **Log configuration differs by platform**:
   - Linux: Logs are written to a specified file directory. Set the `log_path` parameter when calling `agora_rtc_init`.
   - RTOS: Logs are not output by default. Set the `log_printf` parameter when calling `agora_rtc_init` (e.g., `log_printf = printf`).
4. **Feature availability varies by release**: RTSA releases may have some features trimmed to reduce package size for the target platform. If an API documented here is missing from your `agora_rtc_api.h`, this indicates the version has been optimized for your platform. Always program based on the actual function declarations in the `agora_rtc_api.h` header file included in your release package.
5. **Memory optimization for RTOS**: When running on RTOS with limited memory, carefully configure join parameters to disable unused features.

## Core Flow

1. Initialize Agora engine with `AGORA_APP_ID`
2. Join channel with token (or empty string if no App Certificate)
3. Publish local audio/video tracks
4. Subscribe to remote tracks
5. Leave channel and destroy engine on exit

## Auth

- `AGORA_APP_ID` required
- If App Certificate enabled → need RTC token from server
- For token generation, see the Server reference

## Memory Optimization for RTOS

The following features affect SDK memory usage. When running on RTOS with limited available memory, configure these settings when calling `agora_rtc_join_channel`:

| Parameter | Effect When Disabled | Memory Saved | Trade-off |
|-----------|---------------------|--------------|-----------|
| `auto_subscribe_video` | Rejects video data, suitable for audio-only scenarios | Varies | No video received |
| `enable_audio_jitter_buffer` | Disables audio jitter buffer | 10KB+ | Audio stutter rate may increase under weak network |
| `enable_audio_mixer` | Disables audio receive mixing | 3KB+ | Not needed for 1v1 calls |
| `audio_codec_type = AUDIO_CODEC_DISABLED` | Disables built-in audio encoder | 10KB+ | Must send pre-encoded audio via `agora_rtc_send_audio_data` |
| `enable_audio_decode` | Disables built-in audio decoder | 10KB+ | Received audio frames need external decoding |
| `enable_audio_ai_qos` | Disables ConvoAI interoperability audio acceleration | 10KB+ | Audio stutter rate may increase, latency may increase ~200ms |
| `crypto_opt.enable` | Disables content encryption | 3KB+ | Audio/video transmitted in plaintext with security risks |

## Release Package Acquisition

- **Linux**: Download from the official Agora website
- **RTOS**: Contact sales@agora.io to get the release package for your specific platform

## When to Use RTSA vs RTC

- **RTSA**: Linux servers, embedded systems, RTOS environments, IoT devices, ARM/AARCH64/MIPS/RISC-V architectures
- **RTC**: Web, iOS, Android, React Native, Flutter, desktop applications

## Cross-Product Integration

For RTSA integration with other Agora products:
- **RTC + RTSA**: Same channel, different clients — ensure codec compatibility
- **RTSA + ConvoAI**: Enable `enable_audio_ai_qos` for optimized audio acceleration (adds ~10KB memory)
- **RTSA + Cloud Recording**: Server-side recording works with RTSA channels

## When to Fetch More

Use Level 2 documentation lookup for:

### API Reference

Core functions from `agora_rtc_api.h`:

| Function | Purpose |
|----------|---------|
| `agora_rtc_init` | Initialize the RTSA service with App ID and event handlers |
| `agora_rtc_fini` | Release all resources allocated by the SDK |
| `agora_rtc_join_channel` | Join a channel with connection ID, channel name, uid, token, and options |
| `agora_rtc_leave_channel` | Leave the channel |
| `agora_rtc_send_audio_data` | Send an audio frame to the channel |
| `agora_rtc_send_video_data` | Send a video frame to the channel |
| `agora_rtc_mute_local_audio` / `agora_rtc_mute_local_video` | Mute/unmute local audio/video |
| `agora_rtc_mute_remote_audio` / `agora_rtc_mute_remote_video` | Mute/unmute remote audio/video |
| `agora_rtc_renew_token` | Renew token before expiration |

### Error Codes

Key error codes from `agora_err_code_e`:

| Code | Name | Description |
|------|------|-------------|
| 0 | `ERR_OKAY` | No error |
| 1 | `ERR_FAILED` | General error |
| 2 | `ERR_INVALID_PARAM` | Invalid argument |
| 3 | `ERR_INVALID_STATE` | Invalid state to call API |
| 7 | `ERR_NOT_INITIALIZED` | SDK not initialized |
| 101 | `ERR_INVALID_APP_ID` | App ID is invalid |
| 102 | `ERR_INVALID_CHANNEL_NAME` | Channel name is invalid |
| 109 | `ERR_TOKEN_EXPIRED` | Token has expired |
| 110 | `ERR_INVALID_TOKEN` | Token is invalid |
| 115 | `ERR_DYNAMIC_TOKEN_BUT_USE_STATIC_KEY` | Dynamic token required but not provided |
| 123 | `ERR_CLIENT_IS_BANNED_BY_SERVER` | Client is banned by the server |
| 200 | `ERR_AUDIO_CODEC_NOT_SUPPORT` | Audio codec not supported |
| 300 | `ERR_VIDEO_SEND_OVER_BANDWIDTH_LIMIT` | Video sending over bandwidth limit |

### Event Callbacks

Key callbacks from `agora_rtc_event_handler_t`:

| Callback | When Triggered |
|----------|----------------|
| `on_join_channel_success` | Local user joins channel successfully |
| `on_reconnecting` | Connection interrupted or keepalive timeout |
| `on_connection_lost` | Disconnected from server for more than 10s |
| `on_rejoin_channel_success` | Rejoins channel after disconnect |
| `on_user_joined` | Remote user joins channel |
| `on_user_offline` | Remote user leaves channel |
| `on_user_mute_audio` / `on_user_mute_video` | Remote user mutes/unmutes |
| `on_audio_data` | Received audio frame from remote user |
| `on_video_data` | Received video frame from remote user |
| `on_token_privilege_will_expire` | Token will expire soon |
| `on_error` | Error during runtime |
| `on_target_bitrate_changed` | Network bandwidth change detected |
| `on_key_frame_gen_req` | Remote user requests a keyframe |

### Data Types

Key data types from `agora_rtc_api.h`:

| Type | Purpose |
|------|---------|
| `connection_id_t` | Connection identification (uint32_t) |
| `rtc_service_option_t` | Service options: area_code, product_id, log_cfg, license_value |
| `rtc_channel_options_t` | Channel options: auto_subscribe, audio codec, crypto, RDT, etc. |
| `audio_frame_info_t` | Audio frame info with `audio_data_type_e` |
| `video_frame_info_t` | Video frame info with data_type, stream_type, frame_type, rotation |
| `video_data_type_e` | YUV420, H264, H265, generic, generic JPEG |
| `audio_data_type_e` | OPUS, PCMA, PCMU, G722, AAC variants, PCM |
| `area_code_e` | Region codes: CN, NA, EU, AS, JP, IN, GLOB |
