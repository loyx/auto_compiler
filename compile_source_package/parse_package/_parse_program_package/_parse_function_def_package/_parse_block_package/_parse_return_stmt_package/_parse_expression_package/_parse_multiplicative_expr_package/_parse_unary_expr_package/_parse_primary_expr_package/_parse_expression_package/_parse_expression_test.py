import unittest
from unittest.mock import patch


class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""

    def test_parse_expression_delegates_to_or_expr(self):
        """Test that _parse_expression delegates to _parse_or_expr."""
        from ._parse_expression_src import _parse_expression

        mock_parser_state = {
            "tokens": [{"type": "NUMBER", "value": "42", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py"
        }

        expected_ast = {
            "type": "NUMBER",
            "value": 42,
            "line": 1,
            "column": 1
        }

        with patch("._parse_or_expr_package._parse_or_expr_src._parse_or_expr") as mock_or_expr:
            mock_or_expr.return_value = expected_ast

            result = _parse_expression(mock_parser_state)

            mock_or_expr.assert_called_once_with(mock_parser_state)
            self.assertEqual(result, expected_ast)

    def test_parse_expression_propagates_exception(self):
        """Test that _parse_expression propagates exceptions from _parse_or_expr."""
        from ._parse_expression_src import _parse_expression

        mock_parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }

        with patch("._parse_or_expr_package._parse_or_expr_src._parse_or_expr") as mock_or_expr:
            mock_or_expr.side_effect = SyntaxError("Unexpected end of input")

            with self.assertRaises(SyntaxError) as context:
                _parse_expression(mock_parser_state)

            self.assertEqual(str(context.exception), "Unexpected end of input")
            mock_or_expr.assert_called_once_with(mock_parser_state)

    def test_parse_expression_with_complex_expression(self):
        """Test _parse_expression with a complex expression token sequence."""
        from ._parse_expression_src import _parse_expression

        mock_parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py"
        }

        expected_ast = {
            "type": "BINARY_OP",
            "operator": "+",
            "left": {"type": "NUMBER", "value": 1, "line": 1, "column": 1},
            "right": {"type": "NUMBER", "value": 2, "line": 1, "column": 5},
            "line": 1,
            "column": 1
        }

        with patch("._parse_or_expr_package._parse_or_expr_src._parse_or_expr") as mock_or_expr:
            mock_or_expr.return_value = expected_ast

            result = _parse_expression(mock_parser_state)

            mock_or_expr.assert_called_once_with(mock_parser_state)
            self.assertEqual(result, expected_ast)

    def test_parse_expression_with_logical_operators(self):
        """Test _parse_expression with logical operators (OR, AND)."""
        from ._parse_expression_src import _parse_expression

        mock_parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OR", "value": "or", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6},
            ],
            "pos": 0,
            "filename": "test.py"
        }

        expected_ast = {
            "type": "BINARY_OP",
            "operator": "or",
            "left": {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            "right": {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6},
            "line": 1,
            "column": 1
        }

        with patch("._parse_or_expr_package._parse_or_expr_src._parse_or_expr") as mock_or_expr:
            mock_or_expr.return_value = expected_ast

            result = _parse_expression(mock_parser_state)

            mock_or_expr.assert_called_once_with(mock_parser_state)
            self.assertEqual(result, expected_ast)

    def test_parse_expression_modifies_parser_state_pos(self):
        """Test that _parse_expression allows _parse_or_expr to modify parser_state pos."""
        from ._parse_expression_src import _parse_expression

        mock_parser_state = {
            "tokens": [{"type": "NUMBER", "value": "42", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py"
        }

        def side_effect(state):
            state["pos"] = 1
            return {"type": "NUMBER", "value": 42, "line": 1, "column": 1}

        with patch("._parse_or_expr_package._parse_or_expr_src._parse_or_expr") as mock_or_expr:
            mock_or_expr.side_effect = side_effect

            result = _parse_expression(mock_parser_state)

            self.assertEqual(mock_parser_state["pos"], 1)
            self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
