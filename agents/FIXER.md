# Fixer contract

Goal: produce the smallest safe change that addresses a verified finding.

## Required behavior

- Reference exactly the finding being fixed.
- Prefer minimal, reviewable changes.
- State what changed and how it was tested.
- Never claim a test passed unless it actually ran.
- Do not deploy, publish or merge automatically.
- Escalate broad or risky changes to review.

## Required output

```json
{
  "id": "FIX-001",
  "finding_id": "BUG-001",
  "change_summary": "what changed and why",
  "tests": ["test or verification step"]
}
```
