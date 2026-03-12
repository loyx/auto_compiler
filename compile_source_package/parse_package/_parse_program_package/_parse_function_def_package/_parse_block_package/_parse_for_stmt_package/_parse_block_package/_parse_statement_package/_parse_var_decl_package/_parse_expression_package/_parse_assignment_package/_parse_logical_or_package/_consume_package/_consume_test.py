import unittest

from ._consume_src import _consume


class TestConsume(unittest.TestCase):
    """Test cases for _consume function."""
    
    def test_consume_success_token_type_matches(self):
        """Happy path: token type matches expected type."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _consume(parser_state, "IDENTIFIER")
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_consume_pos_at_end_raises_error(self):
        """Boundary: pos equals tokens length."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 1,
            "filename": "test.py"
        }
        
        with self.assertRaises(ValueError) as context:
            _consume(parser_state, "IDENTIFIER")
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("test.py", str(context.exception))
    
    def test_consume_pos_beyond_end_raises_error(self):
        """Boundary: pos exceeds tokens length."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 5,
            "filename": "test.py"
        }
        
        with self.assertRaises(ValueError) as context:
            _consume(parser_state, "IDENTIFIER")
        
        self.assertIn("Unexpected end of input", str(context.exception))
    
    def test_consume_type_mismatch_raises_error(self):
        """Error case: token type doesn't match expected."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 2, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(ValueError) as context:
            _consume(parser_state, "IDENTIFIER")
        
        self.assertIn("Unexpected token", str(context.exception))
        self.assertIn("NUMBER", str(context.exception))
        self.assertIn("IDENTIFIER", str(context.exception))
        self.assertIn("42", str(context.exception))
    
    def test_consume_empty_tokens_raises_error(self):
        """Edge case: empty tokens list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(ValueError) as context:
            _consume(parser_state, "IDENTIFIER")
        
        self.assertIn("Unexpected end of input", str(context.exception))
    
    def test_consume_modifies_pos_in_place(self):
        """Verify side effect: parser_state['pos'] is modified in place."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        original_state = parser_state
        result = _consume(parser_state, "IDENTIFIER")
        
        self.assertIs(parser_state, original_state)
        self.assertEqual(parser_state["pos"], 1)
        self.assertEqual(result["type"], "IDENTIFIER")
    
    def test_consume_multiple_tokens_sequential(self):
        """Multiple tokens consumed sequentially."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        token1 = _consume(parser_state, "IDENTIFIER")
        self.assertEqual(token1["value"], "x")
        self.assertEqual(parser_state["pos"], 1)
        
        token2 = _consume(parser_state, "OPERATOR")
        self.assertEqual(token2["value"], "=")
        self.assertEqual(parser_state["pos"], 2)
        
        token3 = _consume(parser_state, "NUMBER")
        self.assertEqual(token3["value"], "5")
        self.assertEqual(parser_state["pos"], 3)
    
    def test_consume_filename_in_error_message(self):
        """Error message includes filename."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "my_script.py"
        }
        
        with self.assertRaises(ValueError) as context:
            _consume(parser_state, "IDENTIFIER")
        
        self.assertIn("my_script.py", str(context.exception))
    
    def test_consume_unknown_filename_default(self):
        """Error message uses 'unknown' when filename missing."""
        parser_state = {
            "tokens": [],
            "pos": 0
        }
        
        with self.assertRaises(ValueError) as context:
            _consume(parser_state, "IDENTIFIER")
        
        self.assertIn("unknown", str(context.exception))
    
    def test_consume_middle_position(self):
        """Consume token from middle position."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 1,
            "filename": "test.py"
        }
        
        result = _consume(parser_state, "OPERATOR")
        
        self.assertEqual(result["value"], "+")
        self.assertEqual(parser_state["pos"], 2)
    
    def test_consume_type_mismatch_includes_line_column(self):
        """Error message includes line and column info."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "if", "line": 10, "column": 20}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(ValueError) as context:
            _consume(parser_state, "IDENTIFIER")
        
        self.assertIn("line 10", str(context.exception))
        self.assertIn("column 20", str(context.exception))


if __name__ == "__main__":
    unittest.main()
