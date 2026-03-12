#!/usr/bin/env python3
"""Unit tests for _parse_comparison_expr function."""

import unittest
from unittest.mock import patch, MagicMock
import sys

# Mock the entire dependency chain before importing
sys.modules['._parse_additive_expr_package._parse_additive_expr_src'] = MagicMock()

# Relative import for the function under test
from ._parse_comparison_expr_src import _parse_comparison_expr


class TestParseComparisonExpr(unittest.TestCase):
    """Test cases for _parse_comparison_expr function."""
    
    def _create_mock_ast(self, value="mock_value", node_type="IDENTIFIER", line=1, column=1):
        """Helper to create mock AST nodes."""
        return {
            "type": node_type,
            "value": value,
            "children": [],
            "line": line,
            "column": column
        }
    
    def test_equality_operator(self):
        """Test parsing == comparison operator."""
        left_ast = self._create_mock_ast("left")
        right_ast = self._create_mock_ast("right")
        
        tokens = [
            {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
            {"type": "EQ", "value": "==", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr") as mock_additive:
            mock_additive.side_effect = [left_ast, right_ast]
            result = _parse_comparison_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "==")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0], left_ast)
            self.assertEqual(result["children"][1], right_ast)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(parser_state["pos"], 2)
    
    def test_inequality_operator(self):
        """Test parsing != comparison operator."""
        left_ast = self._create_mock_ast("a")
        right_ast = self._create_mock_ast("b")
        
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 2, "column": 5},
            {"type": "NE", "value": "!=", "line": 2, "column": 7},
            {"type": "IDENTIFIER", "value": "b", "line": 2, "column": 9}
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr") as mock_additive:
            mock_additive.side_effect = [left_ast, right_ast]
            result = _parse_comparison_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "!=")
            self.assertEqual(parser_state["pos"], 2)
    
    def test_less_than_operator(self):
        """Test parsing < comparison operator."""
        left_ast = self._create_mock_ast("x")
        right_ast = self._create_mock_ast("y")
        
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 3, "column": 1},
            {"type": "LT", "value": "<", "line": 3, "column": 3},
            {"type": "IDENTIFIER", "value": "y", "line": 3, "column": 5}
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr") as mock_additive:
            mock_additive.side_effect = [left_ast, right_ast]
            result = _parse_comparison_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "<")
            self.assertEqual(parser_state["pos"], 2)
    
    def test_greater_than_operator(self):
        """Test parsing > comparison operator."""
        left_ast = self._create_mock_ast("5")
        right_ast = self._create_mock_ast("10")
        
        tokens = [
            {"type": "NUMBER", "value": "5", "line": 4, "column": 1},
            {"type": "GT", "value": ">", "line": 4, "column": 3},
            {"type": "NUMBER", "value": "10", "line": 4, "column": 5}
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr") as mock_additive:
            mock_additive.side_effect = [left_ast, right_ast]
            result = _parse_comparison_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], ">")
            self.assertEqual(parser_state["pos"], 2)
    
    def test_less_than_or_equal_operator(self):
        """Test parsing <= comparison operator."""
        left_ast = self._create_mock_ast("age")
        right_ast = self._create_mock_ast("18")
        
        tokens = [
            {"type": "IDENTIFIER", "value": "age", "line": 5, "column": 1},
            {"type": "LE", "value": "<=", "line": 5, "column": 5},
            {"type": "NUMBER", "value": "18", "line": 5, "column": 8}
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr") as mock_additive:
            mock_additive.side_effect = [left_ast, right_ast]
            result = _parse_comparison_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "<=")
            self.assertEqual(parser_state["pos"], 2)
    
    def test_greater_than_or_equal_operator(self):
        """Test parsing >= comparison operator."""
        left_ast = self._create_mock_ast("score")
        right_ast = self._create_mock_ast("60")
        
        tokens = [
            {"type": "IDENTIFIER", "value": "score", "line": 6, "column": 1},
            {"type": "GE", "value": ">=", "line": 6, "column": 7},
            {"type": "NUMBER", "value": "60", "line": 6, "column": 10}
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr") as mock_additive:
            mock_additive.side_effect = [left_ast, right_ast]
            result = _parse_comparison_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], ">=")
            self.assertEqual(parser_state["pos"], 2)
    
    def test_no_comparison_operator(self):
        """Test when no comparison operator is present - returns left operand."""
        left_ast = self._create_mock_ast("only_left")
        
        tokens = [
            {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr") as mock_additive:
            mock_additive.return_value = left_ast
            result = _parse_comparison_expr(parser_state)
            
            self.assertEqual(result, left_ast)
            self.assertEqual(parser_state["pos"], 0)
    
    def test_empty_tokens(self):
        """Test with empty token list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        left_ast = self._create_mock_ast("empty")
        
        with patch("._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr") as mock_additive:
            mock_additive.return_value = left_ast
            result = _parse_comparison_expr(parser_state)
            
            self.assertEqual(result, left_ast)
    
    def test_position_at_end_of_tokens(self):
        """Test when position is at end of tokens."""
        tokens = [
            {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.py"
        }
        
        left_ast = self._create_mock_ast("end")
        
        with patch("._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr") as mock_additive:
            mock_additive.return_value = left_ast
            result = _parse_comparison_expr(parser_state)
            
            self.assertEqual(result, left_ast)
    
    def test_non_comparison_operator_token(self):
        """Test when current token is not a comparison operator."""
        left_ast = self._create_mock_ast("left")
        
        tokens = [
            {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
            {"type": "PLUS", "value": "+", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr") as mock_additive:
            mock_additive.return_value = left_ast
            result = _parse_comparison_expr(parser_state)
            
            self.assertEqual(result, left_ast)
            self.assertEqual(parser_state["pos"], 0)
    
    def test_line_column_preserved_from_operator(self):
        """Test that line and column from operator token are preserved in result."""
        left_ast = self._create_mock_ast("left")
        right_ast = self._create_mock_ast("right")
        
        tokens = [
            {"type": "NUMBER", "value": "1", "line": 10, "column": 5},
            {"type": "LT", "value": "<", "line": 10, "column": 7},
            {"type": "NUMBER", "value": "2", "line": 10, "column": 9}
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr") as mock_additive:
            mock_additive.side_effect = [left_ast, right_ast]
            result = _parse_comparison_expr(parser_state)
            
            self.assertEqual(result["line"], 10)
            self.assertEqual(result["column"], 7)
    
    def test_all_comparison_operators_parametrized(self):
        """Test all comparison operators in a parametrized fashion."""
        operators = [
            ("EQ", "=="),
            ("NE", "!="),
            ("LT", "<"),
            ("GT", ">"),
            ("LE", "<="),
            ("GE", ">=")
        ]
        
        for op_type, op_value in operators:
            with self.subTest(operator=op_value):
                left_ast = self._create_mock_ast("left")
                right_ast = self._create_mock_ast("right")
                
                tokens = [
                    {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                    {"type": op_type, "value": op_value, "line": 1, "column": 3},
                    {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
                ]
                
                parser_state = {
                    "tokens": tokens,
                    "pos": 0,
                    "filename": "test.py"
                }
                
                with patch("._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr") as mock_additive:
                    mock_additive.side_effect = [left_ast, right_ast]
                    result = _parse_comparison_expr(parser_state)
                    
                    self.assertEqual(result["type"], "BINARY_OP")
                    self.assertEqual(result["value"], op_value)
                    self.assertEqual(len(result["children"]), 2)
                    self.assertEqual(parser_state["pos"], 2)


if __name__ == "__main__":
    unittest.main()
