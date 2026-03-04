## What does this PR do?

<!-- Brief description of the change -->

## Checklist

- [ ] Freeze-forever test applied to all new inline content — would it still be
  correct if never updated?
- [ ] Routing still correct from `agora/skills/agora/SKILL.md`
- [ ] New or changed local links are valid
- [ ] No duplicate skill names
- [ ] No absolute local paths (`/Users/...`)
- [ ] No hardcoded credentials or API keys
- [ ] At least one eval case added or updated in `tests/eval-cases.md`
  (required for new product/platform additions)
- [ ] If adding code generation guidance: testing guidance updated
- [ ] `scripts/validate-skills.sh` passes locally
