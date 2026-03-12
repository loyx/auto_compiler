# -*- coding: utf-8 -*-
"""Unit tests for _advance function."""

import unittest
from typing import Any, Dict

from ._advance_src import _advance

Token = Dict[str, Any]
ParserState = Dict[str, Any]


class TestAdvance(unittest.TestCase):
    """Test cases for _advance function."""

    def test_advance_returns_current_token_and_increments_pos(self):
        """Happy path: advance returns current token and increments pos."""
        tokens: list[Token] = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
        }

        result = _advance(parser_state)

        self.assertEqual(result, tokens[0])
        self.assertEqual(parser_state["pos"], 1)

    def test_advance_at_first_token(self):
        """Boundary: advance from position 0."""
        tokens: list[Token] = [
            {"type": "KEYWORD", "value": "for", "line": 1, "column": 1},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
        }

        result = _advance(parser_state)

        self.assertEqual(result, tokens[0])
        self.assertEqual(parser_state["pos"], 1)

    def test_advance_at_last_token(self):
        """Boundary: advance from last token position."""
        tokens: list[Token] = [
            {"type": "IDENTIFIER", "value": "i", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.py",
        }

        result = _advance(parser_state)

        self.assertEqual(result, tokens[1])
        self.assertEqual(parser_state["pos"], 2)

    def test_advance_beyond_tokens_length(self):
        """Edge case: advance when pos is already beyond tokens length.
        
        The function allows this without error handling.
        """
        tokens: list[Token] = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.py",
        }

        with self.assertRaises(IndexError):
            _advance(parser_state)

    def test_advance_multiple_times(self):
        """State change: advance multiple times sequentially."""
        tokens: list[Token] = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "1", "line": 1, "column": 5},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
        }

        token1 = _advance(parser_state)
        token2 = _advance(parser_state)
        token3 = _advance(parser_state)

        self.assertEqual(token1, tokens[0])
        self.assertEqual(token2, tokens[1])
        self.assertEqual(token3, tokens[2])
        self.assertEqual(parser_state["pos"], 3)

    def test_advance_does_not_modify_tokens(self):
        """Side effect check: advance only modifies pos, not tokens."""
        tokens: list[Token] = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
        }
        original_tokens_id = id(parser_state["tokens"])

        _advance(parser_state)

        self.assertEqual(id(parser_state["tokens"]), original_tokens_id)
        self.assertEqual(len(parser_state["tokens"]), 1)

    def test_advance_with_empty_tokens(self):
        """Edge case: advance with empty tokens list."""
        tokens: list[Token] = []
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
        }

        with self.assertRaises(IndexError):
            _advance(parser_state)

    def test_advance_preserves_token_structure(self):
        """Verify returned token has all expected fields."""
        tokens: list[Token] = [
            {
                "type": "STRING",
                "value": "hello",
                "line": 5,
                "column": 10,
            },
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
        }

        result = _advance(parser_state)

        self.assertEqual(result["type"], "STRING")
        self.assertEqual(result["value"], "hello")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)


if __name__ == "__main__":
    unittest.main()
