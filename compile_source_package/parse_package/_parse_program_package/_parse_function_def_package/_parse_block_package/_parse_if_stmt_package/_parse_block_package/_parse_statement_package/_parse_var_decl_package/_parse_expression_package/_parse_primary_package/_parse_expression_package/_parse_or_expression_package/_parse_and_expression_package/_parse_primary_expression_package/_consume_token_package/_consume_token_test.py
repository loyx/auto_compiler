import unittest
from typing import Any, Dict

from ._consume_token_src import _consume_token


class TestConsumeToken(unittest.TestCase):
    """Test cases for _consume_token function."""

    def _create_parser_state(
        self,
        tokens: list = None,
        pos: int = 0,
        filename: str = "test.txt",
        error: str = ""
    ) -> Dict[str, Any]:
        """Helper to create parser state dict."""
        return {
            "tokens": tokens if tokens is not None else [],
            "pos": pos,
            "filename": filename,
            "error": error
        }

    def test_consume_token_success(self):
        """Test successful token consumption when types match."""
        tokens = [{"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)

        _consume_token(parser_state, "IDENTIFIER")

        self.assertEqual(parser_state["pos"], 1)
        self.assertEqual(parser_state["error"], "")

    def test_consume_token_success_at_middle_position(self):
        """Test successful consumption when pos is not at start."""
        tokens = [
            {"type": "KEYWORD", "value": "if", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4}
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=1)

        _consume_token(parser_state, "LPAREN")

        self.assertEqual(parser_state["pos"], 2)
        self.assertEqual(parser_state["error"], "")

    def test_consume_token_end_of_input_empty_tokens(self):
        """Test error when consuming from empty tokens list."""
        parser_state = self._create_parser_state(tokens=[], pos=0)

        _consume_token(parser_state, "IDENTIFIER")

        self.assertEqual(parser_state["pos"], 0)
        self.assertIn("Expected IDENTIFIER at end of input", parser_state["error"])

    def test_consume_token_end_of_input_pos_beyond_tokens(self):
        """Test error when pos is beyond token list length."""
        tokens = [{"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}]
        parser_state = self._create_parser_state(tokens=tokens, pos=1)

        _consume_token(parser_state, "IDENTIFIER")

        self.assertEqual(parser_state["pos"], 1)
        self.assertIn("Expected IDENTIFIER at end of input", parser_state["error"])

    def test_consume_token_type_mismatch(self):
        """Test error when token type doesn't match expected type."""
        tokens = [{"type": "NUMBER", "value": "42", "line": 2, "column": 5}]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)

        _consume_token(parser_state, "IDENTIFIER")

        self.assertEqual(parser_state["pos"], 0)
        self.assertIn("Expected IDENTIFIER at line 2, column 5", parser_state["error"])

    def test_consume_token_type_mismatch_preserves_error(self):
        """Test that mismatch overwrites any existing error."""
        tokens = [{"type": "NUMBER", "value": "42", "line": 2, "column": 5}]
        parser_state = self._create_parser_state(tokens=tokens, pos=0, error="previous error")

        _consume_token(parser_state, "IDENTIFIER")

        self.assertEqual(parser_state["pos"], 0)
        self.assertNotEqual(parser_state["error"], "previous error")
        self.assertIn("Expected IDENTIFIER", parser_state["error"])

    def test_consume_token_missing_line_column_uses_fallback(self):
        """Test error message uses '?' when line/column missing from token."""
        tokens = [{"type": "NUMBER", "value": "42"}]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)

        _consume_token(parser_state, "IDENTIFIER")

        self.assertEqual(parser_state["pos"], 0)
        self.assertIn("Expected IDENTIFIER at line ?, column ?", parser_state["error"])

    def test_consume_token_missing_line_only(self):
        """Test error message when only line is missing."""
        tokens = [{"type": "NUMBER", "value": "42", "column": 5}]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)

        _consume_token(parser_state, "IDENTIFIER")

        self.assertEqual(parser_state["pos"], 0)
        self.assertIn("line ?", parser_state["error"])
        self.assertIn("column 5", parser_state["error"])

    def test_consume_token_missing_column_only(self):
        """Test error message when only column is missing."""
        tokens = [{"type": "NUMBER", "value": "42", "line": 3}]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)

        _consume_token(parser_state, "IDENTIFIER")

        self.assertEqual(parser_state["pos"], 0)
        self.assertIn("line 3", parser_state["error"])
        self.assertIn("column ?", parser_state["error"])

    def test_consume_token_multiple_sequential_consumes(self):
        """Test multiple sequential successful consumptions."""
        tokens = [
            {"type": "KEYWORD", "value": "if", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4}
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)

        _consume_token(parser_state, "KEYWORD")
        self.assertEqual(parser_state["pos"], 1)
        self.assertEqual(parser_state["error"], "")

        _consume_token(parser_state, "LPAREN")
        self.assertEqual(parser_state["pos"], 2)
        self.assertEqual(parser_state["error"], "")

        _consume_token(parser_state, "IDENTIFIER")
        self.assertEqual(parser_state["pos"], 3)
        self.assertEqual(parser_state["error"], "")

    def test_consume_token_does_not_modify_tokens(self):
        """Test that function doesn't modify the tokens list itself."""
        tokens = [{"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        original_tokens = parser_state["tokens"].copy()

        _consume_token(parser_state, "IDENTIFIER")

        self.assertEqual(parser_state["tokens"], original_tokens)

    def test_consume_token_does_not_modify_filename(self):
        """Test that function doesn't modify the filename field."""
        tokens = [{"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}]
        parser_state = self._create_parser_state(tokens=tokens, pos=0, filename="source.c")

        _consume_token(parser_state, "IDENTIFIER")

        self.assertEqual(parser_state["filename"], "source.c")


if __name__ == "__main__":
    unittest.main()
