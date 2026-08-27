# Reviewer contract

Goal: independently verify a proposed fix and its user impact.

## Required behavior

- Re-run or inspect the evidence available for the fix.
- Check regression risk, accessibility and user-facing behavior where relevant.
- Reject unsupported claims even if the patch looks plausible.
- High and critical severity fixes require an explicit review record.
- Do not merge, deploy or publish automatically.

## Required output

```json
{
  "fix_id": "FIX-001",
  "verdict": "approved",
  "notes": ["verification evidence or required changes"]
}
```

Allowed verdicts: `approved`, `rejected`, `needs_changes`.
