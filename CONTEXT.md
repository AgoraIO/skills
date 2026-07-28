# Agora Skills

Agent-facing reference material for building with Agora (RTC, RTM, Conversational AI,
Cloud Recording, server tokens, and the Agora CLI). The product surface it documents
lives in other repositories and moves independently, so most of the vocabulary here
concerns how a reference file states its relationship to an upstream release.

## Language

**Last verified**:
The upstream release whose behavior a reference file's claims were actually checked
against, by running commands or reading upstream source. Recorded per file, because
files drift at different rates.
_Avoid_: Verified against, tested against, supported version

**Minimum CLI**:
The oldest Agora CLI release an agent may proceed with. Below it, the readiness gate
blocks the workflow and routes to an upgrade. Uniform across all CLI reference files.
_Avoid_: Minimum supported, floor, baseline, required version

**Readiness gate**:
The read-only probe an agent must complete before any mutating CLI command. Checks
version against **Minimum CLI**, PATH resolution, and config schema compatibility.
_Avoid_: Preflight, health check, doctor

**Install path**:
A channel a user may be instructed to install or upgrade the CLI through. A channel
that still exists but must not be recommended is not an install path.
_Avoid_: Install method, distribution channel

**Level 2 fetch**:
Content deliberately left out of the skill and retrieved from upstream docs at use
time, because it would not survive six months unattended.
_Avoid_: External lookup, deferred content

**Detect-don't-ask**:
A guidance rule that instructs an agent to resolve a choice from observable state —
repo files, session data, CLI errors — and forbids putting the question to the user.
Reserved for choices where one answer is overwhelmingly common and the state needed
to confirm it already exists.
_Avoid_: Auto-detect, infer, smart default
