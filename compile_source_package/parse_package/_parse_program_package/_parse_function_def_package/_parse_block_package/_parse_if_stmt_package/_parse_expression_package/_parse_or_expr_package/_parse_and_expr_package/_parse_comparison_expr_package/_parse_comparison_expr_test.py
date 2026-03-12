#!/usr/bin/env python3
"""
Unit tests for _parse_comparison_expr function.
"""

import unittest
from unittest.mock import patch
from typing import Dict, Any

# Import using relative path from the package structure
from ._parse_comparison_expr_src import _parse_comparison_expr


class TestParseComparisonExpr(unittest.TestCase):
    """Test cases for _parse_comparison_expr function."""
    
    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dictionary."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }
    
    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        """Helper to create a parser state dictionary."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }
    
    @patch('._parse_comparison_expr_src._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_single_less_than(self, mock_additive):
        """Test parsing a single less-than comparison: a < b"""
        left_node = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_node = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        
        mock_additive.side_effect = [left_node, right_node]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "<", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "<")
        self.assertEqual(result["left"], left_node)
        self.assertEqual(result["right"], right_node)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        
        self.assertEqual(parser_state["pos"], 3)
        self.assertEqual(mock_additive.call_count, 2)
    
    @patch('._parse_comparison_expr_src._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_single_greater_than(self, mock_additive):
        """Test parsing a single greater-than comparison: a > b"""
        left_node = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_node = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        
        mock_additive.side_effect = [left_node, right_node]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", ">", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], ">")
    
    @patch('._parse_comparison_expr_src._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_single_less_equal(self, mock_additive):
        """Test parsing less-than-or-equal: a <= b"""
        left_node = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_node = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        
        mock_additive.side_effect = [left_node, right_node]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "<=", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "<=")
    
    @patch('._parse_comparison_expr_src._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_single_greater_equal(self, mock_additive):
        """Test parsing greater-than-or-equal: a >= b"""
        left_node = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_node = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        
        mock_additive.side_effect = [left_node, right_node]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", ">=", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], ">=")
    
    @patch('._parse_comparison_expr_src._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_single_equal(self, mock_additive):
        """Test parsing equality: a == b"""
        left_node = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_node = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        
        mock_additive.side_effect = [left_node, right_node]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "==", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "==")
    
    @patch('._parse_comparison_expr_src._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_single_not_equal(self, mock_additive):
        """Test parsing inequality: a != b"""
        left_node = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_node = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        
        mock_additive.side_effect = [left_node, right_node]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "!=", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "!=")
    
    @patch('._parse_comparison_expr_src._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_chained_comparisons_left_associative(self, mock_additive):
        """Test chained comparisons are left-associative: a < b < c"""
        left_node = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        middle_node = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        right_node = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
        
        mock_additive.side_effect = [left_node, middle_node, right_node]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "<", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
            self._create_token("OPERATOR", "<", 1, 7),
            self._create_token("IDENTIFIER", "c", 1, 9)
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "<")
        
        left_comparison = result["left"]
        self.assertEqual(left_comparison["type"], "BINARY_OP")
        self.assertEqual(left_comparison["operator"], "<")
        self.assertEqual(left_comparison["left"], left_node)
        self.assertEqual(left_comparison["right"], middle_node)
        
        self.assertEqual(result["right"], right_node)
        self.assertEqual(parser_state["pos"], 5)
    
    @patch('._parse_comparison_expr_src._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_no_comparison_operator(self, mock_additive):
        """Test when there's no comparison operator, just returns the additive expression"""
        left_node = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        
        mock_additive.return_value = left_node
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1)
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result, left_node)
        mock_additive.assert_called_once()
        self.assertEqual(parser_state["pos"], 1)
    
    @patch('._parse_comparison_expr_src._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_mixed_comparison_operators(self, mock_additive):
        """Test mixed comparison operators: a < b >= c"""
        left_node = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        middle_node = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        right_node = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 10}
        
        mock_additive.side_effect = [left_node, middle_node, right_node]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "<", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
            self._create_token("OPERATOR", ">=", 1, 8),
            self._create_token("IDENTIFIER", "c", 1, 10)
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], ">=")
        
        left_comparison = result["left"]
        self.assertEqual(left_comparison["type"], "BINARY_OP")
        self.assertEqual(left_comparison["operator"], "<")
        
        self.assertEqual(mock_additive.call_count, 3)
    
    @patch('._parse_comparison_expr_src._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_comparison_with_non_operator_token(self, mock_additive):
        """Test that non-operator tokens stop the comparison loop"""
        left_node = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_node = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        
        mock_additive.side_effect = [left_node, right_node]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "<", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
            self._create_token("KEYWORD", "and", 1, 7)
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "<")
        self.assertEqual(result["right"], right_node)
        self.assertEqual(parser_state["pos"], 3)
    
    @patch('._parse_comparison_expr_src._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_position_tracking(self, mock_additive):
        """Test that parser position is correctly tracked"""
        left_node = {"type": "NUMBER", "value": 1, "line": 1, "column": 1}
        right_node = {"type": "NUMBER", "value": 2, "line": 1, "column": 5}
        
        mock_additive.side_effect = [left_node, right_node]
        
        tokens = [
            self._create_token("NUMBER", "1", 1, 1),
            self._create_token("OPERATOR", "<", 1, 3),
            self._create_token("NUMBER", "2", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        self.assertEqual(parser_state["pos"], 3)
    
    @patch('._parse_comparison_expr_src._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_empty_tokens(self, mock_additive):
        """Test with empty tokens list"""
        left_node = {"type": "EMPTY", "value": None}
        mock_additive.return_value = left_node
        
        tokens = []
        parser_state = self._create_parser_state(tokens, 0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result, left_node)
        self.assertEqual(parser_state["pos"], 0)
    
    @patch('._parse_comparison_expr_src._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_complex_expression_tree(self, mock_additive):
        """Test that complex expression trees are built correctly"""
        left_expr = {
            "type": "BINARY_OP",
            "operator": "+",
            "left": {"type": "IDENTIFIER", "value": "a"},
            "right": {"type": "IDENTIFIER", "value": "b"}
        }
        right_expr = {
            "type": "BINARY_OP",
            "operator": "-",
            "left": {"type": "IDENTIFIER", "value": "c"},
            "right": {"type": "IDENTIFIER", "value": "d"}
        }
        
        mock_additive.side_effect = [left_expr, right_expr]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "+", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
            self._create_token("OPERATOR", "<", 1, 7),
            self._create_token("IDENTIFIER", "c", 1, 9),
            self._create_token("OPERATOR", "-", 1, 11),
            self._create_token("IDENTIFIER", "d", 1, 13)
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "<")
        self.assertEqual(result["left"], left_expr)
        self.assertEqual(result["right"], right_expr)
    
    @patch('._parse_comparison_expr_src._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_operator_type_check(self, mock_additive):
        """Test that only OPERATOR type tokens are considered"""
        left_node = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_node = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        
        mock_additive.side_effect = [left_node, right_node]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            {
                "type": "SYMBOL",
                "value": "<",
                "line": 1,
                "column": 3
            },
            self._create_token("IDENTIFIER", "b", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result, left_node)
        mock_additive.assert_called_once()
    
    @patch('._parse_comparison_expr_src._parse_additive_expr')
    def test_three_way_chain(self, mock_additive):
        """Test three-way chained comparison: a < b == c > d"""
        nodes = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9},
            {"type": "IDENTIFIER", "value": "d", "line": 1, "column": 13}
        ]
        
        mock_additive.side_effect = nodes
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "<", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
            self._create_token("OPERATOR", "==", 1, 7),
            self._create_token("IDENTIFIER", "c", 1, 9),
            self._create_token("OPERATOR", ">", 1, 11),
            self._create_token("IDENTIFIER", "d", 1, 13)
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["operator"], ">")
        self.assertEqual(result["right"], nodes[3])
        
        second_level = result["left"]
        self.assertEqual(second_level["operator"], "==")
        self.assertEqual(second_level["right"], nodes[2])
        
        third_level = second_level["left"]
        self.assertEqual(third_level["operator"], "<")
        self.assertEqual(third_level["left"], nodes[0])
        self.assertEqual(third_level["right"], nodes[1])
        
        self.assertEqual(mock_additive.call_count, 4)
    
    @patch('._parse_comparison_expr_src._parse_additive_expr')
    def test_filename_preserved(self, mock_additive):
        """Test that filename in parser_state is preserved"""
        left_node = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        right_node = {"type": "IDENTIFIER", "value": "y", "line": 2, "column": 3}
        
        mock_additive.side_effect = [left_node, right_node]
        
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("OPERATOR", "!=", 1, 3),
            self._create_token("IDENTIFIER", "y", 2, 3)
        ]
        parser_state = self._create_parser_state(tokens, 0, "my_script.py")
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(parser_state["filename"], "my_script.py")


if __name__ == "__main__":
    unittest.main()
