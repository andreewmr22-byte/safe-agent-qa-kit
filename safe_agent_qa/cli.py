"""Command line interface for Safe Agent QA Kit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .contracts import ContractError, validate_run


def _validate(path: Path) -> int:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        validate_run(data)
    except (OSError, json.JSONDecodeError, ContractError) as exc:
        print(f"INVALID: {exc}")
        return 1
    print("VALID")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="safe-agent-qa")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="validate a QA run JSON file")
    validate.add_argument("path", type=Path)

    args = parser.parse_args()
    if args.command == "validate":
        return _validate(args.path)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
