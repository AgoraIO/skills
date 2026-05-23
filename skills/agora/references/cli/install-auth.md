# Agora CLI Install and Auth

<!-- applies-from: v0.2.1 -->

Use this file when the user needs to install the Agora CLI, authenticate, or verify that the local install is healthy.

Verified against Agora CLI `0.2.1`.

> **Agents:** start with the read-only **CLI readiness** probe in [README.md](README.md). Installers and global npm installs are allowed only as readiness remediation after user approval. That section is the single source of truth for version gates, curl-first upgrade, PATH recovery, and config mismatch errors.

## Install

Ask for user approval before running installers, global package installs, shell-profile updates, or package removal commands.

## Version Gate and Upgrade

Use [README.md](README.md#cli-readiness-agents) as the canonical agent readiness flow.

- Read-only probe first: `agora version` and `which -a agora` / `where.exe agora`.
- If `agora` is missing or below `0.1.7`, stop normal CLI workflow and upgrade. Do not call `agora upgrade` on `0.1.6`; it does not exist there.
- Preferred remediation after approval: `curl -fsSL https://raw.githubusercontent.com/AgoraIO/cli/main/install.sh | sh`.
- Alternate remediation after approval: `npm install -g agoraio-cli` when Node.js 18+ is available.
- If a direct-installer upgrade from `0.1.7`–`0.2.0` fails crossing `0.2.1`, re-run the curl installer once because release archive names changed.
- If `agora version` still reports an old version after install, check PATH shadowing with `which -a agora` / `where.exe agora` and follow `agora doctor`'s shell-specific PATH fix when available. Do not uninstall automatically; remove an old binary only after user approval, using `install.sh --uninstall` / `install.ps1 -Uninstall` for installer-managed installs when applicable.
- If the CLI errors with `Config version N is newer than this CLI supports`, an old binary is usually reading config from a newer CLI. Upgrade through the readiness flow; edit config only as a last resort after backing it up.

Preferred macOS / Linux / POSIX shell installer:

```bash
curl -fsSL https://raw.githubusercontent.com/AgoraIO/cli/main/install.sh | sh
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

In `0.2.1`, the shell installers add the binary directory to `PATH` and wire shell completion by default. Use `--no-path`, `--no-completion`, or `--skip-shell` only when the user explicitly wants to opt out.

The installed command is:

```bash
agora --help
agora version
agora doctor --json
```

If the user still has the deprecated preview package:

```bash
npm uninstall -g agora-cli-preview
npm install -g agoraio-cli
```

For pinned versions, uninstall, custom install directories, Windows details, npm details, or source builds, use the upstream install docs in <https://github.com/AgoraIO/cli>.

> ⚠️ Removed in v0.2.0: `curl -fsSL https://raw.githubusercontent.com/AgoraIO/cli/main/install.sh | sh -s -- --add-to-path`. Use `curl -fsSL https://raw.githubusercontent.com/AgoraIO/cli/main/install.sh | sh` instead.

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

For agents, use `agora auth status --json`. In `0.2.1`, unauthenticated status is still a recoverable auth state; the JSON error envelope uses exit code `3` with `AUTH_UNAUTHENTICATED`.

## Verification and Failure Modes

Run the install self-test before debugging higher-level project issues:

```bash
agora doctor
agora doctor --json
```

Observed `0.2.1` exit codes:

- `0`: healthy install
- `1`: blocking install issues
- `2`: warnings
- `3`: auth or session issues

Common failures:

- If `agora doctor` reports PATH issues, follow the command it prints for the current shell.
- If `agora doctor` reports DNS or network failures, fix network or proxy settings before retrying `agora login`.
- If `agora login` is run in JSON, CI, or non-TTY mode without an existing session, `-y` / `--yes` does not start a new browser flow; the command fails fast with `AUTH_UNAUTHENTICATED`.
- If upgrade from a direct installer fails when crossing 0.2.1, re-run the curl installer once — see [README.md](README.md) CLI readiness.

## OAuth Loopback Rule

The verified `0.2.0` loopback login flow advertises a redirect URI shaped like:

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
- If they ask which environment overrides exist, use `agora env-help --json`.
- If they want a noninteractive or isolated local setup, route to [automation.md](automation.md).

## Things Not to Overstate

- Do not promise headless service-account auth; the verified flow is browser-based OAuth.
- Do not document `--add-to-path`; it was removed in `0.2.0`.
- Do not claim the preview package is still the recommended install target.
- Use `agora` for an installed CLI. Use `./agora` only when running a local binary built from the CLI repository.
