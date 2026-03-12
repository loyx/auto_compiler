# -*- coding: utf-8 -*-
"""
Unit tests for _consume_token function.
"""

import unittest
from typing import Any, Dict

# Relative import from the source module
from ._consume_token_src import _consume_token


class TestConsumeToken(unittest.TestCase):
    """Test cases for _consume_token function."""

    def test_consume_token_success(self):
        """Happy path: token type matches, pos advances, token returned."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
            ],
            "filename": "test.py",
            "pos": 0,
        }

        result = _consume_token(parser_state, "IDENTIFIER")

        # Verify returned token
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)

        # Verify side effect: pos advanced
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_second_token(self):
        """Consume token from middle position."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
            ],
            "filename": "test.py",
            "pos": 1,
        }

        result = _consume_token(parser_state, "OPERATOR")

        self.assertEqual(result["type"], "OPERATOR")
        self.assertEqual(result["value"], "=")
        self.assertEqual(parser_state["pos"], 2)

    def test_consume_token_type_mismatch(self):
        """Error case: token type doesn't match expected type."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 5},
            ],
            "filename": "test.py",
            "pos": 0,
        }

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "NUMBER")

        # Verify error message contains expected info
        error_msg = str(context.exception)
        self.assertIn("test.py:2:5", error_msg)
        self.assertIn("Expected NUMBER", error_msg)
        self.assertIn("got IDENTIFIER", error_msg)

        # Verify pos not modified on error
        self.assertEqual(parser_state["pos"], 0)

    def test_consume_token_out_of_bounds(self):
        """Boundary case: position at end of tokens (out of bounds)."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "filename": "test.py",
            "pos": 1,  # pos equals len(tokens)
        }

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "IDENTIFIER")

        # Verify error message for unexpected end of input
        error_msg = str(context.exception)
        self.assertIn("test.py:0:0", error_msg)
        self.assertIn("Unexpected end of input", error_msg)
        self.assertIn("expected IDENTIFIER", error_msg)

    def test_consume_token_empty_tokens(self):
        """Edge case: empty tokens list."""
        parser_state: Dict[str, Any] = {
            "tokens": [],
            "filename": "empty.py",
            "pos": 0,
        }

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "IDENTIFIER")

        error_msg = str(context.exception)
        self.assertIn("empty.py:0:0", error_msg)
        self.assertIn("Unexpected end of input", error_msg)

    def test_consume_token_pos_beyond_bounds(self):
        """Edge case: position beyond tokens length."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "filename": "test.py",
            "pos": 5,  # pos > len(tokens)
        }

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "IDENTIFIER")

        error_msg = str(context.exception)
        self.assertIn("Unexpected end of input", error_msg)

    def test_consume_token_preserves_state_on_success(self):
        """Verify other parser_state fields remain unchanged on success."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "KEYWORD", "value": "if", "line": 3, "column": 1},
            ],
            "filename": "test.py",
            "pos": 0,
            "error": None,
        }

        _consume_token(parser_state, "KEYWORD")

        # Only pos should change
        self.assertEqual(parser_state["filename"], "test.py")
        self.assertEqual(parser_state["error"], None)
        self.assertEqual(len(parser_state["tokens"]), 1)
        self.assertEqual(parser_state["pos"], 1)


if __name__ == "__main__":
    unittest.main()
