# -*- coding: utf-8 -*-
"""Unit tests for _parse_unary function."""

import unittest
from unittest.mock import patch
from typing import Dict, Any, List

# Relative import from the same package
from ._parse_unary_src import _parse_unary


def _make_parser_state(tokens: List[Dict[str, Any]], pos: int = 0, filename: str = "test.c") -> Dict[str, Any]:
    """Helper to create parser state dict."""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename
    }


def _make_token(token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
    """Helper to create a token dict."""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }


class TestParseUnary(unittest.TestCase):
    """Test cases for _parse_unary function."""

    def test_parse_unary_minus_operator(self):
        """Test parsing unary minus operator."""
        tokens = [
            _make_token("MINUS", "-", 1, 1),
            _make_token("IDENTIFIER", "x", 1, 2),
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        with patch("._parse_atom_package._parse_atom_src._parse_atom") as mock_parse_atom:
            mock_parse_atom.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 2
            }
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "IDENTIFIER")
            self.assertEqual(parser_state["pos"], 2)

    def test_parse_unary_plus_operator(self):
        """Test parsing unary plus operator."""
        tokens = [
            _make_token("PLUS", "+", 1, 1),
            _make_token("LITERAL", "5", 1, 2),
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        with patch("._parse_atom_package._parse_atom_src._parse_atom") as mock_parse_atom:
            mock_parse_atom.return_value = {
                "type": "LITERAL",
                "value": "5",
                "children": [],
                "line": 1,
                "column": 2
            }
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "+")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(parser_state["pos"], 2)

    def test_parse_unary_not_operator(self):
        """Test parsing logical not operator."""
        tokens = [
            _make_token("NOT", "not", 1, 1),
            _make_token("IDENTIFIER", "flag", 1, 5),
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        with patch("._parse_atom_package._parse_atom_src._parse_atom") as mock_parse_atom:
            mock_parse_atom.return_value = {
                "type": "IDENTIFIER",
                "value": "flag",
                "children": [],
                "line": 1,
                "column": 5
            }
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "not")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(parser_state["pos"], 2)

    def test_parse_unary_bitwise_not_operator(self):
        """Test parsing bitwise not operator."""
        tokens = [
            _make_token("BITWISE_NOT", "~", 1, 1),
            _make_token("IDENTIFIER", "mask", 1, 2),
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        with patch("._parse_atom_package._parse_atom_src._parse_atom") as mock_parse_atom:
            mock_parse_atom.return_value = {
                "type": "IDENTIFIER",
                "value": "mask",
                "children": [],
                "line": 1,
                "column": 2
            }
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "~")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(parser_state["pos"], 2)

    def test_parse_unary_nested_operators(self):
        """Test parsing nested unary operators (e.g., --x)."""
        tokens = [
            _make_token("MINUS", "-", 1, 1),
            _make_token("MINUS", "-", 1, 2),
            _make_token("IDENTIFIER", "x", 1, 3),
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        with patch("._parse_atom_package._parse_atom_src._parse_atom") as mock_parse_atom:
            mock_parse_atom.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 3
            }
            
            result = _parse_unary(parser_state)
            
            # Outer unary op
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            
            # Inner unary op
            inner = result["children"][0]
            self.assertEqual(inner["type"], "UNARY_OP")
            self.assertEqual(inner["value"], "-")
            self.assertEqual(inner["line"], 1)
            self.assertEqual(inner["column"], 2)
            self.assertEqual(len(inner["children"]), 1)
            
            # Atom
            self.assertEqual(inner["children"][0]["type"], "IDENTIFIER")
            self.assertEqual(parser_state["pos"], 3)

    def test_parse_unary_atom_direct(self):
        """Test parsing atomic expression (no unary operator)."""
        tokens = [
            _make_token("IDENTIFIER", "x", 1, 1),
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        expected_atom = {
            "type": "IDENTIFIER",
            "value": "x",
            "children": [],
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_atom_package._parse_atom_src._parse_atom") as mock_parse_atom:
            mock_parse_atom.return_value = expected_atom
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result, expected_atom)
            mock_parse_atom.assert_called_once_with(parser_state)

    def test_parse_unary_empty_tokens(self):
        """Test parsing with empty token list (EOF)."""
        parser_state = _make_parser_state([], pos=0)
        
        result = _parse_unary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "unexpected_eof")
        self.assertEqual(parser_state["error"], "Unexpected end of input")
        self.assertEqual(parser_state["pos"], 0)

    def test_parse_unary_pos_at_end(self):
        """Test parsing when position is already at end of tokens."""
        tokens = [
            _make_token("IDENTIFIER", "x", 1, 1),
        ]
        parser_state = _make_parser_state(tokens, pos=1)
        
        result = _parse_unary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "unexpected_eof")
        self.assertEqual(parser_state["error"], "Unexpected end of input")

    def test_parse_unary_preserves_error_state(self):
        """Test that error state is properly set on EOF."""
        parser_state = _make_parser_state([], pos=0)
        
        result = _parse_unary(parser_state)
        
        self.assertIn("error", parser_state)
        self.assertEqual(parser_state["error"], "Unexpected end of input")
        self.assertEqual(result["type"], "ERROR")

    def test_parse_unary_literal_atom(self):
        """Test parsing literal as atomic expression."""
        tokens = [
            _make_token("LITERAL", "42", 1, 1),
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        expected_atom = {
            "type": "LITERAL",
            "value": "42",
            "children": [],
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_atom_package._parse_atom_src._parse_atom") as mock_parse_atom:
            mock_parse_atom.return_value = expected_atom
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "LITERAL")
            self.assertEqual(result["value"], "42")

    def test_parse_unary_complex_nested(self):
        """Test complex nested unary expression (e.g., -+~x)."""
        tokens = [
            _make_token("MINUS", "-", 1, 1),
            _make_token("PLUS", "+", 1, 2),
            _make_token("BITWISE_NOT", "~", 1, 3),
            _make_token("IDENTIFIER", "x", 1, 4),
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        with patch("._parse_atom_package._parse_atom_src._parse_atom") as mock_parse_atom:
            mock_parse_atom.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 4
            }
            
            result = _parse_unary(parser_state)
            
            # Verify the chain: - ( + ( ~ x ) )
            self.assertEqual(result["value"], "-")
            self.assertEqual(result["children"][0]["value"], "+")
            self.assertEqual(result["children"][0]["children"][0]["value"], "~")
            self.assertEqual(result["children"][0]["children"][0]["children"][0]["type"], "IDENTIFIER")
            self.assertEqual(parser_state["pos"], 4)


if __name__ == "__main__":
    unittest.main()
