# -*- coding: utf-8 -*-
"""Unit tests for _parse_not function."""

import unittest
from unittest.mock import patch
from typing import Dict, Any, List

# Import the function under test using relative import
from ._parse_not_src import _parse_not


class TestParseNot(unittest.TestCase):
    """Test cases for _parse_not function."""

    def _create_parser_state(
        self,
        tokens: List[Dict[str, Any]],
        pos: int = 0,
        filename: str = "<test>"
    ) -> Dict[str, Any]:
        """Helper to create parser state dict."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_token(
        self,
        token_type: str,
        value: str,
        line: int = 1,
        column: int = 1
    ) -> Dict[str, Any]:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def test_single_not_expression(self):
        """Test parsing a single 'not' expression."""
        tokens = [
            self._create_token("NOT", "not", 1, 1),
            self._create_token("IDENTIFIER", "x", 1, 5),
        ]
        parser_state = self._create_parser_state(tokens)

        # Mock _parse_comparison to return a simple AST for the operand
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_and_package._parse_not_package._parse_comparison_package._parse_comparison_src._parse_comparison") as mock_comparison:
            mock_comparison.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "line": 1,
                "column": 5
            }

            result = _parse_not(parser_state)

            # Verify AST structure
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["operator"], "not")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "IDENTIFIER")
            self.assertEqual(result["children"][0]["value"], "x")

            # Verify parser state was updated (consumed NOT token)
            self.assertEqual(parser_state["pos"], 1)

            # Verify _parse_comparison was called
            mock_comparison.assert_called_once()

    def test_chained_not_expressions(self):
        """Test parsing chained 'not not' expressions."""
        tokens = [
            self._create_token("NOT", "not", 1, 1),
            self._create_token("NOT", "not", 1, 5),
            self._create_token("IDENTIFIER", "x", 1, 10),
        ]
        parser_state = self._create_parser_state(tokens)

        # Mock _parse_comparison for the final operand
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_and_package._parse_not_package._parse_comparison_package._parse_comparison_src._parse_comparison") as mock_comparison:
            mock_comparison.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "line": 1,
                "column": 10
            }

            result = _parse_not(parser_state)

            # Verify outer UNARY_OP
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["operator"], "not")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)

            # Verify inner UNARY_OP (chained not)
            inner = result["children"][0]
            self.assertEqual(inner["type"], "UNARY_OP")
            self.assertEqual(inner["operator"], "not")
            self.assertEqual(inner["line"], 1)
            self.assertEqual(inner["column"], 5)

            # Verify innermost operand
            self.assertEqual(inner["children"][0]["type"], "IDENTIFIER")
            self.assertEqual(inner["children"][0]["value"], "x")

            # Verify parser state was updated (consumed both NOT tokens)
            self.assertEqual(parser_state["pos"], 2)

    def test_no_not_token_delegates_to_comparison(self):
        """Test that non-NOT token delegates to _parse_comparison."""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
        ]
        parser_state = self._create_parser_state(tokens)

        expected_result = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_and_package._parse_not_package._parse_comparison_package._parse_comparison_src._parse_comparison") as mock_comparison:
            mock_comparison.return_value = expected_result

            result = _parse_not(parser_state)

            self.assertEqual(result, expected_result)
            # Verify parser state was NOT modified (no token consumed)
            self.assertEqual(parser_state["pos"], 0)
            mock_comparison.assert_called_once_with(parser_state)

    def test_empty_tokens_delegates_to_comparison(self):
        """Test that empty token list delegates to _parse_comparison."""
        tokens = []
        parser_state = self._create_parser_state(tokens)

        expected_result = {
            "type": "LITERAL",
            "value": None,
            "line": 0,
            "column": 0
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_and_package._parse_not_package._parse_comparison_package._parse_comparison_src._parse_comparison") as mock_comparison:
            mock_comparison.return_value = expected_result

            result = _parse_not(parser_state)

            self.assertEqual(result, expected_result)
            mock_comparison.assert_called_once()

    def test_pos_at_end_delegates_to_comparison(self):
        """Test when pos is at end of tokens."""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
        ]
        parser_state = self._create_parser_state(tokens, pos=1)

        expected_result = {
            "type": "EOF",
            "value": None,
            "line": 0,
            "column": 0
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_and_package._parse_not_package._parse_comparison_package._parse_comparison_src._parse_comparison") as mock_comparison:
            mock_comparison.return_value = expected_result

            result = _parse_not(parser_state)

            self.assertEqual(result, expected_result)
            mock_comparison.assert_called_once()

    def test_not_with_custom_filename(self):
        """Test parsing with custom filename in parser state."""
        tokens = [
            self._create_token("NOT", "not", 2, 5),
            self._create_token("IDENTIFIER", "flag", 2, 9),
        ]
        parser_state = self._create_parser_state(
            tokens,
            filename="test_module.py"
        )

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_and_package._parse_not_package._parse_comparison_package._parse_comparison_src._parse_comparison") as mock_comparison:
            mock_comparison.return_value = {
                "type": "IDENTIFIER",
                "value": "flag",
                "line": 2,
                "column": 9
            }

            result = _parse_not(parser_state)

            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 5)
            self.assertEqual(parser_state["pos"], 1)

    def test_not_followed_by_comparison_operator(self):
        """Test 'not' followed by comparison expression."""
        tokens = [
            self._create_token("NOT", "not", 1, 1),
            self._create_token("IDENTIFIER", "a", 1, 5),
            self._create_token("COMPARE_OP", "==", 1, 7),
            self._create_token("IDENTIFIER", "b", 1, 10),
        ]
        parser_state = self._create_parser_state(tokens)

        comparison_ast = {
            "type": "BINARY_OP",
            "operator": "==",
            "children": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 5},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 10}
            ],
            "line": 1,
            "column": 5
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_and_package._parse_not_package._parse_comparison_package._parse_comparison_src._parse_comparison") as mock_comparison:
            mock_comparison.return_value = comparison_ast

            result = _parse_not(parser_state)

            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["operator"], "not")
            self.assertEqual(result["children"][0], comparison_ast)
            self.assertEqual(parser_state["pos"], 1)


if __name__ == "__main__":
    unittest.main()
