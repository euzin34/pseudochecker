# Tests for utils, runtime_builtins, and error formatting

import os
import tempfile

from src import utils
from src import runtime_builtins as rb
from src.errors import SyntaxError, SemanticError, TypeError as PTypeError, WarningError, ErrorCollector


def test_utils_basic_functions(tmp_path):
    code = "// comment\nline2\n\nline4"
    assert utils.format_error_location(3, 5) == "Line 3, Column 5"
    assert utils.count_lines(code) == 4
    assert utils.get_line_content(code, 1).startswith("// comment")
    assert utils.get_line_content(code, 99) is None
    assert utils.highlight_error_position("abc", 2).endswith("^")
    assert utils.highlight_error_position("abc", 0) == ""
    assert utils.validate_file_extension("file.txt")
    assert not utils.validate_file_extension("file.py")

    # read_file_safely: create a temp file
    p = tmp_path / "sample.txt"
    p.write_text("hello", encoding="utf-8")
    content, err = utils.read_file_safely(str(p))
    assert err is None and content == "hello"

    missing, err = utils.read_file_safely(str(p) + ".missing")
    assert missing is None and "not found" in err

    stats = utils.get_file_stats(code)
    assert stats["total_lines"] == 4
    formatted = utils.format_file_stats(stats)
    assert "lines" in formatted


def test_runtime_builtins_basic_behavior():
    assert rb.LENGTH("abc") == 3
    assert rb.LEFT("abcd", 2) == "ab"
    assert rb.RIGHT("abcd", 2) == "cd"
    assert rb.MID("hello", 2, 3) == "ell"
    assert rb.LCASE("A") == "a"
    assert rb.UCASE("a") == "A"
    assert isinstance(rb.RAND(5), int)
    assert 1 <= rb.RAND(5) <= 5
    assert isinstance(rb.RANDOM(), float)
    assert rb.NUM_TO_STR(42) == "42"
    assert rb.STR_TO_NUM("42") == 42
    assert rb.IS_NUM("123")
    assert rb.ASC("A") == ord("A")
    assert rb.CHR(65) == "A"
    assert rb.MOD(7, 3) == 7 % 3
    assert rb.DIV(7, 3) == 7 // 3
    assert rb.EOF("no-such-file.txt") is False


def test_error_collector_and_errors():
    ec = ErrorCollector()
    e1 = SyntaxError("bad", 2, 3, "fixit")
    e2 = SemanticError("sem", 1, 1, None)
    w = WarningError("warn", 5, 1, None)

    ec.add_error(e1)
    ec.add_error(e2)
    ec.add_error(w)

    assert ec.has_errors()
    assert ec.has_warnings()

    all_issues = ec.get_all()
    # Should be sorted by line number: e2 (line1), e1 (line2), w (line5)
    assert all_issues[0].line == 1
    assert all_issues[-1].line == 5

    report = ec.report()
    assert "ERROR REPORT" in report
    assert "SYNTAX ERROR" in str(e1)
    assert "SEMANTIC ERROR" in str(e2)
    assert "WARNING" in str(w)
