"""Unit tests for _parse_continue_stmt function."""

import unittest

from ._parse_continue_stmt_src import _parse_continue_stmt


class TestParseContinueStmt(unittest.TestCase):
    """Test cases for _parse_continue_stmt function."""

    def test_happy_path_continue_with_semicolon(self):
        """Test parsing CONTINUE statement followed by SEMICOLON."""
        parser_state = {
            "tokens": [
                {"type": "CONTINUE", "value": "continue", "line": 5, "column": 10},
                {"type": "SEMICOLON", "value": ";", "line": 5, "column": 18},
                {"type": "EOF", "value": "", "line": 6, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        result = _parse_continue_stmt(parser_state)

        self.assertEqual(result["type"], "CONTINUE")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)
        self.assertEqual(parser_state["pos"], 2)

    def test_continue_at_end_of_tokens_raises_error(self):
        """Test that CONTINUE without SEMICOLON at end of tokens raises SyntaxError."""
        parser_state = {
            "tokens": [
                {"type": "CONTINUE", "value": "continue", "line": 5, "column": 10},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_continue_stmt(parser_state)

        self.assertIn("missing ';'", str(context.exception))
        self.assertIn("test.py:5:10", str(context.exception))

    def test_continue_with_non_semicolon_raises_error(self):
        """Test that CONTINUE followed by non-SEMICOLON token raises SyntaxError."""
        parser_state = {
            "tokens": [
                {"type": "CONTINUE", "value": "continue", "line": 3, "column": 5},
                {"type": "IDENTIFIER", "value": "x", "line": 3, "column": 15},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_continue_stmt(parser_state)

        self.assertIn("expected ';'", str(context.exception))
        self.assertIn("test.py:3:5", str(context.exception))

    def test_continue_preserves_line_column_info(self):
        """Test that AST node preserves correct line and column from CONTINUE token."""
        parser_state = {
            "tokens": [
                {"type": "CONTINUE", "value": "continue", "line": 100, "column": 25},
                {"type": "SEMICOLON", "value": ";", "line": 100, "column": 33},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        result = _parse_continue_stmt(parser_state)

        self.assertEqual(result["line"], 100)
        self.assertEqual(result["column"], 25)
        self.assertNotIn("children", result)
        self.assertNotIn("value", result)

    def test_continue_advances_pos_correctly(self):
        """Test that parser_state pos is advanced by exactly 2 tokens."""
        parser_state = {
            "tokens": [
                {"type": "CONTINUE", "value": "continue", "line": 1, "column": 1},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 9},
                {"type": "BREAK", "value": "break", "line": 2, "column": 1},
                {"type": "SEMICOLON", "value": ";", "line": 2, "column": 6},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        result = _parse_continue_stmt(parser_state)

        self.assertEqual(parser_state["pos"], 2)
        self.assertEqual(parser_state["tokens"][parser_state["pos"]]["type"], "BREAK")

    def test_continue_with_multiple_semicolons(self):
        """Test parsing CONTINUE when multiple SEMICOLONs follow."""
        parser_state = {
            "tokens": [
                {"type": "CONTINUE", "value": "continue", "line": 7, "column": 3},
                {"type": "SEMICOLON", "value": ";", "line": 7, "column": 11},
                {"type": "SEMICOLON", "value": ";", "line": 7, "column": 12},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        result = _parse_continue_stmt(parser_state)

        self.assertEqual(result["type"], "CONTINUE")
        self.assertEqual(parser_state["pos"], 2)

    def test_continue_at_first_position(self):
        """Test parsing CONTINUE when it's the first token in the file."""
        parser_state = {
            "tokens": [
                {"type": "CONTINUE", "value": "continue", "line": 1, "column": 1},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 9},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        result = _parse_continue_stmt(parser_state)

        self.assertEqual(result["type"], "CONTINUE")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 2)


if __name__ == "__main__":
    unittest.main()
