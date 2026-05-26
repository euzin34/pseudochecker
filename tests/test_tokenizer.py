# Tokenizer unit tests.

from src.tokenizer import Tokenizer, TokenType


def test_keywords_and_assign():
    tokens = Tokenizer("DECLARE x : INTEGER\nx <- 5").tokenize()
    types = [t.type for t in tokens if t.type != TokenType.EOF]
    assert TokenType.DECLARE in types
    assert TokenType.ASSIGN in types


def test_unterminated_string_raises():
    import pytest
    from src.errors import SyntaxError

    with pytest.raises(SyntaxError):
        Tokenizer('OUTPUT "hello').tokenize()
