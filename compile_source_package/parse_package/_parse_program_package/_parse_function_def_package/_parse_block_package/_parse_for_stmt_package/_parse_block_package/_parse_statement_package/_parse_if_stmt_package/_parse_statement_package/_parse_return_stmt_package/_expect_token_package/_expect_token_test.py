import unittest

# Relative import from the same package
from ._expect_token_src import _expect_token


class TestExpectToken(unittest.TestCase):
    """Test cases for _expect_token function."""
    
    def test_expect_token_success(self):
        """Test successful token consumption when type matches."""
        parser_state = {
            "tokens": [
                {"type": "RETURN", "value": "return", "line": 1, "column": 1},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 7},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _expect_token(parser_state, "RETURN")
        
        self.assertEqual(result["pos"], 1)
        self.assertEqual(result["tokens"], parser_state["tokens"])
        # Original state should be unchanged (function returns copy)
        self.assertEqual(parser_state["pos"], 0)
    
    def test_expect_token_eof(self):
        """Test SyntaxError when pos is out of bounds."""
        parser_state = {
            "tokens": [
                {"type": "RETURN", "value": "return", "line": 1, "column": 1},
            ],
            "pos": 1,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "SEMICOLON")
        
        self.assertIn("Unexpected end of file", str(context.exception))
        self.assertIn("test.py", str(context.exception))
        self.assertIn("expected token type 'SEMICOLON'", str(context.exception))
    
    def test_expect_token_type_mismatch(self):
        """Test SyntaxError when token type doesn't match."""
        parser_state = {
            "tokens": [
                {"type": "RETURN", "value": "return", "line": 2, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "SEMICOLON")
        
        error_msg = str(context.exception)
        self.assertIn("Syntax error", error_msg)
        self.assertIn("test.py", error_msg)
        self.assertIn("line 2", error_msg)
        self.assertIn("column 5", error_msg)
        self.assertIn("expected 'SEMICOLON'", error_msg)
        self.assertIn("got 'RETURN'", error_msg)
    
    def test_expect_token_empty_tokens(self):
        """Test SyntaxError when tokens list is empty."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "RETURN")
        
        self.assertIn("Unexpected end of file", str(context.exception))
    
    def test_expect_token_missing_filename(self):
        """Test error message when filename is not provided."""
        parser_state = {
            "tokens": [],
            "pos": 0
        }
        
        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "RETURN")
        
        self.assertIn("unknown", str(context.exception))
    
    def test_expect_token_multiple_positions(self):
        """Test token consumption at different positions."""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 5},
            ],
            "pos": 2,
            "filename": "test.py"
        }
        
        result = _expect_token(parser_state, "IDENTIFIER")
        
        self.assertEqual(result["pos"], 3)
    
    def test_expect_token_preserves_other_fields(self):
        """Test that other parser_state fields are preserved."""
        parser_state = {
            "tokens": [
                {"type": "RETURN", "value": "return", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": "",
            "custom_field": "custom_value"
        }
        
        result = _expect_token(parser_state, "RETURN")
        
        self.assertEqual(result["filename"], "test.py")
        self.assertEqual(result["error"], "")
        self.assertEqual(result["custom_field"], "custom_value")
    
    def test_expect_token_missing_token_type_field(self):
        """Test error handling when token lacks type field."""
        parser_state = {
            "tokens": [
                {"value": "something", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "RETURN")
        
        error_msg = str(context.exception)
        self.assertIn("Syntax error", error_msg)
        self.assertIn("expected 'RETURN'", error_msg)
        self.assertIn("got 'None'", error_msg)
    
    def test_expect_token_sequential_consumption(self):
        """Test multiple sequential token consumptions."""
        parser_state = {
            "tokens": [
                {"type": "RETURN", "value": "return", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 8},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 9},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result1 = _expect_token(parser_state, "RETURN")
        result2 = _expect_token(result1, "IDENTIFIER")
        result3 = _expect_token(result2, "SEMICOLON")
        
        self.assertEqual(result3["pos"], 3)


if __name__ == "__main__":
    unittest.main()
