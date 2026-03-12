# -*- coding: utf-8 -*-
"""Unit tests for _consume_token function."""

import pytest

from ._consume_token_src import _consume_token


class TestConsumeTokenHappyPath:
    """Test happy path scenarios for _consume_token."""

    def test_consume_token_success(self):
        """Test successful token consumption when type matches."""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
            ],
            "filename": "test.py",
            "pos": 0,
        }

        result = _consume_token(parser_state, "IF")

        assert result == {"type": "IF", "value": "if", "line": 1, "column": 1}
        assert parser_state["pos"] == 1

    def test_consume_token_second_token(self):
        """Test consuming second token after first was consumed."""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
            ],
            "filename": "test.py",
            "pos": 1,
        }

        result = _consume_token(parser_state, "IDENTIFIER")

        assert result == {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4}
        assert parser_state["pos"] == 2

    def test_consume_token_multiple_sequential(self):
        """Test multiple sequential token consumptions."""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
            ],
            "filename": "test.py",
            "pos": 0,
        }

        token1 = _consume_token(parser_state, "IF")
        token2 = _consume_token(parser_state, "LPAREN")
        token3 = _consume_token(parser_state, "IDENTIFIER")

        assert token1["type"] == "IF"
        assert token2["type"] == "LPAREN"
        assert token3["type"] == "IDENTIFIER"
        assert parser_state["pos"] == 3


class TestConsumeTokenEndOfInput:
    """Test end of input error scenarios."""

    def test_consume_token_empty_tokens(self):
        """Test error when tokens list is empty."""
        parser_state = {
            "tokens": [],
            "filename": "test.py",
            "pos": 0,
        }

        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state, "IF")

        assert "Unexpected end of input" in str(exc_info.value)
        assert "test.py:0:0" in str(exc_info.value)
        assert "expected IF" in str(exc_info.value)

    def test_consume_token_pos_beyond_tokens(self):
        """Test error when position is beyond tokens length."""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
            ],
            "filename": "test.py",
            "pos": 1,
        }

        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state, "IDENTIFIER")

        assert "Unexpected end of input" in str(exc_info.value)
        assert "test.py:0:0" in str(exc_info.value)

    def test_consume_token_pos_at_end(self):
        """Test error when position equals tokens length."""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
            ],
            "filename": "module.py",
            "pos": 2,
        }

        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state, "RPAREN")

        assert "Unexpected end of input" in str(exc_info.value)
        assert "module.py:0:0" in str(exc_info.value)


class TestConsumeTokenTypeMismatch:
    """Test token type mismatch error scenarios."""

    def test_consume_token_type_mismatch(self):
        """Test error when token type doesn't match expected."""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
            ],
            "filename": "test.py",
            "pos": 0,
        }

        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state, "WHILE")

        assert "Expected WHILE, got IF" in str(exc_info.value)
        assert "test.py:1:1" in str(exc_info.value)

    def test_consume_token_type_mismatch_different_location(self):
        """Test error message includes correct token location."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 5, "column": 10},
            ],
            "filename": "error.py",
            "pos": 0,
        }

        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state, "NUMBER")

        assert "Expected NUMBER, got IDENTIFIER" in str(exc_info.value)
        assert "error.py:5:10" in str(exc_info.value)

    def test_consume_token_pos_not_advanced_on_error(self):
        """Test that position is not advanced when error occurs."""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
            ],
            "filename": "test.py",
            "pos": 0,
        }

        with pytest.raises(SyntaxError):
            _consume_token(parser_state, "WHILE")

        assert parser_state["pos"] == 0


class TestConsumeTokenEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_consume_token_with_complex_filename(self):
        """Test error message with complex filename path."""
        parser_state = {
            "tokens": [],
            "filename": "/path/to/complex/module_name.py",
            "pos": 0,
        }

        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state, "IF")

        assert "/path/to/complex/module_name.py:0:0" in str(exc_info.value)

    def test_consume_token_preserves_other_state_fields(self):
        """Test that other parser state fields are not modified."""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
            ],
            "filename": "test.py",
            "pos": 0,
            "error": None,
            "extra_field": "should_not_change",
        }

        _consume_token(parser_state, "IF")

        assert parser_state["error"] is None
        assert parser_state["extra_field"] == "should_not_change"
        assert parser_state["filename"] == "test.py"

    def test_consume_token_returns_token_dict(self):
        """Test that returned token is the exact dict from tokens list."""
        token_dict = {"type": "IF", "value": "if", "line": 1, "column": 1}
        parser_state = {
            "tokens": [token_dict],
            "filename": "test.py",
            "pos": 0,
        }

        result = _consume_token(parser_state, "IF")

        assert result is token_dict
