from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

LOCKFILES = [
    "requirements-lock.txt",
    "requirements.lock.txt",
    "poetry.lock",
    "uv.lock",
    "Pipfile.lock",
    "pdm.lock",
]
LICENSE_FILES = ["LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"]
CONTRIBUTING_FILES = ["CONTRIBUTING.md", ".github/CONTRIBUTING.md"]
UPDATE_BOT_FILES = [
    ".github/dependabot.yml",
    ".github/dependabot.yaml",
    "renovate.json",
    ".github/renovate.json",
    ".renovaterc",
]


@dataclass(frozen=True)
class CheckResult:
    name: str
    passed: bool
    weight: int
    advice: str


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def _any_exists(root: Path, names: list[str]) -> bool:
    return any((root / name).is_file() for name in names)


def _workflow_files(root: Path) -> list[Path]:
    wf = root / ".github" / "workflows"
    if not wf.is_dir():
        return []
    return [p for p in sorted(wf.iterdir()) if p.suffix in (".yml", ".yaml")]


def _workflow_text(root: Path) -> str:
    return "\n".join(_read(p) for p in _workflow_files(root)).lower()


def _readme_lines(root: Path) -> int:
    for name in ("README.md", "README.rst", "README.txt"):
        path = root / name
        if path.is_file():
            return sum(1 for line in _read(path).splitlines() if line.strip())
    return 0


def run_checks(root: Path) -> list[CheckResult]:
    root = Path(root)
    pyproject = _read(root / "pyproject.toml")
    workflows = _workflow_text(root)
    tests_dir = root / "tests"

    has_tests = tests_dir.is_dir() and any(tests_dir.rglob("test_*.py"))
    has_lint = (
        "[tool.ruff" in pyproject
        or "[tool.flake8" in pyproject
        or _any_exists(root, ["ruff.toml", ".ruff.toml", ".flake8"])
    )
    has_types = (
        "[tool.mypy" in pyproject
        or "[tool.pyright" in pyproject
        or _any_exists(root, ["mypy.ini", "pyrightconfig.json"])
    )

    return [
        CheckResult(
            "lockfile",
            _any_exists(root, LOCKFILES),
            12,
            "Commit a lockfile (requirements-lock.txt, poetry.lock, or uv.lock) so installs are reproducible.",
        ),
        CheckResult(
            "ci",
            bool(_workflow_files(root)),
            12,
            "Add a workflow in .github/workflows/ so every push is checked automatically.",
        ),
        CheckResult(
            "tests",
            has_tests,
            13,
            "Add a tests/ folder with test_*.py files that check real behavior.",
        ),
        CheckResult(
            "readme",
            _readme_lines(root) >= 15,
            8,
            "Expand the README (install, usage, tests) to at least 15 non-empty lines.",
        ),
        CheckResult(
            "license",
            _any_exists(root, LICENSE_FILES),
            5,
            "Add a LICENSE file so others know how they may use the code.",
        ),
        CheckResult(
            "lint_config",
            has_lint,
            9,
            "Configure a linter such as ruff in pyproject.toml.",
        ),
        CheckResult(
            "type_config",
            has_types,
            5,
            "Configure a type checker such as mypy in pyproject.toml.",
        ),
        CheckResult(
            "gitignore",
            (root / ".gitignore").is_file(),
            5,
            "Add a .gitignore so caches and local files stay out of the repo.",
        ),
        CheckResult(
            "changelog",
            _any_exists(root, ["CHANGELOG.md", "CHANGELOG.rst", "CHANGELOG.txt"]),
            5,
            "Keep a CHANGELOG.md so users can see what changed between releases.",
        ),
        CheckResult(
            "ci_runs_tests",
            "pytest" in workflows or "unittest" in workflows,
            10,
            "Make your CI workflow run the test suite (for example pytest).",
        ),
        CheckResult(
            "ci_runs_lint",
            "ruff" in workflows or "flake8" in workflows,
            5,
            "Make your CI workflow run the linter (for example ruff check .).",
        ),
        CheckResult(
            "contributing",
            _any_exists(root, CONTRIBUTING_FILES),
            3,
            "Add a CONTRIBUTING.md that explains how to set up, test, and submit changes.",
        ),
        CheckResult(
            "dependency_updates",
            _any_exists(root, UPDATE_BOT_FILES),
            5,
            "Enable automatic dependency updates with .github/dependabot.yml or renovate.json.",
        ),
        CheckResult(
            "ci_runs_typecheck",
            "mypy" in workflows or "pyright" in workflows,
            3,
            "Make your CI workflow run a type checker (for example mypy).",
        ),
    ]