"""Run the same documentation gates locally and in pull-request CI."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", type=Path)
    parser.add_argument("--runtime-python", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    final = ["scripts.check_docs", "--site", "site"]
    if args.runtime:
        final.extend(["--runtime", str(args.runtime.absolute())])
    if args.runtime_python:
        final.extend(["--runtime-python", str(args.runtime_python.absolute())])
    checks = [
        ["scripts.check_docs", "--report", ".reports/structure.json"],
        ["pytest", "-q"], ["ruff", "check", "scripts", "tests"],
        ["isort", "--check-only", "scripts", "tests"], ["ty", "check", "scripts", "tests"],
        ["mkdocs", "build", "--strict"], final,
    ]
    for arguments in checks:
        print("+ python -m " + " ".join(arguments), flush=True)
        result = subprocess.run([sys.executable, "-m", *arguments], cwd=root, check=False)
        if result.returncode:
            return result.returncode
    return 0


if __name__ == "__main__":
    sys.exit(main())
