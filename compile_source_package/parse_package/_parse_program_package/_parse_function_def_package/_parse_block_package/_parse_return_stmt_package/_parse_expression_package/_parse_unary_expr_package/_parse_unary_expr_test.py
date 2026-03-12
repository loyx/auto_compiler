import unittest
from unittest.mock import patch

from ._parse_unary_expr_src import _parse_unary_expr


class TestParseUnaryExpr(unittest.TestCase):
    """Test cases for _parse_unary_expr function."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_primary_expr_result = {
            "type": "IDENTIFIER",
            "value": "x",
            "children": [],
            "line": 1,
            "column": 2
        }

    def test_parse_unary_minus(self):
        """Test parsing unary minus operator."""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.c"
        }

        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = self.mock_primary_expr_result

            result = _parse_unary_expr(parser_state)

            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(result["children"], [self.mock_primary_expr_result])
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(parser_state["pos"], 1)
            mock_primary.assert_called_once()

    def test_parse_unary_not(self):
        """Test parsing unary not operator."""
        parser_state = {
            "tokens": [
                {"type": "NOT", "value": "!", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.c"
        }

        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = self.mock_primary_expr_result

            result = _parse_unary_expr(parser_state)

            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "!")
            self.assertEqual(result["children"], [self.mock_primary_expr_result])
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(parser_state["pos"], 1)

    def test_parse_chained_unary_minus(self):
        """Test parsing chained unary minus operators (--x)."""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1},
                {"type": "MINUS", "value": "-", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.c"
        }

        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = self.mock_primary_expr_result

            result = _parse_unary_expr(parser_state)

            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)

            child = result["children"][0]
            self.assertEqual(child["type"], "UNARY_OP")
            self.assertEqual(child["value"], "-")
            self.assertEqual(child["children"], [self.mock_primary_expr_result])
            self.assertEqual(parser_state["pos"], 2)

    def test_parse_chained_unary_not(self):
        """Test parsing chained unary not operators (!!x)."""
        parser_state = {
            "tokens": [
                {"type": "NOT", "value": "!", "line": 1, "column": 1},
                {"type": "NOT", "value": "!", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.c"
        }

        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = self.mock_primary_expr_result

            result = _parse_unary_expr(parser_state)

            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "!")

            child = result["children"][0]
            self.assertEqual(child["type"], "UNARY_OP")
            self.assertEqual(child["value"], "!")
            self.assertEqual(child["children"], [self.mock_primary_expr_result])

    def test_parse_mixed_unary_operators(self):
        """Test parsing mixed unary operators (-!x)."""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1},
                {"type": "NOT", "value": "!", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.c"
        }

        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = self.mock_primary_expr_result

            result = _parse_unary_expr(parser_state)

            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")

            child = result["children"][0]
            self.assertEqual(child["type"], "UNARY_OP")
            self.assertEqual(child["value"], "!")
            self.assertEqual(child["children"], [self.mock_primary_expr_result])

    def test_no_tokens_left(self):
        """Test when position is beyond token list length."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 1,
            "filename": "test.c"
        }

        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = self.mock_primary_expr_result

            result = _parse_unary_expr(parser_state)

            mock_primary.assert_called_once_with(parser_state)
            self.assertEqual(result, self.mock_primary_expr_result)

    def test_current_token_not_unary_operator(self):
        """Test when current token is not a unary operator."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }

        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = self.mock_primary_expr_result

            result = _parse_unary_expr(parser_state)

            mock_primary.assert_called_once_with(parser_state)
            self.assertEqual(result, self.mock_primary_expr_result)

    def test_empty_token_list(self):
        """Test with empty token list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c"
        }

        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = self.mock_primary_expr_result

            result = _parse_unary_expr(parser_state)

            mock_primary.assert_called_once_with(parser_state)
            self.assertEqual(result, self.mock_primary_expr_result)

    def test_unary_operator_line_column_preserved(self):
        """Test that line and column information is preserved in AST node."""
        parser_state = {
            "tokens": [
                {"type": "NOT", "value": "!", "line": 5, "column": 10},
                {"type": "IDENTIFIER", "value": "flag", "line": 5, "column": 11}
            ],
            "pos": 0,
            "filename": "test.c"
        }

        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = self.mock_primary_expr_result

            result = _parse_unary_expr(parser_state)

            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 10)

    def test_token_without_type_field(self):
        """Test handling of token without type field."""
        parser_state = {
            "tokens": [
                {"value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }

        with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = self.mock_primary_expr_result

            result = _parse_unary_expr(parser_state)

            mock_primary.assert_called_once_with(parser_state)
            self.assertEqual(result, self.mock_primary_expr_result)


if __name__ == "__main__":
    unittest.main()
