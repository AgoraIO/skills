# Agora CLI Install and Auth

Verified against Agora CLI `0.1.7`.

## Install

Preferred macOS / Linux / POSIX shell installer:

```bash
curl -fsSL https://raw.githubusercontent.com/AgoraIO/cli/main/install.sh | sh -s -- --add-to-path
```

Windows PowerShell installer:

```powershell
irm https://raw.githubusercontent.com/AgoraIO/cli/main/install.ps1 | iex
```

npm install path:

```bash
npm install -g agoraio-cli
```

The npm package is expected to be a thin install wrapper for the same Go-based `agora` binary. It requires Node.js 18+ when used. Do not describe npm as a permanent separate CLI implementation.

The installed command is:

```bash
agora --help
agora version
```

If the user still has the deprecated preview package:

```bash
npm uninstall -g agora-cli-preview
npm install -g agoraio-cli
```

For pinned versions, dry runs, custom install directories, Windows details, npm details, or source builds, use the upstream install docs in <https://github.com/AgoraIO/cli>.

## Login Flow

Primary commands:

```bash
agora login
agora login --no-browser
agora whoami
agora logout
```

Equivalent auth-group commands:

```bash
agora auth login
agora auth status
agora auth status --json
agora auth logout
```

`agora login` starts an OAuth browser flow and stores a local session.

If browser auto-open fails, use `agora login --no-browser` so the CLI prints a URL and the user can open it manually.

For agents, use `agora auth status --json`. In `0.1.7`, unauthenticated status is a recoverable auth state; the JSON error envelope uses exit code `3` with `AUTH_UNAUTHENTICATED`.

## OAuth Loopback Rule

The verified `0.1.7` loopback login flow advertises a redirect URI shaped like:

```text
http://localhost:<port>/oauth/callback
```

Important rule:

- the `redirect_uri` sent to authorize and token exchange must match exactly
- treat `localhost` and `127.0.0.1` as different strings for OAuth validation

If the user reports a `redirect_uri mismatch` or a browser login that gets a `400` during token exchange, tell them to check for any local tooling or overrides that switch one step to `127.0.0.1` while the other still uses `localhost`.

## Config and Session Location

The CLI stores config, session, logs, and current-project context under the Agora CLI config directory.

- macOS default: `~/.agora-cli`
- Linux default: `$XDG_CONFIG_HOME/agora-cli` or `~/.config/agora-cli`
- local override for testing or isolation: `AGORA_HOME=/custom/path`

## What to Tell the User

- If they are not logged in, tell them to run `agora login` first.
- If they ask "am I logged in?", use `agora whoami`, `agora whoami --plain`, or `agora auth status --json`.
- If they want a noninteractive or isolated local setup, route to [automation.md](automation.md).

## Things Not to Overstate

- Do not promise headless service-account auth; the verified flow in `0.1.7` is browser-based OAuth.
- Do not claim the preview package is still the recommended install target.
- Use `agora` for an installed CLI. Use `./agora` only when running a local binary built from the CLI repository.
