# Safe Agent QA Kit

A small, reusable open-source kit for **AI coding QA workflows**. It defines explicit contracts between three roles:

1. **Bug Hunter** — finds reproducible defects and records evidence.
2. **Fixer** — proposes the smallest safe change and links it to a finding.
3. **Reviewer** — validates behavior, regression risk, accessibility and user impact.

The project is intentionally product-agnostic. Examples use synthetic data only and contain no private application code, credentials, customer data or infrastructure configuration.

## Why this exists

Agentic coding is faster when agents hand work to each other using structured evidence instead of free-form chat. Safe Agent QA Kit provides:

- JSON-compatible contracts for findings, fixes and reviews;
- deterministic validation rules;
- a lightweight CLI for validating agent output;
- reusable role prompts;
- tests and CI;
- synthetic examples that can be reproduced locally.

## Quick start

```bash
python -m pip install -e .
safe-agent-qa validate examples/sample_run.json
pytest
```

## Core safety rules

- Never invent test evidence.
- Every fix must reference a real finding.
- High-risk fixes require explicit review.
- Secrets and personal data must not be copied into reports.
- A reviewer may reject a fix even when tests pass.
- The kit does not deploy, publish or merge code automatically.

## Repository layout

```text
safe_agent_qa/       Python package and validators
agents/              Reusable role contracts/prompts
examples/            Synthetic end-to-end examples
tests/               Contract and CLI tests
.github/workflows/    CI
```

## Status

Early public release. The first milestone is a stable contract for evidence-driven multi-agent QA that can be used from Codex, CI jobs, local scripts or other coding-agent systems.

## Contributing

Issues and pull requests are welcome. Please use synthetic fixtures in bug reports and examples. Do not submit secrets, customer data or proprietary source code.

## License

MIT.
