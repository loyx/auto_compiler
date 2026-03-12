# -*- coding: utf-8 -*-
"""Unit tests for _peek_token function."""

import unittest

from ._peek_token_src import _peek_token


class TestPeekToken(unittest.TestCase):
    """Test cases for _peek_token function."""

    def test_peek_token_at_valid_position(self):
        """Test peeking token at a valid position in the middle of tokens list."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
        ]
        parser_state = {"tokens": tokens, "pos": 1, "filename": "test.py"}
        
        result = _peek_token(parser_state)
        
        self.assertEqual(result, tokens[1])
        self.assertEqual(result["type"], "OPERATOR")
        self.assertEqual(result["value"], "=")

    def test_peek_token_at_first_position(self):
        """Test peeking token at position 0 (first token)."""
        tokens = [
            {"type": "KEYWORD", "value": "if", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 4},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        result = _peek_token(parser_state)
        
        self.assertEqual(result, tokens[0])
        self.assertEqual(result["type"], "KEYWORD")
        self.assertEqual(result["value"], "if")

    def test_peek_token_at_last_position(self):
        """Test peeking token at the last valid position."""
        tokens = [
            {"type": "IDENTIFIER", "value": "func", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 5},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 6},
        ]
        parser_state = {"tokens": tokens, "pos": 2, "filename": "test.py"}
        
        result = _peek_token(parser_state)
        
        self.assertEqual(result, tokens[2])
        self.assertEqual(result["type"], "RPAREN")
        self.assertEqual(result["value"], ")")

    def test_peek_token_at_end_boundary(self):
        """Test peeking when pos equals len(tokens) - should return None."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
        ]
        parser_state = {"tokens": tokens, "pos": 1, "filename": "test.py"}
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_beyond_end(self):
        """Test peeking when pos is beyond the end of tokens - should return None."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
        ]
        parser_state = {"tokens": tokens, "pos": 5, "filename": "test.py"}
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_negative_position(self):
        """Test peeking when pos is negative - should return None."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
        ]
        parser_state = {"tokens": tokens, "pos": -1, "filename": "test.py"}
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_empty_tokens_list(self):
        """Test peeking when tokens list is empty - should return None."""
        parser_state = {"tokens": [], "pos": 0, "filename": "test.py"}
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_missing_tokens_key(self):
        """Test peeking when 'tokens' key is missing - should use default empty list."""
        parser_state = {"pos": 0, "filename": "test.py"}
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_missing_pos_key(self):
        """Test peeking when 'pos' key is missing - should default to 0."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
        ]
        parser_state = {"tokens": tokens, "filename": "test.py"}
        
        result = _peek_token(parser_state)
        
        self.assertEqual(result, tokens[0])

    def test_peek_token_does_not_consume(self):
        """Test that peeking does not modify the parser state (pos remains unchanged)."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        original_pos = parser_state["pos"]
        
        _peek_token(parser_state)
        
        self.assertEqual(parser_state["pos"], original_pos)

    def test_peek_token_preserves_token_structure(self):
        """Test that the returned token preserves all its fields."""
        tokens = [
            {
                "type": "STRING",
                "value": "hello world",
                "line": 5,
                "column": 10,
            },
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        result = _peek_token(parser_state)
        
        self.assertEqual(result["type"], "STRING")
        self.assertEqual(result["value"], "hello world")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)

    def test_peek_token_with_extra_state_fields(self):
        """Test peeking when parser_state has extra fields beyond tokens/pos/filename."""
        tokens = [
            {"type": "NUMBER", "value": "123", "line": 2, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": None,
            "extra_field": "some_value",
        }
        
        result = _peek_token(parser_state)
        
        self.assertEqual(result, tokens[0])


if __name__ == "__main__":
    unittest.main()
