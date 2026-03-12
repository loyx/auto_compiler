#!/usr/bin/env python3
"""Unit tests for _get_current_token function."""

import unittest

from ._get_current_token_src import _get_current_token


class TestGetCurrentToken(unittest.TestCase):
    """Test cases for _get_current_token function."""

    def test_get_token_at_valid_position(self):
        """Happy path: pos is within valid range."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 1,
            "filename": "test.py"
        }
        result = _get_current_token(parser_state)
        self.assertEqual(result["type"], "OPERATOR")
        self.assertEqual(result["value"], "=")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)

    def test_get_first_token(self):
        """Boundary: pos at 0 (first token)."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "if", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        result = _get_current_token(parser_state)
        self.assertEqual(result["type"], "KEYWORD")
        self.assertEqual(result["value"], "if")

    def test_get_last_token(self):
        """Boundary: pos at last index."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "1", "line": 1, "column": 5},
            ],
            "pos": 2,
            "filename": "test.py"
        }
        result = _get_current_token(parser_state)
        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], "1")

    def test_pos_out_of_range_high(self):
        """Boundary: pos >= len(tokens) returns EOF token."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 5,
            "filename": "test.py"
        }
        result = _get_current_token(parser_state)
        self.assertEqual(result["type"], "EOF")
        self.assertEqual(result["value"], "")
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)

    def test_pos_negative(self):
        """Boundary: pos < 0 returns EOF token."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": -1,
            "filename": "test.py"
        }
        result = _get_current_token(parser_state)
        self.assertEqual(result["type"], "EOF")
        self.assertEqual(result["value"], "")

    def test_empty_tokens_list(self):
        """Edge case: empty tokens list returns EOF token."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        result = _get_current_token(parser_state)
        self.assertEqual(result["type"], "EOF")
        self.assertEqual(result["value"], "")

    def test_missing_tokens_key(self):
        """Edge case: missing 'tokens' key defaults to empty list."""
        parser_state = {
            "pos": 0,
            "filename": "test.py"
        }
        result = _get_current_token(parser_state)
        self.assertEqual(result["type"], "EOF")
        self.assertEqual(result["value"], "")

    def test_missing_pos_key(self):
        """Edge case: missing 'pos' key defaults to 0."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "filename": "test.py"
        }
        result = _get_current_token(parser_state)
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")

    def test_does_not_modify_parser_state(self):
        """Verify function does not modify parser_state (no side effects)."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        original_state = parser_state.copy()
        original_tokens = parser_state["tokens"].copy()
        
        _get_current_token(parser_state)
        
        self.assertEqual(parser_state, original_state)
        self.assertEqual(parser_state["tokens"], original_tokens)

    def test_pos_exactly_at_length(self):
        """Boundary: pos == len(tokens) returns EOF token."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
            ],
            "pos": 2,
            "filename": "test.py"
        }
        result = _get_current_token(parser_state)
        self.assertEqual(result["type"], "EOF")
        self.assertEqual(result["value"], "")


if __name__ == "__main__":
    unittest.main()
