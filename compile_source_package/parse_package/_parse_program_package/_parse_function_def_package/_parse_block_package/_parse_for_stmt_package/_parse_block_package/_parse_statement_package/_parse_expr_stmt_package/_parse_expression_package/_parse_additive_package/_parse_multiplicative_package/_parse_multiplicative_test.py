# -*- coding: utf-8 -*-
"""Unit tests for _parse_multiplicative function."""

import unittest
from unittest.mock import patch

from ._parse_multiplicative_src import _parse_multiplicative


class TestParseMultiplicative(unittest.TestCase):
    """Test cases for _parse_multiplicative function."""

    def test_single_operand_no_operator(self):
        """Test parsing a single operand without any multiplicative operators."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        unary_result = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_multiplicative_src._parse_unary") as mock_unary:
            mock_unary.return_value = unary_result
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result, unary_result)
            self.assertEqual(parser_state["pos"], 1)
            mock_unary.assert_called_once()

    def test_multiplication_operator(self):
        """Test parsing expression with multiplication operator."""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "OP_MUL", "value": "*", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        left_operand = {
            "type": "IDENTIFIER",
            "value": "a",
            "line": 1,
            "column": 1
        }
        right_operand = {
            "type": "IDENTIFIER",
            "value": "b",
            "line": 1,
            "column": 5
        }
        
        with patch("._parse_multiplicative_src._parse_unary") as mock_unary:
            mock_unary.side_effect = [left_operand, right_operand, right_operand]
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "*")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0], left_operand)
            self.assertEqual(result["children"][1], right_operand)
            self.assertEqual(parser_state["pos"], 3)

    def test_division_operator(self):
        """Test parsing expression with division operator."""
        tokens = [
            {"type": "NUMBER", "value": "10", "line": 1, "column": 1},
            {"type": "OP_DIV", "value": "/", "line": 1, "column": 4},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 6}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        left_operand = {
            "type": "NUMBER",
            "value": "10",
            "line": 1,
            "column": 1
        }
        right_operand = {
            "type": "NUMBER",
            "value": "2",
            "line": 1,
            "column": 6
        }
        
        with patch("._parse_multiplicative_src._parse_unary") as mock_unary:
            mock_unary.side_effect = [left_operand, right_operand, right_operand]
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "/")
            self.assertEqual(result["children"][0], left_operand)
            self.assertEqual(result["children"][1], right_operand)
            self.assertEqual(parser_state["pos"], 3)

    def test_modulo_operator(self):
        """Test parsing expression with modulo operator."""
        tokens = [
            {"type": "NUMBER", "value": "10", "line": 1, "column": 1},
            {"type": "OP_MOD", "value": "%", "line": 1, "column": 4},
            {"type": "NUMBER", "value": "3", "line": 1, "column": 6}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        left_operand = {
            "type": "NUMBER",
            "value": "10",
            "line": 1,
            "column": 1
        }
        right_operand = {
            "type": "NUMBER",
            "value": "3",
            "line": 1,
            "column": 6
        }
        
        with patch("._parse_multiplicative_src._parse_unary") as mock_unary:
            mock_unary.side_effect = [left_operand, right_operand, right_operand]
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "%")
            self.assertEqual(result["children"][0], left_operand)
            self.assertEqual(result["children"][1], right_operand)
            self.assertEqual(parser_state["pos"], 3)

    def test_chained_multiplicative_operators(self):
        """Test parsing chained multiplicative operators (left-associative)."""
        tokens = [
            {"type": "NUMBER", "value": "a", "line": 1, "column": 1},
            {"type": "OP_MUL", "value": "*", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "b", "line": 1, "column": 5},
            {"type": "OP_DIV", "value": "/", "line": 1, "column": 7},
            {"type": "NUMBER", "value": "c", "line": 1, "column": 9}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        operand_a = {"type": "NUMBER", "value": "a", "line": 1, "column": 1}
        operand_b = {"type": "NUMBER", "value": "b", "line": 1, "column": 5}
        operand_c = {"type": "NUMBER", "value": "c", "line": 1, "column": 9}
        
        with patch("._parse_multiplicative_src._parse_unary") as mock_unary:
            mock_unary.side_effect = [operand_a, operand_b, operand_c, operand_c]
            
            result = _parse_multiplicative(parser_state)
            
            # Should be left-associative: (a * b) / c
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "/")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 7)
            
            # Left child should be (a * b)
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["value"], "*")
            self.assertEqual(left_child["children"][0], operand_a)
            self.assertEqual(left_child["children"][1], operand_b)
            
            # Right child should be c
            self.assertEqual(result["children"][1], operand_c)
            self.assertEqual(parser_state["pos"], 5)

    def test_mixed_operators(self):
        """Test parsing expression with mixed *, /, % operators."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "OP_MUL", "value": "*", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 5},
            {"type": "OP_MOD", "value": "%", "line": 1, "column": 7},
            {"type": "IDENTIFIER", "value": "z", "line": 1, "column": 9}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        operand_x = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        operand_y = {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 5}
        operand_z = {"type": "IDENTIFIER", "value": "z", "line": 1, "column": 9}
        
        with patch("._parse_multiplicative_src._parse_unary") as mock_unary:
            mock_unary.side_effect = [operand_x, operand_y, operand_z, operand_z]
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "%")
            self.assertEqual(result["children"][0]["value"], "*")
            self.assertEqual(parser_state["pos"], 5)

    def test_empty_tokens(self):
        """Test parsing with empty token list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        empty_result = {"type": "EMPTY", "value": None, "line": 0, "column": 0}
        
        with patch("._parse_multiplicative_src._parse_unary") as mock_unary:
            mock_unary.return_value = empty_result
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result, empty_result)
            self.assertEqual(parser_state["pos"], 0)

    def test_pos_at_end_of_tokens(self):
        """Test parsing when pos is already at end of tokens."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 1,  # Already at end
            "filename": "test.py"
        }
        
        unary_result = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        
        with patch("._parse_multiplicative_src._parse_unary") as mock_unary:
            mock_unary.return_value = unary_result
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result, unary_result)
            self.assertEqual(parser_state["pos"], 1)
            mock_unary.assert_called_once()

    def test_operator_followed_by_non_unary_token(self):
        """Test parsing when operator is followed by unexpected token."""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "OP_MUL", "value": "*", "line": 1, "column": 3},
            {"type": "OP_ADD", "value": "+", "line": 1, "column": 5}  # Not a valid unary start
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        left_operand = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        
        with patch("._parse_multiplicative_src._parse_unary") as mock_unary:
            mock_unary.side_effect = [left_operand, SyntaxError("Unexpected token")]
            
            with self.assertRaises(SyntaxError):
                _parse_multiplicative(parser_state)

    def test_preserves_operator_location(self):
        """Test that operator location (line, column) is preserved in AST."""
        tokens = [
            {"type": "NUMBER", "value": "5", "line": 10, "column": 5},
            {"type": "OP_MUL", "value": "*", "line": 10, "column": 7},
            {"type": "NUMBER", "value": "3", "line": 10, "column": 9}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        left_operand = {"type": "NUMBER", "value": "5", "line": 10, "column": 5}
        right_operand = {"type": "NUMBER", "value": "3", "line": 10, "column": 9}
        
        with patch("._parse_multiplicative_src._parse_unary") as mock_unary:
            mock_unary.side_effect = [left_operand, right_operand, right_operand]
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result["line"], 10)
            self.assertEqual(result["column"], 7)


if __name__ == "__main__":
    unittest.main()
