"""
Unit tests for _consume_token function.
"""
import pytest
from ._consume_token_src import _consume_token


class TestConsumeToken:
    """Test cases for _consume_token function."""

    def test_consume_token_without_expected_type(self):
        """Happy path: consume token without specifying expected_type."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state)
        
        assert result == {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        assert parser_state["pos"] == 1

    def test_consume_token_with_matching_expected_type(self):
        """Happy path: consume token with matching expected_type."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "if", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state, expected_type="KEYWORD")
        
        assert result == {"type": "KEYWORD", "value": "if", "line": 1, "column": 1}
        assert parser_state["pos"] == 1

    def test_consume_token_with_mismatched_expected_type(self):
        """Error case: expected_type doesn't match current token type."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state, expected_type="KEYWORD")
        
        assert "Expected token type 'KEYWORD', got 'IDENTIFIER'" in str(exc_info.value)
        # Position should not be advanced on error
        assert parser_state["pos"] == 0

    def test_consume_token_at_end_of_tokens(self):
        """Boundary case: pos equals length of tokens (end of file)."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 1,
            "filename": "test.py",
        }
        
        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state)
        
        assert "Unexpected end of file" in str(exc_info.value)

    def test_consume_token_beyond_end_of_tokens(self):
        """Boundary case: pos exceeds length of tokens."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 5,
            "filename": "test.py",
        }
        
        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state)
        
        assert "Unexpected end of file" in str(exc_info.value)

    def test_consume_token_from_empty_tokens_list(self):
        """Edge case: empty tokens list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
        }
        
        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state)
        
        assert "Unexpected end of file" in str(exc_info.value)

    def test_consume_token_advances_position(self):
        """Side effect: verify parser_state['pos'] is incremented correctly."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 4},
                {"type": "NUMBER", "value": "10", "line": 1, "column": 6},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        # Consume first token
        _consume_token(parser_state)
        assert parser_state["pos"] == 1
        
        # Consume second token
        _consume_token(parser_state)
        assert parser_state["pos"] == 2
        
        # Consume third token
        _consume_token(parser_state)
        assert parser_state["pos"] == 3

    def test_consume_token_middle_of_list(self):
        """Happy path: consume token from middle of token list."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            ],
            "pos": 1,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state)
        
        assert result == {"type": "OPERATOR", "value": "+", "line": 1, "column": 3}
        assert parser_state["pos"] == 2

    def test_consume_token_preserves_token_data(self):
        """Verify returned token contains all expected fields."""
        parser_state = {
            "tokens": [
                {"type": "STRING", "value": "hello", "line": 5, "column": 10},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state)
        
        assert result["type"] == "STRING"
        assert result["value"] == "hello"
        assert result["line"] == 5
        assert result["column"] == 10

    def test_consume_token_multiple_calls_sequential(self):
        """Integration: consume multiple tokens sequentially."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 8},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 9},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        token1 = _consume_token(parser_state, expected_type="KEYWORD")
        assert token1["value"] == "while"
        assert parser_state["pos"] == 1
        
        token2 = _consume_token(parser_state, expected_type="LPAREN")
        assert token2["value"] == "("
        assert parser_state["pos"] == 2
        
        token3 = _consume_token(parser_state, expected_type="IDENTIFIER")
        assert token3["value"] == "x"
        assert parser_state["pos"] == 3
        
        token4 = _consume_token(parser_state, expected_type="RPAREN")
        assert token4["value"] == ")"
        assert parser_state["pos"] == 4
