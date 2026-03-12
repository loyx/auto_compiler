# -*- coding: utf-8 -*-
"""Unit tests for _peek_token function."""

import unittest
from typing import Any, Dict

from ._peek_token_src import _peek_token


Token = Dict[str, Any]
ParserState = Dict[str, Any]


class TestPeekToken(unittest.TestCase):
    """Test cases for _peek_token function."""

    def test_peek_current_token_offset_zero(self):
        """Test peeking at current position with offset=0."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "OP", "value": "=", "line": 1, "column": 3},
                {"type": "NUM", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None,
        }
        result = _peek_token(parser_state, 0)
        self.assertEqual(result["type"], "IDENT")
        self.assertEqual(result["value"], "x")
        # Verify parser state is not modified
        self.assertEqual(parser_state["pos"], 0)

    def test_peek_token_with_positive_offset(self):
        """Test peeking at token with positive offset."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "OP", "value": "=", "line": 1, "column": 3},
                {"type": "NUM", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None,
        }
        result = _peek_token(parser_state, 1)
        self.assertEqual(result["type"], "OP")
        self.assertEqual(result["value"], "=")
        self.assertEqual(parser_state["pos"], 0)

    def test_peek_token_with_large_positive_offset(self):
        """Test peeking at token with larger positive offset."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "OP", "value": "=", "line": 1, "column": 3},
                {"type": "NUM", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None,
        }
        result = _peek_token(parser_state, 2)
        self.assertEqual(result["type"], "NUM")
        self.assertEqual(result["value"], "42")

    def test_peek_token_from_middle_position(self):
        """Test peeking when pos is in the middle of tokens."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "OP", "value": "=", "line": 1, "column": 3},
                {"type": "NUM", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 1,
            "filename": "test.py",
            "error": None,
        }
        result = _peek_token(parser_state, 0)
        self.assertEqual(result["type"], "OP")
        self.assertEqual(result["value"], "=")

    def test_peek_token_offset_beyond_tokens(self):
        """Test peeking when offset goes beyond token list."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "OP", "value": "=", "line": 1, "column": 3},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None,
        }
        result = _peek_token(parser_state, 5)
        self.assertIsNone(result)

    def test_peek_token_offset_exactly_at_boundary(self):
        """Test peeking when offset lands exactly at the last token."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "OP", "value": "=", "line": 1, "column": 3},
                {"type": "NUM", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None,
        }
        result = _peek_token(parser_state, 2)
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "NUM")
        # One beyond should return None
        result_beyond = _peek_token(parser_state, 3)
        self.assertIsNone(result_beyond)

    def test_peek_token_negative_offset(self):
        """Test peeking with negative offset."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "OP", "value": "=", "line": 1, "column": 3},
                {"type": "NUM", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 2,
            "filename": "test.py",
            "error": None,
        }
        result = _peek_token(parser_state, -1)
        self.assertEqual(result["type"], "OP")
        self.assertEqual(result["value"], "=")

    def test_peek_token_negative_offset_out_of_bounds(self):
        """Test peeking with negative offset that goes before start."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "OP", "value": "=", "line": 1, "column": 3},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None,
        }
        result = _peek_token(parser_state, -1)
        self.assertIsNone(result)

    def test_peek_token_empty_tokens(self):
        """Test peeking when tokens list is empty."""
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
            "error": None,
        }
        result = _peek_token(parser_state, 0)
        self.assertIsNone(result)

    def test_peek_token_pos_at_end(self):
        """Test peeking when pos is at the end of tokens."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "OP", "value": "=", "line": 1, "column": 3},
            ],
            "pos": 2,
            "filename": "test.py",
            "error": None,
        }
        result = _peek_token(parser_state, 0)
        self.assertIsNone(result)

    def test_peek_token_pos_beyond_end(self):
        """Test peeking when pos is beyond the end of tokens."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 5,
            "filename": "test.py",
            "error": None,
        }
        result = _peek_token(parser_state, 0)
        self.assertIsNone(result)

    def test_peek_token_single_token(self):
        """Test peeking with a single token in the list."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "KEYWORD", "value": "return", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None,
        }
        result = _peek_token(parser_state, 0)
        self.assertEqual(result["type"], "KEYWORD")
        self.assertEqual(result["value"], "return")
        result_beyond = _peek_token(parser_state, 1)
        self.assertIsNone(result_beyond)

    def test_peek_token_does_not_modify_state(self):
        """Test that _peek_token does not modify parser_state."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "OP", "value": "=", "line": 1, "column": 3},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None,
        }
        original_pos = parser_state["pos"]
        original_tokens_len = len(parser_state["tokens"])
        _peek_token(parser_state, 1)
        self.assertEqual(parser_state["pos"], original_pos)
        self.assertEqual(len(parser_state["tokens"]), original_tokens_len)


if __name__ == "__main__":
    unittest.main()
