import unittest
from unittest.mock import patch

# Relative import from the same package
from ._parse_primary_expr_src import _parse_primary_expr


class TestParsePrimaryExpr(unittest.TestCase):
    """Test cases for _parse_primary_expr function."""

    def test_parse_number_literal(self):
        """Test parsing a NUMBER token."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], "42")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)  # Token should be consumed

    def test_parse_identifier(self):
        """Test parsing an IDENTIFIER token."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)  # Token should be consumed

    def test_parse_parenthesized_expression(self):
        """Test parsing a parenthesized expression with LPAREN and RPAREN."""
        mock_unary_result = {
            "type": "NUMBER",
            "value": "10",
            "line": 1,
            "column": 2
        }

        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "10", "line": 1, "column": 2},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.c"
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_if_stmt_package."
            "_parse_expression_package._parse_or_expr_package._parse_and_expr_package."
            "_parse_comparison_expr_package._parse_additive_expr_package."
            "_parse_multiplicative_expr_package._parse_unary_expr_package."
            "_parse_unary_expr_src._parse_unary_expr",
            return_value=mock_unary_result
        ) as mock_unary:
            result = _parse_primary_expr(parser_state)

            mock_unary.assert_called_once()
            self.assertEqual(result, mock_unary_result)
            self.assertEqual(parser_state["pos"], 3)  # All tokens consumed

    def test_unexpected_end_of_input(self):
        """Test that SyntaxError is raised when input ends unexpectedly."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c"
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_missing_closing_parenthesis_end(self):
        """Test that SyntaxError is raised when RPAREN is missing at end."""
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_if_stmt_package."
            "_parse_expression_package._parse_or_expr_package._parse_and_expr_package."
            "_parse_comparison_expr_package._parse_additive_expr_package."
            "_parse_multiplicative_expr_package._parse_unary_expr_package."
            "_parse_primary_expr_package._parse_primary_expr_src._parse_unary_expr",
            return_value={"type": "NUMBER", "value": "5", "line": 1, "column": 2}
        ):
            with self.assertRaises(SyntaxError) as context:
                _parse_primary_expr(parser_state)

            self.assertIn("Missing closing parenthesis", str(context.exception))

    def test_missing_closing_parenthesis_wrong_token(self):
        """Test that SyntaxError is raised when wrong token follows instead of RPAREN."""
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 2},
                {"type": "NUMBER", "value": "6", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.c"
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_if_stmt_package."
            "_parse_expression_package._parse_or_expr_package._parse_and_expr_package."
            "_parse_comparison_expr_package._parse_additive_expr_package."
            "_parse_multiplicative_expr_package._parse_unary_expr_package."
            "_parse_primary_expr_package._parse_primary_expr_src._parse_unary_expr",
            return_value={"type": "NUMBER", "value": "5", "line": 1, "column": 2}
        ):
            with self.assertRaises(SyntaxError) as context:
                _parse_primary_expr(parser_state)

            self.assertIn("Missing closing parenthesis", str(context.exception))

    def test_unexpected_token_type(self):
        """Test that SyntaxError is raised for unexpected token types."""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)

        self.assertIn("Unexpected token", str(context.exception))
        self.assertIn("+", str(context.exception))

    def test_number_with_decimal(self):
        """Test parsing a NUMBER token with decimal point."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "3.14", "line": 2, "column": 5}
            ],
            "pos": 0,
            "filename": "test.c"
        }

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], "3.14")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)

    def test_identifier_with_underscore(self):
        """Test parsing an IDENTIFIER token with underscore."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "my_var", "line": 3, "column": 10}
            ],
            "pos": 0,
            "filename": "test.c"
        }

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "my_var")
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 10)

    def test_nested_parentheses(self):
        """Test parsing nested parentheses (multiple levels)."""
        inner_result = {
            "type": "NUMBER",
            "value": "7",
            "line": 1,
            "column": 3
        }
        outer_result = {
            "type": "PAREN",
            "operand": inner_result,
            "line": 1,
            "column": 2
        }

        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 2},
                {"type": "NUMBER", "value": "7", "line": 1, "column": 3},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 4},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.c"
        }

        call_count = [0]

        def side_effect(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                # First call (outer parentheses) returns the inner result wrapped
                return inner_result
            else:
                # Second call (inner parentheses) returns the number
                return inner_result

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_if_stmt_package."
            "_parse_expression_package._parse_or_expr_package._parse_and_expr_package."
            "_parse_comparison_expr_package._parse_additive_expr_package."
            "_parse_multiplicative_expr_package._parse_unary_expr_package."
            "_parse_primary_expr_package._parse_primary_expr_src._parse_unary_expr",
            side_effect=side_effect
        ) as mock_unary:
            result = _parse_primary_expr(parser_state)

            self.assertEqual(mock_unary.call_count, 1)
            self.assertEqual(parser_state["pos"], 5)


if __name__ == "__main__":
    unittest.main()
