# === std / third-party imports ===
import unittest
from typing import Any, Dict
from unittest.mock import patch, MagicMock

# === UUT import ===
from ._parse_multiplicative_expr_src import _parse_multiplicative_expr

# === ADT defines ===
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


class TestParseMultiplicativeExpr(unittest.TestCase):
    """Test cases for _parse_multiplicative_expr function."""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Token:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> ParserState:
        """Helper to create a parser state dict."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    @patch("._parse_multiplicative_expr_src._parse_unary_expr")
    def test_simple_multiplication(self, mock_unary: MagicMock) -> None:
        """Test parsing simple multiplication: a * b"""
        # Setup: tokens for "a * b"
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("MULTIPLY", "*", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens)
        
        # Mock _parse_unary_expr to return different values for left and right operands
        left_operand = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_operand = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        mock_unary.side_effect = [left_operand, right_operand]
        
        # Execute
        result = _parse_multiplicative_expr(parser_state)
        
        # Verify
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "*")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0], left_operand)
        self.assertEqual(result["children"][1], right_operand)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        self.assertEqual(parser_state["pos"], 3)  # All tokens consumed

    @patch("._parse_multiplicative_expr_src._parse_unary_expr")
    def test_simple_division(self, mock_unary: MagicMock) -> None:
        """Test parsing simple division: a / b"""
        # Setup: tokens for "a / b"
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("DIVIDE", "/", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens)
        
        # Mock _parse_unary_expr
        left_operand = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_operand = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        mock_unary.side_effect = [left_operand, right_operand]
        
        # Execute
        result = _parse_multiplicative_expr(parser_state)
        
        # Verify
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "/")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0], left_operand)
        self.assertEqual(result["children"][1], right_operand)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        self.assertEqual(parser_state["pos"], 3)

    @patch("._parse_multiplicative_expr_src._parse_unary_expr")
    def test_chained_operations_left_associative(self, mock_unary: MagicMock) -> None:
        """Test parsing chained operations: a * b / c (left-associative)"""
        # Setup: tokens for "a * b / c"
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("MULTIPLY", "*", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
            self._create_token("DIVIDE", "/", 1, 7),
            self._create_token("IDENTIFIER", "c", 1, 9)
        ]
        parser_state = self._create_parser_state(tokens)
        
        # Mock _parse_unary_expr - called 3 times for a, b, c
        operand_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        operand_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        operand_c = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
        mock_unary.side_effect = [operand_a, operand_b, operand_c]
        
        # Execute
        result = _parse_multiplicative_expr(parser_state)
        
        # Verify: Should be ((a * b) / c) - left-associative
        # Outer node should be DIVIDE
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
        right_child = result["children"][1]
        self.assertEqual(right_child, operand_c)
        
        self.assertEqual(parser_state["pos"], 5)  # All tokens consumed

    @patch("._parse_multiplicative_expr_src._parse_unary_expr")
    def test_single_operand_no_operator(self, mock_unary: MagicMock) -> None:
        """Test parsing single operand with no multiplicative operators"""
        # Setup: tokens for just "a"
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1)
        ]
        parser_state = self._create_parser_state(tokens)
        
        # Mock _parse_unary_expr
        operand = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        mock_unary.return_value = operand
        
        # Execute
        result = _parse_multiplicative_expr(parser_state)
        
        # Verify: Should return the operand directly (no BINARY_OP)
        self.assertEqual(result, operand)
        self.assertEqual(parser_state["pos"], 0)  # No tokens consumed after parsing operand

    @patch("._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr")
    def test_empty_tokens(self, mock_unary: MagicMock) -> None:
        """Test parsing with empty token list"""
        # Setup: empty tokens
        tokens = []
        parser_state = self._create_parser_state(tokens)
        
        # Mock _parse_unary_expr - should still be called once
        operand = {"type": "LITERAL", "value": 0, "line": 0, "column": 0}
        mock_unary.return_value = operand
        
        # Execute
        result = _parse_multiplicative_expr(parser_state)
        
        # Verify: Should return operand from _parse_unary_expr
        self.assertEqual(result, operand)
        self.assertEqual(parser_state["pos"], 0)

    @patch("._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr")
    def test_non_multiplicative_token_after_operand(self, mock_unary: MagicMock) -> None:
        """Test parsing when next token is not multiplicative operator"""
        # Setup: tokens for "a + b" (+ is not multiplicative)
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("ADD", "+", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens)
        
        # Mock _parse_unary_expr
        operand = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        mock_unary.return_value = operand
        
        # Execute
        result = _parse_multiplicative_expr(parser_state)
        
        # Verify: Should return operand, not consume + token
        self.assertEqual(result, operand)
        self.assertEqual(parser_state["pos"], 0)  # Only consumed by _parse_unary_expr

    @patch("._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr")
    def test_position_tracking_across_multiple_operations(self, mock_unary: MagicMock) -> None:
        """Test that parser_state['pos'] is correctly updated through multiple operations"""
        # Setup: tokens for "a * b / c * d"
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("MULTIPLY", "*", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
            self._create_token("DIVIDE", "/", 1, 7),
            self._create_token("IDENTIFIER", "c", 1, 9),
            self._create_token("MULTIPLY", "*", 1, 11),
            self._create_token("IDENTIFIER", "d", 1, 13)
        ]
        parser_state = self._create_parser_state(tokens)
        
        # Mock _parse_unary_expr - called 4 times
        operands = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9},
            {"type": "IDENTIFIER", "value": "d", "line": 1, "column": 13}
        ]
        mock_unary.side_effect = operands
        
        # Execute
        result = _parse_multiplicative_expr(parser_state)
        
        # Verify position
        self.assertEqual(parser_state["pos"], 7)  # All tokens consumed
        
        # Verify structure: (((a * b) / c) * d)
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "*")
        self.assertEqual(result["column"], 11)

    @patch("._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr")
    def test_line_column_preservation(self, mock_unary: MagicMock) -> None:
        """Test that line and column from operator token are preserved in AST"""
        # Setup: tokens with different line/column values
        tokens = [
            self._create_token("IDENTIFIER", "a", 2, 5),
            self._create_token("MULTIPLY", "*", 2, 7),
            self._create_token("IDENTIFIER", "b", 2, 9)
        ]
        parser_state = self._create_parser_state(tokens)
        
        # Mock _parse_unary_expr
        left_operand = {"type": "IDENTIFIER", "value": "a", "line": 2, "column": 5}
        right_operand = {"type": "IDENTIFIER", "value": "b", "line": 2, "column": 9}
        mock_unary.side_effect = [left_operand, right_operand]
        
        # Execute
        result = _parse_multiplicative_expr(parser_state)
        
        # Verify operator position is preserved
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 7)


if __name__ == "__main__":
    unittest.main()
