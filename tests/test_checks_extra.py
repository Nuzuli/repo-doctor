from pathlib import Path

from repo_doctor.checks import run_checks


def _results(root: Path) -> dict:
    return {r.name: r for r in run_checks(root)}


def _write(path: Path, text: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_new_checks_fail_on_empty_repo(tmp_path):
    results = _results(tmp_path)
    assert not results["contributing"].passed
    assert not results["dependency_updates"].passed
    assert not results["ci_runs_typecheck"].passed


def test_contributing_in_root(tmp_path):
    _write(tmp_path / "CONTRIBUTING.md", "# Contributing")
    assert _results(tmp_path)["contributing"].passed


def test_contributing_in_github_folder(tmp_path):
    _write(tmp_path / ".github" / "CONTRIBUTING.md", "# Contributing")
    assert _results(tmp_path)["contributing"].passed


def test_dependabot_counts_as_dependency_updates(tmp_path):
    _write(tmp_path / ".github" / "dependabot.yml", "version: 2\n")
    assert _results(tmp_path)["dependency_updates"].passed


def test_renovate_counts_as_dependency_updates(tmp_path):
    _write(tmp_path / "renovate.json", "{}")
    assert _results(tmp_path)["dependency_updates"].passed


def test_workflow_with_mypy_counts_as_typecheck(tmp_path):
    _write(tmp_path / ".github" / "workflows" / "ci.yml", "steps:\n  - run: mypy src\n")
    assert _results(tmp_path)["ci_runs_typecheck"].passed


def test_workflow_without_type_checker_does_not_count(tmp_path):
    _write(tmp_path / ".github" / "workflows" / "ci.yml", "steps:\n  - run: pytest\n")
    assert not _results(tmp_path)["ci_runs_typecheck"].passed