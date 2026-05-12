# Testing Guidance — RTSA (Linux/RTOS)

Code examples for RTSA SDK integration.

## Key APIs

- `agora_rtc_init()` — Initialize SDK with event handlers
- `agora_rtc_fini()` — Cleanup SDK
- `agora_rtc_create_connection()` / `agora_rtc_destroy_connection()` — Connection lifecycle
- `agora_rtc_join_channel()` — Join channel with token
- `agora_rtc_leave_channel()` — Leave channel
- `agora_rtc_send_audio_data()` / `agora_rtc_send_video_data()` — Send media data

## Event Handlers

Key callbacks to implement:

- `on_join_channel_success` — Successfully joined channel
- `on_user_joined` — Remote user joined
- `on_user_offline` — Remote user left
- `on_audio_data` — Received audio data
- `on_video_data` — Received video data
- `on_error` — Error occurred

## Complete Example

```c
#include "agora_rtc_api.h"

typedef struct {
    connection_id_t conn_id;
    bool b_stop_flag;
    bool b_connected_flag;
} app_t;

static app_t g_app = {0};

// Event handlers
static void on_join_channel_success(connection_id_t conn_id, uint32_t uid, int elapsed) {
    g_app.b_connected_flag = true;
    printf("[conn-%u] Join channel success, uid %u, elapsed %d ms\n", conn_id, uid, elapsed);
}

static void on_user_joined(connection_id_t conn_id, uint32_t uid, int elapsed_ms) {
    printf("[conn-%u] Remote user %u joined\n", conn_id, uid);
}

static void on_user_offline(connection_id_t conn_id, uint32_t uid, int reason) {
    printf("[conn-%u] Remote user %u left, reason %d\n", conn_id, uid, reason);
}

static void on_audio_data(connection_id_t conn_id, uint32_t uid, uint16_t sent_ts,
                          const void *data, size_t len, const audio_frame_info_t *info) {
    // Handle received audio data
}

static void on_video_data(connection_id_t conn_id, uint32_t uid, uint16_t sent_ts,
                          const void *data, size_t len, const video_frame_info_t *info) {
    // Handle received video data
}

static void on_error(connection_id_t conn_id, int code, const char *msg) {
    printf("[conn-%u] Error %d: %s\n", conn_id, code, msg);
    g_app.b_stop_flag = true;
}

// Initialize event handlers
static void init_event_handler(agora_rtc_event_handler_t *handler) {
    handler->on_join_channel_success = on_join_channel_success;
    handler->on_user_joined = on_user_joined;
    handler->on_user_offline = on_user_offline;
    handler->on_audio_data = on_audio_data;
    handler->on_video_data = on_video_data;
    handler->on_error = on_error;
}

int main(int argc, char **argv) {
    int rval;
    
    // 1. Initialize event handler
    agora_rtc_event_handler_t event_handler = {0};
    init_event_handler(&event_handler);
    
    // 2. Configure SDK options
    rtc_service_option_t service_opt = {0};
    service_opt.area_code = AREA_CODE_GLOB;
    service_opt.log_cfg.log_path = "io.agora.rtc_sdk";
    service_opt.log_cfg.log_level = RTC_LOG_INFO;
    
    // 3. Initialize SDK
    rval = agora_rtc_init("YOUR_APP_ID", &event_handler, &service_opt);
    if (rval < 0) {
        printf("Failed to init SDK: %s\n", agora_rtc_err_2_str(rval));
        return -1;
    }
    
    // 4. Create connection
    rval = agora_rtc_create_connection(&g_app.conn_id);
    if (rval < 0) {
        printf("Failed to create connection: %s\n", agora_rtc_err_2_str(rval));
        return -1;
    }
    
    // 5. Configure channel options
    rtc_channel_options_t channel_options = {0};
    channel_options.auto_subscribe_audio = true;
    channel_options.auto_subscribe_video = true;
    channel_options.enable_audio_jitter_buffer = true;
    channel_options.enable_audio_mixer = false;
    channel_options.audio_codec_opt.audio_codec_type = AUDIO_CODEC_TYPE_G722;  // Recommended for RTOS
    
    // 6. Join channel
    rval = agora_rtc_join_channel(g_app.conn_id, "test_channel", 12345, NULL, &channel_options);
    if (rval < 0) {
        printf("Failed to join channel: %s\n", agora_rtc_err_2_str(rval));
        return -1;
    }
    
    // 7. Wait for connection
    while (!g_app.b_connected_flag && !g_app.b_stop_flag) {
        usleep(100 * 1000);
    }
    
    // 8. Send audio/video in loop
    while (!g_app.b_stop_flag) {
        if (g_app.b_connected_flag) {
            // Send audio data
            uint8_t audio_data[160] = {0};
            audio_frame_info_t audio_info = { .data_type = AUDIO_DATA_TYPE_PCM };
            agora_rtc_send_audio_data(g_app.conn_id, audio_data, sizeof(audio_data), &audio_info);
            
            // Send video data
            uint8_t video_data[1024] = {0};
            video_frame_info_t video_info = {
                .frame_type = VIDEO_FRAME_KEY,
                .data_type = VIDEO_DATA_TYPE_H264,
                .stream_type = VIDEO_STREAM_HIGH,
            };
            agora_rtc_send_video_data(g_app.conn_id, video_data, sizeof(video_data), &video_info);
        }
        usleep(10 * 1000);
    }
    
    // 9. Leave channel
    agora_rtc_leave_channel(g_app.conn_id);
    
    // 10. Destroy connection
    agora_rtc_destroy_connection(g_app.conn_id);
    
    // 11. Cleanup SDK
    agora_rtc_fini();
    
    return 0;
}
```

