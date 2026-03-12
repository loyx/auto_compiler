import unittest
from ._consume_token_src import _consume_token


class TestConsumeToken(unittest.TestCase):
    """Test cases for _consume_token function."""
    
    def test_consume_token_without_type_check(self):
        """Happy path: consume token without expected_type validation."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _consume_token(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_consume_token_with_matching_type(self):
        """Happy path: consume token with matching expected_type."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _consume_token(parser_state, expected_type="KEYWORD")
        
        self.assertEqual(result["type"], "KEYWORD")
        self.assertEqual(result["value"], "while")
        self.assertEqual(parser_state["pos"], 1)
    
    def test_consume_token_at_end_raises_error(self):
        """Boundary: pos at end of tokens should raise SyntaxError."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 1,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state)
        
        self.assertEqual(str(context.exception), "Unexpected end of input")
    
    def test_consume_token_beyond_end_raises_error(self):
        """Boundary: pos beyond tokens should raise SyntaxError."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 5,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state)
        
        self.assertEqual(str(context.exception), "Unexpected end of input")
    
    def test_consume_token_type_mismatch_raises_error(self):
        """Type mismatch: expected_type doesn't match should raise SyntaxError."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, expected_type="KEYWORD")
        
        self.assertIn("Expected token type 'KEYWORD', got 'IDENTIFIER'", str(context.exception))
    
    def test_consume_token_type_mismatch_pos_unchanged(self):
        """Type mismatch: pos should not advance on error."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError):
            _consume_token(parser_state, expected_type="KEYWORD")
        
        self.assertEqual(parser_state["pos"], 0)
    
    def test_consume_multiple_tokens_sequentially(self):
        """Multiple consumes: should advance pos correctly through tokens."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 6},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 7}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        token1 = _consume_token(parser_state)
        self.assertEqual(token1["type"], "KEYWORD")
        self.assertEqual(parser_state["pos"], 1)
        
        token2 = _consume_token(parser_state)
        self.assertEqual(token2["type"], "LPAREN")
        self.assertEqual(parser_state["pos"], 2)
        
        token3 = _consume_token(parser_state)
        self.assertEqual(token3["type"], "IDENTIFIER")
        self.assertEqual(parser_state["pos"], 3)
    
    def test_consume_token_modifies_original_state(self):
        """Side effect: parser_state dict should be modified in place."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        _consume_token(parser_state)
        
        self.assertEqual(parser_state["pos"], 1)
    
    def test_consume_token_empty_tokens_list(self):
        """Boundary: empty tokens list should raise SyntaxError."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state)
        
        self.assertEqual(str(context.exception), "Unexpected end of input")


if __name__ == "__main__":
    unittest.main()
