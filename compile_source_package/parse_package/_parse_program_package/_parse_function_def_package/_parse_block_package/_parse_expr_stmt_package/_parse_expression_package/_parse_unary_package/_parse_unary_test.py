# -*- coding: utf-8 -*-
"""
Unit tests for _parse_unary function.
Tests parsing of unary expressions with - and ! operators.
"""

import unittest
from unittest.mock import patch

from ._parse_unary_src import _parse_unary


class TestParseUnary(unittest.TestCase):
    """Test cases for _parse_unary function."""

    def test_parse_primary_without_unary_operator(self):
        """Test parsing a primary expression without unary operator."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.txt"
        }

        expected_primary = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_unary_package._parse_unary_src._parse_primary",
            return_value=expected_primary
        ) as mock_parse_primary:
            result = _parse_unary(parser_state)
            self.assertEqual(result, expected_primary)
            mock_parse_primary.assert_called_once_with(parser_state)

    def test_parse_unary_minus(self):
        """Test parsing unary minus operator."""
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.txt"
        }

        expected_operand = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 2
        }

        expected_result = {
            "type": "UNARY_OP",
            "children": [expected_operand],
            "value": "-",
            "line": 1,
            "column": 1
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_unary_package._parse_unary_src._consume_token",
            return_value=parser_state["tokens"][0]
        ) as mock_consume:
            with patch(
                "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_unary_package._parse_unary_src._parse_primary",
                return_value=expected_operand
            ) as mock_parse_primary:
                result = _parse_unary(parser_state)
                self.assertEqual(result, expected_result)
                mock_consume.assert_called_once_with(parser_state)
                mock_parse_primary.assert_called_once_with(parser_state)

    def test_parse_unary_not(self):
        """Test parsing unary not operator."""
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "!", "line": 1, "column": 1},
                {"type": "LITERAL", "value": True, "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.txt"
        }

        expected_operand = {
            "type": "LITERAL",
            "value": True,
            "line": 1,
            "column": 2
        }

        expected_result = {
            "type": "UNARY_OP",
            "children": [expected_operand],
            "value": "!",
            "line": 1,
            "column": 1
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_unary_package._parse_unary_src._consume_token",
            return_value=parser_state["tokens"][0]
        ) as mock_consume:
            with patch(
                "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_unary_package._parse_unary_src._parse_primary",
                return_value=expected_operand
            ) as mock_parse_primary:
                result = _parse_unary(parser_state)
                self.assertEqual(result, expected_result)
                mock_consume.assert_called_once_with(parser_state)
                mock_parse_primary.assert_called_once_with(parser_state)

    def test_parse_nested_unary_operators(self):
        """Test parsing nested unary operators (right-associative): -!x."""
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "!", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.txt"
        }

        # Expected: -(!x)
        inner_unary = {
            "type": "UNARY_OP",
            "children": [{"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}],
            "value": "!",
            "line": 1,
            "column": 2
        }

        expected_result = {
            "type": "UNARY_OP",
            "children": [inner_unary],
            "value": "-",
            "line": 1,
            "column": 1
        }

        # First call consumes '-', second call consumes '!', third call parses primary
        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_unary_package._parse_unary_src._consume_token",
            side_effect=[
                parser_state["tokens"][0],  # First '-'
                parser_state["tokens"][1]   # Second '!'
            ]
        ) as mock_consume:
            with patch(
                "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_unary_package._parse_unary_src._parse_primary",
                return_value={"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
            ) as mock_parse_primary:
                result = _parse_unary(parser_state)
                self.assertEqual(result, expected_result)
                self.assertEqual(mock_consume.call_count, 2)
                mock_parse_primary.assert_called_once()

    def test_empty_tokens_raises_syntax_error(self):
        """Test that empty tokens list raises SyntaxError."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.txt"
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_unary(parser_state)

        self.assertIn("Unexpected end of expression", str(context.exception))
        self.assertIn("test.txt", str(context.exception))

    def test_position_at_end_raises_syntax_error(self):
        """Test that position at end of tokens raises SyntaxError."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 1,  # At the end
            "filename": "test.txt"
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_unary(parser_state)

        self.assertIn("Unexpected end of expression", str(context.exception))

    def test_unary_minus_with_number_literal(self):
        """Test parsing unary minus with number literal."""
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "-", "line": 2, "column": 5},
                {"type": "LITERAL", "value": 42, "line": 2, "column": 6}
            ],
            "pos": 0,
            "filename": "test.txt"
        }

        expected_operand = {
            "type": "LITERAL",
            "value": 42,
            "line": 2,
            "column": 6
        }

        expected_result = {
            "type": "UNARY_OP",
            "children": [expected_operand],
            "value": "-",
            "line": 2,
            "column": 5
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_unary_package._consume_token_package._consume_token_src._consume_token",
            return_value=parser_state["tokens"][0]
        ) as mock_consume:
            with patch(
                "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_unary_package._parse_primary_package._parse_primary_src._parse_primary",
                return_value=expected_operand
            ) as mock_parse_primary:
                result = _parse_unary(parser_state)
                self.assertEqual(result, expected_result)
                mock_consume.assert_called_once()
                mock_parse_primary.assert_called_once()

    def test_multiple_consecutive_unary_minus(self):
        """Test parsing multiple consecutive unary minus: --x."""
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.txt"
        }

        # Expected: -(-x)
        inner_unary = {
            "type": "UNARY_OP",
            "children": [{"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}],
            "value": "-",
            "line": 1,
            "column": 2
        }

        expected_result = {
            "type": "UNARY_OP",
            "children": [inner_unary],
            "value": "-",
            "line": 1,
            "column": 1
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_unary_package._consume_token_package._consume_token_src._consume_token",
            side_effect=[
                parser_state["tokens"][0],
                parser_state["tokens"][1]
            ]
        ) as mock_consume:
            with patch(
                "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_unary_package._parse_primary_package._parse_primary_src._parse_primary",
                return_value={"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
            ) as mock_parse_primary:
                result = _parse_unary(parser_state)
                self.assertEqual(result, expected_result)
                self.assertEqual(mock_consume.call_count, 2)

    def test_other_operator_not_unary(self):
        """Test that non-unary operators are handled by _parse_primary."""
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.txt"
        }

        expected_primary = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 2
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_unary_package._parse_primary_package._parse_primary_src._parse_primary",
            return_value=expected_primary
        ) as mock_parse_primary:
            result = _parse_unary(parser_state)
            self.assertEqual(result, expected_primary)
            mock_parse_primary.assert_called_once_with(parser_state)

    def test_triple_nested_unary_operators(self):
        """Test parsing triple nested unary operators: ---x."""
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 2},
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4}
            ],
            "pos": 0,
            "filename": "test.txt"
        }

        # Expected: -(-(-x))
        innermost = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4}
        inner_unary = {
            "type": "UNARY_OP",
            "children": [innermost],
            "value": "-",
            "line": 1,
            "column": 3
        }
        middle_unary = {
            "type": "UNARY_OP",
            "children": [inner_unary],
            "value": "-",
            "line": 1,
            "column": 2
        }
        expected_result = {
            "type": "UNARY_OP",
            "children": [middle_unary],
            "value": "-",
            "line": 1,
            "column": 1
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_unary_package._consume_token_package._consume_token_src._consume_token",
            side_effect=[
                parser_state["tokens"][0],
                parser_state["tokens"][1],
                parser_state["tokens"][2]
            ]
        ) as mock_consume:
            with patch(
                "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_unary_package._parse_primary_package._parse_primary_src._parse_primary",
                return_value=innermost
            ) as mock_parse_primary:
                result = _parse_unary(parser_state)
                self.assertEqual(result, expected_result)
                self.assertEqual(mock_consume.call_count, 3)


if __name__ == "__main__":
    unittest.main()
