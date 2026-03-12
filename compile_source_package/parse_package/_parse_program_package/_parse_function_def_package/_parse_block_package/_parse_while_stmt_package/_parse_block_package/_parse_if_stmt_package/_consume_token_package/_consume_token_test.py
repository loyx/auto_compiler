import pytest

# Relative import from the same package
from ._consume_token_src import _consume_token


class TestConsumeToken:
    """Test cases for _consume_token function"""
    
    def test_consume_token_success(self):
        """Happy path: consume matching token type"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        result = _consume_token(parser_state, "IDENTIFIER")
        
        # Verify pos incremented
        assert result["pos"] == 1
        # Verify original state unchanged
        assert parser_state["pos"] == 0
        # Verify other fields preserved
        assert result["filename"] == "test.py"
        assert result["tokens"] == parser_state["tokens"]
    
    def test_consume_token_at_end(self):
        """Boundary: raise SyntaxError when at end of tokens"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        
        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state, "IDENTIFIER")
        
        assert "Unexpected end of input" in str(exc_info.value)
        assert "expected IDENTIFIER" in str(exc_info.value)
        # Verify original state unchanged
        assert parser_state["pos"] == 1
    
    def test_consume_token_mismatch(self):
        """Error case: token type doesn't match"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 5},
                {"type": "OPERATOR", "value": "=", "line": 2, "column": 7},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state, "OPERATOR")
        
        assert "Expected token type OPERATOR, got IDENTIFIER" in str(exc_info.value)
        assert "line 2:column 5" in str(exc_info.value)
        # Verify original state unchanged
        assert parser_state["pos"] == 0
    
    def test_consume_token_empty_tokens(self):
        """Edge case: empty tokens list"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state, "IDENTIFIER")
        
        assert "Unexpected end of input" in str(exc_info.value)
    
    def test_consume_token_last_token(self):
        """Boundary: consume last token successfully"""
        parser_state = {
            "tokens": [
                {"type": "SEMICOLON", "value": ";", "line": 3, "column": 10},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        result = _consume_token(parser_state, "SEMICOLON")
        
        assert result["pos"] == 1
        assert parser_state["pos"] == 0
    
    def test_consume_token_missing_line_column(self):
        """Edge case: token missing line/column info in error message"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x"},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        with pytest.raises(SyntaxError) as exc_info:
            _consume_token(parser_state, "OPERATOR")
        
        assert "line ?:column ?" in str(exc_info.value)
    
    def test_consume_token_returns_copy(self):
        """Verify function returns a copy, not modifying original"""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "if", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        result = _consume_token(parser_state, "KEYWORD")
        
        # Modify result, ensure original is unaffected
        result["pos"] = 999
        result["filename"] = "modified.py"
        
        assert parser_state["pos"] == 0
        assert parser_state["filename"] == "test.py"
    
    def test_consume_token_middle_position(self):
        """Consume token from middle position"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        
        result = _consume_token(parser_state, "OPERATOR")
        
        assert result["pos"] == 2
        assert parser_state["pos"] == 1
