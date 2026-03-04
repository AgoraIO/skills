# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly.

**Do not open a public issue.**

Instead, use [GitHub's private vulnerability reporting](https://github.com/BenWeekes/skills/security/advisories/new) to submit your report. This ensures the issue can be assessed and addressed before public disclosure.

For security issues in the broader Agora platform, please follow the reporting process at [https://www.agora.io/en/security](https://www.agora.io/en/security).

## Scope

This repository contains skill content (Markdown files) that guide AI coding agents.
Security concerns here typically involve skill content that could cause agents to
generate insecure code, such as:

- Guidance that leads to hardcoded credentials (App ID, Customer Key, Customer Secret,
  App Certificate, RTC tokens)
- Patterns that introduce injection vulnerabilities in generated code
- Instructions that disable authentication (e.g., advising token auth to be disabled
  in production environments)
- Advice that bypasses or disables Agora Console security settings
- Prompt injection patterns: skills that accept user-provided content as context must
  not include patterns that could be exploited

## Secrets Handling

- Never commit API keys, certificates, or customer secrets.
- Use environment variables in examples.
- Use placeholder values in documentation.

## Response

We aim to acknowledge reports within 48 hours and provide a resolution timeline within 7 days.
