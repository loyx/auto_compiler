import unittest
from ._expect_token_src import _expect_token


class TestExpectToken(unittest.TestCase):
    """Test cases for _expect_token function."""
    
    def test_happy_path_token_matches(self):
        """Test when current token type matches expected type."""
        parser_state = {
            "tokens": [
                {"type": "WHILE", "value": "while", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _expect_token(parser_state, "WHILE")
        
        self.assertEqual(result["type"], "WHILE")
        self.assertEqual(result["value"], "while")
        self.assertEqual(parser_state["pos"], 1)
    
    def test_pos_advances_after_success(self):
        """Test that parser position advances after successful match."""
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 5},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _expect_token(parser_state, "LPAREN")
        
        self.assertEqual(result["type"], "LPAREN")
        self.assertEqual(parser_state["pos"], 1)
    
    def test_out_of_bounds_raises_syntax_error(self):
        """Test SyntaxError when position exceeds token list length."""
        parser_state = {
            "tokens": [
                {"type": "WHILE", "value": "while", "line": 1, "column": 1}
            ],
            "pos": 1,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "WHILE")
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("test.py", str(context.exception))
    
    def test_type_mismatch_raises_syntax_error(self):
        """Test SyntaxError when token type doesn't match expected."""
        parser_state = {
            "tokens": [
                {"type": "WHILE", "value": "while", "line": 3, "column": 10}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "FOR")
        
        self.assertIn("Syntax error", str(context.exception))
        self.assertIn("test.py", str(context.exception))
        self.assertIn("line 3", str(context.exception))
        self.assertIn("column 10", str(context.exception))
        self.assertIn("expected FOR", str(context.exception))
        self.assertIn("found WHILE", str(context.exception))
    
    def test_empty_tokens_list(self):
        """Test behavior with empty tokens list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "empty.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "WHILE")
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("empty.py", str(context.exception))
    
    def test_missing_filename_uses_unknown(self):
        """Test that missing filename defaults to '<unknown>'."""
        parser_state = {
            "tokens": [
                {"type": "WHILE", "value": "while", "line": 1, "column": 1}
            ],
            "pos": 0
        }
        
        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "FOR")
        
        self.assertIn("<unknown>", str(context.exception))
    
    def test_multiple_consecutive_calls(self):
        """Test multiple consecutive calls advance position correctly."""
        parser_state = {
            "tokens": [
                {"type": "WHILE", "value": "while", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 7},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 8}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        token1 = _expect_token(parser_state, "WHILE")
        self.assertEqual(parser_state["pos"], 1)
        
        token2 = _expect_token(parser_state, "LPAREN")
        self.assertEqual(parser_state["pos"], 2)
        
        token3 = _expect_token(parser_state, "RPAREN")
        self.assertEqual(parser_state["pos"], 3)
        
        self.assertEqual(token1["type"], "WHILE")
        self.assertEqual(token2["type"], "LPAREN")
        self.assertEqual(token3["type"], "RPAREN")
    
    def test_token_value_in_error_message(self):
        """Test that token value appears in error message on mismatch."""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "WHILE")
        
        self.assertIn("'if'", str(context.exception))


if __name__ == "__main__":
    unittest.main()
