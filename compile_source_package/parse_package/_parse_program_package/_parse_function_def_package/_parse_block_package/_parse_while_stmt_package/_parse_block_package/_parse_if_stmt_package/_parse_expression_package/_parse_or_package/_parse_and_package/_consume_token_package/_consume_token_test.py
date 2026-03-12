#!/usr/bin/env python3
"""Unit tests for _consume_token function."""

import unittest
from ._consume_token_src import _consume_token


class TestConsumeToken(unittest.TestCase):
    """Test cases for _consume_token function."""

    def test_consume_token_success(self):
        """Test successful token consumption when type matches."""
        parser_state = {
            "tokens": [{"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        result = _consume_token(parser_state, "IDENTIFIER")

        self.assertEqual(result, {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1})
        self.assertEqual(parser_state["pos"], 1)
        self.assertEqual(parser_state.get("error"), "")

    def test_consume_token_type_mismatch(self):
        """Test token consumption fails when type doesn't match."""
        parser_state = {
            "tokens": [{"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        result = _consume_token(parser_state, "NUMBER")

        self.assertEqual(result, {})
        self.assertEqual(parser_state["pos"], 0)
        self.assertIn("Expected token type NUMBER", parser_state.get("error", ""))

    def test_consume_token_empty_tokens(self):
        """Test token consumption fails when tokens list is empty."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        result = _consume_token(parser_state, "IDENTIFIER")

        self.assertEqual(result, {})
        self.assertEqual(parser_state["pos"], 0)
        self.assertIn("Unexpected end of file", parser_state.get("error", ""))

    def test_consume_token_pos_at_end(self):
        """Test token consumption fails when pos is at end of tokens."""
        parser_state = {
            "tokens": [{"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}],
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }

        result = _consume_token(parser_state, "IDENTIFIER")

        self.assertEqual(result, {})
        self.assertEqual(parser_state["pos"], 1)
        self.assertIn("Unexpected end of file", parser_state.get("error", ""))

    def test_consume_token_non_zero_pos(self):
        """Test token consumption at non-zero position."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 5}
            ],
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }

        result = _consume_token(parser_state, "IDENTIFIER")

        self.assertEqual(result, {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3})
        self.assertEqual(parser_state["pos"], 2)
        self.assertEqual(parser_state.get("error"), "")

    def test_consume_token_missing_keys(self):
        """Test token consumption with missing keys in parser_state."""
        parser_state = {}

        result = _consume_token(parser_state, "IDENTIFIER")

        self.assertEqual(result, {})
        self.assertEqual(parser_state.get("pos", 0), 0)
        self.assertIn("Unexpected end of file", parser_state.get("error", ""))

    def test_consume_token_case_sensitive(self):
        """Test token type matching is case-sensitive."""
        parser_state = {
            "tokens": [{"type": "identifier", "value": "x", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        result = _consume_token(parser_state, "IDENTIFIER")

        self.assertEqual(result, {})
        self.assertEqual(parser_state["pos"], 0)
        self.assertIn("Expected token type IDENTIFIER, got identifier", parser_state.get("error", ""))

    def test_consume_token_preserves_other_fields(self):
        """Test that other parser_state fields are preserved."""
        parser_state = {
            "tokens": [{"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py",
            "error": "",
            "custom_field": "value"
        }

        result = _consume_token(parser_state, "IDENTIFIER")

        self.assertEqual(result, {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1})
        self.assertEqual(parser_state["pos"], 1)
        self.assertEqual(parser_state["filename"], "test.py")
        self.assertEqual(parser_state["custom_field"], "value")


if __name__ == "__main__":
    unittest.main()
