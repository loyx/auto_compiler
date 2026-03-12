# -*- coding: utf-8 -*-
"""Unit tests for _consume_token function."""

import unittest
from typing import Any, Dict

# Relative import from the same package
from ._consume_token_src import _consume_token

Token = Dict[str, Any]
ParserState = Dict[str, Any]


class TestConsumeToken(unittest.TestCase):
    """Test cases for _consume_token function."""

    def test_consume_token_success(self):
        """Happy path: token matches expected type, pos advances."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 2},
            ],
            "filename": "test.py",
            "pos": 0,
            "error": ""
        }
        
        result = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertTrue(result)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_type_mismatch(self):
        """Token type doesn't match, pos unchanged."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "filename": "test.py",
            "pos": 0,
            "error": ""
        }
        
        result = _consume_token(parser_state, "OPERATOR")
        
        self.assertFalse(result)
        self.assertEqual(parser_state["pos"], 0)

    def test_consume_token_empty_tokens(self):
        """Empty tokens list, pos out of bounds."""
        parser_state: ParserState = {
            "tokens": [],
            "filename": "test.py",
            "pos": 0,
            "error": ""
        }
        
        result = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertFalse(result)
        self.assertEqual(parser_state["pos"], 0)

    def test_consume_token_pos_beyond_tokens(self):
        """Pos beyond tokens length."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "filename": "test.py",
            "pos": 5,
            "error": ""
        }
        
        result = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertFalse(result)
        self.assertEqual(parser_state["pos"], 5)

    def test_consume_token_missing_tokens_field(self):
        """Tokens field missing from parser_state."""
        parser_state: ParserState = {
            "filename": "test.py",
            "pos": 0,
            "error": ""
        }
        
        result = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertFalse(result)
        self.assertEqual(parser_state["pos"], 0)

    def test_consume_token_missing_pos_field(self):
        """Pos field missing from parser_state, should default to 0."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "filename": "test.py",
            "error": ""
        }
        
        result = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertTrue(result)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_token_missing_type_field(self):
        """Token missing type field."""
        parser_state: ParserState = {
            "tokens": [
                {"value": "x", "line": 1, "column": 1},
            ],
            "filename": "test.py",
            "pos": 0,
            "error": ""
        }
        
        result = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertFalse(result)
        self.assertEqual(parser_state["pos"], 0)

    def test_consume_token_at_last_position(self):
        """Consume token at the last position in tokens list."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 2},
            ],
            "filename": "test.py",
            "pos": 1,
            "error": ""
        }
        
        result = _consume_token(parser_state, "OPERATOR")
        
        self.assertTrue(result)
        self.assertEqual(parser_state["pos"], 2)

    def test_consume_token_does_not_modify_other_state(self):
        """Verify that only pos is modified, other fields unchanged."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "filename": "test.py",
            "pos": 0,
            "error": "some error"
        }
        
        result = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertTrue(result)
        self.assertEqual(parser_state["filename"], "test.py")
        self.assertEqual(parser_state["error"], "some error")
        self.assertEqual(len(parser_state["tokens"]), 1)

    def test_consume_token_multiple_calls(self):
        """Multiple consecutive consume calls."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 2},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 3},
            ],
            "filename": "test.py",
            "pos": 0,
            "error": ""
        }
        
        result1 = _consume_token(parser_state, "IDENTIFIER")
        result2 = _consume_token(parser_state, "OPERATOR")
        result3 = _consume_token(parser_state, "NUMBER")
        result4 = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertTrue(result3)
        self.assertFalse(result4)
        self.assertEqual(parser_state["pos"], 3)


if __name__ == "__main__":
    unittest.main()
