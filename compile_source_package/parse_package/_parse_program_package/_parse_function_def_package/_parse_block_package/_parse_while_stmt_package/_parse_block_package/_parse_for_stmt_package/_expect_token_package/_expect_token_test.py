import unittest

# Relative import from the same package
from ._expect_token_src import _expect_token


class TestExpectToken(unittest.TestCase):
    """Test cases for _expect_token function."""
    
    def test_expect_token_type_only_success(self):
        """Test successful token consumption with type check only."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "for", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _expect_token(parser_state, "KEYWORD")
        
        self.assertEqual(result["type"], "KEYWORD")
        self.assertEqual(result["value"], "for")
        self.assertEqual(parser_state["pos"], 1)
    
    def test_expect_token_type_and_value_success(self):
        """Test successful token consumption with type and value check."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _expect_token(parser_state, "IDENTIFIER", "x")
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(parser_state["pos"], 1)
    
    def test_expect_token_pos_out_of_bounds(self):
        """Test SyntaxError when pos is beyond tokens list."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "for", "line": 1, "column": 1}
            ],
            "pos": 1,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "KEYWORD")
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("test.py:1", str(context.exception))
    
    def test_expect_token_pos_at_end_with_value(self):
        """Test SyntaxError when pos is out of bounds with token_value specified."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "empty.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "IDENTIFIER", "x")
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("IDENTIFIER token 'x'", str(context.exception))
    
    def test_expect_token_type_mismatch(self):
        """Test SyntaxError when token type doesn't match."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "KEYWORD")
        
        self.assertIn("Expected KEYWORD token", str(context.exception))
        self.assertIn("got IDENTIFIER", str(context.exception))
        self.assertIn("test.py:2:3", str(context.exception))
    
    def test_expect_token_type_mismatch_with_value(self):
        """Test SyntaxError when token type doesn't match with expected value."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "KEYWORD", "for")
        
        self.assertIn("Expected KEYWORD token 'for'", str(context.exception))
    
    def test_expect_token_value_mismatch(self):
        """Test SyntaxError when token value doesn't match."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "y", "line": 3, "column": 7}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "IDENTIFIER", "x")
        
        self.assertIn("Expected IDENTIFIER token 'x'", str(context.exception))
        self.assertIn("got IDENTIFIER 'y'", str(context.exception))
        self.assertIn("test.py:3:7", str(context.exception))
    
    def test_expect_token_empty_tokens_list(self):
        """Test SyntaxError with empty tokens list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "empty.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "KEYWORD")
        
        self.assertIn("Unexpected end of input", str(context.exception))
    
    def test_expect_token_pos_at_last_element(self):
        """Test consuming the last token in the list."""
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 10},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 12}
            ],
            "pos": 1,
            "filename": "test.py"
        }
        
        result = _expect_token(parser_state, "NUMBER")
        
        self.assertEqual(result["value"], "42")
        self.assertEqual(parser_state["pos"], 2)
    
    def test_expect_token_multiple_consumptions(self):
        """Test consuming multiple tokens in sequence."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "for", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "i", "line": 1, "column": 5},
                {"type": "KEYWORD", "value": "in", "line": 1, "column": 7}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        token1 = _expect_token(parser_state, "KEYWORD", "for")
        self.assertEqual(parser_state["pos"], 1)
        
        token2 = _expect_token(parser_state, "IDENTIFIER", "i")
        self.assertEqual(parser_state["pos"], 2)
        
        token3 = _expect_token(parser_state, "KEYWORD", "in")
        self.assertEqual(parser_state["pos"], 3)
        
        self.assertEqual(token1["value"], "for")
        self.assertEqual(token2["value"], "i")
        self.assertEqual(token3["value"], "in")
    
    def test_expect_token_pos_beyond_length(self):
        """Test when pos is well beyond the tokens list length."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "for", "line": 1, "column": 1}
            ],
            "pos": 5,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "KEYWORD")
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("test.py:5", str(context.exception))
    
    def test_expect_token_returns_correct_token(self):
        """Test that the returned token is the actual token from the list."""
        parser_state = {
            "tokens": [
                {"type": "STRING", "value": "hello", "line": 10, "column": 20}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _expect_token(parser_state, "STRING", "hello")
        
        self.assertEqual(result["type"], "STRING")
        self.assertEqual(result["value"], "hello")
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 20)


if __name__ == "__main__":
    unittest.main()
