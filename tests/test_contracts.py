import json
from pathlib import Path

import pytest

from safe_agent_qa import ContractError, validate_run


def sample_run():
    return json.loads(Path("examples/sample_run.json").read_text(encoding="utf-8"))


def test_sample_run_is_valid():
    validate_run(sample_run())


def test_fix_must_reference_real_finding():
    run = sample_run()
    run["fixes"][0]["finding_id"] = "BUG-404"
    with pytest.raises(ContractError, match="unknown finding"):
        validate_run(run)


def test_high_risk_fix_requires_review():
    run = sample_run()
    run["reviews"] = []
    with pytest.raises(ContractError, match="requires explicit review"):
        validate_run(run)


def test_possible_secret_is_rejected():
    run = sample_run()
    run["findings"][0]["evidence"].append("token sk-this-is-not-allowed-12345")
    with pytest.raises(ContractError, match="possible secret"):
        validate_run(run)
