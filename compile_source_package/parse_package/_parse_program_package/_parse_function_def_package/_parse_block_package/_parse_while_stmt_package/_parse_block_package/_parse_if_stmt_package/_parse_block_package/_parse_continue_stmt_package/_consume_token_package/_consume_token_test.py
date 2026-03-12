# === test file for _consume_token ===
import pytest
from ._consume_token_src import _consume_token


class TestConsumeToken:
    """Test cases for _consume_token function"""

    def test_consume_token_normal(self):
        """Happy path: consume token when pos is within bounds"""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "OP", "value": "=", "line": 1, "column": 3},
                {"type": "NUM", "value": "5", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state)
        
        assert result["pos"] == 1
        assert result is parser_state  # Should return same object

    def test_consume_token_at_last_token(self):
        """Boundary: pos at the last token, should still increment"""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state)
        
        assert result["pos"] == 1
        assert len(result["tokens"]) == 1  # tokens unchanged

    def test_consume_token_beyond_bounds(self):
        """Boundary: pos already beyond tokens, should not increment"""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 5,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state)
        
        assert result["pos"] == 5  # pos unchanged

    def test_consume_token_at_end_boundary(self):
        """Boundary: pos equals len(tokens), should not increment"""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "OP", "value": "=", "line": 1, "column": 3},
            ],
            "pos": 2,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state)
        
        assert result["pos"] == 2  # pos unchanged

    def test_consume_token_empty_tokens(self):
        """Edge case: empty tokens list"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state)
        
        assert result["pos"] == 0  # pos unchanged

    def test_consume_token_missing_tokens_key(self):
        """Edge case: parser_state without 'tokens' key"""
        parser_state = {
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state)
        
        assert result["pos"] == 0  # pos unchanged (default tokens is [])

    def test_consume_token_missing_pos_key(self):
        """Edge case: parser_state without 'pos' key"""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            ],
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state)
        
        assert result["pos"] == 1  # pos defaults to 0, then increments

    def test_consume_token_multiple_times(self):
        """State change: consume multiple tokens in sequence"""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "OP", "value": "=", "line": 1, "column": 3},
                {"type": "NUM", "value": "5", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        # Consume first token
        result1 = _consume_token(parser_state)
        assert result1["pos"] == 1
        
        # Consume second token
        result2 = _consume_token(parser_state)
        assert result2["pos"] == 2
        
        # Consume third token
        result3 = _consume_token(parser_state)
        assert result3["pos"] == 3
        
        # Try to consume beyond bounds
        result4 = _consume_token(parser_state)
        assert result4["pos"] == 3  # Should not increment

    def test_consume_token_preserves_other_fields(self):
        """Verify other parser_state fields are preserved"""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": "",
            "custom_field": "custom_value",
        }
        
        result = _consume_token(parser_state)
        
        assert result["filename"] == "test.py"
        assert result["error"] == ""
        assert result["custom_field"] == "custom_value"
        assert result["pos"] == 1

    def test_consume_token_does_not_modify_tokens(self):
        """Verify tokens list is not modified"""
        original_tokens = [
            {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            {"type": "OP", "value": "=", "line": 1, "column": 3},
        ]
        parser_state = {
            "tokens": original_tokens,
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state)
        
        assert result["tokens"] is original_tokens
        assert len(result["tokens"]) == 2
        assert result["tokens"][0]["type"] == "IDENT"
        assert result["tokens"][1]["type"] == "OP"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
