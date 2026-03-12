# -*- coding: utf-8 -*-
"""
Unit tests for _peek_token function.
Tests the utility function that reads current token from parser state without modification.
"""

import unittest

# Relative import from the same package
from ._peek_token_src import _peek_token


class TestPeekToken(unittest.TestCase):
    """Test cases for _peek_token function."""

    def test_peek_token_returns_token_when_pos_valid(self):
        """Happy path: pos < len(tokens) should return the token at that position."""
        token1 = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        token2 = {"type": "OPERATOR", "value": "+", "line": 1, "column": 3}
        token3 = {"type": "NUMBER", "value": "5", "line": 1, "column": 5}
        
        parser_state = {
            "tokens": [token1, token2, token3],
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        
        result = _peek_token(parser_state)
        
        self.assertEqual(result, token2)
        self.assertEqual(result["type"], "OPERATOR")
        self.assertEqual(result["value"], "+")

    def test_peek_token_returns_none_at_eof(self):
        """Boundary: pos == len(tokens) should return None (EOF condition)."""
        token1 = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        
        parser_state = {
            "tokens": [token1],
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_returns_none_when_pos_exceeds_tokens(self):
        """Boundary: pos > len(tokens) should return None."""
        token1 = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        
        parser_state = {
            "tokens": [token1],
            "pos": 5,
            "filename": "test.py",
            "error": ""
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_returns_none_with_empty_tokens(self):
        """Edge case: empty tokens list should return None regardless of pos."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_returns_first_token_at_pos_zero(self):
        """Edge case: pos = 0 should return the first token."""
        token1 = {"type": "KEYWORD", "value": "if", "line": 1, "column": 1}
        token2 = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4}
        
        parser_state = {
            "tokens": [token1, token2],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        result = _peek_token(parser_state)
        
        self.assertEqual(result, token1)
        self.assertEqual(result["type"], "KEYWORD")
        self.assertEqual(result["value"], "if")

    def test_peek_token_returns_last_token_at_last_index(self):
        """Edge case: pos at last valid index should return the last token."""
        token1 = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        token2 = {"type": "OPERATOR", "value": "=", "line": 1, "column": 3}
        token3 = {"type": "NUMBER", "value": "10", "line": 1, "column": 5}
        
        parser_state = {
            "tokens": [token1, token2, token3],
            "pos": 2,
            "filename": "test.py",
            "error": ""
        }
        
        result = _peek_token(parser_state)
        
        self.assertEqual(result, token3)
        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], "10")

    def test_peek_token_handles_missing_tokens_key(self):
        """Edge case: missing 'tokens' key should handle gracefully."""
        parser_state = {
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_handles_missing_pos_key(self):
        """Edge case: missing 'pos' key should default to 0."""
        token1 = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        
        parser_state = {
            "tokens": [token1],
            "filename": "test.py",
            "error": ""
        }
        
        result = _peek_token(parser_state)
        
        self.assertEqual(result, token1)

    def test_peek_token_does_not_modify_state(self):
        """Verify: function does not modify parser_state."""
        token1 = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        token2 = {"type": "OPERATOR", "value": "+", "line": 1, "column": 3}
        
        parser_state = {
            "tokens": [token1, token2],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        original_pos = parser_state["pos"]
        original_tokens = parser_state["tokens"].copy()
        
        _peek_token(parser_state)
        
        self.assertEqual(parser_state["pos"], original_pos)
        self.assertEqual(parser_state["tokens"], original_tokens)

    def test_peek_token_with_multiple_tokens_at_various_positions(self):
        """Multi-branch: verify correct token returned at various positions."""
        tokens = [
            {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "i", "line": 1, "column": 7},
            {"type": "OPERATOR", "value": "<", "line": 1, "column": 9},
            {"type": "NUMBER", "value": "10", "line": 1, "column": 11},
        ]
        
        for i, expected_token in enumerate(tokens):
            parser_state = {
                "tokens": tokens,
                "pos": i,
                "filename": "test.py",
                "error": ""
            }
            
            result = _peek_token(parser_state)
            
            self.assertEqual(result, expected_token, f"Failed at position {i}")


if __name__ == "__main__":
    unittest.main()
