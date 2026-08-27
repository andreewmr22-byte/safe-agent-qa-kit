# Contributing

Thanks for helping improve Safe Agent QA Kit.

## Ground rules

- Keep examples synthetic or fully sanitized.
- Include reproducible evidence for behavior changes.
- Add or update tests when contract behavior changes.
- Keep patches small enough to review.
- Do not include secrets, personal data or proprietary code.
- Do not weaken a safety gate without documenting why.

## Development

```bash
python -m pip install -e . pytest
pytest
safe-agent-qa validate examples/sample_run.json
```

For contract changes, describe the old behavior, new behavior, compatibility impact and a minimal example.
