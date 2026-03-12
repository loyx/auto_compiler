# -*- coding: utf-8 -*-
"""Unit tests for _peek_token function."""

import unittest
from typing import Any, Dict

from ._peek_token_src import _peek_token


Token = Dict[str, Any]
ParserState = Dict[str, Any]


class TestPeekToken(unittest.TestCase):
    """Test cases for _peek_token function."""

    def test_peek_token_at_beginning(self):
        """Test peeking token when pos is at the beginning (0)."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 6},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertEqual(result, {"type": "KEYWORD", "value": "while", "line": 1, "column": 1})
        # Verify no side effects
        self.assertEqual(parser_state["pos"], 0)

    def test_peek_token_at_middle(self):
        """Test peeking token when pos is in the middle of tokens list."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 6},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 7},
            ],
            "pos": 1,
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertEqual(result, {"type": "LPAREN", "value": "(", "line": 1, "column": 6})
        # Verify no side effects
        self.assertEqual(parser_state["pos"], 1)

    def test_peek_token_at_last_position(self):
        """Test peeking token when pos is at the last valid position."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 6},
            ],
            "pos": 1,
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertEqual(result, {"type": "LPAREN", "value": "(", "line": 1, "column": 6})

    def test_peek_token_at_eof(self):
        """Test peeking token when pos is at EOF (pos == len(tokens))."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
            ],
            "pos": 1,
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_beyond_eof(self):
        """Test peeking token when pos is beyond EOF (pos > len(tokens))."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
            ],
            "pos": 5,
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_empty_tokens_list(self):
        """Test peeking token when tokens list is empty."""
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_missing_tokens_key(self):
        """Test peeking token when 'tokens' key is missing from parser_state."""
        parser_state: ParserState = {
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_missing_pos_key(self):
        """Test peeking token when 'pos' key is missing from parser_state."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
            ],
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        # Default pos should be 0
        self.assertEqual(result, {"type": "KEYWORD", "value": "while", "line": 1, "column": 1})

    def test_peek_token_no_side_effects(self):
        """Test that _peek_token does not modify parser_state."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 6},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        # Make a copy to compare
        original_state = {
            "tokens": list(parser_state["tokens"]),
            "pos": parser_state["pos"],
            "filename": parser_state["filename"],
        }
        
        _peek_token(parser_state)
        
        # Verify parser_state was not modified
        self.assertEqual(parser_state["tokens"], original_state["tokens"])
        self.assertEqual(parser_state["pos"], original_state["pos"])
        self.assertEqual(parser_state["filename"], original_state["filename"])

    def test_peek_token_preserves_token_structure(self):
        """Test that returned token preserves all fields."""
        token: Token = {
            "type": "NUMBER",
            "value": "42",
            "line": 10,
            "column": 25,
            "extra_field": "should_be_preserved",
        }
        parser_state: ParserState = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertEqual(result, token)
        self.assertIsNot(result, token)  # Should be a reference to same dict


if __name__ == "__main__":
    unittest.main()
