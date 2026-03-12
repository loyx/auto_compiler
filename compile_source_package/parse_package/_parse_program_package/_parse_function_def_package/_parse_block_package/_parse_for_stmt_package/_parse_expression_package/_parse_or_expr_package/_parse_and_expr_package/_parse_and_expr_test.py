import unittest
from unittest.mock import patch

from ._parse_and_expr_src import _parse_and_expr


class TestParseAndExpr(unittest.TestCase):
    """Tests for _parse_and_expr function."""

    def test_single_not_expr_no_and(self):
        """Test parsing a single not_expr without any 'and' operators."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        mock_not_expr_result = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }

        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_not_expr_package._parse_not_expr_src._parse_not_expr') as mock_parse_not_expr:
            mock_parse_not_expr.return_value = mock_not_expr_result

            result = _parse_and_expr(parser_state)

            self.assertEqual(result, mock_not_expr_result)
            mock_parse_not_expr.assert_called_once_with(parser_state)
            self.assertEqual(parser_state["pos"], 0)

    def test_two_not_exprs_with_and(self):
        """Test parsing two not_exprs connected by 'and'."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "AND", "value": "and", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 7}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        left_expr = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        right_expr = {
            "type": "IDENTIFIER",
            "value": "y",
            "line": 1,
            "column": 7
        }

        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_not_expr_package._parse_not_expr_src._parse_not_expr') as mock_parse_not_expr:
            mock_parse_not_expr.side_effect = [left_expr, right_expr]

            result = _parse_and_expr(parser_state)

            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "and")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0], left_expr)
            self.assertEqual(result["children"][1], right_expr)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(parser_state["pos"], 3)
            self.assertEqual(mock_parse_not_expr.call_count, 2)

    def test_three_not_exprs_left_associative(self):
        """Test parsing three not_exprs with 'and' operators (left-associative)."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "AND", "value": "and", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 7},
                {"type": "AND", "value": "and", "line": 1, "column": 9},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 13}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        expr_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        expr_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 7}
        expr_c = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 13}

        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_not_expr_package._parse_not_expr_src._parse_not_expr') as mock_parse_not_expr:
            mock_parse_not_expr.side_effect = [expr_a, expr_b, expr_c]

            result = _parse_and_expr(parser_state)

            # Verify left-associative structure: (a and b) and c
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "and")
            self.assertEqual(len(result["children"]), 2)

            # Left child should be (a and b)
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["value"], "and")
            self.assertEqual(left_child["children"][0], expr_a)
            self.assertEqual(left_child["children"][1], expr_b)

            # Right child should be c
            self.assertEqual(result["children"][1], expr_c)
            self.assertEqual(parser_state["pos"], 5)
            self.assertEqual(mock_parse_not_expr.call_count, 3)

    def test_empty_tokens(self):
        """Test parsing with empty tokens list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }

        mock_not_expr_result = {
            "type": "LITERAL",
            "value": None,
            "line": 0,
            "column": 0
        }

        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_not_expr_package._parse_not_expr_src._parse_not_expr') as mock_parse_not_expr:
            mock_parse_not_expr.return_value = mock_not_expr_result

            result = _parse_and_expr(parser_state)

            self.assertEqual(result, mock_not_expr_result)
            self.assertEqual(parser_state["pos"], 0)

    def test_pos_at_end_of_tokens(self):
        """Test parsing when pos is already at end of tokens."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 1,  # Already at end
            "filename": "test.py"
        }

        mock_not_expr_result = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }

        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_not_expr_package._parse_not_expr_src._parse_not_expr') as mock_parse_not_expr:
            mock_parse_not_expr.return_value = mock_not_expr_result

            result = _parse_and_expr(parser_state)

            self.assertEqual(result, mock_not_expr_result)
            self.assertEqual(parser_state["pos"], 1)

    def test_missing_tokens_in_parser_state(self):
        """Test parsing when tokens key is missing from parser_state."""
        parser_state = {
            "pos": 0,
            "filename": "test.py"
        }

        mock_not_expr_result = {
            "type": "LITERAL",
            "value": None,
            "line": 0,
            "column": 0
        }

        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_not_expr_package._parse_not_expr_src._parse_not_expr') as mock_parse_not_expr:
            mock_parse_not_expr.return_value = mock_not_expr_result

            result = _parse_and_expr(parser_state)

            self.assertEqual(result, mock_not_expr_result)

    def test_and_token_line_column_in_ast(self):
        """Test that AST node uses line/column from 'and' token."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 5, "column": 10},
                {"type": "AND", "value": "and", "line": 5, "column": 12},
                {"type": "IDENTIFIER", "value": "y", "line": 5, "column": 16}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        left_expr = {"type": "IDENTIFIER", "value": "x", "line": 5, "column": 10}
        right_expr = {"type": "IDENTIFIER", "value": "y", "line": 5, "column": 16}

        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_not_expr_package._parse_not_expr_src._parse_not_expr') as mock_parse_not_expr:
            mock_parse_not_expr.side_effect = [left_expr, right_expr]

            result = _parse_and_expr(parser_state)

            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 12)

    def test_not_expr_raises_exception(self):
        """Test that exception from _parse_not_expr is propagated."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_not_expr_package._parse_not_expr_src._parse_not_expr') as mock_parse_not_expr:
            mock_parse_not_expr.side_effect = ValueError("Parse error")

            with self.assertRaises(ValueError):
                _parse_and_expr(parser_state)


if __name__ == '__main__':
    unittest.main()
