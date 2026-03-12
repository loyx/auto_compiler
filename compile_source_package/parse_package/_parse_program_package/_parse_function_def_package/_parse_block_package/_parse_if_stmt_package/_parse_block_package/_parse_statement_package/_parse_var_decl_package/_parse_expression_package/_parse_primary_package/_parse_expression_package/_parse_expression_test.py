"""Unit tests for _parse_expression function."""

import unittest
from unittest.mock import patch

from ._parse_expression_src import _parse_expression


class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""

    def test_delegates_to_parse_or_expression(self):
        """Test that _parse_expression delegates to _parse_or_expression."""
        mock_parser_state = {
            "tokens": [{"type": "NUMBER", "value": "42", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.c",
        }
        expected_ast = {
            "type": "literal",
            "value": 42,
            "line": 1,
            "column": 1,
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_var_decl_package._parse_expression_package._parse_primary_package._parse_expression_package._parse_or_expression_package._parse_or_expression_src._parse_or_expression"
        ) as mock_parse_or:
            mock_parse_or.return_value = expected_ast

            result = _parse_expression(mock_parser_state)

            mock_parse_or.assert_called_once_with(mock_parser_state)
            self.assertEqual(result, expected_ast)

    def test_returns_ast_from_or_expression(self):
        """Test that _parse_expression returns the AST from _parse_or_expression."""
        mock_parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "1", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.c",
        }
        expected_ast = {
            "type": "binary_op",
            "operator": "+",
            "left": {"type": "identifier", "value": "x", "line": 1, "column": 1},
            "right": {"type": "literal", "value": 1, "line": 1, "column": 5},
            "line": 1,
            "column": 1,
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_var_decl_package._parse_expression_package._parse_primary_package._parse_expression_package._parse_or_expression_package._parse_or_expression_src._parse_or_expression"
        ) as mock_parse_or:
            mock_parse_or.return_value = expected_ast

            result = _parse_expression(mock_parser_state)

            self.assertEqual(result, expected_ast)
            self.assertEqual(result["type"], "binary_op")
            self.assertEqual(result["operator"], "+")

    def test_handles_unary_expression(self):
        """Test expression with unary operator."""
        mock_parser_state = {
            "tokens": [
                {"type": "NOT", "value": "!", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "flag", "line": 1, "column": 2},
            ],
            "pos": 0,
            "filename": "test.c",
        }
        expected_ast = {
            "type": "unary_op",
            "operator": "!",
            "operand": {"type": "identifier", "value": "flag", "line": 1, "column": 2},
            "line": 1,
            "column": 1,
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_var_decl_package._parse_expression_package._parse_primary_package._parse_expression_package._parse_or_expression_package._parse_or_expression_src._parse_or_expression"
        ) as mock_parse_or:
            mock_parse_or.return_value = expected_ast

            result = _parse_expression(mock_parser_state)

            self.assertEqual(result["type"], "unary_op")
            self.assertEqual(result["operator"], "!")

    def test_handles_complex_expression(self):
        """Test complex expression with multiple operators."""
        mock_parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "MULTIPLY", "value": "*", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 9},
            ],
            "pos": 0,
            "filename": "test.c",
        }
        expected_ast = {
            "type": "binary_op",
            "operator": "+",
            "left": {"type": "literal", "value": 1, "line": 1, "column": 1},
            "right": {
                "type": "binary_op",
                "operator": "*",
                "left": {"type": "literal", "value": 2, "line": 1, "column": 5},
                "right": {"type": "literal", "value": 3, "line": 1, "column": 9},
                "line": 1,
                "column": 5,
            },
            "line": 1,
            "column": 1,
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_var_decl_package._parse_expression_package._parse_primary_package._parse_expression_package._parse_or_expression_package._parse_or_expression_src._parse_or_expression"
        ) as mock_parse_or:
            mock_parse_or.return_value = expected_ast

            result = _parse_expression(mock_parser_state)

            self.assertEqual(result["type"], "binary_op")
            self.assertEqual(result["operator"], "+")
            self.assertEqual(result["right"]["operator"], "*")

    def test_handles_logical_expression(self):
        """Test expression with logical operators."""
        mock_parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "AND", "value": "&&", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6},
                {"type": "OR", "value": "||", "line": 1, "column": 8},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 11},
            ],
            "pos": 0,
            "filename": "test.c",
        }
        expected_ast = {
            "type": "binary_op",
            "operator": "||",
            "left": {
                "type": "binary_op",
                "operator": "&&",
                "left": {"type": "identifier", "value": "a", "line": 1, "column": 1},
                "right": {"type": "identifier", "value": "b", "line": 1, "column": 6},
                "line": 1,
                "column": 1,
            },
            "right": {"type": "identifier", "value": "c", "line": 1, "column": 11},
            "line": 1,
            "column": 1,
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_var_decl_package._parse_expression_package._parse_primary_package._parse_expression_package._parse_or_expression_package._parse_or_expression_src._parse_or_expression"
        ) as mock_parse_or:
            mock_parse_or.return_value = expected_ast

            result = _parse_expression(mock_parser_state)

            self.assertEqual(result["type"], "binary_op")
            self.assertEqual(result["operator"], "||")

    def test_parser_state_position_updated(self):
        """Test that parser_state position is updated by _parse_or_expression."""
        mock_parser_state = {
            "tokens": [{"type": "NUMBER", "value": "123", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.c",
        }

        def side_effect(state):
            state["pos"] = 1
            return {"type": "literal", "value": 123, "line": 1, "column": 1}

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_var_decl_package._parse_expression_package._parse_primary_package._parse_expression_package._parse_or_expression_package._parse_or_expression_src._parse_or_expression"
        ) as mock_parse_or:
            mock_parse_or.side_effect = side_effect

            result = _parse_expression(mock_parser_state)

            self.assertEqual(mock_parser_state["pos"], 1)
            self.assertIsNotNone(result)

    def test_propagates_syntax_error(self):
        """Test that SyntaxError from _parse_or_expression is propagated."""
        mock_parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c",
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_var_decl_package._parse_expression_package._parse_primary_package._parse_expression_package._parse_or_expression_package._parse_or_expression_src._parse_or_expression"
        ) as mock_parse_or:
            mock_parse_or.side_effect = SyntaxError("test.c:1:1: unexpected end of expression")

            with self.assertRaises(SyntaxError) as context:
                _parse_expression(mock_parser_state)

            self.assertIn("unexpected end of expression", str(context.exception))


if __name__ == "__main__":
    unittest.main()
