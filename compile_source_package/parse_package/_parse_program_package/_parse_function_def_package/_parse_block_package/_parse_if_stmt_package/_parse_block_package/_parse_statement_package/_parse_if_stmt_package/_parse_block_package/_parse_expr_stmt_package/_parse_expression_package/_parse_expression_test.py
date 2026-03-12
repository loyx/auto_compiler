import unittest
from unittest.mock import patch

# Relative import from the same package
from ._parse_expression_src import _parse_expression


class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""

    def test_parse_expression_delegates_to_parse_or(self):
        """Test that _parse_expression delegates to _parse_or."""
        mock_parser_state = {
            "tokens": [{"type": "NUMBER", "value": "42", "line": 1, "column": 1}],
            "filename": "test.cc",
            "pos": 0
        }

        mock_ast_result = {
            "type": "LITERAL",
            "value": 42,
            "line": 1,
            "column": 1
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_or_src._parse_or") as mock_parse_or:
            mock_parse_or.return_value = mock_ast_result

            result = _parse_expression(mock_parser_state)

            mock_parse_or.assert_called_once_with(mock_parser_state)
            self.assertEqual(result, mock_ast_result)

    def test_parse_expression_with_empty_tokens(self):
        """Test _parse_expression with empty token list."""
        mock_parser_state = {
            "tokens": [],
            "filename": "test.cc",
            "pos": 0
        }

        mock_ast_result = {
            "type": "EMPTY",
            "value": None
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_or_src._parse_or") as mock_parse_or:
            mock_parse_or.return_value = mock_ast_result

            result = _parse_expression(mock_parser_state)

            mock_parse_or.assert_called_once_with(mock_parser_state)
            self.assertEqual(result, mock_ast_result)

    def test_parse_expression_with_complex_expression(self):
        """Test _parse_expression with complex expression tokens."""
        mock_parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 2},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 3}
            ],
            "filename": "test.cc",
            "pos": 0
        }

        mock_ast_result = {
            "type": "BINARY_OP",
            "operator": "+",
            "left": {"type": "IDENTIFIER", "name": "x"},
            "right": {"type": "LITERAL", "value": 5}
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_or_src._parse_or") as mock_parse_or:
            mock_parse_or.return_value = mock_ast_result

            result = _parse_expression(mock_parser_state)

            mock_parse_or.assert_called_once_with(mock_parser_state)
            self.assertEqual(result, mock_ast_result)

    def test_parse_expression_propagates_syntax_error(self):
        """Test that _parse_expression propagates SyntaxError from _parse_or."""
        mock_parser_state = {
            "tokens": [{"type": "INVALID", "value": "@", "line": 1, "column": 1}],
            "filename": "test.cc",
            "pos": 0
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_or_src._parse_or") as mock_parse_or:
            mock_parse_or.side_effect = SyntaxError("Invalid token at line 1")

            with self.assertRaises(SyntaxError) as context:
                _parse_expression(mock_parser_state)

            self.assertEqual(str(context.exception), "Invalid token at line 1")
            mock_parse_or.assert_called_once_with(mock_parser_state)

    def test_parse_expression_with_pos_not_at_zero(self):
        """Test _parse_expression when pos is not at the start of tokens."""
        mock_parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "if", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "1", "line": 1, "column": 4}
            ],
            "filename": "test.cc",
            "pos": 2
        }

        mock_ast_result = {
            "type": "LITERAL",
            "value": 1,
            "line": 1,
            "column": 4
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_or_src._parse_or") as mock_parse_or:
            mock_parse_or.return_value = mock_ast_result

            result = _parse_expression(mock_parser_state)

            mock_parse_or.assert_called_once_with(mock_parser_state)
            self.assertEqual(result, mock_ast_result)

    def test_parse_expression_preserves_parser_state_mutation(self):
        """Test that parser_state mutations by _parse_or are preserved."""
        mock_parser_state = {
            "tokens": [{"type": "NUMBER", "value": "42", "line": 1, "column": 1}],
            "filename": "test.cc",
            "pos": 0
        }

        def mutate_state(state):
            state["pos"] = 1
            return {"type": "LITERAL", "value": 42}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_or_src._parse_or") as mock_parse_or:
            mock_parse_or.side_effect = mutate_state

            result = _parse_expression(mock_parser_state)

            self.assertEqual(mock_parser_state["pos"], 1)
            self.assertEqual(result["type"], "LITERAL")
            self.assertEqual(result["value"], 42)


if __name__ == "__main__":
    unittest.main()
