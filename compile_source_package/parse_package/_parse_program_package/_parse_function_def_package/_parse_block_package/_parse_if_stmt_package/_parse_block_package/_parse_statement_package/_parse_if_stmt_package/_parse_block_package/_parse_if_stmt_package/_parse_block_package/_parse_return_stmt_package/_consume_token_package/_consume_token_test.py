# -*- coding: utf-8 -*-
"""Unit tests for _consume_token function."""

import pytest
from typing import Dict, Any

from ._consume_token_src import _consume_token


def _create_parser_state(
    tokens: list,
    filename: str = "test.py",
    pos: int = 0
) -> Dict[str, Any]:
    """Helper to create a parser state dict."""
    return {
        "tokens": tokens,
        "filename": filename,
        "pos": pos
    }


def _create_token(
    token_type: str,
    value: str = "",
    line: int = 1,
    column: int = 1
) -> Dict[str, Any]:
    """Helper to create a token dict."""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }


class TestConsumeTokenHappyPath:
    """Test cases for successful token consumption."""

    def test_consume_token_matches_and_advances_pos(self):
        """Token type matches: pos should advance by 1."""
        token = _create_token("RETURN", "return", line=5, column=10)
        parser_state = _create_parser_state([token], pos=0)
        
        result = _consume_token(parser_state, "RETURN")
        
        assert result == token
        assert parser_state["pos"] == 1

    def test_consume_token_at_middle_position(self):
        """Consume token when pos is not at start."""
        token1 = _create_token("IF", "if", line=1, column=1)
        token2 = _create_token("SEMICOLON", ";", line=1, column=5)
        token3 = _create_token("RETURN", "return", line=2, column=1)
        parser_state = _create_parser_state([token1, token2, token3], pos=1)
        
        result = _consume_token(parser_state, "SEMICOLON")
        
        assert result == token2
        assert parser_state["pos"] == 2

    def test_consume_token_last_token_in_list(self):
        """Consume the last token in the list."""
        token1 = _create_token("IF", "if")
        token2 = _create_token("RETURN", "return")
        parser_state = _create_parser_state([token1, token2], pos=1)
        
        result = _consume_token(parser_state, "RETURN")
        
        assert result == token2
        assert parser_state["pos"] == 2

    def test_consume_token_preserves_other_state_fields(self):
        """Other parser state fields should remain unchanged."""
        token = _create_token("RETURN", "return")
        parser_state = _create_parser_state([token], filename="source.py", pos=0)
        parser_state["error"] = None
        parser_state["extra_field"] = "value"
        
        _consume_token(parser_state, "RETURN")
        
        assert parser_state["filename"] == "source.py"
        assert parser_state["error"] is None
        assert parser_state["extra_field"] == "value"


class TestConsumeTokenNoTokensRemaining:
    """Test cases when no tokens are available to consume."""

    def test_consume_token_empty_tokens_list(self):
        """Empty tokens list should raise SyntaxError with EOF."""
        parser_state = _create_parser_state([], pos=0)
        
        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state, "RETURN")
        
        assert "test.py:0:0: 期望 'RETURN'，但得到 'EOF'" in str(exc_info.value)

    def test_consume_token_pos_beyond_tokens_length(self):
        """Pos beyond tokens length should raise SyntaxError with EOF."""
        token = _create_token("RETURN", "return")
        parser_state = _create_parser_state([token], pos=1)
        
        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state, "SEMICOLON")
        
        assert "test.py:0:0: 期望 'SEMICOLON'，但得到 'EOF'" in str(exc_info.value)

    def test_consume_token_pos_at_exact_tokens_length(self):
        """Pos equal to tokens length should raise SyntaxError with EOF."""
        token1 = _create_token("IF", "if")
        token2 = _create_token("RETURN", "return")
        parser_state = _create_parser_state([token1, token2], pos=2)
        
        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state, "SEMICOLON")
        
        assert "test.py:0:0: 期望 'SEMICOLON'，但得到 'EOF'" in str(exc_info.value)

    def test_consume_token_no_tokens_custom_filename(self):
        """Error message should include custom filename."""
        parser_state = _create_parser_state([], filename="mysource.py", pos=0)
        
        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state, "RETURN")
        
        assert "mysource.py:0:0: 期望 'RETURN'，但得到 'EOF'" in str(exc_info.value)


class TestConsumeTokenTypeMismatch:
    """Test cases when token type does not match expected."""

    def test_consume_token_type_mismatch(self):
        """Token type mismatch should raise SyntaxError with actual type."""
        token = _create_token("IF", "if", line=3, column=5)
        parser_state = _create_parser_state([token], pos=0)
        
        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state, "RETURN")
        
        assert "test.py:3:5: 期望 'RETURN'，但得到 'IF'" in str(exc_info.value)

    def test_consume_token_type_mismatch_preserves_pos(self):
        """Pos should not change on type mismatch."""
        token = _create_token("IF", "if")
        parser_state = _create_parser_state([token], pos=0)
        
        with pytest.raises(SyntaxError):
            _consume_token(parser_state, "RETURN")
        
        assert parser_state["pos"] == 0

    def test_consume_token_type_mismatch_with_line_column(self):
        """Error should include line and column from token."""
        token = _create_token("SEMICOLON", ";", line=10, column=25)
        parser_state = _create_parser_state([token], pos=0)
        
        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state, "RETURN")
        
        assert "test.py:10:25: 期望 'RETURN'，但得到 'SEMICOLON'" in str(exc_info.value)

    def test_consume_token_type_mismatch_missing_line_column(self):
        """Error should use 0:0 if line/column missing from token."""
        token = {"type": "IF", "value": "if"}  # No line/column
        parser_state = _create_parser_state([token], pos=0)
        
        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state, "RETURN")
        
        assert "test.py:0:0: 期望 'RETURN'，但得到 'IF'" in str(exc_info.value)

    def test_consume_token_type_mismatch_custom_filename(self):
        """Error message should include custom filename."""
        token = _create_token("IF", "if", line=2, column=3)
        parser_state = _create_parser_state([token], filename="custom.py", pos=0)
        
        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state, "RETURN")
        
        assert "custom.py:2:3: 期望 'RETURN'，但得到 'IF'" in str(exc_info.value)


class TestConsumeTokenEdgeCases:
    """Edge case tests."""

    def test_consume_token_multiple_sequential_consumes(self):
        """Multiple sequential consumes should work correctly."""
        token1 = _create_token("IF", "if", line=1, column=1)
        token2 = _create_token("LPAREN", "(", line=1, column=3)
        token3 = _create_token("RPAREN", ")", line=1, column=4)
        parser_state = _create_parser_state([token1, token2, token3], pos=0)
        
        result1 = _consume_token(parser_state, "IF")
        result2 = _consume_token(parser_state, "LPAREN")
        result3 = _consume_token(parser_state, "RPAREN")
        
        assert result1 == token1
        assert result2 == token2
        assert result3 == token3
        assert parser_state["pos"] == 3

    def test_consume_token_empty_string_expected_type(self):
        """Empty string as expected_type should still work if matches."""
        token = _create_token("", "empty", line=1, column=1)
        parser_state = _create_parser_state([token], pos=0)
        
        result = _consume_token(parser_state, "")
        
        assert result == token
        assert parser_state["pos"] == 1

    def test_consume_token_special_characters_in_type(self):
        """Token types with special characters should work."""
        token = _create_token("OP+", "+", line=1, column=1)
        parser_state = _create_parser_state([token], pos=0)
        
        result = _consume_token(parser_state, "OP+")
        
        assert result == token
        assert parser_state["pos"] == 1
