# Contributing to repo-doctor

Thanks for helping. This project is small, so the process is short.

## Set up

```bash
git clone https://github.com/Nuzuli/repo-doctor.git
cd repo-doctor
pip install -e ".[dev]"
```

## Before you open a pull request

Run all three; CI runs the same commands:

```bash
ruff check .
mypy repo_doctor
pytest
```

## Adding a new check

1. Add a `CheckResult` entry in `repo_doctor/checks.py` with a name, a weight, and one sentence of advice.
2. Keep the total weight of all checks at exactly 100 (a test enforces this).
3. Add tests for both the passing and the failing case in `tests/`.
4. Note the change in `CHANGELOG.md`.

## Commits

Keep each pull request small and focused: one change together with the tests that prove it. Short messages in the style `feat: ...`, `fix: ...`, `test: ...`, `docs: ...` are appreciated.

## Reporting bugs and suggesting checks

Open an issue with the folder layout that caused the wrong result (file names are enough) and what you expected instead.