# Tests for semantic analyzer behaviors

from pathlib import Path

import pytest

from src.checker import PseudocodeChecker


@pytest.fixture
def checker():
    return PseudocodeChecker(treat_warnings_as_failure=False)


def test_undeclared_variable(checker):
    source = "OUTPUT x\n"
    result = checker.check(source)
    assert result.ok is False
    assert result.stage == "semantic"
    assert any("declared" in e["message"].lower() for e in result.errors)


def test_type_mismatch_assignment(checker):
    source = "DECLARE x : INTEGER\nx <- \"hello\"\n"
    result = checker.check(source)
    assert result.ok is False
    assert any("type mismatch" in e["message"].lower() for e in result.errors)


def test_array_index_type(checker):
    source = (
        "DECLARE a : ARRAY[1:5] OF INTEGER\n"
        "a[\"a\"] <- 1\n"
    )
    result = checker.check(source)
    assert result.ok is False
    assert any("array index" in e["message"].lower() for e in result.errors)


def test_procedure_argument_count_mismatch(checker):
    source = (
        "PROCEDURE p(a: INTEGER, b: INTEGER)\n"
        "ENDPROCEDURE\n"
        "CALL p(1)\n"
    )
    result = checker.check(source)
    assert result.ok is False
    assert any("expects" in e["message"].lower() or "arguments" in e["message"].lower() for e in result.errors)
