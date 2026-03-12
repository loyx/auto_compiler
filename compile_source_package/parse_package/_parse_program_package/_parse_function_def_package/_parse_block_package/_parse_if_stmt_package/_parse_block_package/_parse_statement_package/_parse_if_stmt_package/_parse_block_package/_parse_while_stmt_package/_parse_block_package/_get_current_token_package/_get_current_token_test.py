# -*- coding: utf-8 -*-
"""Unit tests for _get_current_token function."""

import unittest

# Relative import from the same package
from ._get_current_token_src import _get_current_token


class TestGetCurrentToken(unittest.TestCase):
    """Test cases for _get_current_token function."""

    def test_get_first_token(self):
        """Test retrieving the first token (pos=0)."""
        token1 = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        token2 = {"type": "OPERATOR", "value": "=", "line": 1, "column": 3}
        parser_state = {
            "tokens": [token1, token2],
            "filename": "test.py",
            "pos": 0
        }
        
        result = _get_current_token(parser_state)
        
        self.assertEqual(result, token1)
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")

    def test_get_middle_token(self):
        """Test retrieving a token in the middle of the list."""
        tokens = [
            {"type": "KEYWORD", "value": "if", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "condition", "line": 1, "column": 4},
            {"type": "OPERATOR", "value": ":", "line": 1, "column": 13}
        ]
        parser_state = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 1
        }
        
        result = _get_current_token(parser_state)
        
        self.assertEqual(result, tokens[1])
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "condition")

    def test_get_last_token(self):
        """Test retrieving the last token (pos=len-1)."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "1", "line": 1, "column": 5}
        ]
        parser_state = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 2
        }
        
        result = _get_current_token(parser_state)
        
        self.assertEqual(result, tokens[2])
        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], "1")

    def test_pos_exceeds_tokens_length(self):
        """Test IndexError when pos >= len(tokens)."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        ]
        parser_state = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 5
        }
        
        with self.assertRaises(IndexError) as context:
            _get_current_token(parser_state)
        
        self.assertIn("Token index 5 out of range", str(context.exception))
        self.assertIn("test.py", str(context.exception))

    def test_pos_equals_tokens_length(self):
        """Test IndexError when pos == len(tokens)."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "+", "line": 1, "column": 3}
        ]
        parser_state = {
            "tokens": tokens,
            "filename": "module.py",
            "pos": 2
        }
        
        with self.assertRaises(IndexError) as context:
            _get_current_token(parser_state)
        
        self.assertIn("Token index 2 out of range", str(context.exception))
        self.assertIn("module.py", str(context.exception))

    def test_empty_tokens_list(self):
        """Test IndexError when tokens list is empty."""
        parser_state = {
            "tokens": [],
            "filename": "empty.py",
            "pos": 0
        }
        
        with self.assertRaises(IndexError) as context:
            _get_current_token(parser_state)
        
        self.assertIn("Token index 0 out of range", str(context.exception))
        self.assertIn("empty.py", str(context.exception))

    def test_filename_not_present_uses_unknown(self):
        """Test that missing filename defaults to 'unknown' in error message."""
        parser_state = {
            "tokens": [{"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}],
            "pos": 10
        }
        
        with self.assertRaises(IndexError) as context:
            _get_current_token(parser_state)
        
        self.assertIn("unknown", str(context.exception))

    def test_token_with_all_fields(self):
        """Test retrieving a token with all standard fields."""
        token = {
            "type": "STRING",
            "value": "hello world",
            "line": 5,
            "column": 10
        }
        parser_state = {
            "tokens": [token],
            "filename": "test.py",
            "pos": 0
        }
        
        result = _get_current_token(parser_state)
        
        self.assertEqual(result["type"], "STRING")
        self.assertEqual(result["value"], "hello world")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)

    def test_does_not_modify_parser_state(self):
        """Test that function does not modify the parser_state dict."""
        token = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        parser_state = {
            "tokens": [token],
            "filename": "test.py",
            "pos": 0
        }
        original_state = parser_state.copy()
        original_tokens = parser_state["tokens"].copy()
        
        _get_current_token(parser_state)
        
        self.assertEqual(parser_state, original_state)
        self.assertEqual(parser_state["tokens"], original_tokens)


if __name__ == "__main__":
    unittest.main()
