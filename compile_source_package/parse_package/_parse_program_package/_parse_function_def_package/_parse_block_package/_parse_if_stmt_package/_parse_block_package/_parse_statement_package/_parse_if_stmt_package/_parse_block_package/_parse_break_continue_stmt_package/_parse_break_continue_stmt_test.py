# -*- coding: utf-8 -*-
"""
Unit tests for _parse_break_continue_stmt function.
"""

import unittest
from typing import Dict, Any

from ._parse_break_continue_stmt_src import _parse_break_continue_stmt


class TestParseBreakContinueStmt(unittest.TestCase):
    """Test cases for _parse_break_continue_stmt function."""

    def _create_parser_state(
        self,
        tokens: list,
        pos: int = 0,
        filename: str = "test.py"
    ) -> Dict[str, Any]:
        """Helper to create parser state."""
        return {
            "tokens": tokens,
            "filename": filename,
            "pos": pos
        }

    def _create_token(
        self,
        token_type: str,
        value: str = "",
        line: int = 1,
        column: int = 1
    ) -> Dict[str, Any]:
        """Helper to create a token."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    # ==================== Happy Path Tests ====================

    def test_parse_break_statement(self):
        """Test parsing a BREAK token."""
        tokens = [self._create_token("BREAK", "break", line=5, column=10)]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _parse_break_continue_stmt(parser_state)

        self.assertEqual(result["type"], "BREAK")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)
        self.assertNotIn("value", result)
        self.assertNotIn("children", result)

    def test_parse_continue_statement(self):
        """Test parsing a CONTINUE token."""
        tokens = [self._create_token("CONTINUE", "continue", line=10, column=5)]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _parse_break_continue_stmt(parser_state)

        self.assertEqual(result["type"], "CONTINUE")
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 5)

    def test_parse_break_consumes_token(self):
        """Test that parsing BREAK advances parser position."""
        tokens = [
            self._create_token("BREAK", "break"),
            self._create_token("SEMICOLON", ";")
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        _parse_break_continue_stmt(parser_state)

        self.assertEqual(parser_state["pos"], 1)

    def test_parse_continue_consumes_token(self):
        """Test that parsing CONTINUE advances parser position."""
        tokens = [
            self._create_token("CONTINUE", "continue"),
            self._create_token("SEMICOLON", ";")
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        _parse_break_continue_stmt(parser_state)

        self.assertEqual(parser_state["pos"], 1)

    def test_parse_break_at_middle_of_token_stream(self):
        """Test parsing BREAK when pos is not at start."""
        tokens = [
            self._create_token("IF", "if"),
            self._create_token("LPAREN", "("),
            self._create_token("BREAK", "break", line=3, column=15),
            self._create_token("SEMICOLON", ";")
        ]
        parser_state = self._create_parser_state(tokens, pos=2)

        result = _parse_break_continue_stmt(parser_state)

        self.assertEqual(result["type"], "BREAK")
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 15)
        self.assertEqual(parser_state["pos"], 3)

    # ==================== Edge Case Tests ====================

    def test_parse_break_with_default_line_column(self):
        """Test parsing BREAK when line/column are missing (default to 0)."""
        tokens = [{"type": "BREAK", "value": "break"}]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _parse_break_continue_stmt(parser_state)

        self.assertEqual(result["type"], "BREAK")
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)

    def test_parse_continue_with_default_line_column(self):
        """Test parsing CONTINUE when line/column are missing (default to 0)."""
        tokens = [{"type": "CONTINUE", "value": "continue"}]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _parse_break_continue_stmt(parser_state)

        self.assertEqual(result["type"], "CONTINUE")
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)

    def test_parse_break_with_missing_type_field(self):
        """Test parsing BREAK when type field is missing (default to empty string)."""
        tokens = [{"value": "break", "line": 1, "column": 1}]
        parser_state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_break_continue_stmt(parser_state)

        self.assertIn("Expected BREAK or CONTINUE", str(context.exception))

    def test_parse_at_end_of_token_stream(self):
        """Test parsing when pos is at end of tokens (unexpected end of input)."""
        tokens = [self._create_token("BREAK", "break")]
        parser_state = self._create_parser_state(tokens, pos=1)

        with self.assertRaises(SyntaxError) as context:
            _parse_break_continue_stmt(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("test.py:0:0", str(context.exception))

    def test_parse_with_empty_token_list(self):
        """Test parsing when tokens list is empty."""
        tokens = []
        parser_state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_break_continue_stmt(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))

    # ==================== Error Case Tests ====================

    def test_parse_invalid_token_type(self):
        """Test parsing when token type is not BREAK or CONTINUE."""
        tokens = [self._create_token("IF", "if", line=7, column=20)]
        parser_state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_break_continue_stmt(parser_state)

        self.assertIn("Expected BREAK or CONTINUE", str(context.exception))
        self.assertIn("got IF", str(context.exception))
        self.assertIn("test.py:7:20", str(context.exception))

    def test_parse_keyword_token_type(self):
        """Test parsing when token is a keyword like RETURN."""
        tokens = [self._create_token("RETURN", "return", line=2, column=5)]
        parser_state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_break_continue_stmt(parser_state)

        self.assertIn("Expected BREAK or CONTINUE", str(context.exception))
        self.assertIn("got RETURN", str(context.exception))

    def test_parse_identifier_token_type(self):
        """Test parsing when token is an IDENTIFIER."""
        tokens = [self._create_token("IDENTIFIER", "x", line=4, column=8)]
        parser_state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_break_continue_stmt(parser_state)

        self.assertIn("Expected BREAK or CONTINUE", str(context.exception))
        self.assertIn("got IDENTIFIER", str(context.exception))

    def test_parse_with_custom_filename_in_error(self):
        """Test that error message includes custom filename."""
        tokens = [self._create_token("IF", "if")]
        parser_state = self._create_parser_state(tokens, pos=0, filename="my_module.py")

        with self.assertRaises(SyntaxError) as context:
            _parse_break_continue_stmt(parser_state)

        self.assertIn("my_module.py:", str(context.exception))

    def test_parse_pos_beyond_token_length(self):
        """Test parsing when pos is beyond token list length."""
        tokens = [self._create_token("BREAK", "break")]
        parser_state = self._create_parser_state(tokens, pos=5)

        with self.assertRaises(SyntaxError) as context:
            _parse_break_continue_stmt(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))

    # ==================== State Mutation Tests ====================

    def test_parser_state_not_modified_on_error(self):
        """Test that parser_state pos is not modified when error occurs."""
        tokens = [self._create_token("IF", "if")]
        parser_state = self._create_parser_state(tokens, pos=0)
        original_pos = parser_state["pos"]

        try:
            _parse_break_continue_stmt(parser_state)
        except SyntaxError:
            pass

        self.assertEqual(parser_state["pos"], original_pos)

    def test_parser_state_other_fields_unchanged(self):
        """Test that other parser_state fields remain unchanged after parsing."""
        tokens = [self._create_token("BREAK", "break")]
        parser_state = self._create_parser_state(tokens, pos=0)
        original_tokens = parser_state["tokens"]
        original_filename = parser_state["filename"]

        _parse_break_continue_stmt(parser_state)

        self.assertIs(parser_state["tokens"], original_tokens)
        self.assertEqual(parser_state["filename"], original_filename)


if __name__ == "__main__":
    unittest.main()
