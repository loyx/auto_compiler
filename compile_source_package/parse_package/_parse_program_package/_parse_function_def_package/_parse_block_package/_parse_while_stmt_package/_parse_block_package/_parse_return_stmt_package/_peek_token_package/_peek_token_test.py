# -*- coding: utf-8 -*-
"""Unit tests for _peek_token function."""

import unittest

# Relative import from the same package
from ._peek_token_src import _peek_token


class TestPeekToken(unittest.TestCase):
    """Test cases for _peek_token function."""

    def test_peek_token_at_valid_position(self):
        """Happy path: pos is within bounds, should return the token."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 1,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertEqual(result, {"type": "OPERATOR", "value": "=", "line": 1, "column": 3})

    def test_peek_token_at_first_position(self):
        """Boundary: pos is 0, should return first token."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "def", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "foo", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertEqual(result, {"type": "KEYWORD", "value": "def", "line": 1, "column": 1})

    def test_peek_token_at_last_position(self):
        """Boundary: pos equals len(tokens) - 1, should return last token."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "1", "line": 1, "column": 5},
            ],
            "pos": 2,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertEqual(result, {"type": "NUMBER", "value": "1", "line": 1, "column": 5})

    def test_peek_token_pos_equals_length(self):
        """Boundary: pos equals len(tokens), should return None."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
            ],
            "pos": 2,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertIsNone(result)

    def test_peek_token_pos_exceeds_length(self):
        """Edge case: pos exceeds len(tokens), should return None."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 5,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertIsNone(result)

    def test_peek_token_empty_tokens_list(self):
        """Edge case: empty tokens list, should return None."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertIsNone(result)

    def test_peek_token_missing_tokens_key(self):
        """Edge case: parser_state missing 'tokens' key, should default to [] and return None."""
        parser_state = {
            "pos": 0,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertIsNone(result)

    def test_peek_token_missing_pos_key(self):
        """Edge case: parser_state missing 'pos' key, should default to 0."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertEqual(result, {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1})

    def test_peek_token_missing_both_keys(self):
        """Edge case: parser_state missing both 'tokens' and 'pos' keys."""
        parser_state = {
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertIsNone(result)

    def test_peek_token_does_not_modify_state(self):
        """Verify _peek_token is a pure read operation with no side effects."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        # Store original state
        original_pos = parser_state["pos"]
        original_tokens = parser_state["tokens"].copy()
        
        # Call peek
        _peek_token(parser_state)
        
        # Verify state is unchanged
        self.assertEqual(parser_state["pos"], original_pos)
        self.assertEqual(parser_state["tokens"], original_tokens)

    def test_peek_token_with_complex_token_structure(self):
        """Test with tokens that have additional fields beyond type, value, line, column."""
        parser_state = {
            "tokens": [
                {
                    "type": "STRING",
                    "value": "hello world",
                    "line": 5,
                    "column": 10,
                    "raw": '"hello world"',
                    "escape_sequences": [],
                },
            ],
            "pos": 0,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertEqual(result["type"], "STRING")
        self.assertEqual(result["value"], "hello world")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)
        self.assertEqual(result["raw"], '"hello world"')


if __name__ == "__main__":
    unittest.main()
