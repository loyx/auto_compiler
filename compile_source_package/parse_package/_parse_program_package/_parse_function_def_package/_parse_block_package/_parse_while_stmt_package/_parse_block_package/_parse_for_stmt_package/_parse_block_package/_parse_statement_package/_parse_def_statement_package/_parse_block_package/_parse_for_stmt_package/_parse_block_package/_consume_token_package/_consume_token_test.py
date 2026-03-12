import unittest

# Relative import from the same package
from ._consume_token_src import _consume_token


class TestConsumeToken(unittest.TestCase):
    """Test cases for _consume_token function."""
    
    def test_consume_token_success(self):
        """Test successful token consumption when type matches."""
        parser_state = {
            "tokens": [
                {"type": "FOR", "value": "for", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "i", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        token = _consume_token(parser_state, "FOR")
        
        self.assertEqual(token["type"], "FOR")
        self.assertEqual(token["value"], "for")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_consume_token_success_second_token(self):
        """Test successful consumption of second token after advancing pos."""
        parser_state = {
            "tokens": [
                {"type": "FOR", "value": "for", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "i", "line": 1, "column": 5},
                {"type": "COLON", "value": ":", "line": 1, "column": 6},
            ],
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        
        token = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertEqual(token["type"], "IDENTIFIER")
        self.assertEqual(token["value"], "i")
        self.assertEqual(parser_state["pos"], 2)
    
    def test_consume_token_out_of_bounds(self):
        """Test SyntaxError when position is out of bounds."""
        parser_state = {
            "tokens": [
                {"type": "FOR", "value": "for", "line": 1, "column": 1},
            ],
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "FOR")
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("Expected token type 'FOR'", str(context.exception))
        self.assertIn("no more tokens available", str(context.exception))
    
    def test_consume_token_empty_tokens(self):
        """Test SyntaxError when tokens list is empty."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "FOR")
        
        self.assertIn("Unexpected end of input", str(context.exception))
    
    def test_consume_token_type_mismatch(self):
        """Test SyntaxError when token type doesn't match expected type."""
        parser_state = {
            "tokens": [
                {"type": "FOR", "value": "for", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "WHILE")
        
        error_msg = str(context.exception)
        self.assertIn("Expected token type 'WHILE'", error_msg)
        self.assertIn("got 'FOR'", error_msg)
        self.assertIn("line 1", error_msg)
        self.assertIn("column 1", error_msg)
    
    def test_consume_token_type_mismatch_different_token(self):
        """Test SyntaxError with different mismatched token types."""
        parser_state = {
            "tokens": [
                {"type": "SEMICOLON", "value": ";", "line": 2, "column": 10},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "COLON")
        
        error_msg = str(context.exception)
        self.assertIn("Expected token type 'COLON'", error_msg)
        self.assertIn("got 'SEMICOLON'", error_msg)
        self.assertIn("line 2", error_msg)
        self.assertIn("column 10", error_msg)
    
    def test_consume_token_at_last_position(self):
        """Test successful consumption at the last token position."""
        parser_state = {
            "tokens": [
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 10},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        token = _consume_token(parser_state, "SEMICOLON")
        
        self.assertEqual(token["type"], "SEMICOLON")
        self.assertEqual(parser_state["pos"], 1)
    
    def test_consume_token_missing_line_column(self):
        """Test error message when token lacks line/column info."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x"},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "FOR")
        
        error_msg = str(context.exception)
        self.assertIn("Expected token type 'FOR'", error_msg)
        self.assertIn("got 'IDENTIFIER'", error_msg)
        # Should show '?' for missing line/column
        self.assertIn("?", error_msg)
    
    def test_consume_token_multiple_sequential(self):
        """Test multiple sequential token consumptions."""
        parser_state = {
            "tokens": [
                {"type": "FOR", "value": "for", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "i", "line": 1, "column": 5},
                {"type": "COLON", "value": ":", "line": 1, "column": 6},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        token1 = _consume_token(parser_state, "FOR")
        self.assertEqual(token1["type"], "FOR")
        self.assertEqual(parser_state["pos"], 1)
        
        token2 = _consume_token(parser_state, "IDENTIFIER")
        self.assertEqual(token2["type"], "IDENTIFIER")
        self.assertEqual(parser_state["pos"], 2)
        
        token3 = _consume_token(parser_state, "COLON")
        self.assertEqual(token3["type"], "COLON")
        self.assertEqual(parser_state["pos"], 3)
    
    def test_consume_token_pos_not_advanced_on_error(self):
        """Test that pos is not advanced when error occurs."""
        parser_state = {
            "tokens": [
                {"type": "FOR", "value": "for", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        try:
            _consume_token(parser_state, "WHILE")
        except SyntaxError:
            pass
        
        self.assertEqual(parser_state["pos"], 0)


if __name__ == "__main__":
    unittest.main()
