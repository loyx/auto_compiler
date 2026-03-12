#!/usr/bin/env python3
"""
Unit tests for _parse_comparison function.
Tests comparison expression parsing (==, !=, <, >, <=, >=).
"""

import unittest
from unittest.mock import patch
from typing import Dict, Any

# Relative import from the same package
from ._parse_comparison_src import _parse_comparison


class TestParseComparison(unittest.TestCase):
    """Test cases for _parse_comparison function."""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast(self, ast_type: str, value: Any = None, children: list = None, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create an AST node dict."""
        ast = {
            "type": ast_type,
            "line": line,
            "column": column
        }
        if value is not None:
            ast["value"] = value
        if children is not None:
            ast["children"] = children
        return ast

    def test_parse_comparison_equals(self):
        """Test parsing equality comparison (==)."""
        left_ast = self._create_ast("IDENTIFIER", value="x")
        right_ast = self._create_ast("NUMBER", value=5)
        
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("COMPARE_OP", "==", 1, 3),
            self._create_token("NUMBER", "5", 1, 6)
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_comparison_src._parse_additive") as mock_additive:
            mock_additive.side_effect = [left_ast, right_ast]
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "==")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0], left_ast)
            self.assertEqual(result["children"][1], right_ast)
            self.assertEqual(parser_state["pos"], 3)

    def test_parse_comparison_not_equals(self):
        """Test parsing inequality comparison (!=)."""
        left_ast = self._create_ast("IDENTIFIER", value="a")
        right_ast = self._create_ast("IDENTIFIER", value="b")
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 2, 5),
            self._create_token("COMPARE_OP", "!=", 2, 7),
            self._create_token("IDENTIFIER", "b", 2, 10)
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_comparison_src._parse_additive") as mock_additive:
            mock_additive.side_effect = [left_ast, right_ast]
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "!=")
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 7)

    def test_parse_comparison_less_than(self):
        """Test parsing less than comparison (<)."""
        left_ast = self._create_ast("NUMBER", value=10)
        right_ast = self._create_ast("NUMBER", value=20)
        
        tokens = [
            self._create_token("NUMBER", "10", 3, 1),
            self._create_token("COMPARE_OP", "<", 3, 4),
            self._create_token("NUMBER", "20", 3, 6)
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_comparison_src._parse_additive") as mock_additive:
            mock_additive.side_effect = [left_ast, right_ast]
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "<")

    def test_parse_comparison_greater_than(self):
        """Test parsing greater than comparison (>)."""
        left_ast = self._create_ast("IDENTIFIER", value="y")
        right_ast = self._create_ast("NUMBER", value=0)
        
        tokens = [
            self._create_token("IDENTIFIER", "y", 4, 1),
            self._create_token("COMPARE_OP", ">", 4, 3),
            self._create_token("NUMBER", "0", 4, 5)
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_comparison_src._parse_additive") as mock_additive:
            mock_additive.side_effect = [left_ast, right_ast]
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], ">")

    def test_parse_comparison_less_than_or_equal(self):
        """Test parsing less than or equal comparison (<=)."""
        left_ast = self._create_ast("IDENTIFIER", value="count")
        right_ast = self._create_ast("IDENTIFIER", value="max_count")
        
        tokens = [
            self._create_token("IDENTIFIER", "count", 5, 1),
            self._create_token("COMPARE_OP", "<=", 5, 7),
            self._create_token("IDENTIFIER", "max_count", 5, 10)
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_comparison_src._parse_additive") as mock_additive:
            mock_additive.side_effect = [left_ast, right_ast]
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "<=")

    def test_parse_comparison_greater_than_or_equal(self):
        """Test parsing greater than or equal comparison (>=)."""
        left_ast = self._create_ast("NUMBER", value=100)
        right_ast = self._create_ast("NUMBER", value=50)
        
        tokens = [
            self._create_token("NUMBER", "100", 6, 1),
            self._create_token("COMPARE_OP", ">=", 6, 5),
            self._create_token("NUMBER", "50", 6, 8)
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_comparison_src._parse_additive") as mock_additive:
            mock_additive.side_effect = [left_ast, right_ast]
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], ">=")

    def test_parse_comparison_no_operator(self):
        """Test parsing expression without comparison operator."""
        left_ast = self._create_ast("IDENTIFIER", value="x")
        
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("NEWLINE", "\n", 1, 2)
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_comparison_src._parse_additive") as mock_additive:
            mock_additive.return_value = left_ast
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result, left_ast)
            self.assertEqual(parser_state["pos"], 0)

    def test_parse_comparison_empty_tokens(self):
        """Test parsing with empty token list."""
        tokens = []
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        left_ast = self._create_ast("IDENTIFIER", value="empty")
        
        with patch("._parse_comparison_src._parse_additive") as mock_additive:
            mock_additive.return_value = left_ast
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result, left_ast)

    def test_parse_comparison_end_of_tokens(self):
        """Test parsing when tokens are exhausted after left operand."""
        left_ast = self._create_ast("NUMBER", value=42)
        
        tokens = [
            self._create_token("NUMBER", "42", 1, 1)
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_comparison_src._parse_additive") as mock_additive:
            mock_additive.return_value = left_ast
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result, left_ast)

    def test_parse_comparison_non_compare_op_token(self):
        """Test parsing when next token is not a comparison operator."""
        left_ast = self._create_ast("IDENTIFIER", value="x")
        
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("ARITH_OP", "+", 1, 3),
            self._create_token("NUMBER", "1", 1, 5)
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_comparison_src._parse_additive") as mock_additive:
            mock_additive.return_value = left_ast
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result, left_ast)
            self.assertEqual(parser_state["pos"], 0)

    def test_parse_comparison_missing_filename(self):
        """Test parsing when filename is not provided in parser_state."""
        left_ast = self._create_ast("IDENTIFIER", value="x")
        right_ast = self._create_ast("NUMBER", value=1)
        
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("COMPARE_OP", "==", 1, 3),
            self._create_token("NUMBER", "1", 1, 6)
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0
        }
        
        with patch("._parse_comparison_src._parse_additive") as mock_additive:
            mock_additive.side_effect = [left_ast, right_ast]
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "==")

    def test_parse_comparison_token_missing_type(self):
        """Test parsing when token doesn't have 'type' field."""
        left_ast = self._create_ast("IDENTIFIER", value="x")
        
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            {"value": "==", "line": 1, "column": 3},
            self._create_token("NUMBER", "1", 1, 6)
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_comparison_src._parse_additive") as mock_additive:
            mock_additive.return_value = left_ast
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result, left_ast)

    def test_parse_comparison_token_missing_value(self):
        """Test parsing when token doesn't have 'value' field."""
        left_ast = self._create_ast("IDENTIFIER", value="x")
        
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            {"type": "COMPARE_OP", "line": 1, "column": 3},
            self._create_token("NUMBER", "1", 1, 6)
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_comparison_src._parse_additive") as mock_additive:
            mock_additive.return_value = left_ast
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result, left_ast)


if __name__ == "__main__":
    unittest.main()
