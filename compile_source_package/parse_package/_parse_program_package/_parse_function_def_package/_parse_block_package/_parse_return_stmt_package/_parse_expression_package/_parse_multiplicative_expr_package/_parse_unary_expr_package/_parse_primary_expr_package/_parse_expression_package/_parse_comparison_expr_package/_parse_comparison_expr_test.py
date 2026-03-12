#!/usr/bin/env python3
"""Unit tests for _parse_comparison_expr function."""

import unittest
from typing import Dict, Any, List

# Relative imports from the same package
from ._parse_comparison_expr_src import _parse_comparison_expr


class TestParseComparisonExpr(unittest.TestCase):
    """Test cases for _parse_comparison_expr function."""

    def test_single_less_than_comparison(self):
        """Test parsing a single < comparison expression."""
        tokens: List[Dict[str, Any]] = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "<", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        ]
        parser_state: Dict[str, Any] = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "<")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(parser_state["pos"], 3)

    def test_single_equal_comparison(self):
        """Test parsing a single == comparison expression."""
        tokens: List[Dict[str, Any]] = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "==", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 6}
        ]
        parser_state: Dict[str, Any] = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "==")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(parser_state["pos"], 3)

    def test_single_not_equal_comparison(self):
        """Test parsing a single != comparison expression."""
        tokens: List[Dict[str, Any]] = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "!=", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
        ]
        parser_state: Dict[str, Any] = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "!=")
        self.assertEqual(len(result["children"]), 2)

    def test_single_greater_than_comparison(self):
        """Test parsing a single > comparison expression."""
        tokens: List[Dict[str, Any]] = [
            {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 5},
            {"type": "OPERATOR", "value": ">", "line": 2, "column": 7},
            {"type": "IDENTIFIER", "value": "y", "line": 2, "column": 9}
        ]
        parser_state: Dict[str, Any] = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], ">")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 7)

    def test_single_less_equal_comparison(self):
        """Test parsing a single <= comparison expression."""
        tokens: List[Dict[str, Any]] = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "<=", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
        ]
        parser_state: Dict[str, Any] = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "<=")

    def test_single_greater_equal_comparison(self):
        """Test parsing a single >= comparison expression."""
        tokens: List[Dict[str, Any]] = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": ">=", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 6}
        ]
        parser_state: Dict[str, Any] = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], ">=")

    def test_chained_comparisons_left_associative(self):
        """Test parsing chained comparisons with left associativity: a < b < c."""
        tokens: List[Dict[str, Any]] = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "<", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            {"type": "OPERATOR", "value": "<", "line": 1, "column": 7},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
        ]
        parser_state: Dict[str, Any] = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        result = _parse_comparison_expr(parser_state)
        
        # Should be left associative: ((a < b) < c)
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "<")
        self.assertEqual(len(result["children"]), 2)
        # Left child should be another BINARY_OP (a < b)
        left_child = result["children"][0]
        self.assertEqual(left_child["type"], "BINARY_OP")
        self.assertEqual(left_child["value"], "<")
        # Right child should be identifier c
        right_child = result["children"][1]
        self.assertEqual(right_child["type"], "IDENTIFIER")
        self.assertEqual(right_child["value"], "c")
        self.assertEqual(parser_state["pos"], 5)

    def test_mixed_comparison_operators(self):
        """Test parsing expressions with mixed comparison operators: a < b >= c."""
        tokens: List[Dict[str, Any]] = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "<", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            {"type": "OPERATOR", "value": ">=", "line": 1, "column": 7},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 10}
        ]
        parser_state: Dict[str, Any] = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        result = _parse_comparison_expr(parser_state)
        
        # Should be left associative: ((a < b) >= c)
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], ">=")
        self.assertEqual(result["column"], 7)
        left_child = result["children"][0]
        self.assertEqual(left_child["type"], "BINARY_OP")
        self.assertEqual(left_child["value"], "<")
        self.assertEqual(parser_state["pos"], 5)

    def test_no_comparison_operator(self):
        """Test parsing expression without comparison operator (just additive expr)."""
        tokens: List[Dict[str, Any]] = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        ]
        parser_state: Dict[str, Any] = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        result = _parse_comparison_expr(parser_state)
        
        # Should return just the additive expression result
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "a")
        self.assertEqual(parser_state["pos"], 1)

    def test_comparison_with_number_literal(self):
        """Test parsing comparison with number literal: x > 5."""
        tokens: List[Dict[str, Any]] = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": ">", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "5", "line": 1, "column": 5}
        ]
        parser_state: Dict[str, Any] = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], ">")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][1]["type"], "NUMBER")
        self.assertEqual(result["children"][1]["value"], "5")

    def test_three_chained_comparisons(self):
        """Test parsing three chained comparisons: a < b <= c < d."""
        tokens: List[Dict[str, Any]] = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "<", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            {"type": "OPERATOR", "value": "<=", "line": 1, "column": 7},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 10},
            {"type": "OPERATOR", "value": "<", "line": 1, "column": 12},
            {"type": "IDENTIFIER", "value": "d", "line": 1, "column": 14}
        ]
        parser_state: Dict[str, Any] = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        result = _parse_comparison_expr(parser_state)
        
        # Should be left associative: (((a < b) <= c) < d)
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "<")
        self.assertEqual(result["column"], 12)
        # Left child should be ((a < b) <= c)
        left_child = result["children"][0]
        self.assertEqual(left_child["type"], "BINARY_OP")
        self.assertEqual(left_child["value"], "<=")
        self.assertEqual(parser_state["pos"], 7)

    def test_empty_tokens_raises_error(self):
        """Test that empty tokens list raises SyntaxError."""
        tokens: List[Dict[str, Any]] = []
        parser_state: Dict[str, Any] = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_comparison_expr(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_operator_at_end_raises_error(self):
        """Test that comparison operator at end without right operand raises SyntaxError."""
        tokens: List[Dict[str, Any]] = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "<", "line": 1, "column": 3}
        ]
        parser_state: Dict[str, Any] = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_comparison_expr(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_non_operator_token_stops_parsing(self):
        """Test that non-operator token stops comparison parsing."""
        tokens: List[Dict[str, Any]] = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        ]
        parser_state: Dict[str, Any] = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        result = _parse_comparison_expr(parser_state)
        
        # Should return just the first additive expression
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "a")
        self.assertEqual(parser_state["pos"], 1)

    def test_wrong_token_type_stops_parsing(self):
        """Test that OPERATOR token with non-comparison value stops parsing."""
        tokens: List[Dict[str, Any]] = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "KEYWORD", "value": "<", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        ]
        parser_state: Dict[str, Any] = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        result = _parse_comparison_expr(parser_state)
        
        # Should return just the first additive expression (type must be OPERATOR)
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "a")
        self.assertEqual(parser_state["pos"], 1)

    def test_position_advancement_correct(self):
        """Test that parser position is correctly advanced through parsing."""
        tokens: List[Dict[str, Any]] = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "==", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 6},
            {"type": "OPERATOR", "value": "+", "line": 1, "column": 8}
        ]
        parser_state: Dict[str, Any] = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "==")
        self.assertEqual(parser_state["pos"], 3)

    def test_line_column_from_operator_token(self):
        """Test that line and column come from operator token."""
        tokens: List[Dict[str, Any]] = [
            {"type": "IDENTIFIER", "value": "a", "line": 5, "column": 10},
            {"type": "OPERATOR", "value": "!=", "line": 5, "column": 12},
            {"type": "IDENTIFIER", "value": "b", "line": 5, "column": 15}
        ]
        parser_state: Dict[str, Any] = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 12)


if __name__ == "__main__":
    unittest.main()
