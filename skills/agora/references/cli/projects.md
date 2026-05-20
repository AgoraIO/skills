# Agora CLI Projects

<!-- applies-from: v0.2.1 -->

Use this file when the user needs to create, select, inspect, or feature-enable Agora projects from the CLI.

Verified against Agora CLI `0.2.1`.

## Core Workflow

Use `agora init` for the fastest end-to-end demo setup. Use low-level project commands when the workflow must be decomposed:

```bash
agora login
agora project create my-agent-demo --feature rtc --feature rtm --feature convoai
agora project use my-agent-demo
agora project env
agora project feature list
agora project list --refresh-cache
```

## Project Commands

### Create

```bash
agora project create <name> [--region global|cn] [--template voice-agent] [--feature rtc|rtm|convoai]
agora project create <name> --dry-run
agora project create <name> --idempotency-key <key>
agora project create <name> --rtm-data-center EU
```

For agent guidance, prefer explicit `--feature` flags because they match the later `project feature` workflow. Omitted `--feature` defaults to `rtc`, `rtm`, and `convoai`, and `convoai` implies `rtm`.

### List

```bash
agora project list [--page N] [--page-size N] [--keyword <text>]
agora project list --refresh-cache
```

Use this when the user needs to discover a project ID or exact project name.

`--refresh-cache` updates the unfiltered first-page cache the CLI uses for shell completion. That matters when the user's completion results lag behind recent project changes.

### Select Current Project

```bash
agora project use <project>
```

`<project>` can be a project ID or exact project name.

After `project use`, commands like `project show`, `project feature list`, and `project doctor` can run without repeating the project argument.

### Show One Project

```bash
agora project show [project]
agora project show --json
```

This is the quickest way to inspect App ID, App Certificate, region, sign key, and token-enabled status for the current project.

Use `project show --json` for project metadata inspection.

If the user wants exported env vars or a dotenv workflow, route to [env.md](env.md) and use:

```bash
agora project env
agora project env --json
agora project env write
```

## Feature Commands

Valid verified feature names:

- `rtc`
- `rtm`
- `convoai`

Commands:

```bash
agora project feature list [project]
agora project feature status <feature> [project]
agora project feature enable <feature> [project]
```

Most ConvoAI onboarding preparation starts with:

```bash
agora project feature enable convoai
```

## Current-Project Context

If the user omits `[project]`, the CLI uses the locally selected project context.

In a bound quickstart repo, project resolution prefers repo-local `.agora/project.json` before global `agora project use` context. See [quickstarts.md](quickstarts.md) for the full precedence.

If no project is selected, the verified recovery is:

```bash
agora project use <project>
```

or rerun the command with a project argument.

## Things Not to Hallucinate

- Do not invent `agora project delete`.
- Do not invent `agora project feature disable`.
- Do not invent ConvoAI-specific nested groups under `agora project`.
- Do not invent `agora project doctor all`; use `agora project doctor --feature convoai`, `--feature rtc`, or `--feature rtm`.