## Memory Optimization for RTOS

Configure channel options to reduce memory usage:

```c
rtc_channel_options_t channel_options = {0};

// Audio-only scenario
channel_options.auto_subscribe_audio = true;
channel_options.auto_subscribe_video = false;  // Reject video, save memory

// Disable unused features
channel_options.enable_audio_jitter_buffer = false;  // Save ~10KB
channel_options.enable_audio_mixer = false;          // Save ~3KB

// Recommended audio codec for RTOS: G722 (lower memory footprint)
channel_options.audio_codec_opt.audio_codec_type = AUDIO_CODEC_TYPE_G722;

rval = agora_rtc_join_channel(conn_id, "channel", uid, token, &channel_options);
```

## Send Encoded Audio (Disable Built-in Codec)

Disable built-in audio codec to reduce memory by ~10KB. Use external encoder and send pre-encoded audio data.

**Important: Each audio frame must be 20ms in duration.**

```c
// 1. Configure channel options to disable built-in codec
rtc_channel_options_t channel_options = {0};
channel_options.audio_codec_opt.audio_codec_type = AUDIO_CODEC_DISABLED;  // Disable built-in codec

// When built-in codec is disabled, these must also be set to false
channel_options.enable_audio_jitter_buffer = false;
channel_options.enable_audio_mixer = false;
channel_options.enable_audio_decode = false;

rval = agora_rtc_join_channel(conn_id, "channel", uid, token, &channel_options);

// 2. Send pre-encoded audio data (e.g., G722)
// G722 @ 16kHz sample rate: 20ms = 320 samples = 160 bytes encoded (4:1 compression)
uint8_t g722_frame[160];  // 20ms G722 frame (320 samples * 16-bit / 4 = 160 bytes)
audio_frame_info_t audio_info = {
    .data_type = AUDIO_DATA_TYPE_G722,
};

rval = agora_rtc_send_audio_data(conn_id, g722_frame, sizeof(g722_frame), &audio_info);

// 3. Timing: Send frames at 20ms intervals
// Use a timer or pacer to ensure 20ms frame interval
usleep(20 * 1000);  // 20ms
```

### Frame Size Reference (20ms Duration)

| Codec | Sample Rate | Raw Samples (20ms) | Encoded Size (bytes) |
|-------|-------------|-------------------|---------------------|
| G722 | 16kHz | 320 samples | 160 (4:1 compression) |
| Opus | 16kHz / 48kHz | 320 / 960 samples | varies (VBR) |
| AAC | any | 1024 samples per frame | varies (VBR) |

### Notes

- **G722**: Fixed 4:1 compression ratio. 20ms @ 16kHz = 320 samples = 160 bytes encoded.
- **Opus**: Supports 8kHz, 16kHz, 24kHz, 48kHz sample rates. At 16kHz, 20ms = 320 samples. Use 20ms packet duration for optimal latency.
- **AAC**: Each AAC frame contains exactly 1024 samples. Frame duration varies by sample rate:
  - @ 48kHz: 1024 samples ≈ 21.3ms per frame
  - @ 44.1kHz: 1024 samples ≈ 23.2ms per frame
  - @ 16kHz: 1024 samples ≈ 64ms per frame
  - For RTSA with AAC, align sending interval with actual frame duration (not fixed 20ms).

### Critical Rules for Encoded Audio

1. **Frame duration must be 20ms** — Do not send frames shorter or longer than 20ms
2. **Disable built-in codec** — Set `audio_codec_type = AUDIO_CODEC_DISABLED` when using external encoder
3. **Match data_type** — `audio_frame_info_t.data_type` must match the actual encoded format
4. **Consistent timing** — Send frames at regular 20ms intervals to avoid audio glitches

## Cleanup Order

Always follow this order:

1. `agora_rtc_leave_channel(conn_id)`
2. `agora_rtc_destroy_connection(conn_id)`
3. `agora_rtc_fini()`
