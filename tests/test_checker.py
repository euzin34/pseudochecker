# Golden tests for PseudocodeChecker.

from pathlib import Path

import pytest

from src.checker import PseudocodeChecker

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = PROJECT_ROOT / "examples"
BUGGY = PROJECT_ROOT / "tests" / "buggy_code.txt"


@pytest.fixture
def checker():
    return PseudocodeChecker(treat_warnings_as_failure=False)


def test_basic_example_valid(checker):
    source = (EXAMPLES / "basic_example.txt").read_text(encoding="utf-8")
    result = checker.check(source)
    assert result.ok is True
    assert len(result.errors) == 0


def test_advanced_example_valid(checker):
    source = (EXAMPLES / "advanced_example.txt").read_text(encoding="utf-8")
    result = checker.check(source)
    assert result.ok is True
    assert len(result.errors) == 0


def test_buggy_code_has_syntax_errors(checker):
    source = BUGGY.read_text(encoding="utf-8")
    result = checker.check(source)
    assert result.ok is False
    assert len(result.errors) > 0
    assert any(e["line"] > 1 for e in result.errors)


def test_empty_source_fails():
    result = PseudocodeChecker().check("   \n  ")
    assert result.ok is False


def test_syntax_error_missing_then(checker):
    source = "DECLARE x : INTEGER\nIF x > 0\n  OUTPUT x\nENDIF\n"
    result = checker.check(source)
    assert result.ok is False
    assert result.stage == "syntax"


def test_for_next_mismatch(checker):
    source = """DECLARE i : INTEGER
FOR i <- 1 TO 3
  OUTPUT i
NEXT j
"""
    result = checker.check(source)
    assert result.ok is False
    assert any("NEXT" in e["message"] for e in result.errors)


def test_python_preview_on_valid(checker):
    source = (EXAMPLES / "basic_example.txt").read_text(encoding="utf-8")
    result = checker.check(source)
    assert result.python_preview is not None
    assert "print" in result.python_preview


def test_result_to_dict(checker):
    result = checker.check("DECLARE x : INTEGER\nx <- 1\n")
    d = result.to_dict()
    assert "ok" in d
    assert "errors" in d
    assert "stats" in d
