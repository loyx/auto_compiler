# -*- coding: utf-8 -*-
"""Unit tests for _consume_token function."""

import pytest
from typing import Dict, Any

from ._consume_token_src import _consume_token


class TestConsumeTokenHappyPath:
    """Test happy path scenarios for _consume_token."""

    def test_consume_first_token(self):
        """Test consuming the first token in the list."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        token = _consume_token(parser_state)
        
        assert token == {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        assert parser_state["pos"] == 1

    def test_consume_middle_token(self):
        """Test consuming a token in the middle of the list."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 1,
            "filename": "test.py"
        }
        
        token = _consume_token(parser_state)
        
        assert token == {"type": "OPERATOR", "value": "=", "line": 1, "column": 3}
        assert parser_state["pos"] == 2

    def test_consume_last_token(self):
        """Test consuming the last token in the list (boundary case)."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 2,
            "filename": "test.py"
        }
        
        token = _consume_token(parser_state)
        
        assert token == {"type": "NUMBER", "value": "42", "line": 1, "column": 5}
        assert parser_state["pos"] == 3

    def test_consume_single_token(self):
        """Test consuming from a list with only one token."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "KEYWORD", "value": "return", "line": 5, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        token = _consume_token(parser_state)
        
        assert token == {"type": "KEYWORD", "value": "return", "line": 5, "column": 1}
        assert parser_state["pos"] == 1

    def test_consume_preserves_other_state_fields(self):
        """Test that other fields in parser_state are preserved."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None,
            "custom_field": "custom_value"
        }
        
        token = _consume_token(parser_state)
        
        assert parser_state["filename"] == "test.py"
        assert parser_state["error"] is None
        assert parser_state["custom_field"] == "custom_value"


class TestConsumeTokenErrorCases:
    """Test error scenarios for _consume_token."""

    def test_pos_beyond_tokens_raises_syntax_error(self):
        """Test that consuming when pos >= len(tokens) raises SyntaxError."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 1,
            "filename": "test.py"
        }
        
        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state)
        
        assert "Unexpected end of input" in str(exc_info.value)
        assert "test.py" in str(exc_info.value)

    def test_pos_at_empty_tokens_raises_syntax_error(self):
        """Test that consuming from empty tokens list raises SyntaxError."""
        parser_state: Dict[str, Any] = {
            "tokens": [],
            "pos": 0,
            "filename": "empty.py"
        }
        
        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state)
        
        assert "Unexpected end of input" in str(exc_info.value)
        assert "empty.py" in str(exc_info.value)

    def test_pos_far_beyond_tokens_raises_syntax_error(self):
        """Test that consuming when pos is far beyond tokens raises SyntaxError."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 10,
            "filename": "test.py"
        }
        
        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state)
        
        assert "Unexpected end of input" in str(exc_info.value)

    def test_syntax_error_uses_unknown_filename_when_missing(self):
        """Test that SyntaxError uses '<unknown>' when filename is not provided."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 1
            # No filename field
        }
        
        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state)
        
        assert "<unknown>" in str(exc_info.value)

    def test_pos_not_incremented_on_error(self):
        """Test that pos is not incremented when SyntaxError is raised."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 1,
            "filename": "test.py"
        }
        
        with pytest.raises(SyntaxError):
            _consume_token(parser_state)
        
        assert parser_state["pos"] == 1  # Should remain unchanged


class TestConsumeTokenTokenStructure:
    """Test that token structure is correctly returned."""

    def test_token_contains_all_required_fields(self):
        """Test that returned token contains type, value, line, column."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {
                    "type": "STRING",
                    "value": "hello",
                    "line": 10,
                    "column": 20
                },
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        token = _consume_token(parser_state)
        
        assert "type" in token
        assert "value" in token
        assert "line" in token
        assert "column" in token
        assert token["type"] == "STRING"
        assert token["value"] == "hello"
        assert token["line"] == 10
        assert token["column"] == 20

    def test_token_is_dict_copy_not_reference(self):
        """Test that returned token is independent (modifying it doesn't affect source)."""
        original_token = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        parser_state: Dict[str, Any] = {
            "tokens": [original_token],
            "pos": 0,
            "filename": "test.py"
        }
        
        token = _consume_token(parser_state)
        token["value"] = "modified"
        
        # The original token in the list should remain unchanged
        assert parser_state["tokens"][0]["value"] == "x"
