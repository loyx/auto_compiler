# === imports ===
import unittest

# === relative import of target function ===
from ._consume_token_src import _consume_token


# === test cases ===
class TestConsumeToken(unittest.TestCase):
    """Test cases for _consume_token function."""

    def test_consume_token_success(self):
        """Happy path: token type matches, pos increments."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 7},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _consume_token(parser_state, "KEYWORD")
        
        self.assertEqual(result["pos"], 1)
        self.assertEqual(result["tokens"], parser_state["tokens"])
        # Original state should not be modified
        self.assertEqual(parser_state["pos"], 0)

    def test_consume_token_second_token(self):
        """Consume second token in sequence."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 7},
            ],
            "pos": 1,
            "filename": "test.py"
        }
        
        result = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertEqual(result["pos"], 2)

    def test_consume_token_type_mismatch(self):
        """Type mismatch raises SyntaxError with proper message."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 5, "column": 10},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "KEYWORD")
        
        error_msg = str(context.exception)
        self.assertIn("Syntax error", error_msg)
        self.assertIn("test.py", error_msg)
        self.assertIn("line 5", error_msg)
        self.assertIn("column 10", error_msg)
        self.assertIn("expected token type 'KEYWORD'", error_msg)
        self.assertIn("got 'IDENTIFIER'", error_msg)

    def test_consume_token_end_of_tokens(self):
        """End of tokens raises SyntaxError."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
            ],
            "pos": 1,  # Already past the last token
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "KEYWORD")
        
        error_msg = str(context.exception)
        self.assertIn("Unexpected end of file", error_msg)
        self.assertIn("test.py", error_msg)
        self.assertIn("expected token type 'KEYWORD'", error_msg)

    def test_consume_token_empty_tokens_list(self):
        """Empty tokens list raises SyntaxError."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "empty.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "KEYWORD")
        
        error_msg = str(context.exception)
        self.assertIn("Unexpected end of file", error_msg)
        self.assertIn("empty.py", error_msg)

    def test_consume_token_default_filename(self):
        """Missing filename defaults to <unknown>."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
            ],
            "pos": 0
            # No filename key
        }
        
        # Should work without filename
        result = _consume_token(parser_state, "KEYWORD")
        self.assertEqual(result["pos"], 1)

    def test_consume_token_missing_line_column(self):
        """Missing line/column in token uses '?' placeholder."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x"},  # No line/column
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "KEYWORD")
        
        error_msg = str(context.exception)
        self.assertIn("line ?", error_msg)
        self.assertIn("column ?", error_msg)

    def test_consume_token_state_not_mutated(self):
        """Original parser_state is not mutated."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        original_pos = parser_state["pos"]
        _consume_token(parser_state, "KEYWORD")
        
        # Original state should remain unchanged
        self.assertEqual(parser_state["pos"], original_pos)

    def test_consume_token_preserves_other_fields(self):
        """Other fields in parser_state are preserved."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None,
            "custom_field": "custom_value"
        }
        
        result = _consume_token(parser_state, "KEYWORD")
        
        self.assertEqual(result["filename"], "test.py")
        self.assertEqual(result["error"], None)
        self.assertEqual(result["custom_field"], "custom_value")


# === test runner ===
if __name__ == "__main__":
    unittest.main()
