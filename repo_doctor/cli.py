from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .checks import CheckResult, run_checks


def compute_score(results: list[CheckResult]) -> int:
    return sum(r.weight for r in results if r.passed)


def grade(score: int) -> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 50:
        return "D"
    return "F"


def format_text(root: Path, results: list[CheckResult]) -> str:
    score = compute_score(results)
    lines = [
        f"repo-doctor {__version__}",
        f"Path:  {root}",
        f"Score: {score}/100 ({grade(score)})",
        "",
    ]
    for r in results:
        tag = "PASS" if r.passed else "FAIL"
        lines.append(f"[{tag}] {r.name} ({r.weight})")
    failed = [r for r in results if not r.passed]
    if failed:
        lines.append("")
        lines.append("To improve (highest impact first):")
        for r in sorted(failed, key=lambda item: -item.weight):
            lines.append(f"  - {r.advice} (+{r.weight})")
    return "\n".join(lines)


def format_json(root: Path, results: list[CheckResult]) -> str:
    score = compute_score(results)
    payload = {
        "path": str(root),
        "score": score,
        "grade": grade(score),
        "checks": [
            {
                "name": r.name,
                "passed": r.passed,
                "weight": r.weight,
                "advice": r.advice,
            }
            for r in results
        ],
    }
    return json.dumps(payload, indent=2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="repo-doctor",
        description="Score your Python repo's health in one command.",
    )
    parser.add_argument("path", nargs="?", default=".", help="project folder (default: .)")
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    parser.add_argument(
        "--min-score",
        type=int,
        default=0,
        help="exit with code 1 if the score is below this value",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args(argv)

    root = Path(args.path).resolve()
    if not root.is_dir():
        print(f"error: not a directory: {args.path}", file=sys.stderr)
        return 2

    results = run_checks(root)
    if args.json:
        print(format_json(root, results))
    else:
        print(format_text(root, results))

    return 1 if compute_score(results) < args.min_score else 0


if __name__ == "__main__":
    sys.exit(main())