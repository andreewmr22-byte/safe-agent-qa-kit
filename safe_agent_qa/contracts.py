"""Deterministic validation for evidence-driven coding-agent QA runs."""

from __future__ import annotations

import re
from typing import Any


class ContractError(ValueError):
    """Raised when an agent run violates the public QA contract."""


_ALLOWED_SEVERITY = {"low", "medium", "high", "critical"}
_ALLOWED_REVIEW = {"approved", "rejected", "needs_changes"}
_SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{12,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]


def _need(obj: dict[str, Any], key: str, kind: type) -> Any:
    if key not in obj:
        raise ContractError(f"missing required field: {key}")
    value = obj[key]
    if not isinstance(value, kind):
        raise ContractError(f"{key} must be {kind.__name__}")
    return value


def _scan_for_secrets(value: Any, path: str = "root") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            _scan_for_secrets(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _scan_for_secrets(child, f"{path}[{index}]")
    elif isinstance(value, str):
        for pattern in _SECRET_PATTERNS:
            if pattern.search(value):
                raise ContractError(f"possible secret detected at {path}")


def validate_run(run: dict[str, Any]) -> None:
    """Validate a complete Bug Hunter -> Fixer -> Reviewer handoff.

    The function returns ``None`` on success and raises ``ContractError`` on
    the first deterministic contract violation.
    """

    if not isinstance(run, dict):
        raise ContractError("run must be an object")

    _scan_for_secrets(run)

    findings = _need(run, "findings", list)
    fixes = _need(run, "fixes", list)
    reviews = _need(run, "reviews", list)

    finding_ids: set[str] = set()
    severity_by_id: dict[str, str] = {}

    for finding in findings:
        if not isinstance(finding, dict):
            raise ContractError("each finding must be an object")
        finding_id = _need(finding, "id", str).strip()
        if not finding_id or finding_id in finding_ids:
            raise ContractError("finding ids must be non-empty and unique")
        severity = _need(finding, "severity", str)
        if severity not in _ALLOWED_SEVERITY:
            raise ContractError(f"invalid severity for {finding_id}: {severity}")
        evidence = _need(finding, "evidence", list)
        if not evidence or not all(isinstance(item, str) and item.strip() for item in evidence):
            raise ContractError(f"{finding_id} requires concrete evidence")
        _need(finding, "summary", str)
        _need(finding, "reproduction", list)
        finding_ids.add(finding_id)
        severity_by_id[finding_id] = severity

    fix_ids: set[str] = set()
    fixed_findings: dict[str, str] = {}
    for fix in fixes:
        if not isinstance(fix, dict):
            raise ContractError("each fix must be an object")
        fix_id = _need(fix, "id", str).strip()
        finding_id = _need(fix, "finding_id", str).strip()
        if not fix_id or fix_id in fix_ids:
            raise ContractError("fix ids must be non-empty and unique")
        if finding_id not in finding_ids:
            raise ContractError(f"{fix_id} references unknown finding {finding_id}")
        _need(fix, "change_summary", str)
        tests = _need(fix, "tests", list)
        if not tests:
            raise ContractError(f"{fix_id} must list verification tests")
        fix_ids.add(fix_id)
        fixed_findings[fix_id] = finding_id

    reviewed_fixes: set[str] = set()
    for review in reviews:
        if not isinstance(review, dict):
            raise ContractError("each review must be an object")
        fix_id = _need(review, "fix_id", str).strip()
        if fix_id not in fix_ids:
            raise ContractError(f"review references unknown fix {fix_id}")
        verdict = _need(review, "verdict", str)
        if verdict not in _ALLOWED_REVIEW:
            raise ContractError(f"invalid review verdict for {fix_id}: {verdict}")
        _need(review, "notes", list)
        reviewed_fixes.add(fix_id)

    for fix_id, finding_id in fixed_findings.items():
        if severity_by_id[finding_id] in {"high", "critical"} and fix_id not in reviewed_fixes:
            raise ContractError(f"high-risk fix {fix_id} requires explicit review")
