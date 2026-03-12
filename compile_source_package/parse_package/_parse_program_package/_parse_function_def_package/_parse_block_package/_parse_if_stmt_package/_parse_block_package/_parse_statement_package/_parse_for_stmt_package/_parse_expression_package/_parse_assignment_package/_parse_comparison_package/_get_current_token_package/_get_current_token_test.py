# -*- coding: utf-8 -*-
"""Unit tests for _get_current_token function."""

import unittest
from typing import Any, Dict

from ._get_current_token_src import _get_current_token


class TestGetCurrentToken(unittest.TestCase):
    """Test cases for _get_current_token function."""

    def test_get_current_token_valid_position_zero(self):
        """Test retrieving token at position 0."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "KEYWORD", "value": "if", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
                {"type": "OPERATOR", "value": ">", "line": 1, "column": 6},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        result = _get_current_token(parser_state)
        self.assertEqual(result, {"type": "KEYWORD", "value": "if", "line": 1, "column": 1})

    def test_get_current_token_valid_position_middle(self):
        """Test retrieving token at middle position."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "KEYWORD", "value": "if", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
                {"type": "OPERATOR", "value": ">", "line": 1, "column": 6},
            ],
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        result = _get_current_token(parser_state)
        self.assertEqual(result, {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4})

    def test_get_current_token_valid_position_last(self):
        """Test retrieving token at last position."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "KEYWORD", "value": "if", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
                {"type": "OPERATOR", "value": ">", "line": 1, "column": 6},
            ],
            "pos": 2,
            "filename": "test.py",
            "error": ""
        }
        result = _get_current_token(parser_state)
        self.assertEqual(result, {"type": "OPERATOR", "value": ">", "line": 1, "column": 6})

    def test_get_current_token_empty_tokens_list(self):
        """Test with empty tokens list."""
        parser_state: Dict[str, Any] = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        result = _get_current_token(parser_state)
        self.assertIsNone(result)

    def test_get_current_token_position_out_of_bounds_positive(self):
        """Test with position beyond tokens length."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "KEYWORD", "value": "if", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
            ],
            "pos": 5,
            "filename": "test.py",
            "error": ""
        }
        result = _get_current_token(parser_state)
        self.assertIsNone(result)

    def test_get_current_token_position_negative(self):
        """Test with negative position."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "KEYWORD", "value": "if", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
            ],
            "pos": -1,
            "filename": "test.py",
            "error": ""
        }
        result = _get_current_token(parser_state)
        self.assertIsNone(result)

    def test_get_current_token_missing_tokens_key(self):
        """Test when tokens key is missing from parser_state."""
        parser_state: Dict[str, Any] = {
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        result = _get_current_token(parser_state)
        self.assertIsNone(result)

    def test_get_current_token_missing_pos_key(self):
        """Test when pos key is missing from parser_state."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "KEYWORD", "value": "if", "line": 1, "column": 1},
            ],
            "filename": "test.py",
            "error": ""
        }
        result = _get_current_token(parser_state)
        self.assertEqual(result, {"type": "KEYWORD", "value": "if", "line": 1, "column": 1})

    def test_get_current_token_single_token(self):
        """Test with single token in list."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        result = _get_current_token(parser_state)
        self.assertEqual(result, {"type": "NUMBER", "value": "42", "line": 1, "column": 1})

    def test_get_current_token_position_at_boundary_len(self):
        """Test with position exactly at tokens length (should return None)."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "KEYWORD", "value": "if", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
            ],
            "pos": 2,
            "filename": "test.py",
            "error": ""
        }
        result = _get_current_token(parser_state)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
