# === std / third-party imports ===
import unittest
from typing import Any, Dict

# === UUT import ===
from main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._expect_token_package._expect_token_src import (
    _expect_token,
)

# === Type aliases (matching UUT) ===
Token = Dict[str, Any]
ParserState = Dict[str, Any]


class TestExpectToken(unittest.TestCase):
    """Unit tests for _expect_token function."""

    def test_happy_path_matches_and_consumes_token(self):
        """Token matches expected type and value - pos should increment."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "KEYWORD", "value": "for", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "i", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        _expect_token(parser_state, "KEYWORD", "for")

        self.assertEqual(parser_state["pos"], 1)

    def test_happy_path_second_token(self):
        """Token matches at non-zero position - pos should increment."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "KEYWORD", "value": "for", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "i", "line": 1, "column": 5},
                {"type": "OPERATOR", "value": "in", "line": 1, "column": 7},
            ],
            "pos": 1,
            "filename": "test.py",
        }

        _expect_token(parser_state, "IDENTIFIER", "i")

        self.assertEqual(parser_state["pos"], 2)

    def test_boundary_pos_at_end_raises_syntax_error(self):
        """Position at end of tokens list raises SyntaxError."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "KEYWORD", "value": "for", "line": 1, "column": 1},
            ],
            "pos": 1,
            "filename": "test.py",
        }

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "IDENTIFIER", "i")

        self.assertIn("Expected 'i' at end of file", str(context.exception))

    def test_boundary_empty_tokens_raises_syntax_error(self):
        """Empty tokens list raises SyntaxError."""
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
        }

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "KEYWORD", "for")

        self.assertIn("Expected 'for' at end of file", str(context.exception))

    def test_mismatch_token_type_raises_syntax_error_with_location(self):
        """Token type mismatch raises SyntaxError with line/column info."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "for", "line": 5, "column": 10},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "KEYWORD", "for")

        error_msg = str(context.exception)
        self.assertIn("Expected 'for'", error_msg)
        self.assertIn("line 5", error_msg)
        self.assertIn("column 10", error_msg)
        self.assertIn("got 'for'", error_msg)

    def test_mismatch_token_value_raises_syntax_error_with_location(self):
        """Token value mismatch raises SyntaxError with line/column info."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 3, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "KEYWORD", "for")

        error_msg = str(context.exception)
        self.assertIn("Expected 'for'", error_msg)
        self.assertIn("line 3", error_msg)
        self.assertIn("column 1", error_msg)
        self.assertIn("got 'while'", error_msg)

    def test_mismatch_both_type_and_value_raises_syntax_error(self):
        """Both type and value mismatch raises SyntaxError."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "OPERATOR", "value": "+", "line": 2, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "KEYWORD", "for")

        error_msg = str(context.exception)
        self.assertIn("Expected 'for'", error_msg)
        self.assertIn("got '+'", error_msg)

    def test_missing_line_column_defaults_to_zero(self):
        """Token without line/column info defaults to 0 in error message."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x"},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "KEYWORD", "for")

        error_msg = str(context.exception)
        self.assertIn("line 0", error_msg)
        self.assertIn("column 0", error_msg)

    def test_pos_beyond_tokens_length_raises_syntax_error(self):
        """Position beyond tokens length raises SyntaxError."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "KEYWORD", "value": "for", "line": 1, "column": 1},
            ],
            "pos": 5,
            "filename": "test.py",
        }

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "IDENTIFIER", "i")

        self.assertIn("Expected 'i' at end of file", str(context.exception))

    def test_multiple_consumes_sequential_tokens(self):
        """Multiple calls consume sequential tokens correctly."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "KEYWORD", "value": "for", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "i", "line": 1, "column": 5},
                {"type": "OPERATOR", "value": "in", "line": 1, "column": 7},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        _expect_token(parser_state, "KEYWORD", "for")
        self.assertEqual(parser_state["pos"], 1)

        _expect_token(parser_state, "IDENTIFIER", "i")
        self.assertEqual(parser_state["pos"], 2)

        _expect_token(parser_state, "OPERATOR", "in")
        self.assertEqual(parser_state["pos"], 3)


if __name__ == "__main__":
    unittest.main()
