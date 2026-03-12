"""Unit tests for _peek_token function."""

import unittest
from typing import Any, Dict

from ._peek_token_src import _peek_token


class TestPeekToken(unittest.TestCase):
    """Test cases for _peek_token function."""

    def test_peek_token_at_first_position(self):
        """Test peeking token at position 0 (first token)."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "KEYWORD", "value": "def", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "main", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertEqual(result, {"type": "KEYWORD", "value": "def", "line": 1, "column": 1})
        self.assertEqual(parser_state["pos"], 0)  # pos should not change

    def test_peek_token_at_middle_position(self):
        """Test peeking token at a middle position."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "KEYWORD", "value": "def", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "main", "line": 1, "column": 5},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 9},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 10},
            ],
            "pos": 2,
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertEqual(result, {"type": "LPAREN", "value": "(", "line": 1, "column": 9})
        self.assertEqual(parser_state["pos"], 2)  # pos should not change

    def test_peek_token_at_last_position(self):
        """Test peeking token at the last valid position."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "KEYWORD", "value": "return", "line": 2, "column": 5},
                {"type": "NUMBER", "value": "42", "line": 2, "column": 12},
            ],
            "pos": 1,
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertEqual(result, {"type": "NUMBER", "value": "42", "line": 2, "column": 12})
        self.assertEqual(parser_state["pos"], 1)  # pos should not change

    def test_peek_token_at_eof(self):
        """Test peeking when pos is at EOF (equal to len(tokens))."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "KEYWORD", "value": "def", "line": 1, "column": 1},
            ],
            "pos": 1,
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["pos"], 1)  # pos should not change

    def test_peek_token_beyond_eof(self):
        """Test peeking when pos is beyond EOF (greater than len(tokens))."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "KEYWORD", "value": "def", "line": 1, "column": 1},
            ],
            "pos": 5,
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["pos"], 5)  # pos should not change

    def test_peek_token_empty_tokens_list(self):
        """Test peeking when tokens list is empty."""
        parser_state: Dict[str, Any] = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["pos"], 0)  # pos should not change

    def test_peek_token_preserves_parser_state(self):
        """Test that _peek_token does not modify parser_state."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        original_state = parser_state.copy()
        original_tokens = parser_state["tokens"].copy()
        
        _peek_token(parser_state)
        
        self.assertEqual(parser_state, original_state)
        self.assertEqual(parser_state["tokens"], original_tokens)

    def test_peek_token_with_complex_token_structure(self):
        """Test peeking token with all possible fields."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {
                    "type": "STRING",
                    "value": "hello world",
                    "line": 10,
                    "column": 25,
                },
            ],
            "pos": 0,
            "filename": "complex.py",
            "error": "",
        }
        
        result = _peek_token(parser_state)
        
        self.assertEqual(result["type"], "STRING")
        self.assertEqual(result["value"], "hello world")
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 25)


if __name__ == "__main__":
    unittest.main()
