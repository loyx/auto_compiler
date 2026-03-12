"""
Unit tests for _parse_expression function.
Tests assignment expressions, delegation to _parse_or, and error handling.
"""

import unittest
from unittest.mock import patch

from ._parse_expression_src import _parse_expression


class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""

    def test_assignment_expression(self):
        """Test parsing assignment expression: identifier = expression"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "ASSIGN", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.c",
        }

        # Mock _consume_token to return updated parser_state
        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_while_stmt_package."
            "_parse_block_package._parse_var_decl_package._parse_expression_package."
            "_parse_expression_src._consume_token"
        ) as mock_consume:
            # Mock _parse_or for the RHS expression
            with patch(
                "main_package.compile_source_package.parse_package._parse_program_package."
                "_parse_function_def_package._parse_block_package._parse_while_stmt_package."
                "_parse_block_package._parse_var_decl_package._parse_expression_package."
                "_parse_expression_src._parse_or"
            ) as mock_parse_or:
                # Setup mock consume to advance position
                mock_consume.side_effect = lambda state, expected: {
                    **state,
                    "pos": state["pos"] + 1,
                }
                # Setup mock _parse_or to return RHS AST
                mock_parse_or.return_value = (
                    {"type": "NUMBER", "value": "42", "children": [], "line": 1, "column": 5},
                    {"pos": 2, "tokens": parser_state["tokens"], "filename": "test.c"},
                )

                result = _parse_expression(parser_state)

                # Verify result structure
                self.assertEqual(result["type"], "ASSIGN")
                self.assertEqual(result["value"], "x")
                self.assertEqual(result["line"], 1)
                self.assertEqual(result["column"], 1)
                self.assertEqual(len(result["children"]), 1)
                self.assertEqual(result["children"][0]["type"], "NUMBER")

                # Verify _consume_token was called twice (IDENTIFIER and ASSIGN)
                self.assertEqual(mock_consume.call_count, 2)
                mock_consume.assert_any_call(parser_state, "IDENTIFIER")
                mock_consume.assert_any_call(
                    {"pos": 1, "tokens": parser_state["tokens"], "filename": "test.c"},
                    "ASSIGN",
                )

                # Verify _parse_or was called for RHS
                mock_parse_or.assert_called_once()

    def test_non_assignment_expression(self):
        """Test parsing non-assignment expression (delegates to _parse_or)"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.c",
        }

        expected_ast = {
            "type": "NUMBER",
            "value": "42",
            "children": [],
            "line": 1,
            "column": 1,
        }
        updated_state = {**parser_state, "pos": 1}

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_while_stmt_package."
            "_parse_block_package._parse_var_decl_package._parse_expression_package."
            "_parse_expression_src._parse_or"
        ) as mock_parse_or:
            mock_parse_or.return_value = (expected_ast, updated_state)

            result = _parse_expression(parser_state)

            self.assertEqual(result, expected_ast)
            mock_parse_or.assert_called_once_with(parser_state)

    def test_identifier_not_assignment(self):
        """Test identifier not followed by ASSIGN delegates to _parse_or"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
            ],
            "pos": 0,
            "filename": "test.c",
        }

        expected_ast = {
            "type": "IDENTIFIER",
            "value": "x",
            "children": [],
            "line": 1,
            "column": 1,
        }
        updated_state = {**parser_state, "pos": 1}

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_while_stmt_package."
            "_parse_block_package._parse_var_decl_package._parse_expression_package."
            "_parse_expression_src._parse_or"
        ) as mock_parse_or:
            mock_parse_or.return_value = (expected_ast, updated_state)

            result = _parse_expression(parser_state)

            self.assertEqual(result, expected_ast)
            mock_parse_or.assert_called_once_with(parser_state)

    def test_end_of_input_raises_error(self):
        """Test that empty token list raises SyntaxError"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c",
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_position_beyond_tokens_raises_error(self):
        """Test that position beyond token list raises SyntaxError"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
            ],
            "pos": 5,  # Beyond token list
            "filename": "test.c",
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_nested_assignment_expression(self):
        """Test nested assignment: x = y = 5"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "ASSIGN", "value": "=", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 5},
                {"type": "ASSIGN", "value": "=", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 9},
            ],
            "pos": 0,
            "filename": "test.c",
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_while_stmt_package."
            "_parse_block_package._parse_var_decl_package._parse_expression_package."
            "_parse_expression_src._consume_token"
        ) as mock_consume:
            with patch(
                "main_package.compile_source_package.parse_package._parse_program_package."
                "_parse_function_def_package._parse_block_package._parse_while_stmt_package."
                "_parse_block_package._parse_var_decl_package._parse_expression_package."
                "_parse_expression_src._parse_or"
            ) as mock_parse_or:
                mock_consume.side_effect = lambda state, expected: {
                    **state,
                    "pos": state["pos"] + 1,
                }

                # Inner assignment AST (y = 5)
                inner_ast = {
                    "type": "ASSIGN",
                    "value": "y",
                    "children": [{"type": "NUMBER", "value": "5", "children": [], "line": 1, "column": 9}],
                    "line": 1,
                    "column": 5,
                }
                mock_parse_or.return_value = (inner_ast, {"pos": 4, "tokens": parser_state["tokens"], "filename": "test.c"})

                result = _parse_expression(parser_state)

                self.assertEqual(result["type"], "ASSIGN")
                self.assertEqual(result["value"], "x")
                self.assertEqual(result["children"][0]["type"], "ASSIGN")
                self.assertEqual(result["children"][0]["value"], "y")

    def test_complex_expression_delegation(self):
        """Test complex expression like a + b * c delegates to _parse_or"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "STAR", "value": "*", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9},
            ],
            "pos": 0,
            "filename": "test.c",
        }

        expected_ast = {
            "type": "BINARY_OP",
            "value": "+",
            "children": [
                {"type": "IDENTIFIER", "value": "a", "children": [], "line": 1, "column": 1},
                {
                    "type": "BINARY_OP",
                    "value": "*",
                    "children": [
                        {"type": "IDENTIFIER", "value": "b", "children": [], "line": 1, "column": 5},
                        {"type": "IDENTIFIER", "value": "c", "children": [], "line": 1, "column": 9},
                    ],
                    "line": 1,
                    "column": 7,
                },
            ],
            "line": 1,
            "column": 3,
        }
        updated_state = {**parser_state, "pos": 5}

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_while_stmt_package."
            "_parse_block_package._parse_var_decl_package._parse_expression_package."
            "_parse_expression_src._parse_or"
        ) as mock_parse_or:
            mock_parse_or.return_value = (expected_ast, updated_state)

            result = _parse_expression(parser_state)

            self.assertEqual(result, expected_ast)
            mock_parse_or.assert_called_once_with(parser_state)


if __name__ == "__main__":
    unittest.main()
