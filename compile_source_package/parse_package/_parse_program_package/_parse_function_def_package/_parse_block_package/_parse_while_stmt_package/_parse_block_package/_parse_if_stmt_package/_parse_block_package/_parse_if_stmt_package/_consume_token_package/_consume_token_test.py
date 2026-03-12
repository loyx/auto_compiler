import unittest

# Relative import from the same package
from ._consume_token_src import _consume_token


class TestConsumeToken(unittest.TestCase):
    """Test cases for _consume_token function."""
    
    def test_consume_token_no_type_check(self):
        """Test consuming token without type checking (expected_type=None)."""
        token1 = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        token2 = {"type": "OPERATOR", "value": "+", "line": 1, "column": 2}
        parser_state = {
            "tokens": [token1, token2],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _consume_token(parser_state)
        
        self.assertEqual(result, token1)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_consume_token_with_matching_type(self):
        """Test consuming token with matching expected_type."""
        token = {"type": "KEYWORD", "value": "if", "line": 1, "column": 1}
        parser_state = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _consume_token(parser_state, expected_type="KEYWORD")
        
        self.assertEqual(result, token)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_consume_token_type_mismatch(self):
        """Test that SyntaxError is raised when token type doesn't match expected_type."""
        token = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        parser_state = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, expected_type="KEYWORD")
        
        self.assertIn("Expected 'KEYWORD', got IDENTIFIER", str(context.exception))
        # pos should not be modified on error
        self.assertEqual(parser_state["pos"], 0)
    
    def test_consume_token_at_end(self):
        """Test that SyntaxError is raised when pos is at end of tokens."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state)
        
        self.assertEqual(str(context.exception), "Unexpected end of input")
    
    def test_consume_token_past_end(self):
        """Test that SyntaxError is raised when pos is past end of tokens."""
        token = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        parser_state = {
            "tokens": [token],
            "pos": 1,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state)
        
        self.assertEqual(str(context.exception), "Unexpected end of input")
    
    def test_consume_last_token(self):
        """Test consuming the last token in the list."""
        token = {"type": "SEMICOLON", "value": ";", "line": 1, "column": 5}
        parser_state = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _consume_token(parser_state)
        
        self.assertEqual(result, token)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_consume_multiple_tokens_sequentially(self):
        """Test consuming multiple tokens in sequence."""
        token1 = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        token2 = {"type": "OPERATOR", "value": "=", "line": 1, "column": 2}
        token3 = {"type": "NUMBER", "value": "5", "line": 1, "column": 3}
        parser_state = {
            "tokens": [token1, token2, token3],
            "pos": 0,
            "filename": "test.py"
        }
        
        result1 = _consume_token(parser_state)
        self.assertEqual(result1, token1)
        self.assertEqual(parser_state["pos"], 1)
        
        result2 = _consume_token(parser_state)
        self.assertEqual(result2, token2)
        self.assertEqual(parser_state["pos"], 2)
        
        result3 = _consume_token(parser_state)
        self.assertEqual(result3, token3)
        self.assertEqual(parser_state["pos"], 3)
    
    def test_consume_token_empty_tokens_list(self):
        """Test consuming token from empty tokens list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state)
        
        self.assertEqual(str(context.exception), "Unexpected end of input")
    
    def test_consume_token_preserves_other_state_fields(self):
        """Test that other parser_state fields are not modified."""
        token = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        parser_state = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.py",
            "error": None,
            "custom_field": "value"
        }
        
        _consume_token(parser_state)
        
        self.assertEqual(parser_state["filename"], "test.py")
        self.assertEqual(parser_state["error"], None)
        self.assertEqual(parser_state["custom_field"], "value")


if __name__ == "__main__":
    unittest.main()
