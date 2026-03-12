import unittest

# Relative import from the same package
from ._consume_token_src import _consume_token


class TestConsumeToken(unittest.TestCase):
    """Test cases for _consume_token function."""
    
    def test_consume_token_success(self):
        """Test successful token consumption when type matches."""
        token = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5}
        parser_state = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.py"
        }
        
        consumed_token, updated_state = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertEqual(consumed_token, token)
        self.assertEqual(updated_state["pos"], 1)
        self.assertEqual(updated_state["tokens"], parser_state["tokens"])
        self.assertEqual(updated_state["filename"], parser_state["filename"])
    
    def test_consume_token_eof_error(self):
        """Test SyntaxError when position is at end of tokens."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "IDENTIFIER")
        
        self.assertIn("EOF", str(context.exception))
        self.assertIn("test.py", str(context.exception))
    
    def test_consume_token_type_mismatch(self):
        """Test SyntaxError when token type doesn't match expected type."""
        token = {"type": "NUMBER", "value": "42", "line": 2, "column": 10}
        parser_state = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "IDENTIFIER")
        
        error_msg = str(context.exception)
        self.assertIn("expected IDENTIFIER", error_msg)
        self.assertIn("got NUMBER", error_msg)
        self.assertIn("test.py", error_msg)
        self.assertIn("2", error_msg)
        self.assertIn("10", error_msg)
    
    def test_consume_token_state_not_mutated(self):
        """Test that original parser_state is not mutated."""
        token = {"type": "OPERATOR", "value": "+", "line": 1, "column": 3}
        parser_state = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.py"
        }
        
        _consume_token(parser_state, "OPERATOR")
        
        self.assertEqual(parser_state["pos"], 0)
    
    def test_consume_token_empty_tokens_list(self):
        """Test EOF error with empty tokens list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "empty.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "ANY_TYPE")
        
        self.assertIn("EOF", str(context.exception))
    
    def test_consume_token_position_at_end(self):
        """Test EOF error when position equals tokens length."""
        token = {"type": "KEYWORD", "value": "if", "line": 1, "column": 1}
        parser_state = {
            "tokens": [token],
            "pos": 1,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "KEYWORD")
        
        self.assertIn("EOF", str(context.exception))
    
    def test_consume_token_position_beyond_end(self):
        """Test EOF error when position exceeds tokens length."""
        token = {"type": "KEYWORD", "value": "if", "line": 1, "column": 1}
        parser_state = {
            "tokens": [token],
            "pos": 5,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "KEYWORD")
        
        self.assertIn("EOF", str(context.exception))
    
    def test_consume_token_multiple_tokens(self):
        """Test consumption from middle of token list."""
        tokens = [
            {"type": "KEYWORD", "value": "def", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "func", "line": 1, "column": 5},
            {"type": "OPERATOR", "value": "(", "line": 1, "column": 9}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.py"
        }
        
        consumed_token, updated_state = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertEqual(consumed_token, tokens[1])
        self.assertEqual(updated_state["pos"], 2)
    
    def test_consume_token_without_line_column(self):
        """Test error message when token lacks line/column info."""
        token = {"type": "NUMBER", "value": "123"}
        parser_state = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "IDENTIFIER")
        
        error_msg = str(context.exception)
        self.assertIn("expected IDENTIFIER", error_msg)
        self.assertIn("got NUMBER", error_msg)
        self.assertIn("test.py", error_msg)
    
    def test_consume_token_various_types(self):
        """Test consumption of different token types."""
        for token_type in ["OPERATOR", "NUMBER", "STRING", "KEYWORD", "IDENTIFIER"]:
            with self.subTest(token_type=token_type):
                token = {"type": token_type, "value": "test", "line": 1, "column": 1}
                parser_state = {
                    "tokens": [token],
                    "pos": 0,
                    "filename": "test.py"
                }
                
                consumed_token, updated_state = _consume_token(parser_state, token_type)
                
                self.assertEqual(consumed_token["type"], token_type)
                self.assertEqual(updated_state["pos"], 1)


if __name__ == "__main__":
    unittest.main()
