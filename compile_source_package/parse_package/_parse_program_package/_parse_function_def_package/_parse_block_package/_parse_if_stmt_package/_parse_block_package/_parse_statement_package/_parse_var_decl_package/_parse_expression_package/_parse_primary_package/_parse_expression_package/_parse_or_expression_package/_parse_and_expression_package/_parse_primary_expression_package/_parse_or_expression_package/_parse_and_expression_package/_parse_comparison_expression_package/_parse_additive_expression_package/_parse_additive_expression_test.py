# -*- coding: utf-8 -*-
"""
Unit tests for _parse_additive_expression function.
Tests additive expression parsing (+, -) with left associativity.
"""

import unittest
from unittest.mock import patch, MagicMock
from typing import Any, Dict

from ._parse_additive_expression_src import _parse_additive_expression


class TestParseAdditiveExpression(unittest.TestCase):
    """Test cases for _parse_additive_expression function."""

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

    def _create_ast_node(self, node_type: str, **kwargs) -> Dict[str, Any]:
        """Helper to create an AST node."""
        node = {"type": node_type}
        node.update(kwargs)
        return node

    @patch('._parse_additive_expression_src._parse_multiplicative_expression')
    def test_simple_addition(self, mock_parse_mult: MagicMock) -> None:
        """Test parsing a simple addition expression: a + b"""
        # Setup mock to return left operand, then right operand
        left_operand = self._create_ast_node("identifier", value="a", line=1, column=1)
        right_operand = self._create_ast_node("identifier", value="b", line=1, column=5)
        
        mock_parse_mult.side_effect = [left_operand, right_operand]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "+", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_additive_expression(parser_state)
        
        # Verify result structure
        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["operator"], "add")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        
        # Verify left and right operands
        self.assertEqual(result["left"], left_operand)
        self.assertEqual(result["right"], right_operand)
        
        # Verify parser_state position advanced
        self.assertEqual(parser_state["pos"], 3)
        
        # Verify _parse_multiplicative_expression was called twice
        self.assertEqual(mock_parse_mult.call_count, 2)

    @patch('._parse_additive_expression_src._parse_multiplicative_expression')
    def test_simple_subtraction(self, mock_parse_mult: MagicMock) -> None:
        """Test parsing a simple subtraction expression: a - b"""
        left_operand = self._create_ast_node("identifier", value="a", line=1, column=1)
        right_operand = self._create_ast_node("identifier", value="b", line=1, column=5)
        
        mock_parse_mult.side_effect = [left_operand, right_operand]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "-", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_additive_expression(parser_state)
        
        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["operator"], "sub")
        self.assertEqual(result["left"], left_operand)
        self.assertEqual(result["right"], right_operand)

    @patch('._parse_additive_expression_src._parse_multiplicative_expression')
    def test_chained_operations_left_associative(self, mock_parse_mult: MagicMock) -> None:
        """Test left associativity: a + b - c should be ((a + b) - c)"""
        # Three operands for a + b - c
        operand_a = self._create_ast_node("identifier", value="a", line=1, column=1)
        operand_b = self._create_ast_node("identifier", value="b", line=1, column=5)
        operand_c = self._create_ast_node("identifier", value="c", line=1, column=9)
        
        mock_parse_mult.side_effect = [operand_a, operand_b, operand_c]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "+", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
            self._create_token("OPERATOR", "-", 1, 7),
            self._create_token("IDENTIFIER", "c", 1, 9)
        ]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_additive_expression(parser_state)
        
        # Result should be (a + b) - c
        # Outer operation is subtraction
        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["operator"], "sub")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 7)
        
        # Left side should be (a + b)
        left_side = result["left"]
        self.assertEqual(left_side["type"], "binary_op")
        self.assertEqual(left_side["operator"], "add")
        self.assertEqual(left_side["left"], operand_a)
        self.assertEqual(left_side["right"], operand_b)
        
        # Right side should be c
        self.assertEqual(result["right"], operand_c)
        
        # Verify _parse_multiplicative_expression was called three times
        self.assertEqual(mock_parse_mult.call_count, 3)

    @patch('._parse_additive_expression_src._parse_multiplicative_expression')
    def test_no_additive_operator(self, mock_parse_mult: MagicMock) -> None:
        """Test expression without + or - operators: just returns multiplicative expression"""
        operand = self._create_ast_node("identifier", value="a", line=1, column=1)
        mock_parse_mult.return_value = operand
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1)
        ]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_additive_expression(parser_state)
        
        # Should return the operand directly without wrapping
        self.assertEqual(result, operand)
        self.assertEqual(parser_state["pos"], 0)  # Position not advanced
        mock_parse_mult.assert_called_once()

    @patch('._parse_additive_expression_src._parse_multiplicative_expression')
    def test_error_from_multiplicative_expression_initial(self, mock_parse_mult: MagicMock) -> None:
        """Test when _parse_multiplicative_expression sets error on first call"""
        error_operand = self._create_ast_node("error", value="parse_error")
        mock_parse_mult.return_value = error_operand
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "+", 1, 3)
        ]
        parser_state = self._create_parser_state(tokens)
        parser_state["error"] = "parse_error"
        
        result = _parse_additive_expression(parser_state)
        
        # Should return early with error
        self.assertEqual(result, error_operand)
        mock_parse_mult.assert_called_once()

    @patch('._parse_additive_expression_src._parse_multiplicative_expression')
    def test_error_from_multiplicative_expression_during_parsing(self, mock_parse_mult: MagicMock) -> None:
        """Test when _parse_multiplicative_expression sets error during operator parsing"""
        left_operand = self._create_ast_node("identifier", value="a", line=1, column=1)
        error_operand = self._create_ast_node("error", value="parse_error")
        
        mock_parse_mult.side_effect = [left_operand, error_operand]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "+", 1, 3),
            self._create_token("INVALID", "x", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens)
        
        # Set error after first multiplicative parse
        def set_error_after_first(*args):
            if mock_parse_mult.call_count == 2:
                parser_state["error"] = "parse_error"
            return mock_parse_mult.side_effect[mock_parse_mult.call_count - 1]
        
        mock_parse_mult.side_effect = set_error_after_first
        
        result = _parse_additive_expression(parser_state)
        
        # Should return left operand when error occurs
        self.assertEqual(result, left_operand)

    def test_empty_tokens(self) -> None:
        """Test with empty token list"""
        parser_state = self._create_parser_state([])
        
        with patch('._parse_additive_expression_src._parse_multiplicative_expression') as mock_parse_mult:
            empty_result = self._create_ast_node("empty")
            mock_parse_mult.return_value = empty_result
            
            result = _parse_additive_expression(parser_state)
            
            self.assertEqual(result, empty_result)
            self.assertEqual(parser_state["pos"], 0)

    @patch('._parse_additive_expression_src._parse_multiplicative_expression')
    def test_operator_not_at_current_position(self, mock_parse_mult: MagicMock) -> None:
        """Test when operator is not at current position (already consumed)"""
        operand = self._create_ast_node("identifier", value="a", line=1, column=1)
        mock_parse_mult.return_value = operand
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=1)  # Position already past tokens
        
        result = _parse_additive_expression(parser_state)
        
        self.assertEqual(result, operand)
        self.assertEqual(parser_state["pos"], 1)

    @patch('._parse_additive_expression_src._parse_multiplicative_expression')
    def test_non_operator_token(self, mock_parse_mult: MagicMock) -> None:
        """Test when next token is not an OPERATOR type"""
        left_operand = self._create_ast_node("identifier", value="a", line=1, column=1)
        mock_parse_mult.return_value = left_operand
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("IDENTIFIER", "b", 1, 3)  # Not an operator
        ]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_additive_expression(parser_state)
        
        self.assertEqual(result, left_operand)
        self.assertEqual(parser_state["pos"], 0)

    @patch('._parse_additive_expression_src._parse_multiplicative_expression')
    def test_operator_but_not_additive(self, mock_parse_mult: MagicMock) -> None:
        """Test when operator is not + or - (e.g., * or /)"""
        left_operand = self._create_ast_node("identifier", value="a", line=1, column=1)
        mock_parse_mult.return_value = left_operand
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "*", 1, 3)  # Multiplicative, not additive
        ]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_additive_expression(parser_state)
        
        self.assertEqual(result, left_operand)
        self.assertEqual(parser_state["pos"], 0)

    @patch('._parse_additive_expression_src._parse_multiplicative_expression')
    def test_multiple_additions(self, mock_parse_mult: MagicMock) -> None:
        """Test multiple consecutive additions: a + b + c + d"""
        operands = [
            self._create_ast_node("identifier", value="a", line=1, column=1),
            self._create_ast_node("identifier", value="b", line=1, column=5),
            self._create_ast_node("identifier", value="c", line=1, column=9),
            self._create_ast_node("identifier", value="d", line=1, column=13)
        ]
        mock_parse_mult.side_effect = operands
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "+", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
            self._create_token("OPERATOR", "+", 1, 7),
            self._create_token("IDENTIFIER", "c", 1, 9),
            self._create_token("OPERATOR", "+", 1, 11),
            self._create_token("IDENTIFIER", "d", 1, 13)
        ]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_additive_expression(parser_state)
        
        # Verify left associativity: ((a + b) + c) + d
        self.assertEqual(result["operator"], "add")
        self.assertEqual(result["right"], operands[3])  # d
        
        # Navigate to innermost left
        inner = result["left"]
        self.assertEqual(inner["operator"], "add")
        self.assertEqual(inner["right"], operands[2])  # c
        
        innermost = inner["left"]
        self.assertEqual(innermost["operator"], "add")
        self.assertEqual(innermost["left"], operands[0])  # a
        self.assertEqual(innermost["right"], operands[1])  # b
        
        self.assertEqual(mock_parse_mult.call_count, 4)

    @patch('._parse_additive_expression_src._parse_multiplicative_expression')
    def test_mixed_add_subtract(self, mock_parse_mult: MagicMock) -> None:
        """Test mixed + and - operators: a + b - c + d"""
        operands = [
            self._create_ast_node("identifier", value="a", line=1, column=1),
            self._create_ast_node("identifier", value="b", line=1, column=5),
            self._create_ast_node("identifier", value="c", line=1, column=9),
            self._create_ast_node("identifier", value="d", line=1, column=13)
        ]
        mock_parse_mult.side_effect = operands
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "+", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
            self._create_token("OPERATOR", "-", 1, 7),
            self._create_token("IDENTIFIER", "c", 1, 9),
            self._create_token("OPERATOR", "+", 1, 11),
            self._create_token("IDENTIFIER", "d", 1, 13)
        ]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_additive_expression(parser_state)
        
        # Verify structure: ((a + b) - c) + d
        self.assertEqual(result["operator"], "add")
        self.assertEqual(result["right"], operands[3])  # d
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 11)
        
        inner = result["left"]
        self.assertEqual(inner["operator"], "sub")
        self.assertEqual(inner["right"], operands[2])  # c
        
        innermost = inner["left"]
        self.assertEqual(innermost["operator"], "add")
        self.assertEqual(innermost["left"], operands[0])  # a
        self.assertEqual(innermost["right"], operands[1])  # b


if __name__ == "__main__":
    unittest.main()
