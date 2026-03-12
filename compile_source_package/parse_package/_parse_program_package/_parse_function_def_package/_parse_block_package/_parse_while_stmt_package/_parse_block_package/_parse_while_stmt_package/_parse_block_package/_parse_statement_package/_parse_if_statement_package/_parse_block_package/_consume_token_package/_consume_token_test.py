# -*- coding: utf-8 -*-
"""Unit tests for _consume_token function."""

import unittest
from typing import Any, Dict

from ._consume_token_src import _consume_token


class TestConsumeToken(unittest.TestCase):
    """Test cases for _consume_token function."""

    def _create_parser_state(
        self,
        tokens: list,
        pos: int = 0,
        filename: str = "test.py"
    ) -> Dict[str, Any]:
        """Helper to create parser state dict."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename,
            "error": None
        }

    def _create_token(
        self,
        token_type: str,
        value: str,
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

    def test_consume_token_without_type_validation(self):
        """Happy path: consume token without expected_type."""
        token = self._create_token("IDENTIFIER", "x", line=1, column=1)
        parser_state = self._create_parser_state([token])

        result = _consume_token(parser_state)

        self.assertEqual(result, token)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_with_matching_expected_type(self):
        """Happy path: consume token with matching expected_type."""
        token = self._create_token("KEYWORD", "if", line=2, column=5)
        parser_state = self._create_parser_state([token])

        result = _consume_token(parser_state, expected_type="KEYWORD")

        self.assertEqual(result, token)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_eof_raises_syntax_error(self):
        """Edge case: EOF raises SyntaxError."""
        parser_state = self._create_parser_state([], pos=0)

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state)

        self.assertIn("Unexpected EOF", str(context.exception))
        self.assertIn("test.py", str(context.exception))

    def test_consume_token_eof_with_custom_filename(self):
        """Edge case: EOF with custom filename in error message."""
        parser_state = self._create_parser_state([], pos=0, filename="main.py")

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state)

        self.assertIn("Unexpected EOF at line main.py", str(context.exception))

    def test_consume_token_type_mismatch_raises_syntax_error(self):
        """Edge case: type mismatch raises SyntaxError."""
        token = self._create_token("IDENTIFIER", "x", line=3, column=10)
        parser_state = self._create_parser_state([token])

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, expected_type="KEYWORD")

        self.assertIn("Expected KEYWORD but got IDENTIFIER", str(context.exception))
        self.assertIn("line 3", str(context.exception))
        self.assertIn("column 10", str(context.exception))

    def test_consume_token_pos_not_advanced_on_error(self):
        """Verify pos is not advanced when error occurs."""
        token = self._create_token("IDENTIFIER", "x")
        parser_state = self._create_parser_state([token], pos=0)

        try:
            _consume_token(parser_state, expected_type="KEYWORD")
        except SyntaxError:
            pass

        self.assertEqual(parser_state["pos"], 0)

    def test_consume_token_multiple_tokens_sequential(self):
        """Happy path: consume multiple tokens sequentially."""
        tokens = [
            self._create_token("KEYWORD", "while", line=1, column=1),
            self._create_token("LPAREN", "(", line=1, column=7),
            self._create_token("IDENTIFIER", "x", line=1, column=8),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        token1 = _consume_token(parser_state)
        token2 = _consume_token(parser_state)
        token3 = _consume_token(parser_state)

        self.assertEqual(token1["type"], "KEYWORD")
        self.assertEqual(token1["value"], "while")
        self.assertEqual(token2["type"], "LPAREN")
        self.assertEqual(token3["type"], "IDENTIFIER")
        self.assertEqual(parser_state["pos"], 3)

    def test_consume_token_at_middle_position(self):
        """Boundary: consume token when pos is in the middle."""
        tokens = [
            self._create_token("KEYWORD", "def", line=1, column=1),
            self._create_token("IDENTIFIER", "foo", line=1, column=5),
            self._create_token("LPAREN", "(", line=1, column=9),
        ]
        parser_state = self._create_parser_state(tokens, pos=1)

        result = _consume_token(parser_state)

        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "foo")
        self.assertEqual(parser_state["pos"], 2)

    def test_consume_token_last_token(self):
        """Boundary: consume the last token in the list."""
        tokens = [
            self._create_token("KEYWORD", "if", line=1, column=1),
            self._create_token("IDENTIFIER", "x", line=1, column=4),
        ]
        parser_state = self._create_parser_state(tokens, pos=1)

        result = _consume_token(parser_state)

        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(parser_state["pos"], 2)

    def test_consume_token_after_last_raises_eof(self):
        """Boundary: consuming after last token raises EOF."""
        tokens = [self._create_token("KEYWORD", "if")]
        parser_state = self._create_parser_state(tokens, pos=1)

        with self.assertRaises(SyntaxError):
            _consume_token(parser_state)

    def test_consume_token_preserves_token_integrity(self):
        """Verify returned token is the exact same dict (not a copy)."""
        token = self._create_token("NUMBER", "42", line=5, column=20)
        parser_state = self._create_parser_state([token])

        result = _consume_token(parser_state)

        self.assertIs(result, token)

    def test_consume_token_none_expected_type_allows_any(self):
        """Verify expected_type=None allows any token type."""
        token = self._create_token("OPERATOR", "+")
        parser_state = self._create_parser_state([token])

        result = _consume_token(parser_state, expected_type=None)

        self.assertEqual(result, token)
        self.assertEqual(parser_state["pos"], 1)


if __name__ == "__main__":
    unittest.main()
