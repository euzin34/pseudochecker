# Tests for transpiler output

import pytest

from src.checker import PseudocodeChecker


@pytest.fixture
def checker():
    return PseudocodeChecker(treat_warnings_as_failure=False)


def test_transpile_declare_and_assign(checker):
    source = "DECLARE x : INTEGER\nx <- 1\n"
    result = checker.check(source)
    assert result.ok is True
    assert result.python_preview is not None
    assert "# DECLARE x : INTEGER" in result.python_preview
    assert "x = 1" in result.python_preview


def test_transpile_for_loop(checker):
    source = "FOR i <- 1 TO 3\n  OUTPUT i\nNEXT i\n"
    result = checker.check(source)
    assert result.ok is True
    preview = result.python_preview
    assert "for i in range(" in preview
    assert "print" in preview or "OUTPUT" not in preview
