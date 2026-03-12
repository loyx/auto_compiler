#!/usr/bin/env python3
"""Unit tests for _parse_break_stmt parser function."""

import unittest

from ._parse_break_stmt_src import _parse_break_stmt


class TestParseBreakStmt(unittest.TestCase):
    """Test cases for _parse_break_stmt function."""

    def test_happy_path_valid_break_statement(self):
        """Test parsing a valid break; statement."""
        tokens = [
            {"type": "BREAK", "value": "break", "line": 5, "column": 10},
            {"type": "SEMICOLON", "value": ";", "line": 5, "column": 15},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }

        result = _parse_break_stmt(parser_state)

        self.assertEqual(result["type"], "BREAK_STMT")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)
        self.assertEqual(parser_state["pos"], 2)

    def test_break_statement_with_subsequent_tokens(self):
        """Test parsing break; when there are more tokens after."""
        tokens = [
            {"type": "BREAK", "value": "break", "line": 3, "column": 1},
            {"type": "SEMICOLON", "value": ";", "line": 3, "column": 6},
            {"type": "RETURN", "value": "return", "line": 4, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }

        result = _parse_break_stmt(parser_state)

        self.assertEqual(result["type"], "BREAK_STMT")
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 2)

    def test_break_statement_not_at_start(self):
        """Test parsing break; when position is not at start of tokens."""
        tokens = [
            {"type": "IF", "value": "if", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 3},
            {"type": "BREAK", "value": "break", "line": 2, "column": 5},
            {"type": "SEMICOLON", "value": ";", "line": 2, "column": 10},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 2,
            "filename": "test.c"
        }

        result = _parse_break_stmt(parser_state)

        self.assertEqual(result["type"], "BREAK_STMT")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 4)

    def test_empty_tokens_raises_syntax_error(self):
        """Test that empty tokens list raises SyntaxError."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c"
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_break_stmt(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_position_beyond_tokens_raises_syntax_error(self):
        """Test that position beyond tokens list raises SyntaxError."""
        tokens = [
            {"type": "BREAK", "value": "break", "line": 1, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 5,
            "filename": "test.c"
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_break_stmt(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_wrong_token_type_raises_syntax_error(self):
        """Test that non-BREAK token at current position raises SyntaxError."""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 1, "column": 1},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 7},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_break_stmt(parser_state)

        self.assertIn("Expected 'break' keyword", str(context.exception))

    def test_wrong_token_value_raises_syntax_error(self):
        """Test that BREAK token with wrong value raises SyntaxError."""
        tokens = [
            {"type": "BREAK", "value": "BREAK", "line": 1, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_break_stmt(parser_state)

        self.assertIn("Expected 'break' keyword", str(context.exception))

    def test_missing_semicolon_raises_syntax_error(self):
        """Test that missing semicolon after break raises SyntaxError."""
        tokens = [
            {"type": "BREAK", "value": "break", "line": 1, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_break_stmt(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertEqual(parser_state["pos"], 1)

    def test_wrong_token_after_break_raises_syntax_error(self):
        """Test that non-semicolon token after break raises SyntaxError."""
        tokens = [
            {"type": "BREAK", "value": "break", "line": 1, "column": 1},
            {"type": "RETURN", "value": "return", "line": 1, "column": 7},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_break_stmt(parser_state)

        self.assertIn("Expected ';'", str(context.exception))
        self.assertEqual(parser_state["pos"], 1)

    def test_wrong_semicolon_value_raises_syntax_error(self):
        """Test that SEMICOLON token with wrong value raises SyntaxError."""
        tokens = [
            {"type": "BREAK", "value": "break", "line": 1, "column": 1},
            {"type": "SEMICOLON", "value": ":", "line": 1, "column": 6},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_break_stmt(parser_state)

        self.assertIn("Expected ';'", str(context.exception))

    def test_break_statement_preserves_line_column_info(self):
        """Test that line and column information is preserved from token."""
        tokens = [
            {"type": "BREAK", "value": "break", "line": 100, "column": 250},
            {"type": "SEMICOLON", "value": ";", "line": 100, "column": 255},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }

        result = _parse_break_stmt(parser_state)

        self.assertEqual(result["line"], 100)
        self.assertEqual(result["column"], 250)

    def test_break_statement_with_zero_line_column(self):
        """Test handling of tokens without line/column info."""
        tokens = [
            {"type": "BREAK", "value": "break"},
            {"type": "SEMICOLON", "value": ";"},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }

        result = _parse_break_stmt(parser_state)

        self.assertEqual(result["type"], "BREAK_STMT")
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)

    def test_token_without_type_field_raises_syntax_error(self):
        """Test that token without type field raises SyntaxError."""
        tokens = [
            {"value": "break", "line": 1, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_break_stmt(parser_state)

        self.assertIn("Expected 'break' keyword", str(context.exception))

    def test_token_without_value_field_raises_syntax_error(self):
        """Test that token without value field raises SyntaxError."""
        tokens = [
            {"type": "BREAK", "line": 1, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_break_stmt(parser_state)

        self.assertIn("Expected 'break' keyword", str(context.exception))


if __name__ == "__main__":
    unittest.main()
