# -*- coding: utf-8 -*-
"""Unit tests for _consume_token function."""

import unittest
from typing import Any, Dict

from ._consume_token_src import _consume_token


class TestConsumeToken(unittest.TestCase):
    """Test cases for _consume_token function."""

    def test_consume_token_success(self):
        """Test successful token consumption when type matches."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
            ],
            "filename": "test.py",
            "pos": 0,
        }
        
        result = _consume_token(parser_state, "IF")
        
        self.assertEqual(result, {"type": "IF", "value": "if", "line": 1, "column": 1})
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_second_token(self):
        """Test consuming token at non-zero position."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
            ],
            "filename": "test.py",
            "pos": 1,
        }
        
        result = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertEqual(result, {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4})
        self.assertEqual(parser_state["pos"], 2)

    def test_consume_token_type_mismatch(self):
        """Test SyntaxError when token type does not match."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 2, "column": 5},
            ],
            "filename": "test.py",
            "pos": 0,
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "ELSE")
        
        self.assertIn("test.py:2:5", str(context.exception))
        self.assertIn("期望 ELSE", str(context.exception))
        self.assertIn("但得到 IF", str(context.exception))
        self.assertEqual(parser_state["pos"], 0)

    def test_consume_token_end_of_file(self):
        """Test SyntaxError when pos is at end of tokens."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 3, "column": 10},
            ],
            "filename": "test.py",
            "pos": 1,
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "ELSE")
        
        self.assertIn("test.py:3:10", str(context.exception))
        self.assertIn("期望 ELSE", str(context.exception))
        self.assertIn("但已到达文件末尾", str(context.exception))
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_empty_tokens(self):
        """Test SyntaxError when tokens list is empty."""
        parser_state: Dict[str, Any] = {
            "tokens": [],
            "filename": "test.py",
            "pos": 0,
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "IF")
        
        self.assertIn("test.py:1:1", str(context.exception))
        self.assertIn("期望 IF", str(context.exception))
        self.assertIn("但已到达文件末尾", str(context.exception))

    def test_consume_token_default_filename(self):
        """Test default filename when not provided."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
            ],
            "pos": 0,
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "ELSE")
        
        self.assertIn("<unknown>:1:1", str(context.exception))

    def test_consume_token_missing_line_column(self):
        """Test default line/column when not provided in token."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IF", "value": "if"},
            ],
            "filename": "test.py",
            "pos": 0,
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "ELSE")
        
        self.assertIn("test.py:1:1", str(context.exception))

    def test_consume_token_missing_line_column_eof(self):
        """Test default line/column for EOF when last token lacks them."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IF", "value": "if"},
            ],
            "filename": "test.py",
            "pos": 1,
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "ELSE")
        
        self.assertIn("test.py:1:1", str(context.exception))

    def test_consume_token_pos_not_incremented_on_error(self):
        """Test that pos is not incremented when error occurs."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
            ],
            "filename": "test.py",
            "pos": 0,
        }
        
        with self.assertRaises(SyntaxError):
            _consume_token(parser_state, "ELSE")
        
        self.assertEqual(parser_state["pos"], 0)


if __name__ == "__main__":
    unittest.main()
