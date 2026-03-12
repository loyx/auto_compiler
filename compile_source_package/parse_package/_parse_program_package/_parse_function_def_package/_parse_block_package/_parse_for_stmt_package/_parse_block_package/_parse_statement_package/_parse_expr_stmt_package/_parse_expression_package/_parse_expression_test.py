#!/usr/bin/env python3
"""Unit tests for _parse_expression function."""

import unittest
from unittest.mock import patch
from typing import Dict, Any

# Relative import from the same package
from ._parse_expression_src import _parse_expression


class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""

    def test_parse_expression_delegates_to_or_expression(self):
        """Test that _parse_expression delegates to _parse_or_expression."""
        mock_parser_state: Dict[str, Any] = {
            "tokens": [{"type": "NUMBER", "value": "42", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.src"
        }
        mock_result: Dict[str, Any] = {
            "type": "LITERAL",
            "value": 42,
            "line": 1,
            "column": 1
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_or_expression_package._parse_or_expression_src._parse_or_expression") as mock_or_expr:
            mock_or_expr.return_value = mock_result

            result = _parse_expression(mock_parser_state)

            mock_or_expr.assert_called_once_with(mock_parser_state)
            self.assertEqual(result, mock_result)

    def test_parse_expression_returns_or_expression_result(self):
        """Test that _parse_expression returns the result from _parse_or_expression."""
        mock_parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OR", "value": "||", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        expected_result: Dict[str, Any] = {
            "type": "BINARY_OP",
            "operator": "||",
            "left": {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            "right": {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 6},
            "line": 1,
            "column": 1
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_or_expression_package._parse_or_expression_src._parse_or_expression") as mock_or_expr:
            mock_or_expr.return_value = expected_result

            result = _parse_expression(mock_parser_state)

            self.assertEqual(result, expected_result)

    def test_parse_expression_propagates_syntax_error(self):
        """Test that _parse_expression propagates SyntaxError from _parse_or_expression."""
        mock_parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "OR", "value": "||", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.src"
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_or_expression_package._parse_or_expression_src._parse_or_expression") as mock_or_expr:
            mock_or_expr.side_effect = SyntaxError("Unexpected token '||' at line 1, column 1")

            with self.assertRaises(SyntaxError) as context:
                _parse_expression(mock_parser_state)

            self.assertIn("Unexpected token", str(context.exception))
            mock_or_expr.assert_called_once_with(mock_parser_state)

    def test_parse_expression_with_empty_tokens(self):
        """Test _parse_expression with empty token list."""
        mock_parser_state: Dict[str, Any] = {
            "tokens": [],
            "pos": 0,
            "filename": "test.src"
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_or_expression_package._parse_or_expression_src._parse_or_expression") as mock_or_expr:
            mock_or_expr.side_effect = SyntaxError("Unexpected end of input")

            with self.assertRaises(SyntaxError):
                _parse_expression(mock_parser_state)

    def test_parse_expression_with_complex_expression(self):
        """Test _parse_expression with a complex nested expression."""
        mock_parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "STAR", "value": "*", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        expected_result: Dict[str, Any] = {
            "type": "BINARY_OP",
            "operator": "+",
            "left": {"type": "LITERAL", "value": 1, "line": 1, "column": 1},
            "right": {
                "type": "BINARY_OP",
                "operator": "*",
                "left": {"type": "LITERAL", "value": 2, "line": 1, "column": 5},
                "right": {"type": "LITERAL", "value": 3, "line": 1, "column": 9},
                "line": 1,
                "column": 7
            },
            "line": 1,
            "column": 1
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_or_expression_package._parse_or_expression_src._parse_or_expression") as mock_or_expr:
            mock_or_expr.return_value = expected_result

            result = _parse_expression(mock_parser_state)

            self.assertEqual(result, expected_result)
            mock_or_expr.assert_called_once_with(mock_parser_state)

    def test_parse_expression_updates_position(self):
        """Test that parser_state position is updated after parsing."""
        mock_parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.src"
        }

        def update_pos(state: Dict[str, Any]) -> Dict[str, Any]:
            state["pos"] = 1
            return {"type": "LITERAL", "value": 42, "line": 1, "column": 1}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_or_expression_package._parse_or_expression_src._parse_or_expression") as mock_or_expr:
            mock_or_expr.side_effect = update_pos

            result = _parse_expression(mock_parser_state)

            self.assertEqual(mock_parser_state["pos"], 1)
            self.assertIsNotNone(result)

    def test_parse_expression_with_function_call(self):
        """Test _parse_expression with a function call expression."""
        mock_parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "foo", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 4},
                {"type": "NUMBER", "value": "1", "line": 1, "column": 5},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        expected_result: Dict[str, Any] = {
            "type": "CALL",
            "function": {"type": "IDENTIFIER", "value": "foo", "line": 1, "column": 1},
            "arguments": [{"type": "LITERAL", "value": 1, "line": 1, "column": 5}],
            "line": 1,
            "column": 1
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_or_expression_package._parse_or_expression_src._parse_or_expression") as mock_or_expr:
            mock_or_expr.return_value = expected_result

            result = _parse_expression(mock_parser_state)

            self.assertEqual(result, expected_result)

    def test_parse_expression_with_member_access(self):
        """Test _parse_expression with member access expression."""
        mock_parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "obj", "line": 1, "column": 1},
                {"type": "DOT", "value": ".", "line": 1, "column": 4},
                {"type": "IDENTIFIER", "value": "prop", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        expected_result: Dict[str, Any] = {
            "type": "ACCESS",
            "object": {"type": "IDENTIFIER", "value": "obj", "line": 1, "column": 1},
            "property": "prop",
            "line": 1,
            "column": 1
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_or_expression_package._parse_or_expression_src._parse_or_expression") as mock_or_expr:
            mock_or_expr.return_value = expected_result

            result = _parse_expression(mock_parser_state)

            self.assertEqual(result, expected_result)

    def test_parse_expression_with_unary_operator(self):
        """Test _parse_expression with unary operator."""
        mock_parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        expected_result: Dict[str, Any] = {
            "type": "UNARY_OP",
            "operator": "-",
            "operand": {"type": "LITERAL", "value": 5, "line": 1, "column": 2},
            "line": 1,
            "column": 1
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_or_expression_package._parse_or_expression_src._parse_or_expression") as mock_or_expr:
            mock_or_expr.return_value = expected_result

            result = _parse_expression(mock_parser_state)

            self.assertEqual(result, expected_result)

    def test_parse_expression_preserves_parser_state_reference(self):
        """Test that _parse_expression passes the same parser_state object reference."""
        mock_parser_state: Dict[str, Any] = {
            "tokens": [{"type": "NUMBER", "value": "1", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.src"
        }
        mock_result: Dict[str, Any] = {"type": "LITERAL", "value": 1, "line": 1, "column": 1}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_or_expression_package._parse_or_expression_src._parse_or_expression") as mock_or_expr:
            mock_or_expr.return_value = mock_result

            _parse_expression(mock_parser_state)

            # Verify the same object reference was passed
            call_args = mock_or_expr.call_args[0][0]
            self.assertIs(call_args, mock_parser_state)


if __name__ == "__main__":
    unittest.main()
