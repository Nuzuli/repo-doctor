from pathlib import Path

from repo_doctor.checks import run_checks


def _results(root: Path) -> dict:
    return {r.name: r for r in run_checks(root)}


def _write(path: Path, text: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_weights_sum_to_100(tmp_path):
    assert sum(r.weight for r in run_checks(tmp_path)) == 100


def test_empty_repo_passes_nothing(tmp_path):
    assert not any(r.passed for r in run_checks(tmp_path))


def test_lockfile_detected(tmp_path):
    _write(tmp_path / "requirements-lock.txt", "rich==13.0.0\n")
    assert _results(tmp_path)["lockfile"].passed


def test_ci_detected_and_tests_found_in_workflow(tmp_path):
    _write(tmp_path / ".github" / "workflows" / "ci.yml", "steps:\n  - run: pytest\n")
    results = _results(tmp_path)
    assert results["ci"].passed
    assert results["ci_runs_tests"].passed
    assert not results["ci_runs_lint"].passed


def test_ci_detects_lint_step(tmp_path):
    _write(tmp_path / ".github" / "workflows" / "ci.yml", "steps:\n  - run: ruff check .\n")
    assert _results(tmp_path)["ci_runs_lint"].passed


def test_non_yaml_file_in_workflows_is_ignored(tmp_path):
    _write(tmp_path / ".github" / "workflows" / "notes.txt", "pytest")
    assert not _results(tmp_path)["ci"].passed


def test_tests_folder_needs_test_files(tmp_path):
    (tmp_path / "tests").mkdir()
    assert not _results(tmp_path)["tests"].passed
    _write(tmp_path / "tests" / "test_a.py", "def test_a():\n    pass\n")
    assert _results(tmp_path)["tests"].passed


def test_readme_needs_enough_lines(tmp_path):
    _write(tmp_path / "README.md", "\n".join(["baris"] * 5))
    assert not _results(tmp_path)["readme"].passed
    _write(tmp_path / "README.md", "\n".join(["baris"] * 15))
    assert _results(tmp_path)["readme"].passed


def test_lint_and_type_config_from_pyproject(tmp_path):
    _write(tmp_path / "pyproject.toml", "[tool.ruff]\nline-length = 100\n\n[tool.mypy]\n")
    results = _results(tmp_path)
    assert results["lint_config"].passed
    assert results["type_config"].passed


def test_license_gitignore_changelog(tmp_path):
    _write(tmp_path / "LICENSE", "MIT")
    _write(tmp_path / ".gitignore", "__pycache__/")
    _write(tmp_path / "CHANGELOG.md", "# Changelog")
    results = _results(tmp_path)
    assert results["license"].passed
    assert results["gitignore"].passed
    assert results["changelog"].passed