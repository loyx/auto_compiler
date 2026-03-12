# -*- coding: utf-8 -*-
"""Unit tests for _parse_comparison function."""

import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any

# Mock the deep dependency chain to avoid import errors
import sys
from unittest.mock import MagicMock

# Create mock modules for the deep dependency chain
mock_primary_src = MagicMock()
mock_primary_src._parse_primary = MagicMock(return_value={"type": "IDENTIFIER", "value": "mocked", "line": 0, "column": 0})

sys.modules['main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_binop_tail_package._parse_primary_expr_package._parse_expression_package._parse_logical_or_package._parse_logical_and_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package'] = MagicMock()
sys.modules['main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_binop_tail_package._parse_primary_expr_package._parse_expression_package._parse_logical_or_package._parse_logical_and_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package._parse_primary_src'] = mock_primary_src

from ._parse_comparison_src import _parse_comparison


class TestParseComparison(unittest.TestCase):
    """Test cases for _parse_comparison function."""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dictionary."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast_node(self, node_type: str, value: Any = None, operator: str = None,
                         children: list = None, line: int = 0, column: int = 0) -> Dict[str, Any]:
        """Helper to create an AST node dictionary."""
        node = {
            "type": node_type,
            "line": line,
            "column": column
        }
        if value is not None:
            node["value"] = value
        if operator is not None:
            node["operator"] = operator
        if children is not None:
            node["children"] = children
        return node

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_binop_tail_package._parse_primary_expr_package._parse_expression_package._parse_logical_or_package._parse_logical_and_package._parse_comparison_package._parse_comparison_src._parse_additive')
    def test_no_comparison_operator(self, mock_parse_additive: MagicMock):
        """Test when there is no comparison operator - should return left operand only."""
        left_node = self._create_ast_node("IDENTIFIER", value="x", line=1, column=1)
        mock_parse_additive.return_value = left_node

        parser_state = {
            "tokens": [self._create_token("IDENTIFIER", "x")],
            "pos": 1,  # Past the identifier, no more tokens
            "filename": "test.py",
            "error": ""
        }

        result = _parse_comparison(parser_state)

        self.assertEqual(result, left_node)
        mock_parse_additive.assert_called_once_with(parser_state)

    @patch('_parse_comparison_src._parse_additive')
    def test_lt_operator(self, mock_parse_additive: MagicMock):
        """Test less than operator (<)."""
        left_node = self._create_ast_node("IDENTIFIER", value="a", line=1, column=1)
        right_node = self._create_ast_node("IDENTIFIER", value="b", line=1, column=3)

        mock_parse_additive.side_effect = [left_node, right_node]

        parser_state = {
            "tokens": [
                self._create_token("IDENTIFIER", "a", 1, 1),
                self._create_token("LT", "<", 1, 2),
                self._create_token("IDENTIFIER", "b", 1, 3)
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        result = _parse_comparison(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "<")
        self.assertEqual(result["children"], [left_node, right_node])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 2)
        self.assertEqual(parser_state["pos"], 2)  # Should have consumed the LT token

    @patch('_parse_comparison_src._parse_additive')
    def test_gt_operator(self, mock_parse_additive: MagicMock):
        """Test greater than operator (>)."""
        left_node = self._create_ast_node("NUMBER", value="5", line=1, column=1)
        right_node = self._create_ast_node("NUMBER", value="3", line=1, column=3)

        mock_parse_additive.side_effect = [left_node, right_node]

        parser_state = {
            "tokens": [
                self._create_token("NUMBER", "5", 1, 1),
                self._create_token("GT", ">", 1, 2),
                self._create_token("NUMBER", "3", 1, 3)
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        result = _parse_comparison(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], ">")
        self.assertEqual(result["children"], [left_node, right_node])

    @patch('_parse_comparison_src._parse_additive')
    def test_lte_operator(self, mock_parse_additive: MagicMock):
        """Test less than or equal operator (<=)."""
        left_node = self._create_ast_node("IDENTIFIER", value="x", line=2, column=5)
        right_node = self._create_ast_node("NUMBER", value="10", line=2, column=8)

        mock_parse_additive.side_effect = [left_node, right_node]

        parser_state = {
            "tokens": [
                self._create_token("IDENTIFIER", "x", 2, 5),
                self._create_token("LTE", "<=", 2, 6),
                self._create_token("NUMBER", "10", 2, 8)
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        result = _parse_comparison(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "<=")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 6)

    @patch('_parse_comparison_src._parse_additive')
    def test_gte_operator(self, mock_parse_additive: MagicMock):
        """Test greater than or equal operator (>=)."""
        left_node = self._create_ast_node("IDENTIFIER", value="y", line=3, column=1)
        right_node = self._create_ast_node("IDENTIFIER", value="z", line=3, column=4)

        mock_parse_additive.side_effect = [left_node, right_node]

        parser_state = {
            "tokens": [
                self._create_token("IDENTIFIER", "y", 3, 1),
                self._create_token("GTE", ">=", 3, 2),
                self._create_token("IDENTIFIER", "z", 3, 4)
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        result = _parse_comparison(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], ">=")

    @patch('_parse_comparison_src._parse_additive')
    def test_eq_operator(self, mock_parse_additive: MagicMock):
        """Test equality operator (==)."""
        left_node = self._create_ast_node("IDENTIFIER", value="a", line=1, column=1)
        right_node = self._create_ast_node("IDENTIFIER", value="b", line=1, column=4)

        mock_parse_additive.side_effect = [left_node, right_node]

        parser_state = {
            "tokens": [
                self._create_token("IDENTIFIER", "a", 1, 1),
                self._create_token("EQ", "==", 1, 2),
                self._create_token("IDENTIFIER", "b", 1, 4)
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        result = _parse_comparison(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "==")

    @patch('_parse_comparison_src._parse_additive')
    def test_neq_operator(self, mock_parse_additive: MagicMock):
        """Test not equal operator (!=)."""
        left_node = self._create_ast_node("IDENTIFIER", value="x", line=1, column=1)
        right_node = self._create_ast_node("NUMBER", value="0", line=1, column=4)

        mock_parse_additive.side_effect = [left_node, right_node]

        parser_state = {
            "tokens": [
                self._create_token("IDENTIFIER", "x", 1, 1),
                self._create_token("NEQ", "!=", 1, 2),
                self._create_token("NUMBER", "0", 1, 4)
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        result = _parse_comparison(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "!=")

    @patch('_parse_comparison_src._parse_additive')
    def test_error_in_parser_state_before_comparison(self, mock_parse_additive: MagicMock):
        """Test when error is already set in parser_state before checking comparison operator."""
        error_node = self._create_ast_node("ERROR", value="Previous error", line=1, column=1)
        mock_parse_additive.return_value = error_node

        parser_state = {
            "tokens": [
                self._create_token("IDENTIFIER", "x", 1, 1),
                self._create_token("LT", "<", 1, 2)
            ],
            "pos": 0,
            "filename": "test.py",
            "error": "Previous error"
        }

        result = _parse_comparison(parser_state)

        self.assertEqual(result, error_node)
        # Should not consume the LT token since we returned early
        self.assertEqual(parser_state["pos"], 0)

    @patch('_parse_comparison_src._parse_additive')
    def test_error_after_parsing_right_operand(self, mock_parse_additive: MagicMock):
        """Test when error is set after parsing the right operand."""
        left_node = self._create_ast_node("IDENTIFIER", value="a", line=1, column=1)
        right_node = self._create_ast_node("ERROR", value="Right operand error", line=1, column=3)

        def parse_additive_side_effect(state):
            if state["pos"] == 0:
                return left_node
            else:
                state["error"] = "Right operand error"
                return right_node

        mock_parse_additive.side_effect = parse_additive_side_effect

        parser_state = {
            "tokens": [
                self._create_token("IDENTIFIER", "a", 1, 1),
                self._create_token("LT", "<", 1, 2),
                self._create_token("IDENTIFIER", "b", 1, 3)
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        result = _parse_comparison(parser_state)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Right operand error")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 2)

    @patch('_parse_comparison_src._parse_additive')
    def test_empty_tokens(self, mock_parse_additive: MagicMock):
        """Test with empty tokens list."""
        left_node = self._create_ast_node("EMPTY", line=0, column=0)
        mock_parse_additive.return_value = left_node

        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        result = _parse_comparison(parser_state)

        self.assertEqual(result, left_node)

    @patch('_parse_comparison_src._parse_additive')
    def test_pos_at_end_of_tokens(self, mock_parse_additive: MagicMock):
        """Test when pos is already at the end of tokens."""
        left_node = self._create_ast_node("IDENTIFIER", value="x", line=1, column=1)
        mock_parse_additive.return_value = left_node

        parser_state = {
            "tokens": [self._create_token("IDENTIFIER", "x", 1, 1)],
            "pos": 1,  # At the end
            "filename": "test.py",
            "error": ""
        }

        result = _parse_comparison(parser_state)

        self.assertEqual(result, left_node)

    @patch('_parse_comparison_src._parse_additive')
    def test_non_comparison_token_type(self, mock_parse_additive: MagicMock):
        """Test when current token is not a comparison operator."""
        left_node = self._create_ast_node("IDENTIFIER", value="x", line=1, column=1)
        mock_parse_additive.return_value = left_node

        parser_state = {
            "tokens": [
                self._create_token("IDENTIFIER", "x", 1, 1),
                self._create_token("PLUS", "+", 1, 2),  # Not a comparison operator
                self._create_token("NUMBER", "5", 1, 3)
            ],
            "pos": 1,  # Pointing to PLUS
            "filename": "test.py",
            "error": ""
        }

        result = _parse_comparison(parser_state)

        self.assertEqual(result, left_node)
        # Should not consume the PLUS token
        self.assertEqual(parser_state["pos"], 1)


if __name__ == "__main__":
    unittest.main()