"""
Unit tests for _parse_expression function.
"""

import unittest
from unittest.mock import patch

# Relative import from the same package
from ._parse_expression_src import _parse_expression


class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""

    def test_parse_expression_delegates_to_or_expr(self):
        """Test that _parse_expression delegates to _parse_or_expr."""
        expected_ast = {
            "type": "BINARY_OP",
            "operator": "or",
            "left": {"type": "LITERAL", "value": True},
            "right": {"type": "LITERAL", "value": False}
        }

        parser_state = {
            "tokens": [{"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py"
        }

        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr', return_value=expected_ast) as mock_parse_or_expr:
            result = _parse_expression(parser_state)

            mock_parse_or_expr.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)

    def test_parse_expression_with_empty_tokens(self):
        """Test _parse_expression with empty token list."""
        expected_ast = {"type": "ERROR", "message": "Empty expression"}

        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }

        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr', return_value=expected_ast) as mock_parse_or_expr:
            result = _parse_expression(parser_state)

            mock_parse_or_expr.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)

    def test_parse_expression_with_number_literal(self):
        """Test _parse_expression with a simple number literal."""
        expected_ast = {"type": "LITERAL", "literal_type": "NUMBER", "value": 42, "line": 1, "column": 1}

        parser_state = {
            "tokens": [{"type": "NUMBER", "value": "42", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py"
        }

        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr', return_value=expected_ast) as mock_parse_or_expr:
            result = _parse_expression(parser_state)

            mock_parse_or_expr.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)

    def test_parse_expression_with_string_literal(self):
        """Test _parse_expression with a string literal."""
        expected_ast = {"type": "LITERAL", "literal_type": "STRING", "value": "hello", "line": 1, "column": 1}

        parser_state = {
            "tokens": [{"type": "STRING", "value": '"hello"', "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py"
        }

        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr', return_value=expected_ast) as mock_parse_or_expr:
            result = _parse_expression(parser_state)

            mock_parse_or_expr.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)

    def test_parse_expression_with_identifier(self):
        """Test _parse_expression with an identifier."""
        expected_ast = {"type": "IDENTIFIER", "name": "x", "line": 1, "column": 1}

        parser_state = {
            "tokens": [{"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py"
        }

        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr', return_value=expected_ast) as mock_parse_or_expr:
            result = _parse_expression(parser_state)

            mock_parse_or_expr.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)

    def test_parse_expression_with_complex_expression(self):
        """Test _parse_expression with complex expression tokens."""
        expected_ast = {
            "type": "BINARY_OP",
            "operator": "+",
            "left": {"type": "LITERAL", "literal_type": "NUMBER", "value": 1},
            "right": {
                "type": "BINARY_OP",
                "operator": "*",
                "left": {"type": "LITERAL", "literal_type": "NUMBER", "value": 2},
                "right": {"type": "LITERAL", "literal_type": "NUMBER", "value": 3}
            }
        }

        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "OPERATOR", "value": "*", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr', return_value=expected_ast) as mock_parse_or_expr:
            result = _parse_expression(parser_state)

            mock_parse_or_expr.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)

    def test_parse_expression_position_updated(self):
        """Test that parser_state position is updated after parsing."""
        def side_effect(state):
            state["pos"] = 5
            return {"type": "LITERAL", "value": 42}

        parser_state = {
            "tokens": [{"type": "NUMBER", "value": "42", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py"
        }

        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr', side_effect=side_effect) as mock_parse_or_expr:
            result = _parse_expression(parser_state)

            self.assertEqual(parser_state["pos"], 5)
            self.assertEqual(result["type"], "LITERAL")
            self.assertEqual(result["value"], 42)
            mock_parse_or_expr.assert_called_once()

    def test_parse_expression_with_bool_literal(self):
        """Test _parse_expression with boolean literal."""
        expected_ast = {"type": "LITERAL", "literal_type": "BOOL", "value": True, "line": 1, "column": 1}

        parser_state = {
            "tokens": [{"type": "KEYWORD", "value": "true", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py"
        }

        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr', return_value=expected_ast) as mock_parse_or_expr:
            result = _parse_expression(parser_state)

            mock_parse_or_expr.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)

    def test_parse_expression_with_none_literal(self):
        """Test _parse_expression with None literal."""
        expected_ast = {"type": "LITERAL", "literal_type": "NONE", "value": None, "line": 1, "column": 1}

        parser_state = {
            "tokens": [{"type": "KEYWORD", "value": "null", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py"
        }

        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr', return_value=expected_ast) as mock_parse_or_expr:
            result = _parse_expression(parser_state)

            mock_parse_or_expr.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)

    def test_parse_expression_preserves_parser_state_reference(self):
        """Test that _parse_expression passes the same parser_state reference."""
        expected_ast = {"type": "LITERAL", "value": 100}

        parser_state = {
            "tokens": [{"type": "NUMBER", "value": "100", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py"
        }

        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr', return_value=expected_ast) as mock_parse_or_expr:
            _parse_expression(parser_state)

            called_state = mock_parse_or_expr.call_args[0][0]
            self.assertIs(called_state, parser_state)


if __name__ == "__main__":
    unittest.main()
