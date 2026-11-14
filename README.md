# repo-doctor

[![CI](https://github.com/Nuzuli/repo-doctor/actions/workflows/ci.yml/badge.svg)](https://github.com/Nuzuli/repo-doctor/actions/workflows/ci.yml)

Score your Python repo's health in one command. No dependencies, no internet, works on private repos.

repo-doctor looks at your project folder and checks the things buyers, contributors, and reviewers look at first: lockfile, CI, tests, README, license, lint and type config, and more. You get a score out of 100 and a list of fixes, highest impact first.

## Install

```
pip install pyrepo-doctor
```

The package on PyPI is called `pyrepo-doctor`; the command is `repo-doctor`.

Requires Python 3.10 or newer. It has zero third-party dependencies.

## Usage

```
repo-doctor            # check the current folder
repo-doctor path/to/project
repo-doctor . --json   # machine-readable report
repo-doctor . --min-score 70   # exit code 1 if the score is below 70
```

## Example output

That is repo-doctor checking its own repository in CI:

```
repo-doctor 0.2.0
Path:  /home/runner/work/repo-doctor/repo-doctor
Score: 100/100 (A)

[PASS] lockfile (12)
[PASS] ci (12)
[PASS] tests (13)
[PASS] readme (8)
[PASS] license (5)
[PASS] lint_config (9)
[PASS] type_config (5)
[PASS] gitignore (5)
[PASS] changelog (5)
[PASS] ci_runs_tests (10)
[PASS] ci_runs_lint (5)
[PASS] contributing (3)
[PASS] dependency_updates (5)
[PASS] ci_runs_typecheck (3)
```

When something fails, it also prints a "To improve" list, highest impact first.

## What it checks

14 checks, with weights that add up to exactly 100:

| Check              | Weight | Passes when                                                                    |
| ------------------ | ------ | ------------------------------------------------------------------------------ |
| tests              | 13     | `tests/` contains `test_*.py` files                                            |
| lockfile           | 12     | a lockfile such as `requirements-lock.txt`, `poetry.lock`, or `uv.lock` exists |
| ci                 | 12     | `.github/workflows/` has a `.yml` or `.yaml` file                              |
| ci_runs_tests      | 10     | a workflow runs pytest or unittest                                             |
| lint_config        | 9      | ruff or flake8 is configured                                                   |
| readme             | 8      | the README has at least 15 non-empty lines                                     |
| license            | 5      | a `LICENSE` file exists                                                        |
| type_config        | 5      | mypy or pyright is configured                                                  |
| gitignore          | 5      | a `.gitignore` exists                                                          |
| changelog          | 5      | a `CHANGELOG.md` exists                                                        |
| ci_runs_lint       | 5      | a workflow runs ruff or flake8                                                 |
| dependency_updates | 5      | dependabot or renovate is configured                                           |
| contributing       | 3      | a `CONTRIBUTING.md` exists                                                     |
| ci_runs_typecheck  | 3      | a workflow runs mypy or pyright                                                |

Grades: A (90+), B (80+), C (70+), D (50+), F (below 50).

## Use it in CI

```
- name: Repo health
  run: |
    pip install pyrepo-doctor
    repo-doctor . --min-score 70
```

## Development

```
pip install -e ".[dev]"
ruff check .
mypy repo_doctor
pytest
```

## License

MIT, see [LICENSE](LICENSE).