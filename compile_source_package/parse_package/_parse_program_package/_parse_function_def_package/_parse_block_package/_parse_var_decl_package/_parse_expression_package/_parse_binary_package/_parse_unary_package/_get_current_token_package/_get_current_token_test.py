#!/usr/bin/env python3
"""Unit tests for _get_current_token function."""

import unittest
from typing import Any, Dict

# Relative import from the same package
from ._get_current_token_src import _get_current_token


class TestGetCurrentToken(unittest.TestCase):
    """Test cases for _get_current_token function."""

    def _make_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dictionary."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _make_parser_state(self, tokens: list, pos: int, filename: str = "test.c") -> Dict[str, Any]:
        """Helper to create a parser_state dictionary."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def test_get_first_token(self):
        """Test getting the first token (pos=0)."""
        tokens = [
            self._make_token("KEYWORD", "int", 1, 1),
            self._make_token("IDENTIFIER", "main", 1, 5),
        ]
        parser_state = self._make_parser_state(tokens, 0)
        
        result = _get_current_token(parser_state)
        
        self.assertEqual(result, tokens[0])
        self.assertEqual(result["type"], "KEYWORD")
        self.assertEqual(result["value"], "int")

    def test_get_middle_token(self):
        """Test getting a token in the middle of the list."""
        tokens = [
            self._make_token("KEYWORD", "int", 1, 1),
            self._make_token("IDENTIFIER", "main", 1, 5),
            self._make_token("PUNCTUATION", "(", 1, 9),
            self._make_token("PUNCTUATION", ")", 1, 10),
        ]
        parser_state = self._make_parser_state(tokens, 2)
        
        result = _get_current_token(parser_state)
        
        self.assertEqual(result, tokens[2])
        self.assertEqual(result["type"], "PUNCTUATION")
        self.assertEqual(result["value"], "(")

    def test_get_last_token(self):
        """Test getting the last token (pos=len(tokens)-1)."""
        tokens = [
            self._make_token("KEYWORD", "int", 1, 1),
            self._make_token("IDENTIFIER", "x", 1, 5),
            self._make_token("PUNCTUATION", ";", 1, 6),
        ]
        parser_state = self._make_parser_state(tokens, 2)
        
        result = _get_current_token(parser_state)
        
        self.assertEqual(result, tokens[2])
        self.assertEqual(result["type"], "PUNCTUATION")
        self.assertEqual(result["value"], ";")

    def test_pos_at_end_returns_none(self):
        """Test when pos equals len(tokens), should return None."""
        tokens = [
            self._make_token("KEYWORD", "int", 1, 1),
            self._make_token("IDENTIFIER", "main", 1, 5),
        ]
        parser_state = self._make_parser_state(tokens, 2)
        
        result = _get_current_token(parser_state)
        
        self.assertIsNone(result)

    def test_pos_beyond_end_returns_none(self):
        """Test when pos is greater than len(tokens), should return None."""
        tokens = [
            self._make_token("KEYWORD", "int", 1, 1),
        ]
        parser_state = self._make_parser_state(tokens, 5)
        
        result = _get_current_token(parser_state)
        
        self.assertIsNone(result)

    def test_empty_tokens_list_returns_none(self):
        """Test when tokens list is empty, should return None."""
        tokens = []
        parser_state = self._make_parser_state(tokens, 0)
        
        result = _get_current_token(parser_state)
        
        self.assertIsNone(result)

    def test_empty_tokens_with_nonzero_pos_returns_none(self):
        """Test when tokens list is empty and pos > 0, should return None."""
        tokens = []
        parser_state = self._make_parser_state(tokens, 10)
        
        result = _get_current_token(parser_state)
        
        self.assertIsNone(result)

    def test_missing_tokens_key_raises_keyerror(self):
        """Test when 'tokens' key is missing, should raise KeyError."""
        parser_state = {
            "pos": 0,
            "filename": "test.c"
        }
        
        with self.assertRaises(KeyError):
            _get_current_token(parser_state)

    def test_missing_pos_key_raises_keyerror(self):
        """Test when 'pos' key is missing, should raise KeyError."""
        tokens = [self._make_token("KEYWORD", "int", 1, 1)]
        parser_state = {
            "tokens": tokens,
            "filename": "test.c"
        }
        
        with self.assertRaises(KeyError):
            _get_current_token(parser_state)

    def test_token_with_all_fields(self):
        """Test token with all standard fields (type, value, line, column)."""
        tokens = [
            {
                "type": "STRING_LITERAL",
                "value": '"hello world"',
                "line": 5,
                "column": 12
            }
        ]
        parser_state = self._make_parser_state(tokens, 0)
        
        result = _get_current_token(parser_state)
        
        self.assertEqual(result["type"], "STRING_LITERAL")
        self.assertEqual(result["value"], '"hello world"')
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 12)

    def test_token_with_extra_fields(self):
        """Test that extra fields in token are preserved."""
        tokens = [
            {
                "type": "IDENTIFIER",
                "value": "count",
                "line": 1,
                "column": 1,
                "extra_field": "extra_value"
            }
        ]
        parser_state = self._make_parser_state(tokens, 0)
        
        result = _get_current_token(parser_state)
        
        self.assertEqual(result["extra_field"], "extra_value")

    def test_does_not_modify_parser_state(self):
        """Test that the function does not modify the input parser_state."""
        tokens = [self._make_token("KEYWORD", "int", 1, 1)]
        parser_state = self._make_parser_state(tokens, 0)
        
        original_pos = parser_state["pos"]
        original_tokens_len = len(parser_state["tokens"])
        
        _get_current_token(parser_state)
        
        self.assertEqual(parser_state["pos"], original_pos)
        self.assertEqual(len(parser_state["tokens"]), original_tokens_len)

    def test_multiple_calls_same_result(self):
        """Test that multiple calls with same state return same result."""
        tokens = [
            self._make_token("KEYWORD", "int", 1, 1),
            self._make_token("IDENTIFIER", "x", 1, 5),
        ]
        parser_state = self._make_parser_state(tokens, 1)
        
        result1 = _get_current_token(parser_state)
        result2 = _get_current_token(parser_state)
        
        self.assertEqual(result1, result2)
        self.assertIs(result1, result2)  # Same object reference


if __name__ == "__main__":
    unittest.main()
