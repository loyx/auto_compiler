# -*- coding: utf-8 -*-
"""Unit tests for _parse_identifier function."""

import unittest
from ._parse_identifier_src import _parse_identifier


class TestParseIdentifier(unittest.TestCase):
    """Test cases for _parse_identifier parser function."""

    def test_parse_valid_identifier(self):
        """Happy path: parse a valid IDENTIFIER token."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "myVar", "line": 5, "column": 10}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_identifier(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "myVar")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_identifier_at_end_of_tokens(self):
        """Edge case: pos is at end of tokens list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_identifier(parser_state)
        
        self.assertIn("test.py:1:1: expected identifier", str(context.exception))

    def test_parse_identifier_pos_beyond_tokens(self):
        """Edge case: pos is beyond tokens list length."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 5,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_identifier(parser_state)
        
        self.assertIn("test.py:1:1: expected identifier", str(context.exception))

    def test_parse_identifier_non_identifier_token(self):
        """Edge case: current token is not IDENTIFIER."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "if", "line": 3, "column": 7}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_identifier(parser_state)
        
        self.assertIn("test.py:3:7: expected identifier", str(context.exception))

    def test_parse_identifier_missing_filename(self):
        """Edge case: filename not provided, should default to '<unknown>'."""
        parser_state = {
            "tokens": [],
            "pos": 0
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_identifier(parser_state)
        
        self.assertIn("<unknown>:1:1: expected identifier", str(context.exception))

    def test_parse_identifier_token_missing_line_column(self):
        """Edge case: token missing line/column, should default to 1."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42"}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_identifier(parser_state)
        
        self.assertIn("test.py:1:1: expected identifier", str(context.exception))

    def test_parse_identifier_consumes_token(self):
        """Verify that pos is incremented after consuming token."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "first", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "second", "line": 1, "column": 10}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_identifier(parser_state)
        
        self.assertEqual(result["value"], "first")
        self.assertEqual(parser_state["pos"], 1)
        
        # Parse second identifier
        result2 = _parse_identifier(parser_state)
        
        self.assertEqual(result2["value"], "second")
        self.assertEqual(parser_state["pos"], 2)

    def test_parse_identifier_preserves_original_state_except_pos(self):
        """Verify that only pos changes in parser_state."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        _ = _parse_identifier(parser_state)
        
        self.assertEqual(len(parser_state["tokens"]), 1)
        self.assertEqual(parser_state["filename"], "test.py")
        self.assertEqual(parser_state["error"], "")
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_identifier_with_special_characters_in_value(self):
        """Test identifier with underscores and numbers in value."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "_private_var123", "line": 10, "column": 5}
            ],
            "pos": 0,
            "filename": "module.py"
        }
        
        result = _parse_identifier(parser_state)
        
        self.assertEqual(result["value"], "_private_var123")
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 5)

    def test_parse_identifier_empty_value(self):
        """Test identifier with empty string value."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_identifier(parser_state)
        
        self.assertEqual(result["value"], "")
        self.assertEqual(result["type"], "IDENTIFIER")


if __name__ == "__main__":
    unittest.main()
