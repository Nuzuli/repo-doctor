# repo-doctor



![CI](https://github.com/Nuzuli/repo-doctor/actions/workflows/ci.yml/badge.svg)



Score your Python repo's health in one command. No dependencies, no internet, works on private repos.

repo-doctor looks at your project folder and checks the things buyers, contributors, and reviewers look at first: lockfile, CI, tests, README, license, lint and type config, and more. You get a score out of 100 and a list of fixes, highest impact first.

## Install

```bash
pip install git+https://github.com/Nuzuli/repo-doctor.git
```

Requires Python 3.10 or newer. It has zero third-party dependencies.

## Usage

```bash
repo-doctor            # check the current folder
repo-doctor path/to/project
repo-doctor . --json   # machine-readable report
repo-doctor . --min-score 70   # exit code 1 if the score is below 70
```

## Example output

```text
repo-doctor 0.1.0
Path:  /home/runner/work/repo-doctor/repo-doctor
Score: 100/100 (A)

[PASS] lockfile (15)
[PASS] ci (15)
[PASS] tests (15)
[PASS] readme (10)
[PASS] license (5)
[PASS] lint_config (10)
[PASS] type_config (5)
[PASS] gitignore (5)
[PASS] changelog (5)
[PASS] ci_runs_tests (10)
[PASS] ci_runs_lint (5)
```

That is repo-doctor checking its own repository in CI. When something fails, it also prints a "To improve" list, highest impact first.

## What it checks

| Check | Weight | Passes when |
| --- | --- | --- |
| lockfile | 15 | a lockfile such as `requirements-lock.txt`, `poetry.lock`, or `uv.lock` exists |
| ci | 15 | `.github/workflows/` has a `.yml` or `.yaml` file |
| tests | 15 | `tests/` contains `test_*.py` files |
| readme | 10 | the README has at least 15 non-empty lines |
| lint_config | 10 | ruff or flake8 is configured |
| ci_runs_tests | 10 | a workflow runs pytest or unittest |
| license | 5 | a `LICENSE` file exists |
| type_config | 5 | mypy or pyright is configured |
| gitignore | 5 | a `.gitignore` exists |
| changelog | 5 | a `CHANGELOG.md` exists |
| ci_runs_lint | 5 | a workflow runs ruff or flake8 |

Grades: A (90+), B (80+), C (70+), D (50+), F (below 50).

## Use it in CI

```yaml
- name: Repo health
  run: |
    pip install git+https://github.com/Nuzuli/repo-doctor.git
    repo-doctor . --min-score 70
```

## Development

```bash
pip install -e ".[dev]"
ruff check .
mypy repo_doctor
pytest
```

## License

MIT, see [LICENSE](LICENSE).