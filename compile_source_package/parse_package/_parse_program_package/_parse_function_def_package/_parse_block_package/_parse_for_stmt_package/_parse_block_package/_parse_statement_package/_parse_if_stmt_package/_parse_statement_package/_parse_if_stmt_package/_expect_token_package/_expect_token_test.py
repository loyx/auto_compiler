import pytest

# Relative import from the same package
from ._expect_token_src import _expect_token, ParserState


class TestExpectToken:
    """Test cases for _expect_token function"""
    
    def test_expect_token_success_consumes_token(self):
        """Happy path: token type matches, pos increments by 1"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "RPAREN", "value": ")", "line": 1, "column": 10},
                {"type": "LBRACE", "value": "{", "line": 1, "column": 11},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        _expect_token(parser_state, "RPAREN")
        
        assert parser_state["pos"] == 1
        # Verify other fields unchanged
        assert parser_state["filename"] == "test.py"
        assert parser_state["error"] == ""
    
    def test_expect_token_success_multiple_tokens(self):
        """Verify consecutive token consumption works correctly"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 5},
                {"type": "IDENT", "value": "x", "line": 1, "column": 6},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 7},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        _expect_token(parser_state, "LPAREN")
        assert parser_state["pos"] == 1
        
        _expect_token(parser_state, "IDENT")
        assert parser_state["pos"] == 2
        
        _expect_token(parser_state, "RPAREN")
        assert parser_state["pos"] == 3
    
    def test_expect_token_pos_at_end_raises_syntax_error(self):
        """Edge case: pos >= len(tokens) should raise SyntaxError"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "RPAREN", "value": ")", "line": 1, "column": 10},
            ],
            "pos": 1,  # pos at end
            "filename": "test.py",
            "error": ""
        }
        
        with pytest.raises(SyntaxError) as exc_info:
            _expect_token(parser_state, "LBRACE")
        
        assert "Expected 'LBRACE' but found end of input" in str(exc_info.value)
        # Verify pos not modified on error
        assert parser_state["pos"] == 1
    
    def test_expect_token_type_mismatch_raises_syntax_error(self):
        """Error case: token type doesn't match expected"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "RPAREN", "value": ")", "line": 2, "column": 15},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        with pytest.raises(SyntaxError) as exc_info:
            _expect_token(parser_state, "LBRACE")
        
        error_msg = str(exc_info.value)
        assert "Expected 'LBRACE'" in error_msg
        assert "but found ')'" in error_msg
        assert "at line 2, column 15" in error_msg
        # Verify parser_state not modified on error
        assert parser_state["pos"] == 0
        assert parser_state["error"] == ""
    
    def test_expect_token_empty_tokens_list(self):
        """Edge case: empty tokens list should raise SyntaxError"""
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        with pytest.raises(SyntaxError) as exc_info:
            _expect_token(parser_state, "IDENT")
        
        assert "Expected 'IDENT' but found end of input" in str(exc_info.value)
        assert parser_state["pos"] == 0
    
    def test_expect_token_consume_last_token(self):
        """Boundary: consuming the last token in the list"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "SEMICOLON", "value": ";", "line": 5, "column": 20},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        _expect_token(parser_state, "SEMICOLON")
        
        assert parser_state["pos"] == 1
        assert parser_state["pos"] == len(parser_state["tokens"])
    
    def test_expect_token_error_message_includes_location(self):
        """Verify error message contains line and column info"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "KEYWORD", "value": "for", "line": 10, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        with pytest.raises(SyntaxError) as exc_info:
            _expect_token(parser_state, "IDENT")
        
        error_msg = str(exc_info.value)
        # Verify complete error message format
        assert error_msg == "Expected 'IDENT' but found 'for' at line 10, column 5"
