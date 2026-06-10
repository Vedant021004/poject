# test_project.py
import json
import os
import subprocess
import pytest
from unittest.mock import patch, MagicMock, call
from project import (
    QUESTION_BANK,
    build_question_pool,
    get_grade,
    present_question,
    save_results,
    format_question_check,
    git_auto_push,
    _find_git_root,
)


# ── helpers ───────────────────────────────────────────────────────────────────
def make_q(ans="B"):
    return {
        "q": "What is 2 + 2?",
        "opts": {"A": "3", "B": "4", "C": "5", "D": "6"},
        "ans": ans,
        "exp": "Basic arithmetic.",
    }


# ══════════════════════════════════════════════
#  QUESTION BANK TESTS
# ══════════════════════════════════════════════
def test_bank_has_three_topics():
    assert set(QUESTION_BANK.keys()) == {"NumPy", "Pandas", "SQL"}


def test_each_topic_has_15_questions():
    for topic, qs in QUESTION_BANK.items():
        assert len(qs) == 15, f"{topic} should have 15 questions"


def test_every_question_has_required_keys():
    required = {"q", "opts", "ans", "exp"}
    for topic, qs in QUESTION_BANK.items():
        for i, q in enumerate(qs):
            assert required.issubset(q.keys()), f"{topic} Q{i+1} missing keys"


def test_every_answer_is_valid_option():
    for topic, qs in QUESTION_BANK.items():
        for i, q in enumerate(qs):
            assert q["ans"] in q["opts"], f"{topic} Q{i+1} bad answer key"


def test_every_question_has_four_options():
    for topic, qs in QUESTION_BANK.items():
        for i, q in enumerate(qs):
            assert len(q["opts"]) == 4, f"{topic} Q{i+1} needs 4 options"


def test_format_question_check_valid():
    assert format_question_check(make_q()) is True


def test_format_question_check_missing_key():
    bad = make_q()
    del bad["exp"]
    assert format_question_check(bad) is False


def test_format_question_check_wrong_answer_key():
    bad = make_q()
    bad["ans"] = "Z"
    assert format_question_check(bad) is False


# ══════════════════════════════════════════════
#  BUILD POOL TESTS
# ══════════════════════════════════════════════
def test_build_pool_numpy_any():
    assert len(build_question_pool("NumPy", "any")) == 15


def test_build_pool_pandas_any():
    assert len(build_question_pool("Pandas", "any")) == 15


def test_build_pool_sql_any():
    assert len(build_question_pool("SQL", "any")) == 15


def test_build_pool_mixed_any():
    assert len(build_question_pool("Mixed (All Topics)", "any")) == 45


def test_build_pool_easy():
    assert len(build_question_pool("NumPy", "easy")) == 5


def test_build_pool_medium():
    assert len(build_question_pool("SQL", "medium")) == 5


def test_build_pool_hard():
    assert len(build_question_pool("Pandas", "hard")) == 5


def test_build_pool_mixed_easy():
    assert len(build_question_pool("Mixed (All Topics)", "easy")) == 15


def test_build_pool_returns_list():
    pool = build_question_pool("SQL", "any")
    assert isinstance(pool, list)


def test_build_pool_is_shuffled():
    """Run 10 times — at least once order must differ (probability ≈ 1)."""
    original = build_question_pool("NumPy", "any")
    different = any(
        build_question_pool("NumPy", "any") != original for _ in range(10)
    )
    assert different


# ══════════════════════════════════════════════
#  GRADE TESTS
# ══════════════════════════════════════════════
@pytest.mark.parametrize("pct,expected", [
    (100, "A+"), (93, "A+"), (92, "A"),  (90, "A"),
    (88,  "A-"), (84, "B+"), (80, "B"),  (78, "B-"),
    (74,  "C+"), (70, "C"),  (68, "C-"), (61, "D"),
    (60,  "D"),  (59, "F"),  (0,  "F"),
])
def test_get_grade(pct, expected):
    grade, _ = get_grade(pct)
    assert grade == expected


def test_get_grade_returns_tuple():
    result = get_grade(75)
    assert isinstance(result, tuple) and len(result) == 2


def test_get_grade_emoji_not_empty():
    _, emoji = get_grade(50)
    assert len(emoji) > 0


# ══════════════════════════════════════════════
#  PRESENT QUESTION TESTS
# ══════════════════════════════════════════════
def test_present_correct():
    with patch("builtins.input", return_value="B"):
        assert present_question(make_q("B"), 1, 5) == "CORRECT"


def test_present_wrong():
    with patch("builtins.input", return_value="A"):
        assert present_question(make_q("B"), 1, 5) == "WRONG"


def test_present_skip():
    with patch("builtins.input", return_value="next"):
        assert present_question(make_q("B"), 1, 5) == "SKIPPED"


def test_present_quit():
    with patch("builtins.input", return_value="quit"):
        assert present_question(make_q("B"), 1, 5) == "QUIT"


def test_present_lowercase_accepted():
    with patch("builtins.input", return_value="b"):
        assert present_question(make_q("B"), 1, 5) == "CORRECT"


