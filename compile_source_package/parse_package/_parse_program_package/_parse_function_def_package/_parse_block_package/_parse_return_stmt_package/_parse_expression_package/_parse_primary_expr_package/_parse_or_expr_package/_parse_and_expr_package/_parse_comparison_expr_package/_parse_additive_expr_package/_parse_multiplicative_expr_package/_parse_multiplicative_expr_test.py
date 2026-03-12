#!/usr/bin/env python3
"""
Unit tests for _parse_multiplicative_expr function.
"""

import unittest
from unittest.mock import patch

# Relative import for the function under test
from ._parse_multiplicative_expr_src import _parse_multiplicative_expr


class TestParseMultiplicativeExpr(unittest.TestCase):
    """Test cases for _parse_multiplicative_expr function."""
    
    def test_simple_multiplication(self):
        """Test parsing a simple multiplication expression: a * b"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "MUL", "value": "*", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with patch("._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.side_effect = [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            ]
            
            result = _parse_multiplicative_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "*")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
    
    def test_division_expression(self):
        """Test parsing a division expression: a / b"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "DIV", "value": "/", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with patch("._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.side_effect = [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            ]
            
            result = _parse_multiplicative_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "/")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
    
    def test_modulo_expression(self):
        """Test parsing a modulo expression: a % b"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "MOD", "value": "%", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with patch("._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.side_effect = [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            ]
            
            result = _parse_multiplicative_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "%")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
    
    def test_chained_operations_left_associative(self):
        """Test parsing chained multiplicative operations: a * b / c (left-associative)"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "MUL", "value": "*", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            {"type": "DIV", "value": "/", "line": 1, "column": 7},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with patch("._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.side_effect = [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9},
            ]
            
            result = _parse_multiplicative_expr(parser_state)
            
            # Should be left-associative: (a * b) / c
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "/")
            self.assertEqual(len(result["children"]), 2)
            # Left child should be the multiplication
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["value"], "*")
    
    def test_no_multiplicative_operator(self):
        """Test parsing expression without multiplicative operator"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        expected_ast = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        
        with patch("._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.return_value = expected_ast
            
            result = _parse_multiplicative_expr(parser_state)
            
            self.assertEqual(result, expected_ast)
            # Position should not change since no operator was consumed
            self.assertEqual(parser_state["pos"], 0)
    
    def test_empty_tokens(self):
        """Test parsing with empty token list"""
        tokens = []
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        expected_ast = {"type": "LITERAL", "value": None, "line": 0, "column": 0}
        
        with patch("._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.return_value = expected_ast
            
            result = _parse_multiplicative_expr(parser_state)
            
            self.assertEqual(result, expected_ast)
    
    def test_error_from_unary_expr_initial(self):
        """Test handling error from _parse_unary_expr on initial parse"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "MUL", "value": "*", "line": 1, "column": 3},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        error_ast = {"type": "ERROR", "value": "parse error", "line": 1, "column": 1}
        
        with patch("._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.return_value = error_ast
            parser_state["error"] = "parse error"
            
            result = _parse_multiplicative_expr(parser_state)
            
            self.assertEqual(result, error_ast)
    
    def test_error_from_unary_expr_right_operand(self):
        """Test handling error from _parse_unary_expr when parsing right operand"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "MUL", "value": "*", "line": 1, "column": 3},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        left_ast = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        error_ast = {"type": "ERROR", "value": "unexpected end", "line": 1, "column": 3}
        
        with patch("._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr") as mock_unary:
            # First call returns left operand, second call (for right operand) sets error
            mock_unary.side_effect = [left_ast, error_ast]
            parser_state["error"] = "unexpected end"
            
            result = _parse_multiplicative_expr(parser_state)
            
            # Should return left operand when error occurs
            self.assertEqual(result, left_ast)
    
    def test_mixed_operators(self):
        """Test parsing expression with mixed operators: a * b % c / d"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "MUL", "value": "*", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            {"type": "MOD", "value": "%", "line": 1, "column": 7},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9},
            {"type": "DIV", "value": "/", "line": 1, "column": 11},
            {"type": "IDENTIFIER", "value": "d", "line": 1, "column": 13},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with patch("._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.side_effect = [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9},
                {"type": "IDENTIFIER", "value": "d", "line": 1, "column": 13},
            ]
            
            result = _parse_multiplicative_expr(parser_state)
            
            # Should be left-associative: ((a * b) % c) / d
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "/")
            # Verify the nested structure
            middle = result["children"][0]
            self.assertEqual(middle["type"], "BINARY_OP")
            self.assertEqual(middle["value"], "%")
            leftmost = middle["children"][0]
            self.assertEqual(leftmost["type"], "BINARY_OP")
            self.assertEqual(leftmost["value"], "*")
    
    def test_position_updates_correctly(self):
        """Test that parser_state['pos'] is updated correctly"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "MUL", "value": "*", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with patch("._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.side_effect = [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            ]
            
            _parse_multiplicative_expr(parser_state)
            
            # After parsing: pos 0 -> parse unary -> consume MUL (pos=1) -> parse unary
            self.assertEqual(parser_state["pos"], 1)
    
    def test_ast_node_contains_correct_metadata(self):
        """Test that BINARY_OP node contains correct line and column metadata"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 2, "column": 5},
            {"type": "DIV", "value": "/", "line": 2, "column": 7},
            {"type": "IDENTIFIER", "value": "b", "line": 2, "column": 9},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with patch("._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.side_effect = [
                {"type": "IDENTIFIER", "value": "a", "line": 2, "column": 5},
                {"type": "IDENTIFIER", "value": "b", "line": 2, "column": 9},
            ]
            
            result = _parse_multiplicative_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "/")
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 7)
    
    def test_multiple_same_operators(self):
        """Test parsing expression with multiple same operators: a * b * c"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "MUL", "value": "*", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            {"type": "MUL", "value": "*", "line": 1, "column": 7},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with patch("._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.side_effect = [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9},
            ]
            
            result = _parse_multiplicative_expr(parser_state)
            
            # Should be left-associative: (a * b) * c
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "*")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 7)
            # Verify nested structure
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["value"], "*")
            self.assertEqual(left_child["line"], 1)
            self.assertEqual(left_child["column"], 3)


if __name__ == "__main__":
    unittest.main()
