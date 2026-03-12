import unittest

from ._consume_token_src import _consume_token


class TestConsumeToken(unittest.TestCase):
    """Test cases for _consume_token function."""
    
    def test_consume_token_success(self):
        """Test successful token consumption when type matches."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        result = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertEqual(result["pos"], 1)
        self.assertEqual(result["tokens"], parser_state["tokens"])
        self.assertEqual(result["filename"], "test.py")
        self.assertEqual(result["error"], "")
    
    def test_consume_token_multiple_tokens(self):
        """Test token consumption with multiple tokens."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 5}
            ],
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        
        result = _consume_token(parser_state, "PLUS")
        
        self.assertEqual(result["pos"], 2)
        self.assertEqual(result["tokens"], parser_state["tokens"])
    
    def test_consume_token_pos_at_end(self):
        """Test SyntaxError when pos is at end of tokens."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "IDENTIFIER")
        
        self.assertEqual(str(context.exception), "Unexpected end of input")
    
    def test_consume_token_pos_out_of_bounds(self):
        """Test SyntaxError when pos is beyond tokens length."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 5,
            "filename": "test.py",
            "error": ""
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "IDENTIFIER")
        
        self.assertEqual(str(context.exception), "Unexpected end of input")
    
    def test_consume_token_type_mismatch(self):
        """Test SyntaxError when token type doesn't match expected."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "NUMBER")
        
        self.assertEqual(str(context.exception), "Expected NUMBER, got IDENTIFIER")
    
    def test_consume_token_empty_tokens(self):
        """Test SyntaxError with empty tokens list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "IDENTIFIER")
        
        self.assertEqual(str(context.exception), "Unexpected end of input")
    
    def test_consume_token_preserves_optional_fields(self):
        """Test that optional fields are preserved in result."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
        }
        
        result = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertEqual(result["pos"], 1)
        self.assertEqual(result["filename"], "")
        self.assertEqual(result["error"], "")
    
    def test_consume_token_preserves_error_field(self):
        """Test that existing error field is preserved."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": "previous error"
        }
        
        result = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertEqual(result["error"], "previous error")
        self.assertEqual(result["filename"], "test.py")


if __name__ == "__main__":
    unittest.main()
