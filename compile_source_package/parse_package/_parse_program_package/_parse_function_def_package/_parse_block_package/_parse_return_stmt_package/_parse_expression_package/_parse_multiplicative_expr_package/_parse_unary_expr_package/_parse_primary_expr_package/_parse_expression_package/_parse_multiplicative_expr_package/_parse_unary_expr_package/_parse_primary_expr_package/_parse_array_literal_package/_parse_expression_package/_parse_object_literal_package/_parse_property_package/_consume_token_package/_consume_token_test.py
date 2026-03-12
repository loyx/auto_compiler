import pytest
from ._consume_token_src import _consume_token


class TestConsumeToken:
    """Test cases for _consume_token function."""
    
    def test_consume_token_success(self):
        """Happy path: token type matches expected type."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        result = _consume_token(parser_state, "NUMBER")
        
        assert result == {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
        assert parser_state["pos"] == 1
    
    def test_consume_token_type_mismatch(self):
        """Error case: token type doesn't match expected type."""
        parser_state = {
            "tokens": [
                {"type": "STRING", "value": "hello", "line": 2, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        with pytest.raises(ValueError) as exc_info:
            _consume_token(parser_state, "NUMBER")
        
        assert "Expected NUMBER, got STRING" in str(exc_info.value)
        assert "line 2" in str(exc_info.value)
        assert "column 5" in str(exc_info.value)
        assert parser_state["pos"] == 0  # pos should not change on error
    
    def test_consume_token_pos_out_of_bounds(self):
        """Error case: pos is at end of tokens."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            ],
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        
        with pytest.raises(ValueError) as exc_info:
            _consume_token(parser_state, "NUMBER")
        
        assert "Unexpected end of input" in str(exc_info.value)
        assert parser_state["pos"] == 1  # pos should not change on error
    
    def test_consume_token_empty_tokens(self):
        """Edge case: empty tokens list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        with pytest.raises(ValueError) as exc_info:
            _consume_token(parser_state, "NUMBER")
        
        assert "Unexpected end of input" in str(exc_info.value)
        assert parser_state["pos"] == 0
    
    def test_consume_token_last_element(self):
        """Edge case: consuming the last token in the list."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 3, "column": 10}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        result = _consume_token(parser_state, "IDENTIFIER")
        
        assert result == {"type": "IDENTIFIER", "value": "x", "line": 3, "column": 10}
        assert parser_state["pos"] == 1
    
    def test_consume_token_multiple_tokens(self):
        """Test consuming tokens from a list with multiple tokens."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
            ],
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        
        result = _consume_token(parser_state, "PLUS")
        
        assert result == {"type": "PLUS", "value": "+", "line": 1, "column": 3}
        assert parser_state["pos"] == 2
    
    def test_consume_token_missing_line_column(self):
        """Edge case: token missing line/column info."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "if"}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        with pytest.raises(ValueError) as exc_info:
            _consume_token(parser_state, "NUMBER")
        
        error_msg = str(exc_info.value)
        assert "Expected NUMBER, got KEYWORD" in error_msg
        assert "line ?" in error_msg
        assert "column ?" in error_msg
