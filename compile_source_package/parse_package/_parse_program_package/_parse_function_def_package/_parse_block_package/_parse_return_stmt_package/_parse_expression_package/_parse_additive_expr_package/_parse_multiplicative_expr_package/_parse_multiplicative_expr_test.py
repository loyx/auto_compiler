#!/usr/bin/env python3
"""Unit tests for _parse_multiplicative_expr function."""

import unittest
from unittest.mock import patch
from typing import Dict, Any

# Relative import from the same package
from ._parse_multiplicative_expr_src import _parse_multiplicative_expr


Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


class TestParseMultiplicativeExpr(unittest.TestCase):
    """Test cases for _parse_multiplicative_expr function."""

    def test_single_unary_expr_no_operator(self):
        """Test parsing a single unary expression without multiplicative operators."""
        left_operand = {"type": "LITERAL", "value": 5, "line": 1, "column": 1}
        
        parser_state = {
            "tokens": [{"type": "NUMBER", "value": "5", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.return_value = left_operand
            
            result = _parse_multiplicative_expr(parser_state)
            
            self.assertEqual(result, left_operand)
            mock_unary.assert_called_once()

    def test_one_multiplication_operator(self):
        """Test parsing expression with one multiplication operator (a * b)."""
        left_operand = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_operand = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 3}
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "STAR", "value": "*", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        call_count = [0]
        def unary_side_effect(ps):
            if call_count[0] == 0:
                call_count[0] += 1
                return left_operand
            else:
                return right_operand
        
        with patch("._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.side_effect = unary_side_effect
            
            result = _parse_multiplicative_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "*")
            self.assertEqual(result["children"], [left_operand, right_operand])
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 2)
            self.assertEqual(mock_unary.call_count, 2)

    def test_multiple_operators_left_associative(self):
        """Test left-associative parsing (a * b / c)."""
        operand_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        operand_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 3}
        operand_c = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 5}
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "STAR", "value": "*", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 3},
                {"type": "SLASH", "value": "/", "line": 1, "column": 4},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        operands = [operand_a, operand_b, operand_c]
        call_count = [0]
        
        def unary_side_effect(ps):
            idx = min(call_count[0], len(operands) - 1)
            call_count[0] += 1
            return operands[idx]
        
        with patch("._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.side_effect = unary_side_effect
            
            result = _parse_multiplicative_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "/")
            self.assertEqual(result["children"][1], operand_c)
            
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["value"], "*")
            self.assertEqual(left_child["children"], [operand_a, operand_b])
            
            self.assertEqual(mock_unary.call_count, 3)

    def test_division_operator(self):
        """Test parsing division operator (a / b)."""
        left_operand = {"type": "LITERAL", "value": 10, "line": 1, "column": 1}
        right_operand = {"type": "LITERAL", "value": 2, "line": 1, "column": 3}
        
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "10", "line": 1, "column": 1},
                {"type": "SLASH", "value": "/", "line": 1, "column": 2},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        call_count = [0]
        def unary_side_effect(ps):
            if call_count[0] == 0:
                call_count[0] += 1
                return left_operand
            else:
                return right_operand
        
        with patch("._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.side_effect = unary_side_effect
            
            result = _parse_multiplicative_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "/")
            self.assertEqual(result["children"], [left_operand, right_operand])
            self.assertEqual(mock_unary.call_count, 2)

    def test_modulo_operator(self):
        """Test parsing modulo operator (a % b)."""
        left_operand = {"type": "LITERAL", "value": 10, "line": 1, "column": 1}
        right_operand = {"type": "LITERAL", "value": 3, "line": 1, "column": 3}
        
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "10", "line": 1, "column": 1},
                {"type": "PERCENT", "value": "%", "line": 1, "column": 2},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        call_count = [0]
        def unary_side_effect(ps):
            if call_count[0] == 0:
                call_count[0] += 1
                return left_operand
            else:
                return right_operand
        
        with patch("._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.side_effect = unary_side_effect
            
            result = _parse_multiplicative_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "%")
            self.assertEqual(result["children"], [left_operand, right_operand])
            self.assertEqual(mock_unary.call_count, 2)

    def test_empty_tokens(self):
        """Test parsing with empty token list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.return_value = {"type": "LITERAL", "value": 0}
            
            result = _parse_multiplicative_expr(parser_state)
            
            mock_unary.assert_called_once()
            self.assertEqual(result["type"], "LITERAL")

    def test_position_at_end(self):
        """Test when position is already at end of tokens."""
        parser_state = {
            "tokens": [{"type": "NUMBER", "value": "5"}],
            "pos": 1,
            "filename": "test.py"
        }
        
        with patch("._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.return_value = {"type": "LITERAL", "value": 5}
            
            result = _parse_multiplicative_expr(parser_state)
            
            mock_unary.assert_called_once()
            self.assertEqual(result["type"], "LITERAL")

    def test_mixed_operators(self):
        """Test parsing mixed multiplicative operators (a * b % c / d)."""
        operand_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        operand_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 3}
        operand_c = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 5}
        operand_d = {"type": "IDENTIFIER", "value": "d", "line": 1, "column": 7}
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "STAR", "value": "*", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 3},
                {"type": "PERCENT", "value": "%", "line": 1, "column": 4},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 5},
                {"type": "SLASH", "value": "/", "line": 1, "column": 6},
                {"type": "IDENTIFIER", "value": "d", "line": 1, "column": 7}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        operands = [operand_a, operand_b, operand_c, operand_d]
        call_count = [0]
        
        def unary_side_effect(ps):
            idx = min(call_count[0], len(operands) - 1)
            call_count[0] += 1
            return operands[idx]
        
        with patch("._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.side_effect = unary_side_effect
            
            result = _parse_multiplicative_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "/")
            self.assertEqual(result["children"][1], operand_d)
            
            mid_child = result["children"][0]
            self.assertEqual(mid_child["type"], "BINARY_OP")
            self.assertEqual(mid_child["value"], "%")
            self.assertEqual(mid_child["children"][1], operand_c)
            
            left_child = mid_child["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["value"], "*")
            self.assertEqual(left_child["children"], [operand_a, operand_b])
            
            self.assertEqual(mock_unary.call_count, 4)


if __name__ == "__main__":
    unittest.main()
