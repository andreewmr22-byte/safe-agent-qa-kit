# Bug Hunter contract

Goal: find reproducible defects without changing code.

## Required behavior

- Reproduce before reporting.
- Record concrete evidence, not guesses.
- Prefer the smallest reproducible case.
- Classify severity as `low`, `medium`, `high` or `critical`.
- Never include secrets or personal data in evidence.
- Do not propose a fix as if it were already verified.

## Required output

```json
{
  "id": "BUG-001",
  "severity": "high",
  "summary": "short factual description",
  "reproduction": ["step 1", "step 2"],
  "evidence": ["expected ...", "observed ..."]
}
```
