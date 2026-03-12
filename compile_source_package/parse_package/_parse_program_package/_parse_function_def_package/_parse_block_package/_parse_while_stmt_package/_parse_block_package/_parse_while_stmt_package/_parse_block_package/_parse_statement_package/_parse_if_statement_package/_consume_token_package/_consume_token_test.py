# -*- coding: utf-8 -*-
"""Unit tests for _consume_token function."""

import pytest
from typing import Dict, Any

from ._consume_token_src import _consume_token


def _create_parser_state(tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
    """Helper to create a parser state dict."""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename
    }


def _create_token(token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
    """Helper to create a token dict."""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }


class TestConsumeTokenHappyPath:
    """Test happy path scenarios for _consume_token."""

    def test_consume_token_without_expected_type(self):
        """Test consuming token without type validation."""
        token = _create_token("IDENTIFIER", "x", line=1, column=5)
        parser_state = _create_parser_state([token], pos=0)
        
        result = _consume_token(parser_state)
        
        assert result == token
        assert parser_state["pos"] == 1

    def test_consume_token_with_matching_expected_type(self):
        """Test consuming token with matching expected type."""
        token = _create_token("KEYWORD", "while", line=3, column=1)
        parser_state = _create_parser_state([token], pos=0)
        
        result = _consume_token(parser_state, expected_type="KEYWORD")
        
        assert result == token
        assert parser_state["pos"] == 1

    def test_consume_multiple_tokens_sequentially(self):
        """Test consuming multiple tokens in sequence."""
        tokens = [
            _create_token("KEYWORD", "while", line=1, column=1),
            _create_token("LPAREN", "(", line=1, column=6),
            _create_token("IDENTIFIER", "x", line=1, column=7),
        ]
        parser_state = _create_parser_state(tokens, pos=0)
        
        result1 = _consume_token(parser_state, expected_type="KEYWORD")
        result2 = _consume_token(parser_state, expected_type="LPAREN")
        result3 = _consume_token(parser_state, expected_type="IDENTIFIER")
        
        assert result1 == tokens[0]
        assert result2 == tokens[1]
        assert result3 == tokens[2]
        assert parser_state["pos"] == 3

    def test_consume_token_from_middle_position(self):
        """Test consuming token starting from middle position."""
        tokens = [
            _create_token("KEYWORD", "if", line=1, column=1),
            _create_token("LPAREN", "(", line=1, column=3),
            _create_token("IDENTIFIER", "x", line=1, column=4),
        ]
        parser_state = _create_parser_state(tokens, pos=1)
        
        result = _consume_token(parser_state)
        
        assert result == tokens[1]
        assert parser_state["pos"] == 2


class TestConsumeTokenEOF:
    """Test EOF (end of file) error scenarios."""

    def test_consume_token_at_eof(self):
        """Test error when pos is at end of tokens."""
        tokens = [_create_token("IDENTIFIER", "x")]
        parser_state = _create_parser_state(tokens, pos=1)
        
        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state)
        
        assert "Unexpected end of input" in str(exc_info.value)
        assert "test.py" in str(exc_info.value)

    def test_consume_token_beyond_eof(self):
        """Test error when pos is beyond end of tokens."""
        tokens = [_create_token("IDENTIFIER", "x")]
        parser_state = _create_parser_state(tokens, pos=5)
        
        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state)
        
        assert "Unexpected end of input" in str(exc_info.value)

    def test_consume_token_from_empty_tokens_list(self):
        """Test error when tokens list is empty."""
        parser_state = _create_parser_state([], pos=0)
        
        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state)
        
        assert "Unexpected end of input" in str(exc_info.value)

    def test_eof_error_includes_filename(self):
        """Test that EOF error includes the filename."""
        tokens = [_create_token("IDENTIFIER", "x")]
        parser_state = _create_parser_state(tokens, pos=1, filename="my_module.py")
        
        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state)
        
        assert "my_module.py" in str(exc_info.value)

    def test_eof_error_with_unknown_filename(self):
        """Test EOF error when filename is not provided."""
        parser_state = {"tokens": [], "pos": 0}
        
        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state)
        
        assert "unknown" in str(exc_info.value)


class TestConsumeTokenTypeMismatch:
    """Test token type mismatch error scenarios."""

    def test_consume_token_with_wrong_expected_type(self):
        """Test error when token type doesn't match expected type."""
        token = _create_token("IDENTIFIER", "x", line=2, column=10)
        parser_state = _create_parser_state([token], pos=0)
        
        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state, expected_type="KEYWORD")
        
        assert "Expected token type 'KEYWORD'" in str(exc_info.value)
        assert "got 'IDENTIFIER'" in str(exc_info.value)
        assert "line 2" in str(exc_info.value)
        assert "column 10" in str(exc_info.value)

    def test_type_mismatch_error_includes_location(self):
        """Test that type mismatch error includes line and column."""
        token = _create_token("OPERATOR", "+", line=5, column=15)
        parser_state = _create_parser_state([token], pos=0)
        
        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state, expected_type="IDENTIFIER")
        
        assert "line 5" in str(exc_info.value)
        assert "column 15" in str(exc_info.value)

    def test_type_mismatch_preserves_pos(self):
        """Test that pos is not advanced on type mismatch."""
        token = _create_token("IDENTIFIER", "x")
        parser_state = _create_parser_state([token], pos=0)
        
        with pytest.raises(SyntaxError):
            _consume_token(parser_state, expected_type="KEYWORD")
        
        assert parser_state["pos"] == 0


class TestConsumeTokenEdgeCases:
    """Test edge cases and special scenarios."""

    def test_consume_token_with_none_expected_type(self):
        """Test that None expected_type behaves like no validation."""
        token = _create_token("IDENTIFIER", "x")
        parser_state = _create_parser_state([token], pos=0)
        
        result = _consume_token(parser_state, expected_type=None)
        
        assert result == token
        assert parser_state["pos"] == 1

    def test_consume_token_modifies_state_in_place(self):
        """Test that parser_state is modified in-place, not copied."""
        token = _create_token("IDENTIFIER", "x")
        parser_state = _create_parser_state([token], pos=0)
        original_ref = parser_state
        
        _consume_token(parser_state)
        
        assert original_ref is parser_state
        assert original_ref["pos"] == 1

    def test_consume_token_returns_same_dict_reference(self):
        """Test that returned token is the same dict reference."""
        token = _create_token("IDENTIFIER", "x")
        parser_state = _create_parser_state([token], pos=0)
        
        result = _consume_token(parser_state)
        
        assert result is token

    def test_consume_token_with_special_characters_in_value(self):
        """Test consuming token with special characters in value."""
        token = _create_token("STRING", '"hello\\nworld"', line=1, column=1)
        parser_state = _create_parser_state([token], pos=0)
        
        result = _consume_token(parser_state)
        
        assert result["value"] == '"hello\\nworld"'
        assert parser_state["pos"] == 1

    def test_consume_token_with_unicode_value(self):
        """Test consuming token with unicode characters."""
        token = _create_token("IDENTIFIER", "变量", line=1, column=1)
        parser_state = _create_parser_state([token], pos=0)
        
        result = _consume_token(parser_state)
        
        assert result["value"] == "变量"
        assert parser_state["pos"] == 1
