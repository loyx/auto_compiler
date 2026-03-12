# -*- coding: utf-8 -*-
"""
Unit tests for _handle_paren_expr function.
Tests the handling of parenthesized expressions: ( expression )
"""

import unittest
from unittest.mock import patch

# Relative import from the same package
from ._handle_paren_expr_src import _handle_paren_expr


class TestHandleParenExpr(unittest.TestCase):
    """Test cases for _handle_paren_expr function."""

    def setUp(self):
        """Set up common test fixtures."""
        self.base_token = {
            "type": "LPAREN",
            "value": "(",
            "line": 1,
            "column": 5
        }

    def _create_parser_state(self, tokens, pos=0, filename="test.py"):
        """Helper to create parser state."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def test_happy_path_simple_identifier(self):
        """Test parsing (x) - simple identifier in parentheses."""
        tokens = [
            {"type": "LPAREN", "value": "(", "line": 1, "column": 5},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 6},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 7}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        lparen_token = tokens[0]

        mock_inner_ast = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 6
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_inner_ast

            result = _handle_paren_expr(parser_state, lparen_token)

            self.assertEqual(result, mock_inner_ast)
            self.assertEqual(parser_state["pos"], 3)  # Should consume LPAREN and RPAREN
            mock_parse_expr.assert_called_once()

    def test_happy_path_nested_expression(self):
        """Test parsing ((x + y)) - nested parentheses."""
        tokens = [
            {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 2},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3},
            {"type": "PLUS", "value": "+", "line": 1, "column": 5},
            {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 7},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 8},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 9}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        lparen_token = tokens[0]

        mock_inner_ast = {
            "type": "BINARY_OP",
            "children": [
                {"type": "IDENTIFIER", "value": "x"},
                {"type": "IDENTIFIER", "value": "y"}
            ],
            "line": 1,
            "column": 2
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_inner_ast

            result = _handle_paren_expr(parser_state, lparen_token)

            self.assertEqual(result, mock_inner_ast)
            self.assertEqual(parser_state["pos"], 7)  # Should be at second RPAREN
            mock_parse_expr.assert_called_once()

    def test_happy_path_literal_value(self):
        """Test parsing (42) - literal value in parentheses."""
        tokens = [
            {"type": "LPAREN", "value": "(", "line": 2, "column": 10},
            {"type": "NUMBER", "value": "42", "line": 2, "column": 11},
            {"type": "RPAREN", "value": ")", "line": 2, "column": 13}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        lparen_token = tokens[0]

        mock_inner_ast = {
            "type": "LITERAL",
            "value": 42,
            "line": 2,
            "column": 11
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_not_expr_package._parse_primary_expr_package._handle_paren_expr_package._handle_paren_expr_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_inner_ast

            result = _handle_paren_expr(parser_state, lparen_token)

            self.assertEqual(result, mock_inner_ast)
            self.assertEqual(parser_state["pos"], 3)

    def test_error_unexpected_end_inside_parentheses(self):
        """Test error when input ends immediately after LPAREN."""
        tokens = [
            {"type": "LPAREN", "value": "(", "line": 1, "column": 5}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        lparen_token = tokens[0]

        mock_error_node = {
            "type": "ERROR",
            "value": "unexpected end of input inside parentheses",
            "line": 1,
            "column": 5
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_not_expr_package._parse_primary_expr_package._handle_paren_expr_package._handle_paren_expr_src._build_error_node") as mock_build_error:
            mock_build_error.return_value = mock_error_node

            result = _handle_paren_expr(parser_state, lparen_token)

            self.assertEqual(result, mock_error_node)
            self.assertEqual(parser_state["pos"], 1)  # LPAREN consumed
            mock_build_error.assert_called_once_with(
                parser_state,
                "unexpected end of input inside parentheses",
                1,
                5
            )

    def test_error_expected_rparen_but_end_of_input(self):
        """Test error when expression exists but no RPAREN."""
        tokens = [
            {"type": "LPAREN", "value": "(", "line": 1, "column": 5},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 6}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        lparen_token = tokens[0]

        mock_inner_ast = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 6
        }

        mock_error_node = {
            "type": "ERROR",
            "value": "expected ')' but found end of input",
            "line": 1,
            "column": 5
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_not_expr_package._parse_primary_expr_package._handle_paren_expr_package._handle_paren_expr_src._parse_expression") as mock_parse_expr:
            with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_not_expr_package._parse_primary_expr_package._handle_paren_expr_package._handle_paren_expr_src._build_error_node") as mock_build_error:
                mock_parse_expr.return_value = mock_inner_ast
                mock_build_error.return_value = mock_error_node

                result = _handle_paren_expr(parser_state, lparen_token)

                self.assertEqual(result, mock_error_node)
                self.assertEqual(parser_state["pos"], 2)  # LPAREN consumed, inner parsed
                mock_build_error.assert_called_once_with(
                    parser_state,
                    "expected ')' but found end of input",
                    1,
                    5
                )

    def test_error_expected_rparen_but_found_other_token(self):
        """Test error when RPAREN is missing and another token is found."""
        tokens = [
            {"type": "LPAREN", "value": "(", "line": 1, "column": 5},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 6},
            {"type": "COMMA", "value": ",", "line": 1, "column": 8}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        lparen_token = tokens[0]

        mock_inner_ast = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 6
        }

        mock_error_node = {
            "type": "ERROR",
            "value": "expected ')' but found ','",
            "line": 1,
            "column": 8
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_not_expr_package._parse_primary_expr_package._handle_paren_expr_package._handle_paren_expr_src._parse_expression") as mock_parse_expr:
            with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_not_expr_package._parse_primary_expr_package._handle_paren_expr_package._handle_paren_expr_src._build_error_node") as mock_build_error:
                mock_parse_expr.return_value = mock_inner_ast
                mock_build_error.return_value = mock_error_node

                result = _handle_paren_expr(parser_state, lparen_token)

                self.assertEqual(result, mock_error_node)
                self.assertEqual(parser_state["pos"], 2)  # LPAREN consumed, inner parsed
                mock_build_error.assert_called_once_with(
                    parser_state,
                    "expected ')' but found ','",
                    1,
                    8
                )

    def test_error_state_propagation(self):
        """Test that error state is set in parser_state when error occurs."""
        tokens = [
            {"type": "LPAREN", "value": "(", "line": 1, "column": 5}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        lparen_token = tokens[0]

        def build_error_side_effect(ps, msg, line, col):
            ps["error"] = "解析失败"
            return {
                "type": "ERROR",
                "value": msg,
                "line": line,
                "column": col
            }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_not_expr_package._parse_primary_expr_package._handle_paren_expr_package._handle_paren_expr_src._build_error_node") as mock_build_error:
            mock_build_error.side_effect = build_error_side_effect

            result = _handle_paren_expr(parser_state, lparen_token)

            self.assertEqual(result["type"], "ERROR")
            self.assertEqual(parser_state.get("error"), "解析失败")

    def test_complex_expression_with_function_call(self):
        """Test parsing (foo(bar)) - function call in parentheses."""
        tokens = [
            {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "foo", "line": 1, "column": 2},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 5},
            {"type": "IDENTIFIER", "value": "bar", "line": 1, "column": 6},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 9},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 10}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        lparen_token = tokens[0]

        mock_inner_ast = {
            "type": "CALL",
            "value": "foo",
            "children": [
                {"type": "IDENTIFIER", "value": "bar"}
            ],
            "line": 1,
            "column": 2
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_not_expr_package._parse_primary_expr_package._handle_paren_expr_package._handle_paren_expr_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_inner_ast

            result = _handle_paren_expr(parser_state, lparen_token)

            self.assertEqual(result, mock_inner_ast)
            self.assertEqual(parser_state["pos"], 6)

    def test_empty_parentheses_error(self):
        """Test error when parentheses are empty: ()"""
        tokens = [
            {"type": "LPAREN", "value": "(", "line": 1, "column": 5},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 6}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        lparen_token = tokens[0]

        # _parse_expression should handle empty expression and return error or valid AST
        mock_inner_ast = {
            "type": "ERROR",
            "value": "empty expression",
            "line": 1,
            "column": 6
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_not_expr_package._parse_primary_expr_package._handle_paren_expr_package._handle_paren_expr_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_inner_ast

            result = _handle_paren_expr(parser_state, lparen_token)

            # The function returns whatever _parse_expression returns
            self.assertEqual(result, mock_inner_ast)
            self.assertEqual(parser_state["pos"], 2)  # Both LPAREN and RPAREN consumed

    def test_multiple_expressions_separated_by_comma(self):
        """Test parsing (a, b) - tuple-like expression."""
        tokens = [
            {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 2},
            {"type": "COMMA", "value": ",", "line": 1, "column": 4},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 7}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        lparen_token = tokens[0]

        mock_inner_ast = {
            "type": "TUPLE",
            "children": [
                {"type": "IDENTIFIER", "value": "a"},
                {"type": "IDENTIFIER", "value": "b"}
            ],
            "line": 1,
            "column": 2
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_not_expr_package._parse_primary_expr_package._handle_paren_expr_package._handle_paren_expr_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_inner_ast

            result = _handle_paren_expr(parser_state, lparen_token)

            self.assertEqual(result, mock_inner_ast)
            self.assertEqual(parser_state["pos"], 5)

    def test_whitespace_handling(self):
        """Test parsing with whitespace: (  x  )"""
        tokens = [
            {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
            {"type": "WHITESPACE", "value": "  ", "line": 1, "column": 2},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
            {"type": "WHITESPACE", "value": "  ", "line": 1, "column": 5},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 7}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        lparen_token = tokens[0]

        mock_inner_ast = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 4
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_not_expr_package._parse_primary_expr_package._handle_paren_expr_package._handle_paren_expr_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_inner_ast

            result = _handle_paren_expr(parser_state, lparen_token)

            self.assertEqual(result, mock_inner_ast)
            self.assertEqual(parser_state["pos"], 5)


if __name__ == "__main__":
    unittest.main()
