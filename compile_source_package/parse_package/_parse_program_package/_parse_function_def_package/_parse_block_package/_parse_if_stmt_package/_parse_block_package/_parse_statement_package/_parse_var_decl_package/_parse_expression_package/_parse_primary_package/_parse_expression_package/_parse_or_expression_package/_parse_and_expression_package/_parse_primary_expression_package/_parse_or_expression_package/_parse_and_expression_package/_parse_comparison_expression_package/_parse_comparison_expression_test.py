import unittest
from unittest.mock import patch

from ._parse_comparison_expression_src import _parse_comparison_expression


class TestParseComparisonExpression(unittest.TestCase):
    """Test cases for _parse_comparison_expression function."""

    @patch('._parse_additive_expression_package._parse_additive_expression_src._parse_additive_expression')
    def test_parse_less_than(self, mock_parse_additive):
        """Test parsing less than operator."""
        mock_parse_additive.side_effect = [
            {"type": "identifier", "value": "a"},
            {"type": "identifier", "value": "b"}
        ]

        parser_state = {
            "tokens": [
                {"type": "identifier", "value": "a", "line": 1, "column": 1},
                {"type": "operator", "value": "<", "line": 1, "column": 3},
                {"type": "identifier", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 0,
            "error": ""
        }

        result = _parse_comparison_expression(parser_state)

        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["operator"], "lt")
        self.assertEqual(result["left"]["value"], "a")
        self.assertEqual(result["right"]["value"], "b")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)

    @patch('._parse_additive_expression_package._parse_additive_expression_src._parse_additive_expression')
    def test_parse_greater_than(self, mock_parse_additive):
        """Test parsing greater than operator."""
        mock_parse_additive.side_effect = [
            {"type": "identifier", "value": "x"},
            {"type": "number", "value": 10}
        ]

        parser_state = {
            "tokens": [
                {"type": "identifier", "value": "x", "line": 2, "column": 1},
                {"type": "operator", "value": ">", "line": 2, "column": 3},
                {"type": "number", "value": 10, "line": 2, "column": 5}
            ],
            "pos": 0,
            "error": ""
        }

        result = _parse_comparison_expression(parser_state)

        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["operator"], "gt")
        self.assertEqual(result["left"]["value"], "x")
        self.assertEqual(result["right"]["value"], 10)

    @patch('._parse_additive_expression_package._parse_additive_expression_src._parse_additive_expression')
    def test_parse_less_than_or_equal(self, mock_parse_additive):
        """Test parsing less than or equal operator."""
        mock_parse_additive.side_effect = [
            {"type": "identifier", "value": "m"},
            {"type": "identifier", "value": "n"}
        ]

        parser_state = {
            "tokens": [
                {"type": "identifier", "value": "m", "line": 3, "column": 1},
                {"type": "operator", "value": "<=", "line": 3, "column": 3},
                {"type": "identifier", "value": "n", "line": 3, "column": 6}
            ],
            "pos": 0,
            "error": ""
        }

        result = _parse_comparison_expression(parser_state)

        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["operator"], "le")
        self.assertEqual(result["left"]["value"], "m")
        self.assertEqual(result["right"]["value"], "n")

    @patch('._parse_additive_expression_package._parse_additive_expression_src._parse_additive_expression')
    def test_parse_greater_than_or_equal(self, mock_parse_additive):
        """Test parsing greater than or equal operator."""
        mock_parse_additive.side_effect = [
            {"type": "number", "value": 5},
            {"type": "number", "value": 3}
        ]

        parser_state = {
            "tokens": [
                {"type": "number", "value": 5, "line": 4, "column": 1},
                {"type": "operator", "value": ">=", "line": 4, "column": 3},
                {"type": "number", "value": 3, "line": 4, "column": 6}
            ],
            "pos": 0,
            "error": ""
        }

        result = _parse_comparison_expression(parser_state)

        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["operator"], "ge")
        self.assertEqual(result["left"]["value"], 5)
        self.assertEqual(result["right"]["value"], 3)

    @patch('._parse_additive_expression_package._parse_additive_expression_src._parse_additive_expression')
    def test_parse_equal(self, mock_parse_additive):
        """Test parsing equal operator."""
        mock_parse_additive.side_effect = [
            {"type": "identifier", "value": "foo"},
            {"type": "identifier", "value": "bar"}
        ]

        parser_state = {
            "tokens": [
                {"type": "identifier", "value": "foo", "line": 5, "column": 1},
                {"type": "operator", "value": "==", "line": 5, "column": 5},
                {"type": "identifier", "value": "bar", "line": 5, "column": 8}
            ],
            "pos": 0,
            "error": ""
        }

        result = _parse_comparison_expression(parser_state)

        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["operator"], "eq")
        self.assertEqual(result["left"]["value"], "foo")
        self.assertEqual(result["right"]["value"], "bar")

    @patch('._parse_additive_expression_package._parse_additive_expression_src._parse_additive_expression')
    def test_parse_not_equal(self, mock_parse_additive):
        """Test parsing not equal operator."""
        mock_parse_additive.side_effect = [
            {"type": "identifier", "value": "p"},
            {"type": "identifier", "value": "q"}
        ]

        parser_state = {
            "tokens": [
                {"type": "identifier", "value": "p", "line": 6, "column": 1},
                {"type": "operator", "value": "!=", "line": 6, "column": 3},
                {"type": "identifier", "value": "q", "line": 6, "column": 6}
            ],
            "pos": 0,
            "error": ""
        }

        result = _parse_comparison_expression(parser_state)

        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["operator"], "ne")
        self.assertEqual(result["left"]["value"], "p")
        self.assertEqual(result["right"]["value"], "q")

    @patch('._parse_additive_expression_package._parse_additive_expression_src._parse_additive_expression')
    def test_no_comparison_operator(self, mock_parse_additive):
        """Test parsing expression without comparison operator."""
        mock_parse_additive.return_value = {"type": "identifier", "value": "x"}

        parser_state = {
            "tokens": [
                {"type": "identifier", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "error": ""
        }

        result = _parse_comparison_expression(parser_state)

        self.assertEqual(result["type"], "identifier")
        self.assertEqual(result["value"], "x")
        mock_parse_additive.assert_called_once()

    @patch('._parse_additive_expression_package._parse_additive_expression_src._parse_additive_expression')
    def test_error_after_left_parse(self, mock_parse_additive):
        """Test error handling when error occurs after parsing left expression."""
        mock_parse_additive.return_value = {"type": "identifier", "value": "x"}

        parser_state = {
            "tokens": [
                {"type": "identifier", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "error": "some error"
        }

        result = _parse_comparison_expression(parser_state)

        self.assertEqual(result["type"], "identifier")
        self.assertEqual(result["value"], "x")

    @patch('._parse_additive_expression_package._parse_additive_expression_src._parse_additive_expression')
    def test_error_after_right_parse(self, mock_parse_additive):
        """Test error handling when error occurs after parsing right expression."""
        def side_effect(state):
            if state.get("pos") == 0:
                return {"type": "identifier", "value": "a"}
            else:
                state["error"] = "error in right parse"
                return {"type": "identifier", "value": "b"}

        mock_parse_additive.side_effect = side_effect

        parser_state = {
            "tokens": [
                {"type": "identifier", "value": "a", "line": 1, "column": 1},
                {"type": "operator", "value": "<", "line": 1, "column": 3},
                {"type": "identifier", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 0,
            "error": ""
        }

        result = _parse_comparison_expression(parser_state)

        self.assertEqual(result["type"], "identifier")
        self.assertEqual(result["value"], "a")

    @patch('._parse_additive_expression_package._parse_additive_expression_src._parse_additive_expression')
    def test_end_of_tokens(self, mock_parse_additive):
        """Test handling when tokens are exhausted."""
        mock_parse_additive.return_value = {"type": "identifier", "value": "x"}

        parser_state = {
            "tokens": [
                {"type": "identifier", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "error": ""
        }

        result = _parse_comparison_expression(parser_state)

        self.assertEqual(result["type"], "identifier")
        self.assertEqual(result["value"], "x")

    @patch('._parse_additive_expression_package._parse_additive_expression_src._parse_additive_expression')
    def test_position_advancement(self, mock_parse_additive):
        """Test that parser position is advanced correctly."""
        mock_parse_additive.side_effect = [
            {"type": "identifier", "value": "a"},
            {"type": "identifier", "value": "b"}
        ]

        parser_state = {
            "tokens": [
                {"type": "identifier", "value": "a", "line": 1, "column": 1},
                {"type": "operator", "value": "<", "line": 1, "column": 3},
                {"type": "identifier", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 0,
            "error": ""
        }

        result = _parse_comparison_expression(parser_state)

        self.assertEqual(parser_state["pos"], 3)

    @patch('._parse_additive_expression_package._parse_additive_expression_src._parse_additive_expression')
    def test_line_column_preservation(self, mock_parse_additive):
        """Test that line and column information is preserved."""
        mock_parse_additive.side_effect = [
            {"type": "identifier", "value": "x"},
            {"type": "number", "value": 42}
        ]

        parser_state = {
            "tokens": [
                {"type": "identifier", "value": "x", "line": 10, "column": 5},
                {"type": "operator", "value": ">", "line": 10, "column": 7},
                {"type": "number", "value": 42, "line": 10, "column": 9}
            ],
            "pos": 0,
            "error": ""
        }

        result = _parse_comparison_expression(parser_state)

        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 7)

    @patch('._parse_additive_expression_package._parse_additive_expression_src._parse_additive_expression')
    def test_chained_comparisons(self, mock_parse_additive):
        """Test parsing chained comparison operators (left-associative)."""
        mock_parse_additive.side_effect = [
            {"type": "identifier", "value": "a"},
            {"type": "identifier", "value": "b"},
            {"type": "identifier", "value": "c"}
        ]

        parser_state = {
            "tokens": [
                {"type": "identifier", "value": "a", "line": 1, "column": 1},
                {"type": "operator", "value": "<", "line": 1, "column": 3},
                {"type": "identifier", "value": "b", "line": 1, "column": 5},
                {"type": "operator", "value": "<", "line": 1, "column": 7},
                {"type": "identifier", "value": "c", "line": 1, "column": 9}
            ],
            "pos": 0,
            "error": ""
        }

        result = _parse_comparison_expression(parser_state)

        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["operator"], "lt")
        self.assertEqual(result["right"]["value"], "c")
        self.assertEqual(result["left"]["type"], "binary_op")
        self.assertEqual(result["left"]["operator"], "lt")
        self.assertEqual(result["left"]["left"]["value"], "a")
        self.assertEqual(result["left"]["right"]["value"], "b")

    @patch('._parse_additive_expression_package._parse_additive_expression_src._parse_additive_expression')
    def test_mixed_comparison_operators(self, mock_parse_additive):
        """Test parsing mixed comparison operators."""
        mock_parse_additive.side_effect = [
            {"type": "number", "value": 1},
            {"type": "number", "value": 2},
            {"type": "number", "value": 3}
        ]

        parser_state = {
            "tokens": [
                {"type": "number", "value": 1, "line": 1, "column": 1},
                {"type": "operator", "value": "<", "line": 1, "column": 3},
                {"type": "number", "value": 2, "line": 1, "column": 5},
                {"type": "operator", "value": "<=", "line": 1, "column": 7},
                {"type": "number", "value": 3, "line": 1, "column": 10}
            ],
            "pos": 0,
            "error": ""
        }

        result = _parse_comparison_expression(parser_state)

        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["operator"], "le")
        self.assertEqual(result["left"]["operator"], "lt")

    @patch('._parse_additive_expression_package._parse_additive_expression_src._parse_additive_expression')
    def test_empty_tokens(self, mock_parse_additive):
        """Test handling empty token list."""
        mock_parse_additive.return_value = {"type": "empty", "value": None}

        parser_state = {
            "tokens": [],
            "pos": 0,
            "error": ""
        }

        result = _parse_comparison_expression(parser_state)

        self.assertEqual(result["type"], "empty")
        self.assertIsNone(result["value"])

    @patch('._parse_additive_expression_package._parse_additive_expression_src._parse_additive_expression')
    def test_token_without_value_key(self, mock_parse_additive):
        """Test handling token without value key."""
        mock_parse_additive.return_value = {"type": "identifier", "value": "x"}

        parser_state = {
            "tokens": [
                {"type": "identifier", "value": "x", "line": 1, "column": 1},
                {"type": "operator", "line": 1, "column": 3},
            ],
            "pos": 0,
            "error": ""
        }

        result = _parse_comparison_expression(parser_state)

        self.assertEqual(result["type"], "identifier")
        self.assertEqual(result["value"], "x")


if __name__ == '__main__':
    unittest.main()
