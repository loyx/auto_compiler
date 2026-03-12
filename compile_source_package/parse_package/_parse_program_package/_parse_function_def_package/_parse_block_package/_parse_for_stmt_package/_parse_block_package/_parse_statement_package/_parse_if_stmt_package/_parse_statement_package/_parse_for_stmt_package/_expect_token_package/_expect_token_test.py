# -*- coding: utf-8 -*-
"""Unit tests for _expect_token function."""

import unittest
from typing import Any, Dict

from ._expect_token_src import _expect_token


class TestExpectToken(unittest.TestCase):
    """Test cases for _expect_token function."""

    def _create_parser_state(
        self,
        tokens: list = None,
        pos: int = 0,
        filename: str = "test.py"
    ) -> Dict[str, Any]:
        """Helper to create a parser state dict."""
        if tokens is None:
            tokens = []
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename,
            "error": ""
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

    def test_expect_token_success_consumes_token(self):
        """Happy path: token type matches, pos increments."""
        tokens = [
            self._create_token("NAME", "x", 1, 1),
            self._create_token("OP", "=", 1, 3),
            self._create_token("NUMBER", "42", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)

        _expect_token(parser_state, "NAME")

        self.assertEqual(parser_state["pos"], 1)

    def test_expect_token_success_multiple_calls(self):
        """Happy path: multiple consecutive successful expectations."""
        tokens = [
            self._create_token("NAME", "x", 1, 1),
            self._create_token("OP", "=", 1, 3),
            self._create_token("NUMBER", "42", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)

        _expect_token(parser_state, "NAME")
        self.assertEqual(parser_state["pos"], 1)

        _expect_token(parser_state, "OP")
        self.assertEqual(parser_state["pos"], 2)

        _expect_token(parser_state, "NUMBER")
        self.assertEqual(parser_state["pos"], 3)

    def test_expect_token_bounds_error_empty_tokens(self):
        """Boundary: empty token list raises SyntaxError."""
        parser_state = self._create_parser_state(tokens=[], pos=0)

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "NAME")

        self.assertIn("Unexpected end of file", str(context.exception))
        self.assertIn("expected NAME", str(context.exception))

    def test_expect_token_bounds_error_at_end(self):
        """Boundary: pos at end of tokens raises SyntaxError."""
        tokens = [self._create_token("NAME", "x", 1, 1)]
        parser_state = self._create_parser_state(tokens=tokens, pos=1)

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "OP")

        self.assertIn("Unexpected end of file", str(context.exception))

    def test_expect_token_bounds_error_beyond_end(self):
        """Boundary: pos beyond end of tokens raises SyntaxError."""
        tokens = [self._create_token("NAME", "x", 1, 1)]
        parser_state = self._create_parser_state(tokens=tokens, pos=5)

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "NAME")

        self.assertIn("Unexpected end of file", str(context.exception))

    def test_expect_token_type_mismatch(self):
        """Invalid input: token type mismatch raises SyntaxError."""
        tokens = [self._create_token("NAME", "x", 1, 1)]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "NUMBER")

        self.assertIn("Expected NUMBER", str(context.exception))
        self.assertIn("got NAME", str(context.exception))

    def test_expect_token_error_includes_location(self):
        """Error message includes filename, line, column."""
        tokens = [self._create_token("NAME", "x", 5, 10)]
        parser_state = self._create_parser_state(tokens=tokens, pos=0, filename="source.py")

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "NUMBER")

        error_msg = str(context.exception)
        self.assertIn("source.py", error_msg)
        self.assertIn("5", error_msg)
        self.assertIn("10", error_msg)

    def test_expect_token_error_includes_expected_type(self):
        """Error message includes expected token type."""
        tokens = [self._create_token("STRING", '"hello"', 1, 1)]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "NAME")

        self.assertIn("Expected NAME", str(context.exception))

    def test_expect_token_default_filename_unknown(self):
        """Error uses default filename when not provided."""
        tokens = [self._create_token("NAME", "x", 1, 1)]
        parser_state = {"tokens": tokens, "pos": 0}

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "NUMBER")

        self.assertIn("<unknown>", str(context.exception))

    def test_expect_token_pos_not_changed_on_error(self):
        """On error, pos should not be incremented."""
        tokens = [self._create_token("NAME", "x", 1, 1)]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)

        try:
            _expect_token(parser_state, "NUMBER")
        except SyntaxError:
            pass

        self.assertEqual(parser_state["pos"], 0)

    def test_expect_token_single_token_success(self):
        """Edge case: single token list, successful match."""
        tokens = [self._create_token("EOF", "", 1, 1)]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)

        _expect_token(parser_state, "EOF")

        self.assertEqual(parser_state["pos"], 1)

    def test_expect_token_mid_list_success(self):
        """Edge case: matching token in middle of list."""
        tokens = [
            self._create_token("NAME", "a", 1, 1),
            self._create_token("OP", "+", 1, 3),
            self._create_token("NAME", "b", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=1)

        _expect_token(parser_state, "OP")

        self.assertEqual(parser_state["pos"], 2)


if __name__ == "__main__":
    unittest.main()
