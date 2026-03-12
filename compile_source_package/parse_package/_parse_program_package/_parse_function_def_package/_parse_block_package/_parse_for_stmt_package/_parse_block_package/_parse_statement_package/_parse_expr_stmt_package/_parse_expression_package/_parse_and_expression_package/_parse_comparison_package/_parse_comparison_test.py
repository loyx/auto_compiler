# -*- coding: utf-8 -*-
"""Unit tests for _parse_comparison function."""

import unittest
from unittest.mock import patch
from typing import Dict, Any

# Relative import from the same package
from ._parse_comparison_src import _parse_comparison


class TestParseComparison(unittest.TestCase):
    """Test cases for _parse_comparison parser function."""

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        """Helper to create parser state dict."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast_node(self, node_type: str, value: Any = None, children: list = None, line: int = 0, column: int = 0) -> Dict[str, Any]:
        """Helper to create an AST node dict."""
        return {
            "type": node_type,
            "value": value,
            "children": children if children is not None else [],
            "line": line,
            "column": column
        }

    def test_simple_less_than_comparison(self):
        """Test parsing simple 'a < b' comparison."""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "<", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
        ]
        parser_state = self._create_parser_state(tokens)

        left_operand = self._create_ast_node("IDENTIFIER", "a", [], 1, 1)
        right_operand = self._create_ast_node("IDENTIFIER", "b", [], 1, 5)

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_and_expression_package._parse_comparison_package._parse_additive_expression_package._parse_additive_expression_src._parse_additive_expression") as mock_additive:
            mock_additive.side_effect = [left_operand, right_operand]

            result = _parse_comparison(parser_state)

            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "<")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(parser_state["pos"], 3)

    def test_simple_greater_than_comparison(self):
        """Test parsing simple 'a > b' comparison."""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", ">", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
        ]
        parser_state = self._create_parser_state(tokens)

        left_operand = self._create_ast_node("IDENTIFIER", "a", [], 1, 1)
        right_operand = self._create_ast_node("IDENTIFIER", "b", [], 1, 5)

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_and_expression_package._parse_comparison_package._parse_additive_expression_package._parse_additive_expression_src._parse_additive_expression") as mock_additive:
            mock_additive.side_effect = [left_operand, right_operand]

            result = _parse_comparison(parser_state)

            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], ">")
            self.assertEqual(parser_state["pos"], 3)

    def test_less_than_or_equal_comparison(self):
        """Test parsing 'a <= b' comparison."""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "<=", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 6),
        ]
        parser_state = self._create_parser_state(tokens)

        left_operand = self._create_ast_node("IDENTIFIER", "a", [], 1, 1)
        right_operand = self._create_ast_node("IDENTIFIER", "b", [], 1, 6)

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_and_expression_package._parse_comparison_package._parse_additive_expression_package._parse_additive_expression_src._parse_additive_expression") as mock_additive:
            mock_additive.side_effect = [left_operand, right_operand]

            result = _parse_comparison(parser_state)

            self.assertEqual(result["value"], "<=")

    def test_greater_than_or_equal_comparison(self):
        """Test parsing 'a >= b' comparison."""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", ">=", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 6),
        ]
        parser_state = self._create_parser_state(tokens)

        left_operand = self._create_ast_node("IDENTIFIER", "a", [], 1, 1)
        right_operand = self._create_ast_node("IDENTIFIER", "b", [], 1, 6)

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_and_expression_package._parse_comparison_package._parse_additive_expression_package._parse_additive_expression_src._parse_additive_expression") as mock_additive:
            mock_additive.side_effect = [left_operand, right_operand]

            result = _parse_comparison(parser_state)

            self.assertEqual(result["value"], ">=")

    def test_equality_comparison(self):
        """Test parsing 'a == b' comparison."""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "==", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 6),
        ]
        parser_state = self._create_parser_state(tokens)

        left_operand = self._create_ast_node("IDENTIFIER", "a", [], 1, 1)
        right_operand = self._create_ast_node("IDENTIFIER", "b", [], 1, 6)

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_and_expression_package._parse_comparison_package._parse_additive_expression_package._parse_additive_expression_src._parse_additive_expression") as mock_additive:
            mock_additive.side_effect = [left_operand, right_operand]

            result = _parse_comparison(parser_state)

            self.assertEqual(result["value"], "==")

    def test_inequality_comparison(self):
        """Test parsing 'a != b' comparison."""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "!=", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 6),
        ]
        parser_state = self._create_parser_state(tokens)

        left_operand = self._create_ast_node("IDENTIFIER", "a", [], 1, 1)
        right_operand = self._create_ast_node("IDENTIFIER", "b", [], 1, 6)

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_and_expression_package._parse_comparison_package._parse_additive_expression_package._parse_additive_expression_src._parse_additive_expression") as mock_additive:
            mock_additive.side_effect = [left_operand, right_operand]

            result = _parse_comparison(parser_state)

            self.assertEqual(result["value"], "!=")

    def test_no_comparison_operator(self):
        """Test parsing expression without comparison operator (just additive expression)."""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "+", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
        ]
        parser_state = self._create_parser_state(tokens)

        left_operand = self._create_ast_node("IDENTIFIER", "a", [], 1, 1)

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_and_expression_package._parse_comparison_package._parse_additive_expression_package._parse_additive_expression_src._parse_additive_expression") as mock_additive:
            mock_additive.return_value = left_operand

            result = _parse_comparison(parser_state)

            self.assertEqual(result, left_operand)
            self.assertEqual(parser_state["pos"], 0)

    def test_chained_comparison(self):
        """Test parsing chained comparison 'a < b < c'."""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "<", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
            self._create_token("OPERATOR", "<", 1, 7),
            self._create_token("IDENTIFIER", "c", 1, 9),
        ]
        parser_state = self._create_parser_state(tokens)

        operand_a = self._create_ast_node("IDENTIFIER", "a", [], 1, 1)
        operand_b = self._create_ast_node("IDENTIFIER", "b", [], 1, 5)
        operand_c = self._create_ast_node("IDENTIFIER", "c", [], 1, 9)

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_and_expression_package._parse_comparison_package._parse_additive_expression_package._parse_additive_expression_src._parse_additive_expression") as mock_additive:
            mock_additive.side_effect = [operand_a, operand_b, operand_c]

            result = _parse_comparison(parser_state)

            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "<")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 7)
            self.assertEqual(parser_state["pos"], 5)

            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["value"], "<")
            self.assertEqual(left_child["line"], 1)
            self.assertEqual(left_child["column"], 3)

    def test_missing_right_operand_raises_syntax_error(self):
        """Test that missing right operand raises SyntaxError."""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "<", 1, 3),
        ]
        parser_state = self._create_parser_state(tokens)

        left_operand = self._create_ast_node("IDENTIFIER", "a", [], 1, 1)

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_and_expression_package._parse_comparison_package._parse_additive_expression_package._parse_additive_expression_src._parse_additive_expression") as mock_additive:
            mock_additive.return_value = left_operand

            with self.assertRaises(SyntaxError) as context:
                _parse_comparison(parser_state)

            self.assertIn("Expected right operand", str(context.exception))
            self.assertIn("<", str(context.exception))

    def test_comparison_with_numeric_literals(self):
        """Test parsing comparison with numeric literals '5 > 3'."""
        tokens = [
            self._create_token("NUMBER", "5", 1, 1),
            self._create_token("OPERATOR", ">", 1, 3),
            self._create_token("NUMBER", "3", 1, 5),
        ]
        parser_state = self._create_parser_state(tokens)

        left_operand = self._create_ast_node("NUMBER", "5", [], 1, 1)
        right_operand = self._create_ast_node("NUMBER", "3", [], 1, 5)

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_and_expression_package._parse_comparison_package._parse_additive_expression_package._parse_additive_expression_src._parse_additive_expression") as mock_additive:
            mock_additive.side_effect = [left_operand, right_operand]

            result = _parse_comparison(parser_state)

            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], ">")

    def test_comparison_with_complex_expressions(self):
        """Test parsing comparison with complex additive expressions 'a + b < c - d'."""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "+", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
            self._create_token("OPERATOR", "<", 1, 7),
            self._create_token("IDENTIFIER", "c", 1, 9),
            self._create_token("OPERATOR", "-", 1, 11),
            self._create_token("IDENTIFIER", "d", 1, 13),
        ]
        parser_state = self._create_parser_state(tokens)

        left_expr = self._create_ast_node("BINARY_OP", "+", [
            self._create_ast_node("IDENTIFIER", "a", [], 1, 1),
            self._create_ast_node("IDENTIFIER", "b", [], 1, 5)
        ], 1, 3)
        right_expr = self._create_ast_node("BINARY_OP", "-", [
            self._create_ast_node("IDENTIFIER", "c", [], 1, 9),
            self._create_ast_node("IDENTIFIER", "d", [], 1, 13)
        ], 1, 11)

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_and_expression_package._parse_comparison_package._parse_additive_expression_package._parse_additive_expression_src._parse_additive_expression") as mock_additive:
            mock_additive.side_effect = [left_expr, right_expr]

            result = _parse_comparison(parser_state)

            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "<")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0], left_expr)
            self.assertEqual(result["children"][1], right_expr)

    def test_empty_tokens_raises_error(self):
        """Test that empty tokens list raises appropriate error."""
        tokens = []
        parser_state = self._create_parser_state(tokens)

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_and_expression_package._parse_comparison_package._parse_additive_expression_package._parse_additive_expression_src._parse_additive_expression") as mock_additive:
            mock_additive.side_effect = IndexError("Token index out of range")

            with self.assertRaises(IndexError):
                _parse_comparison(parser_state)

    def test_comparison_operator_line_column_preserved(self):
        """Test that line and column information is preserved from operator token."""
        tokens = [
            self._create_token("IDENTIFIER", "a", 5, 10),
            self._create_token("OPERATOR", "==", 5, 12),
            self._create_token("IDENTIFIER", "b", 5, 15),
        ]
        parser_state = self._create_parser_state(tokens)

        left_operand = self._create_ast_node("IDENTIFIER", "a", [], 5, 10)
        right_operand = self._create_ast_node("IDENTIFIER", "b", [], 5, 15)

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_and_expression_package._parse_comparison_package._parse_additive_expression_package._parse_additive_expression_src._parse_additive_expression") as mock_additive:
            mock_additive.side_effect = [left_operand, right_operand]

            result = _parse_comparison(parser_state)

            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 12)


if __name__ == "__main__":
    unittest.main()
