#!/usr/bin/env python3
"""
Unit tests for _peek_token function.
Tests the peek operation that returns current token without advancing parser position.
"""

import unittest

# Relative import from the same package
from ._peek_token_src import _peek_token


class TestPeekToken(unittest.TestCase):
    """Test cases for _peek_token function."""

    def test_peek_token_valid_position_first(self):
        """Test peeking at first token (pos=0)."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 6},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None,
        }
        result = _peek_token(parser_state)
        self.assertEqual(result["type"], "KEYWORD")
        self.assertEqual(result["value"], "while")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)

    def test_peek_token_valid_position_middle(self):
        """Test peeking at middle token."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 6},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 7},
            ],
            "pos": 1,
            "filename": "test.py",
            "error": None,
        }
        result = _peek_token(parser_state)
        self.assertEqual(result["type"], "LPAREN")
        self.assertEqual(result["value"], "(")

    def test_peek_token_valid_position_last(self):
        """Test peeking at last token (pos=len-1)."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 10},
            ],
            "pos": 1,
            "filename": "test.py",
            "error": None,
        }
        result = _peek_token(parser_state)
        self.assertEqual(result["type"], "RPAREN")
        self.assertEqual(result["value"], ")")

    def test_peek_token_pos_out_of_range(self):
        """Test peeking when pos >= len(tokens)."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
            ],
            "pos": 5,
            "filename": "test.py",
            "error": None,
        }
        result = _peek_token(parser_state)
        self.assertIsNone(result)

    def test_peek_token_pos_negative(self):
        """Test peeking when pos is negative."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
            ],
            "pos": -1,
            "filename": "test.py",
            "error": None,
        }
        result = _peek_token(parser_state)
        self.assertIsNone(result)

    def test_peek_token_empty_tokens_list(self):
        """Test peeking when tokens list is empty."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
            "error": None,
        }
        result = _peek_token(parser_state)
        self.assertIsNone(result)

    def test_peek_token_missing_tokens_key(self):
        """Test peeking when 'tokens' key is missing from parser_state."""
        parser_state = {
            "pos": 0,
            "filename": "test.py",
            "error": None,
        }
        result = _peek_token(parser_state)
        self.assertIsNone(result)

    def test_peek_token_missing_pos_key(self):
        """Test peeking when 'pos' key is missing (should default to 0)."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "if", "line": 1, "column": 1},
            ],
            "filename": "test.py",
            "error": None,
        }
        result = _peek_token(parser_state)
        self.assertEqual(result["type"], "KEYWORD")
        self.assertEqual(result["value"], "if")

    def test_peek_token_does_not_modify_state(self):
        """Test that peek operation does not modify parser_state."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None,
        }
        original_pos = parser_state["pos"]
        original_tokens = parser_state["tokens"].copy()
        
        _peek_token(parser_state)
        
        self.assertEqual(parser_state["pos"], original_pos)
        self.assertEqual(parser_state["tokens"], original_tokens)

    def test_peek_token_single_token(self):
        """Test peeking with single token in list."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 2, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None,
        }
        result = _peek_token(parser_state)
        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], "42")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)


if __name__ == "__main__":
    unittest.main()
