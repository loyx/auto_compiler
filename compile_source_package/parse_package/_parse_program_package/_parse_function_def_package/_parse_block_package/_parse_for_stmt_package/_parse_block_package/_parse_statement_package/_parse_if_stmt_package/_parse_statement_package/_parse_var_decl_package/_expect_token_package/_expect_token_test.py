# -*- coding: utf-8 -*-
"""
Unit tests for _expect_token function.
Tests token consumption logic, error handling, and side effects.
"""

import unittest
from typing import Any, Dict

# Relative import from the same package
from ._expect_token_src import _expect_token


class TestExpectToken(unittest.TestCase):
    """Test cases for _expect_token function."""

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        """Helper to create parser state dictionary."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename,
            "error": ""
        }

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dictionary."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def test_expect_token_success(self):
        """Happy path: token type matches, pos advances, token returned."""
        tokens = [
            self._create_token("VAR", "var", line=1, column=1),
            self._create_token("IDENTIFIER", "x", line=1, column=5),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _expect_token(parser_state, "VAR")

        self.assertEqual(result, tokens[0])
        self.assertEqual(parser_state["pos"], 1)

    def test_expect_token_second_token(self):
        """Test consuming token at non-zero position."""
        tokens = [
            self._create_token("VAR", "var", line=1, column=1),
            self._create_token("IDENTIFIER", "x", line=1, column=5),
            self._create_token("ASSIGN", "=", line=1, column=7),
        ]
        parser_state = self._create_parser_state(tokens, pos=1)

        result = _expect_token(parser_state, "IDENTIFIER")

        self.assertEqual(result, tokens[1])
        self.assertEqual(parser_state["pos"], 2)

    def test_expect_token_empty_tokens(self):
        """Edge case: empty tokens list raises SyntaxError."""
        parser_state = self._create_parser_state([], pos=0)

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "VAR")

        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("expected VAR", str(context.exception))

    def test_expect_token_pos_at_end(self):
        """Edge case: pos equals length of tokens raises SyntaxError."""
        tokens = [
            self._create_token("VAR", "var", line=1, column=1),
        ]
        parser_state = self._create_parser_state(tokens, pos=1)

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "IDENTIFIER")

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_expect_token_pos_beyond_end(self):
        """Edge case: pos beyond tokens length raises SyntaxError."""
        tokens = [
            self._create_token("VAR", "var", line=1, column=1),
        ]
        parser_state = self._create_parser_state(tokens, pos=5)

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "IDENTIFIER")

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_expect_token_type_mismatch(self):
        """Edge case: token type mismatch raises SyntaxError with location."""
        tokens = [
            self._create_token("VAR", "var", line=3, column=10),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "IDENTIFIER")

        self.assertIn("Expected IDENTIFIER", str(context.exception))
        self.assertIn("got VAR", str(context.exception))
        self.assertIn("line 3", str(context.exception))

    def test_expect_token_preserves_state_on_error(self):
        """Verify pos is not modified when error is raised."""
        tokens = [
            self._create_token("VAR", "var", line=1, column=1),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        try:
            _expect_token(parser_state, "IDENTIFIER")
        except SyntaxError:
            pass

        self.assertEqual(parser_state["pos"], 0)

    def test_expect_token_multiple_consumes(self):
        """Test multiple consecutive token consumptions."""
        tokens = [
            self._create_token("VAR", "var", line=1, column=1),
            self._create_token("IDENTIFIER", "x", line=1, column=5),
            self._create_token("ASSIGN", "=", line=1, column=7),
            self._create_token("NUMBER", "42", line=1, column=9),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        token1 = _expect_token(parser_state, "VAR")
        self.assertEqual(token1, tokens[0])
        self.assertEqual(parser_state["pos"], 1)

        token2 = _expect_token(parser_state, "IDENTIFIER")
        self.assertEqual(token2, tokens[1])
        self.assertEqual(parser_state["pos"], 2)

        token3 = _expect_token(parser_state, "ASSIGN")
        self.assertEqual(token3, tokens[2])
        self.assertEqual(parser_state["pos"], 3)

        token4 = _expect_token(parser_state, "NUMBER")
        self.assertEqual(token4, tokens[3])
        self.assertEqual(parser_state["pos"], 4)

    def test_expect_token_case_sensitive(self):
        """Token type matching is case-sensitive."""
        tokens = [
            self._create_token("var", "var", line=1, column=1),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError):
            _expect_token(parser_state, "VAR")

        self.assertEqual(parser_state["pos"], 0)

    def test_expect_token_with_special_characters(self):
        """Test token types with special characters or keywords."""
        tokens = [
            self._create_token("KEYWORD_IF", "if", line=5, column=1),
            self._create_token("OPERATOR_+", "+", line=5, column=4),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _expect_token(parser_state, "KEYWORD_IF")
        self.assertEqual(result["type"], "KEYWORD_IF")
        self.assertEqual(parser_state["pos"], 1)

        result = _expect_token(parser_state, "OPERATOR_+")
        self.assertEqual(result["type"], "OPERATOR_+")
        self.assertEqual(parser_state["pos"], 2)


if __name__ == "__main__":
    unittest.main()