def test_present_invalid_then_correct():
    inputs = iter(["X", "99", "C"])
    with patch("builtins.input", side_effect=inputs):
        assert present_question(make_q("C"), 1, 5) == "CORRECT"


def test_present_all_four_options():
    for lbl in ("A", "B", "C", "D"):
        q = make_q(ans=lbl)
        with patch("builtins.input", return_value=lbl):
            assert present_question(q, 1, 5) == "CORRECT"


# ══════════════════════════════════════════════
#  SAVE RESULTS TESTS
# ══════════════════════════════════════════════
def test_save_results_creates_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with patch("project.__file__", str(tmp_path / "project.py")):
        save_results(1, 1, 100.0, "A+", ["CORRECT"])
    assert (tmp_path / "quiz_history.json").exists()


def test_save_results_content(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with patch("project.__file__", str(tmp_path / "project.py")):
        save_results(3, 5, 60.0, "D", ["CORRECT", "WRONG", "CORRECT", "SKIPPED", "WRONG"])
    with open(tmp_path / "quiz_history.json") as f:
        data = json.load(f)
    last = data[-1]
    assert last["score"] == 3
    assert last["total"] == 5
    assert last["percentage"] == 60.0
    assert last["grade"] == "D"


def test_save_results_appends(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with patch("project.__file__", str(tmp_path / "project.py")):
        save_results(1, 1, 100.0, "A+", ["CORRECT"])
        save_results(0, 1, 0.0,   "F",  ["WRONG"])
    with open(tmp_path / "quiz_history.json") as f:
        data = json.load(f)
    assert len(data) == 2


def test_save_results_handles_corrupt_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "quiz_history.json").write_text("NOT JSON")
    with patch("project.__file__", str(tmp_path / "project.py")):
        save_results(2, 4, 50.0, "F", ["CORRECT", "WRONG"])
    with open(tmp_path / "quiz_history.json") as f:
        data = json.load(f)
    assert data[-1]["score"] == 2


def test_save_results_returns_filepath(tmp_path):
    with patch("project.__file__", str(tmp_path / "project.py")):
        path = save_results(1, 2, 50.0, "F", ["CORRECT", "WRONG"])
    assert path.endswith("quiz_history.json")
    assert os.path.isabs(path)


# ══════════════════════════════════════════════
#  GIT AUTO-PUSH TESTS
# ══════════════════════════════════════════════
def test_git_auto_push_no_repo(tmp_path):
    """Should print warning and return when not inside a git repo."""
    with patch("project._find_git_root", return_value=None):
        # Should not raise
        git_auto_push(str(tmp_path / "quiz_history.json"), 5, 10, "B")


def test_git_auto_push_calls_subprocess(tmp_path):
    """Should call subprocess.run 4 times (configure, add, commit, push)."""
    mock_result       = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout     = ""
    mock_result.stderr     = ""

    with patch("project._find_git_root", return_value=str(tmp_path)), \
         patch("subprocess.run", return_value=mock_result) as mock_run:
        git_auto_push(str(tmp_path / "quiz_history.json"), 8, 10, "A")
        assert mock_run.call_count == 4


def test_git_auto_push_commit_message_contains_score(tmp_path):
    """Commit message must include score and grade."""
    mock_result            = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout     = ""
    mock_result.stderr     = ""

    with patch("project._find_git_root", return_value=str(tmp_path)), \
         patch("subprocess.run", return_value=mock_result) as mock_run:
        git_auto_push(str(tmp_path / "f.json"), 7, 10, "B+")

    # The commit step is the 3rd call (index 2)
    commit_call = mock_run.call_args_list[2]
    cmd_args    = commit_call[0][0]          # positional first arg → list
    full_cmd    = " ".join(cmd_args)
    assert "7/10" in full_cmd or "score=7" in full_cmd
    assert "B+" in full_cmd


def test_git_auto_push_handles_nothing_to_commit(tmp_path):
    """'nothing to commit' stderr should not crash the function."""
    def side(cmd, **kwargs):
        r            = MagicMock()
        r.returncode = 1
        r.stdout     = "nothing to commit"
        r.stderr     = "nothing to commit"
        return r

    with patch("project._find_git_root", return_value=str(tmp_path)), \
         patch("subprocess.run", side_effect=side):
        git_auto_push(str(tmp_path / "f.json"), 5, 10, "C")   # must not raise


def test_find_git_root_returns_none_outside_repo(tmp_path):
    """_find_git_root should return None when no .git folder exists."""
    with patch("os.getcwd", return_value=str(tmp_path)):
        result = _find_git_root()
    assert result is None


def test_find_git_root_finds_dotgit(tmp_path):
    """_find_git_root should find a directory containing .git."""
    (tmp_path / ".git").mkdir()
    sub = tmp_path / "sub" / "dir"
    sub.mkdir(parents=True)
    with patch("os.getcwd", return_value=str(sub)):
        result = _find_git_root()
    assert result == str(tmp_path)