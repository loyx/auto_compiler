# -*- coding: utf-8 -*-
"""
Unit tests for _advance_parser function.
"""

import unittest
from typing import Any, Dict

from ._advance_parser_src import _advance_parser


ParserState = Dict[str, Any]


class TestAdvanceParser(unittest.TestCase):
    """Test cases for _advance_parser function."""

    def test_advance_parser_increments_pos(self):
        """Happy path: pos should be incremented by 1."""
        parser_state: ParserState = {
            "tokens": ["token1", "token2", "token3"],
            "pos": 0,
            "filename": "test.py"
        }
        
        _advance_parser(parser_state)
        
        self.assertEqual(parser_state["pos"], 1)

    def test_advance_parser_from_middle_position(self):
        """Test incrementing pos from a middle position."""
        parser_state: ParserState = {
            "tokens": ["token1", "token2", "token3", "token4"],
            "pos": 2,
            "filename": "test.py"
        }
        
        _advance_parser(parser_state)
        
        self.assertEqual(parser_state["pos"], 3)

    def test_advance_parser_at_token_end(self):
        """Edge case: pos at last token index, should still increment (no boundary check)."""
        parser_state: ParserState = {
            "tokens": ["token1", "token2"],
            "pos": 1,
            "filename": "test.py"
        }
        
        _advance_parser(parser_state)
        
        self.assertEqual(parser_state["pos"], 2)

    def test_advance_parser_beyond_token_end(self):
        """Edge case: pos beyond tokens length, should still increment (no boundary check)."""
        parser_state: ParserState = {
            "tokens": ["token1"],
            "pos": 5,
            "filename": "test.py"
        }
        
        _advance_parser(parser_state)
        
        self.assertEqual(parser_state["pos"], 6)

    def test_advance_parser_empty_tokens(self):
        """Edge case: empty tokens list, pos should still increment."""
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        _advance_parser(parser_state)
        
        self.assertEqual(parser_state["pos"], 1)

    def test_advance_parser_modifies_in_place(self):
        """Verify that the function modifies the dict in place (side effect)."""
        parser_state: ParserState = {
            "tokens": ["token1"],
            "pos": 0,
            "filename": "test.py"
        }
        original_id = id(parser_state)
        
        _advance_parser(parser_state)
        
        self.assertEqual(id(parser_state), original_id)
        self.assertEqual(parser_state["pos"], 1)

    def test_advance_parser_preserves_other_fields(self):
        """Verify that other fields in parser_state are not modified."""
        parser_state: ParserState = {
            "tokens": ["token1", "token2"],
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        _advance_parser(parser_state)
        
        self.assertEqual(parser_state["tokens"], ["token1", "token2"])
        self.assertEqual(parser_state["filename"], "test.py")
        self.assertIsNone(parser_state["error"])
        self.assertEqual(parser_state["pos"], 1)

    def test_advance_parser_multiple_calls(self):
        """Test multiple consecutive calls to advance parser."""
        parser_state: ParserState = {
            "tokens": ["token1", "token2", "token3"],
            "pos": 0,
            "filename": "test.py"
        }
        
        _advance_parser(parser_state)
        _advance_parser(parser_state)
        _advance_parser(parser_state)
        
        self.assertEqual(parser_state["pos"], 3)

    def test_advance_parser_returns_none(self):
        """Verify that the function returns None."""
        parser_state: ParserState = {
            "tokens": ["token1"],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _advance_parser(parser_state)
        
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
