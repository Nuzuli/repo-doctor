import json

import pytest

from repo_doctor.checks import CheckResult
from repo_doctor.cli import compute_score, grade, main


def _result(passed: bool, weight: int) -> CheckResult:
    return CheckResult("x", passed, weight, "saran")


def test_compute_score_sums_only_passed():
    results = [_result(True, 15), _result(False, 10), _result(True, 5)]
    assert compute_score(results) == 20


@pytest.mark.parametrize(
    "score, expected",
    [(100, "A"), (90, "A"), (89, "B"), (80, "B"), (70, "C"), (50, "D"), (49, "F"), (0, "F")],
)
def test_grade_boundaries(score, expected):
    assert grade(score) == expected


def test_text_report_for_empty_folder(tmp_path, capsys):
    assert main([str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "Score: 0/100 (F)" in out
    assert "[FAIL] lockfile" in out
    assert "To improve" in out


def test_text_report_lists_highest_impact_first(tmp_path, capsys):
    main([str(tmp_path)])
    out = capsys.readouterr().out
    assert out.index("Commit a lockfile") < out.index("Add a LICENSE file")


def test_json_report_is_valid(tmp_path, capsys):
    assert main([str(tmp_path), "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["score"] == 0
    assert data["grade"] == "F"
    assert len(data["checks"]) == 11


def test_min_score_fails_when_below(tmp_path):
    assert main([str(tmp_path), "--min-score", "50"]) == 1


def test_min_score_passes_when_met(tmp_path):
    assert main([str(tmp_path), "--min-score", "0"]) == 0


def test_not_a_directory_returns_2(tmp_path, capsys):
    assert main([str(tmp_path / "tidak-ada")]) == 2
    assert "not a directory" in capsys.readouterr().err


def test_version_flag_exits_cleanly(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert "repo-doctor" in capsys.readouterr().out