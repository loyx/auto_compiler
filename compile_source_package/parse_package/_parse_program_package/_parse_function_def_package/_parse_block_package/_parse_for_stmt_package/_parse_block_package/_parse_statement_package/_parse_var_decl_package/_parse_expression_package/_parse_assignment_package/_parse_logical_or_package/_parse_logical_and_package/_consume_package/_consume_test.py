"""Unit tests for _consume function."""
import pytest
from ._consume_src import _consume


class TestConsume:
    """Test cases for _consume function."""

    def test_consume_success_type_only(self):
        """Test consuming token with only type check."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        result = _consume(parser_state, "IDENTIFIER")

        assert result == {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        assert parser_state["pos"] == 1
        assert "error" not in parser_state

    def test_consume_success_with_value(self):
        """Test consuming token with type and value check."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "for", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        result = _consume(parser_state, "KEYWORD", "for")

        assert result == {"type": "KEYWORD", "value": "for", "line": 1, "column": 1}
        assert parser_state["pos"] == 1
        assert "error" not in parser_state

    def test_consume_multiple_tokens_sequentially(self):
        """Test consuming multiple tokens in sequence."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        result1 = _consume(parser_state, "IDENTIFIER")
        assert result1["value"] == "x"
        assert parser_state["pos"] == 1

        result2 = _consume(parser_state, "OPERATOR", "=")
        assert result2["value"] == "="
        assert parser_state["pos"] == 2

        result3 = _consume(parser_state, "NUMBER")
        assert result3["value"] == "5"
        assert parser_state["pos"] == 3

    def test_consume_from_middle_position(self):
        """Test consuming token from non-zero position."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 5}
            ],
            "pos": 1,
            "filename": "test.py"
        }

        result = _consume(parser_state, "OPERATOR", "=")

        assert result["value"] == "="
        assert parser_state["pos"] == 2

    def test_consume_end_of_input(self):
        """Test consuming when pos is at end of tokens."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 1,
            "filename": "test.py"
        }

        with pytest.raises(ValueError) as exc_info:
            _consume(parser_state, "IDENTIFIER")

        assert "Unexpected end of input" in str(exc_info.value)
        assert parser_state["error"] is not None
        assert "expected IDENTIFIER" in parser_state["error"]
        assert parser_state["pos"] == 1

    def test_consume_empty_tokens(self):
        """Test consuming from empty token list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }

        with pytest.raises(ValueError) as exc_info:
            _consume(parser_state, "IDENTIFIER")

        assert "Unexpected end of input" in str(exc_info.value)
        assert parser_state["error"] is not None
        assert parser_state["pos"] == 0

    def test_consume_type_mismatch(self):
        """Test consuming with wrong token type."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "5", "line": 2, "column": 10}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        with pytest.raises(ValueError) as exc_info:
            _consume(parser_state, "IDENTIFIER")

        assert "Token type mismatch" in str(exc_info.value)
        assert "line 2" in str(exc_info.value)
        assert "column 10" in str(exc_info.value)
        assert "expected IDENTIFIER" in str(exc_info.value)
        assert "got NUMBER" in str(exc_info.value)
        assert parser_state["error"] is not None
        assert parser_state["pos"] == 0

    def test_consume_value_mismatch(self):
        """Test consuming with wrong token value."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 3, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        with pytest.raises(ValueError) as exc_info:
            _consume(parser_state, "KEYWORD", "for")

        assert "Token value mismatch" in str(exc_info.value)
        assert "line 3" in str(exc_info.value)
        assert "column 5" in str(exc_info.value)
        assert "expected 'for'" in str(exc_info.value)
        assert "got 'while'" in str(exc_info.value)
        assert parser_state["error"] is not None
        assert parser_state["pos"] == 0

    def test_consume_missing_filename(self):
        """Test error message when filename is missing."""
        parser_state = {
            "tokens": [],
            "pos": 0
        }

        with pytest.raises(ValueError) as exc_info:
            _consume(parser_state, "IDENTIFIER")

        assert "unknown" in str(exc_info.value)
        assert parser_state["error"] is not None

    def test_consume_token_missing_type_field(self):
        """Test consuming token without type field."""
        parser_state = {
            "tokens": [
                {"value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        with pytest.raises(ValueError) as exc_info:
            _consume(parser_state, "IDENTIFIER")

        assert "Token type mismatch" in str(exc_info.value)
        assert parser_state["error"] is not None
        assert parser_state["pos"] == 0

    def test_consume_token_missing_value_field(self):
        """Test consuming token without value field when value is expected."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        with pytest.raises(ValueError) as exc_info:
            _consume(parser_state, "KEYWORD", "for")

        assert "Token value mismatch" in str(exc_info.value)
        assert parser_state["error"] is not None
        assert parser_state["pos"] == 0

    def test_consume_pos_beyond_tokens(self):
        """Test consuming when pos is beyond tokens length."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 5,
            "filename": "test.py"
        }

        with pytest.raises(ValueError) as exc_info:
            _consume(parser_state, "IDENTIFIER")

        assert "Unexpected end of input" in str(exc_info.value)
        assert parser_state["error"] is not None
        assert parser_state["pos"] == 5
