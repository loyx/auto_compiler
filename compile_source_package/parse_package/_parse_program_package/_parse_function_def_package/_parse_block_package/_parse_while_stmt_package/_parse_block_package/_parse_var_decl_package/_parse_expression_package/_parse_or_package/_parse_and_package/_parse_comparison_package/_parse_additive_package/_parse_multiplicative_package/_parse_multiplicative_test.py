#!/usr/bin/env python3
"""
Unit tests for _parse_multiplicative function.
Tests multiplicative expression parsing (* / % operators) with left-associativity.
"""

import unittest
from unittest.mock import patch
from typing import Any, Dict

# Relative import from the same package
from ._parse_multiplicative_src import _parse_multiplicative


class TestParseMultiplicative(unittest.TestCase):
    """Test cases for _parse_multiplicative function."""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.txt") -> Dict[str, Any]:
        """Helper to create a parser state dict."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_ast_node(self, node_type: str, value: Any = None, children: list = None, 
                         line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create an AST node dict."""
        return {
            "type": node_type,
            "value": value,
            "children": children if children is not None else [],
            "line": line,
            "column": column
        }

    @patch('_parse_multiplicative_package._parse_multiplicative_src._parse_unary')
    @patch('_parse_multiplicative_package._parse_multiplicative_src._consume_token')
    def test_single_multiplication(self, mock_consume_token, mock_parse_unary):
        """Test parsing a single multiplication expression: a * b"""
        # Setup: tokens for "a * b"
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("STAR", "*", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
            self._create_token("EOF", "", 1, 6)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Mock _parse_unary to return left operand then right operand
        left_operand = self._create_ast_node("IDENTIFIER", "a", line=1, column=1)
        right_operand = self._create_ast_node("IDENTIFIER", "b", line=1, column=5)
        
        mock_parse_unary.side_effect = [
            (left_operand, self._create_parser_state(tokens, pos=1)),  # First call for left
            (right_operand, self._create_parser_state(tokens, pos=3))   # Second call for right
        ]
        
        # Mock _consume_token to consume STAR
        mock_consume_token.return_value = (
            self._create_token("STAR", "*", 1, 3),
            self._create_parser_state(tokens, pos=2)
        )
        
        # Execute
        result_ast, result_state = _parse_multiplicative(parser_state)
        
        # Verify
        self.assertEqual(result_ast["type"], "BINARY_OP")
        self.assertEqual(result_ast["value"], "*")
        self.assertEqual(len(result_ast["children"]), 2)
        self.assertEqual(result_ast["line"], 1)
        self.assertEqual(result_ast["column"], 3)
        
        # Verify left-associativity structure
        self.assertEqual(result_ast["children"][0]["type"], "IDENTIFIER")
        self.assertEqual(result_ast["children"][0]["value"], "a")
        self.assertEqual(result_ast["children"][1]["type"], "IDENTIFIER")
        self.assertEqual(result_ast["children"][1]["value"], "b")
        
        # Verify mocks were called correctly
        self.assertEqual(mock_parse_unary.call_count, 2)
        self.assertEqual(mock_consume_token.call_count, 1)
        mock_consume_token.assert_called_with(self._create_parser_state(tokens, pos=1), "STAR")

    @patch('_parse_multiplicative_package._parse_multiplicative_src._parse_unary')
    @patch('_parse_multiplicative_package._parse_multiplicative_src._consume_token')
    def test_left_associativity(self, mock_consume_token, mock_parse_unary):
        """Test left-associativity: a * b / c should be ((a * b) / c)"""
        # Setup: tokens for "a * b / c"
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("STAR", "*", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
            self._create_token("SLASH", "/", 1, 7),
            self._create_token("IDENTIFIER", "c", 1, 9),
            self._create_token("EOF", "", 1, 10)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Mock _parse_unary to return operands sequentially
        operand_a = self._create_ast_node("IDENTIFIER", "a", line=1, column=1)
        operand_b = self._create_ast_node("IDENTIFIER", "b", line=1, column=5)
        operand_c = self._create_ast_node("IDENTIFIER", "c", line=1, column=9)
        
        mock_parse_unary.side_effect = [
            (operand_a, self._create_parser_state(tokens, pos=1)),  # First call for left
            (operand_b, self._create_parser_state(tokens, pos=3)),  # Second call for right of *
            (operand_c, self._create_parser_state(tokens, pos=5))   # Third call for right of /
        ]
        
        # Mock _consume_token for STAR then SLASH
        mock_consume_token.side_effect = [
            (self._create_token("STAR", "*", 1, 3), self._create_parser_state(tokens, pos=2)),
            (self._create_token("SLASH", "/", 1, 7), self._create_parser_state(tokens, pos=4))
        ]
        
        # Execute
        result_ast, result_state = _parse_multiplicative(parser_state)
        
        # Verify outer operation is division
        self.assertEqual(result_ast["type"], "BINARY_OP")
        self.assertEqual(result_ast["value"], "/")
        self.assertEqual(result_ast["line"], 1)
        self.assertEqual(result_ast["column"], 7)
        
        # Verify left child is the multiplication (left-associativity)
        left_child = result_ast["children"][0]
        self.assertEqual(left_child["type"], "BINARY_OP")
        self.assertEqual(left_child["value"], "*")
        self.assertEqual(left_child["children"][0]["value"], "a")
        self.assertEqual(left_child["children"][1]["value"], "b")
        
        # Verify right child is c
        right_child = result_ast["children"][1]
        self.assertEqual(right_child["type"], "IDENTIFIER")
        self.assertEqual(right_child["value"], "c")
        
        # Verify mocks were called correctly
        self.assertEqual(mock_parse_unary.call_count, 3)
        self.assertEqual(mock_consume_token.call_count, 2)

    @patch('_parse_multiplicative_package._parse_multiplicative_src._parse_unary')
    @patch('_parse_multiplicative_package._parse_multiplicative_src._consume_token')
    def test_modulo_operator(self, mock_consume_token, mock_parse_unary):
        """Test parsing modulo operator: a % b"""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("PERCENT", "%", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
            self._create_token("EOF", "", 1, 6)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        left_operand = self._create_ast_node("IDENTIFIER", "a", line=1, column=1)
        right_operand = self._create_ast_node("IDENTIFIER", "b", line=1, column=5)
        
        mock_parse_unary.side_effect = [
            (left_operand, self._create_parser_state(tokens, pos=1)),
            (right_operand, self._create_parser_state(tokens, pos=3))
        ]
        
        mock_consume_token.return_value = (
            self._create_token("PERCENT", "%", 1, 3),
            self._create_parser_state(tokens, pos=2)
        )
        
        # Execute
        result_ast, result_state = _parse_multiplicative(parser_state)
        
        # Verify
        self.assertEqual(result_ast["type"], "BINARY_OP")
        self.assertEqual(result_ast["value"], "%")
        self.assertEqual(result_ast["line"], 1)
        self.assertEqual(result_ast["column"], 3)

    @patch('_parse_multiplicative_package._parse_multiplicative_src._parse_unary')
    def test_no_multiplicative_operator(self, mock_parse_unary):
        """Test when there's no multiplicative operator (just unary expression)"""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("EOF", "", 1, 2)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        left_operand = self._create_ast_node("IDENTIFIER", "a", line=1, column=1)
        mock_parse_unary.return_value = (left_operand, self._create_parser_state(tokens, pos=1))
        
        # Execute
        result_ast, result_state = _parse_multiplicative(parser_state)
        
        # Verify: should return the unary result directly
        self.assertEqual(result_ast["type"], "IDENTIFIER")
        self.assertEqual(result_ast["value"], "a")
        
        # Verify _parse_unary was called once
        mock_parse_unary.assert_called_once()

    @patch('_parse_multiplicative_package._parse_multiplicative_src._parse_unary')
    @patch('_parse_multiplicative_package._parse_multiplicative_src._consume_token')
    def test_mixed_operators(self, mock_consume_token, mock_parse_unary):
        """Test mixed multiplicative operators: a * b % c / d"""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("STAR", "*", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
            self._create_token("PERCENT", "%", 1, 7),
            self._create_token("IDENTIFIER", "c", 1, 9),
            self._create_token("SLASH", "/", 1, 11),
            self._create_token("IDENTIFIER", "d", 1, 13),
            self._create_token("EOF", "", 1, 14)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Create operands
        operand_a = self._create_ast_node("IDENTIFIER", "a", line=1, column=1)
        operand_b = self._create_ast_node("IDENTIFIER", "b", line=1, column=5)
        operand_c = self._create_ast_node("IDENTIFIER", "c", line=1, column=9)
        operand_d = self._create_ast_node("IDENTIFIER", "d", line=1, column=13)
        
        mock_parse_unary.side_effect = [
            (operand_a, self._create_parser_state(tokens, pos=1)),
            (operand_b, self._create_parser_state(tokens, pos=3)),
            (operand_c, self._create_parser_state(tokens, pos=5)),
            (operand_d, self._create_parser_state(tokens, pos=7))
        ]
        
        mock_consume_token.side_effect = [
            (self._create_token("STAR", "*", 1, 3), self._create_parser_state(tokens, pos=2)),
            (self._create_token("PERCENT", "%", 1, 7), self._create_parser_state(tokens, pos=4)),
            (self._create_token("SLASH", "/", 1, 11), self._create_parser_state(tokens, pos=6))
        ]
        
        # Execute
        result_ast, result_state = _parse_multiplicative(parser_state)
        
        # Verify outermost operation is division (last operator)
        self.assertEqual(result_ast["type"], "BINARY_OP")
        self.assertEqual(result_ast["value"], "/")
        self.assertEqual(result_ast["line"], 1)
        self.assertEqual(result_ast["column"], 11)
        
        # Verify left-associativity: ((a * b) % c) / d
        left_child = result_ast["children"][0]
        self.assertEqual(left_child["value"], "%")
        
        left_left = left_child["children"][0]
        self.assertEqual(left_left["value"], "*")
        self.assertEqual(left_left["children"][0]["value"], "a")
        self.assertEqual(left_left["children"][1]["value"], "b")
        
        left_right = left_child["children"][1]
        self.assertEqual(left_right["value"], "c")
        
        right_child = result_ast["children"][1]
        self.assertEqual(right_child["value"], "d")

    @patch('_parse_multiplicative_package._parse_multiplicative_src._parse_unary')
    def test_eof_token_handling(self, mock_parse_unary):
        """Test handling when parser reaches EOF"""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("EOF", "", 1, 2)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        operand = self._create_ast_node("IDENTIFIER", "x", line=1, column=1)
        mock_parse_unary.return_value = (operand, self._create_parser_state(tokens, pos=1))
        
        # Execute
        result_ast, result_state = _parse_multiplicative(parser_state)
        
        # Verify
        self.assertEqual(result_ast["type"], "IDENTIFIER")
        self.assertEqual(result_ast["value"], "x")

    @patch('_parse_multiplicative_package._parse_multiplicative_src._parse_unary')
    @patch('_parse_multiplicative_package._parse_multiplicative_src._consume_token')
    def test_preserves_line_column_info(self, mock_consume_token, mock_parse_unary):
        """Test that line and column information is preserved in AST"""
        tokens = [
            self._create_token("IDENTIFIER", "a", 5, 10),
            self._create_token("STAR", "*", 5, 12),
            self._create_token("IDENTIFIER", "b", 5, 14),
            self._create_token("EOF", "", 5, 15)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        left_operand = self._create_ast_node("IDENTIFIER", "a", line=5, column=10)
        right_operand = self._create_ast_node("IDENTIFIER", "b", line=5, column=14)
        
        mock_parse_unary.side_effect = [
            (left_operand, self._create_parser_state(tokens, pos=1)),
            (right_operand, self._create_parser_state(tokens, pos=3))
        ]
        
        mock_consume_token.return_value = (
            self._create_token("STAR", "*", 5, 12),
            self._create_parser_state(tokens, pos=2)
        )
        
        # Execute
        result_ast, result_state = _parse_multiplicative(parser_state)
        
        # Verify operator position is preserved
        self.assertEqual(result_ast["line"], 5)
        self.assertEqual(result_ast["column"], 12)


if __name__ == "__main__":
    unittest.main()
