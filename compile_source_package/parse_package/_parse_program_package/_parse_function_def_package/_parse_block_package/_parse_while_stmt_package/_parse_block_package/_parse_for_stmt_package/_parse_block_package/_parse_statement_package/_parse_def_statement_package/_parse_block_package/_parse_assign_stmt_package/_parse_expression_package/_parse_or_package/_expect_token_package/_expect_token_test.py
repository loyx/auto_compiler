# -*- coding: utf-8 -*-
"""Unit tests for _expect_token function."""

import unittest
from typing import Any, Dict

from ._expect_token_src import _expect_token

ParserState = Dict[str, Any]
Token = Dict[str, Any]


class TestExpectToken(unittest.TestCase):
    """Test cases for _expect_token function."""

    def test_expect_token_success_advances_pos(self):
        """Happy path: token type matches, pos advances, token returned."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "OR", "value": "or", "line": 1, "column": 5},
                {"type": "AND", "value": "and", "line": 1, "column": 10},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _expect_token(parser_state, "OR")
        
        self.assertEqual(result, {"type": "OR", "value": "or", "line": 1, "column": 5})
        self.assertEqual(parser_state["pos"], 1)

    def test_expect_token_success_multiple_calls(self):
        """Verify multiple consecutive calls work correctly."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "OR", "value": "or", "line": 1, "column": 5},
                {"type": "AND", "value": "and", "line": 1, "column": 10},
                {"type": "NOT", "value": "not", "line": 2, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        token1 = _expect_token(parser_state, "OR")
        token2 = _expect_token(parser_state, "AND")
        token3 = _expect_token(parser_state, "NOT")
        
        self.assertEqual(token1["type"], "OR")
        self.assertEqual(token2["type"], "AND")
        self.assertEqual(token3["type"], "NOT")
        self.assertEqual(parser_state["pos"], 3)

    def test_expect_token_empty_tokens_raises(self):
        """Edge case: empty tokens list should raise SyntaxError."""
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
        }
        
        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "OR")
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("line 1", str(context.exception))
        self.assertIn("column 1", str(context.exception))

    def test_expect_token_pos_at_end_raises(self):
        """Edge case: pos at end of tokens should raise SyntaxError."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "OR", "value": "or", "line": 1, "column": 5},
                {"type": "AND", "value": "and", "line": 2, "column": 3},
            ],
            "pos": 2,
            "filename": "test.py",
        }
        
        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "OR")
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("line 2", str(context.exception))
        self.assertIn("column 3", str(context.exception))

    def test_expect_token_pos_beyond_end_raises(self):
        """Edge case: pos beyond tokens length should raise SyntaxError."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "OR", "value": "or", "line": 1, "column": 5},
            ],
            "pos": 5,
            "filename": "test.py",
        }
        
        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "OR")
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("line 1", str(context.exception))
        self.assertIn("column 5", str(context.exception))

    def test_expect_token_type_mismatch_raises(self):
        """Error case: token type doesn't match should raise SyntaxError."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "AND", "value": "and", "line": 3, "column": 7},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "OR")
        
        self.assertIn("Expected token type OR", str(context.exception))
        self.assertIn("but got AND", str(context.exception))
        self.assertIn("line 3", str(context.exception))
        self.assertIn("column 7", str(context.exception))

    def test_expect_token_pos_not_advanced_on_error(self):
        """Verify pos is not advanced when error occurs."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "AND", "value": "and", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        with self.assertRaises(SyntaxError):
            _expect_token(parser_state, "OR")
        
        self.assertEqual(parser_state["pos"], 0)

    def test_expect_token_preserves_other_state_fields(self):
        """Verify other parser_state fields are not modified."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "OR", "value": "or", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None,
            "extra_field": "should_remain",
        }
        
        _expect_token(parser_state, "OR")
        
        self.assertEqual(parser_state["filename"], "test.py")
        self.assertIsNone(parser_state["error"])
        self.assertEqual(parser_state["extra_field"], "should_remain")


if __name__ == "__main__":
    unittest.main()
