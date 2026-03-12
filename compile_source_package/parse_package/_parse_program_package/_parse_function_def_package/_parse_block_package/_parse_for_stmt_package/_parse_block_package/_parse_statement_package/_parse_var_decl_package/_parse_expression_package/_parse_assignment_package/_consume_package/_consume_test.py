# -*- coding: utf-8 -*-
"""Unit tests for _consume function."""

import unittest
from ._consume_src import _consume


class TestConsume(unittest.TestCase):
    """Test cases for _consume function."""

    def test_consume_success_type_matches(self):
        """Happy path: token type matches expected type, position advances."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
                {"type": "LITERAL", "value": "5", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.src",
        }

        result = _consume(parser_state, "IDENTIFIER")

        self.assertEqual(result, {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1})
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_success_middle_position(self):
        """Consume token from middle position."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
                {"type": "LITERAL", "value": "5", "line": 1, "column": 5},
            ],
            "pos": 1,
            "filename": "test.src",
        }

        result = _consume(parser_state, "OPERATOR")

        self.assertEqual(result, {"type": "OPERATOR", "value": "=", "line": 1, "column": 3})
        self.assertEqual(parser_state["pos"], 2)

    def test_consume_empty_tokens_raises_syntax_error(self):
        """Empty tokens list should raise SyntaxError."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.src",
        }

        with self.assertRaises(SyntaxError) as context:
            _consume(parser_state, "IDENTIFIER")

        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("test.src", str(context.exception))

    def test_consume_position_at_end_raises_syntax_error(self):
        """Position at end of tokens should raise SyntaxError."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 1,
            "filename": "test.src",
        }

        with self.assertRaises(SyntaxError) as context:
            _consume(parser_state, "IDENTIFIER")

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_consume_position_beyond_end_raises_syntax_error(self):
        """Position beyond end of tokens should raise SyntaxError."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 5,
            "filename": "test.src",
        }

        with self.assertRaises(SyntaxError) as context:
            _consume(parser_state, "IDENTIFIER")

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_consume_type_mismatch_raises_syntax_error(self):
        """Type mismatch should raise SyntaxError with details."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 10},
            ],
            "pos": 0,
            "filename": "test.src",
        }

        with self.assertRaises(SyntaxError) as context:
            _consume(parser_state, "OPERATOR")

        error_msg = str(context.exception)
        self.assertIn("Expected token type 'OPERATOR'", error_msg)
        self.assertIn("got 'IDENTIFIER'", error_msg)
        self.assertIn("line 2", error_msg)
        self.assertIn("column 10", error_msg)

    def test_consume_type_mismatch_position_unchanged(self):
        """Type mismatch should not modify position."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.src",
        }

        try:
            _consume(parser_state, "OPERATOR")
        except SyntaxError:
            pass

        self.assertEqual(parser_state["pos"], 0)

    def test_consume_unknown_filename_in_error(self):
        """Error message should handle missing filename gracefully."""
        parser_state = {
            "tokens": [],
            "pos": 0,
        }

        with self.assertRaises(SyntaxError) as context:
            _consume(parser_state, "IDENTIFIER")

        self.assertIn("unknown", str(context.exception))

    def test_consume_token_missing_line_column(self):
        """Error message should handle missing line/column in token."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x"},
            ],
            "pos": 0,
            "filename": "test.src",
        }

        with self.assertRaises(SyntaxError) as context:
            _consume(parser_state, "OPERATOR")

        error_msg = str(context.exception)
        self.assertIn("line ?", error_msg)
        self.assertIn("column ?", error_msg)

    def test_consume_multiple_sequential_consumes(self):
        """Multiple sequential consumes should work correctly."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
                {"type": "LITERAL", "value": "5", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.src",
        }

        token1 = _consume(parser_state, "IDENTIFIER")
        token2 = _consume(parser_state, "OPERATOR")
        token3 = _consume(parser_state, "LITERAL")

        self.assertEqual(token1["value"], "x")
        self.assertEqual(token2["value"], "=")
        self.assertEqual(token3["value"], "5")
        self.assertEqual(parser_state["pos"], 3)

    def test_consume_after_all_consumed_raises_error(self):
        """Consuming after all tokens consumed should raise error."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.src",
        }

        _consume(parser_state, "IDENTIFIER")

        with self.assertRaises(SyntaxError):
            _consume(parser_state, "IDENTIFIER")


if __name__ == "__main__":
    unittest.main()
