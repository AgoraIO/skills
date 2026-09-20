#!/usr/bin/env bash
# Exercise the same session used by the case verifier before spending model calls.
set -euo pipefail

session="${1:-eval-browser}"
log_file="$(mktemp "${TMPDIR:-/tmp}/eval-browser-preflight.XXXXXX")"
cleanup() {
  agent-browser --session "$session" close >/dev/null 2>&1 || true
  rm -f "$log_file"
}
trap cleanup EXIT

agent-browser --version
if ! agent-browser --session "$session" open about:blank >"$log_file" 2>&1; then
  cat "$log_file"
  echo "::error::agent-browser preflight failed; collecting daemon startup diagnostics."
  agent-browser --debug --session "$session" open about:blank >>"$log_file" 2>&1 || true
  cat "$log_file"
  exit 1
fi
agent-browser --session "$session" snapshot
