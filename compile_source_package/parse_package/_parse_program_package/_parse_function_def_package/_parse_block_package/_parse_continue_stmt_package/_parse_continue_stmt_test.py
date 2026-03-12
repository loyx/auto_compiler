# -*- coding: utf-8 -*-
"""Unit tests for _parse_continue_stmt parser function."""

import unittest
from typing import Any, Dict

from ._parse_continue_stmt_src import _parse_continue_stmt


class TestParseContinueStmt(unittest.TestCase):
    """Test cases for _parse_continue_stmt function."""

    def _create_parser_state(
        self,
        tokens: list,
        pos: int = 0,
        filename: str = "test.c"
    ) -> Dict[str, Any]:
        """Helper to create parser state dict."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_token(
        self,
        token_type: str,
        value: str = "",
        line: int = 1,
        column: int = 1
    ) -> Dict[str, Any]:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def test_parse_continue_stmt_simple(self):
        """Test parsing a simple continue statement without semicolon."""
        tokens = [
            self._create_token("CONTINUE", "continue", line=5, column=10)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _parse_continue_stmt(parser_state)

        self.assertEqual(result["type"], "CONTINUE_STMT")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_continue_stmt_with_semicolon(self):
        """Test parsing a continue statement with semicolon."""
        tokens = [
            self._create_token("CONTINUE", "continue", line=3, column=5),
            self._create_token("SEMICOLON", ";", line=3, column=13)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _parse_continue_stmt(parser_state)

        self.assertEqual(result["type"], "CONTINUE_STMT")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 2)

    def test_parse_continue_stmt_empty_tokens(self):
        """Test parsing continue with empty tokens list raises SyntaxError."""
        tokens = []
        parser_state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_continue_stmt(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_parse_continue_stmt_pos_at_end(self):
        """Test parsing continue when pos is at end of tokens raises SyntaxError."""
        tokens = [
            self._create_token("IDENTIFIER", "x", line=1, column=1)
        ]
        parser_state = self._create_parser_state(tokens, pos=1)

        with self.assertRaises(SyntaxError) as context:
            _parse_continue_stmt(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_parse_continue_stmt_wrong_token_type(self):
        """Test parsing continue when current token is not CONTINUE raises SyntaxError."""
        tokens = [
            self._create_token("BREAK", "break", line=2, column=3)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_continue_stmt(parser_state)

        self.assertIn("Expected CONTINUE token", str(context.exception))
        self.assertIn("got BREAK", str(context.exception))

    def test_parse_continue_stmt_preserves_position_on_error(self):
        """Test that parser position is not modified on error."""
        tokens = [
            self._create_token("RETURN", "return", line=1, column=1)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        original_pos = parser_state["pos"]

        try:
            _parse_continue_stmt(parser_state)
        except SyntaxError:
            pass

        self.assertEqual(parser_state["pos"], original_pos)

    def test_parse_continue_stmt_multiple_tokens_after(self):
        """Test parsing continue leaves remaining tokens untouched."""
        tokens = [
            self._create_token("CONTINUE", "continue", line=1, column=1),
            self._create_token("SEMICOLON", ";", line=1, column=9),
            self._create_token("IDENTIFIER", "x", line=2, column=1),
            self._create_token("RETURN", "return", line=3, column=1)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _parse_continue_stmt(parser_state)

        self.assertEqual(result["type"], "CONTINUE_STMT")
        self.assertEqual(parser_state["pos"], 2)
        self.assertEqual(len(tokens), 4)

    def test_parse_continue_stmt_different_line_column(self):
        """Test parsing continue with various line and column values."""
        test_cases = [
            (1, 1),
            (10, 5),
            (100, 50),
            (0, 0)
        ]

        for line, column in test_cases:
            with self.subTest(line=line, column=column):
                tokens = [
                    self._create_token("CONTINUE", "continue", line=line, column=column)
                ]
                parser_state = self._create_parser_state(tokens, pos=0)

                result = _parse_continue_stmt(parser_state)

                self.assertEqual(result["line"], line)
                self.assertEqual(result["column"], column)


if __name__ == "__main__":
    unittest.main()
