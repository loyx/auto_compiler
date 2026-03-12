import unittest
from unittest.mock import patch

# Import the function under test using relative import
from ._parse_comparison_expr_src import _parse_comparison_expr


class TestParseComparisonExpr(unittest.TestCase):
    """Test cases for _parse_comparison_expr function."""

    def test_gt_operator(self):
        """Test parsing greater than operator (a > b)."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "GT", "value": ">", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py"
        }

        left_ast = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_ast = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}

        with patch("._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr") as mock_additive:
            mock_additive.side_effect = [left_ast, right_ast]

            result = _parse_comparison_expr(parser_state)

            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], ">")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0], left_ast)
            self.assertEqual(result["children"][1], right_ast)
            self.assertEqual(parser_state["pos"], 3)

    def test_lt_operator(self):
        """Test parsing less than operator (x < y)."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 1},
                {"type": "LT", "value": "<", "line": 2, "column": 3},
                {"type": "IDENTIFIER", "value": "y", "line": 2, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py"
        }

        left_ast = {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 1}
        right_ast = {"type": "IDENTIFIER", "value": "y", "line": 2, "column": 5}

        with patch("._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr") as mock_additive:
            mock_additive.side_effect = [left_ast, right_ast]

            result = _parse_comparison_expr(parser_state)

            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "<")

    def test_ge_operator(self):
        """Test parsing greater than or equal operator (x >= y)."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 5, "column": 1},
                {"type": "GE", "value": ">=", "line": 5, "column": 3},
                {"type": "IDENTIFIER", "value": "y", "line": 5, "column": 6},
            ],
            "pos": 0,
            "filename": "test.py"
        }

        left_ast = {"type": "IDENTIFIER", "value": "x", "line": 5, "column": 1}
        right_ast = {"type": "IDENTIFIER", "value": "y", "line": 5, "column": 6}

        with patch("._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr") as mock_additive:
            mock_additive.side_effect = [left_ast, right_ast]

            result = _parse_comparison_expr(parser_state)

            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], ">=")

    def test_le_operator(self):
        """Test parsing less than or equal operator (a <= b)."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 6, "column": 1},
                {"type": "LE", "value": "<=", "line": 6, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 6, "column": 6},
            ],
            "pos": 0,
            "filename": "test.py"
        }

        left_ast = {"type": "IDENTIFIER", "value": "a", "line": 6, "column": 1}
        right_ast = {"type": "IDENTIFIER", "value": "b", "line": 6, "column": 6}

        with patch("._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr") as mock_additive:
            mock_additive.side_effect = [left_ast, right_ast]

            result = _parse_comparison_expr(parser_state)

            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "<=")

    def test_eq_operator(self):
        """Test parsing equal operator (foo == bar)."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "foo", "line": 3, "column": 1},
                {"type": "EQ", "value": "==", "line": 3, "column": 5},
                {"type": "IDENTIFIER", "value": "bar", "line": 3, "column": 8},
            ],
            "pos": 0,
            "filename": "test.py"
        }

        left_ast = {"type": "IDENTIFIER", "value": "foo", "line": 3, "column": 1}
        right_ast = {"type": "IDENTIFIER", "value": "bar", "line": 3, "column": 8}

        with patch("._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr") as mock_additive:
            mock_additive.side_effect = [left_ast, right_ast]

            result = _parse_comparison_expr(parser_state)

            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "==")

    def test_ne_operator(self):
        """Test parsing not equal operator (a != b)."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 4, "column": 1},
                {"type": "NE", "value": "!=", "line": 4, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 4, "column": 6},
            ],
            "pos": 0,
            "filename": "test.py"
        }

        left_ast = {"type": "IDENTIFIER", "value": "a", "line": 4, "column": 1}
        right_ast = {"type": "IDENTIFIER", "value": "b", "line": 4, "column": 6}

        with patch("._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr") as mock_additive:
            mock_additive.side_effect = [left_ast, right_ast]

            result = _parse_comparison_expr(parser_state)

            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "!=")

    def test_no_comparison_operator(self):
        """Test when there is no comparison operator (just a single expression)."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py"
        }

        left_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}

        with patch("._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr") as mock_additive:
            mock_additive.return_value = left_ast

            result = _parse_comparison_expr(parser_state)

            # Should return the left operand directly
            self.assertEqual(result, left_ast)
            # Position should not advance (no operator consumed)
            self.assertEqual(parser_state["pos"], 0)

    def test_position_at_end(self):
        """Test when position is already at end of tokens."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 1,  # Already at end
            "filename": "test.py"
        }

        left_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}

        with patch("._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr") as mock_additive:
            mock_additive.return_value = left_ast

            result = _parse_comparison_expr(parser_state)

            self.assertEqual(result, left_ast)

    def test_error_in_left_operand(self):
        """Test when error occurs while parsing left operand."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
            "error": "Some error"
        }

        left_ast = {"type": "ERROR", "value": "error"}

        with patch("._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr") as mock_additive:
            mock_additive.return_value = left_ast

            result = _parse_comparison_expr(parser_state)

            # Should return left_ast when error exists
            self.assertEqual(result, left_ast)

    def test_error_in_right_operand(self):
        """Test when error occurs while parsing right operand."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "GT", "value": ">", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py"
        }

        left_ast = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_ast = {"type": "ERROR", "value": "error"}

        def parse_additive_side_effect(state):
            if state["pos"] == 0:
                return left_ast
            else:
                state["error"] = "Error in right operand"
                return right_ast

        with patch("._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr") as mock_additive:
            mock_additive.side_effect = parse_additive_side_effect

            result = _parse_comparison_expr(parser_state)

            # When error occurs in right operand, should return left_ast
            self.assertEqual(result, left_ast)

    def test_empty_tokens(self):
        """Test with empty tokens list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }

        left_ast = {"type": "LITERAL", "value": 42, "line": 1, "column": 1}

        with patch("._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr") as mock_additive:
            mock_additive.return_value = left_ast

            result = _parse_comparison_expr(parser_state)

            self.assertEqual(result, left_ast)

    def test_non_comparison_token(self):
        """Test when current token is not a comparison operator."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py"
        }

        left_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}

        with patch("._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr") as mock_additive:
            mock_additive.return_value = left_ast

            result = _parse_comparison_expr(parser_state)

            # Should return left operand when next token is not comparison operator
            self.assertEqual(result, left_ast)

    def test_position_advancement(self):
        """Test that position is correctly advanced after consuming operator."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "GT", "value": ">", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py"
        }

        with patch("._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr") as mock_additive:
            mock_additive.side_effect = [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            ]

            _parse_comparison_expr(parser_state)

            # Position should be advanced past the operator and right operand
            self.assertEqual(parser_state["pos"], 3)

    def test_ast_node_structure(self):
        """Test that the returned AST node has correct structure."""
        parser_state = {
            "tokens": [
                {"type": "LITERAL", "value": "5", "line": 1, "column": 1},
                {"type": "EQ", "value": "==", "line": 1, "column": 3},
                {"type": "LITERAL", "value": "5", "line": 1, "column": 6},
            ],
            "pos": 0,
            "filename": "test.py"
        }

        left_ast = {"type": "LITERAL", "value": "5", "line": 1, "column": 1}
        right_ast = {"type": "LITERAL", "value": "5", "line": 1, "column": 6}

        with patch("._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr") as mock_additive:
            mock_additive.side_effect = [left_ast, right_ast]

            result = _parse_comparison_expr(parser_state)

            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "==")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0], left_ast)
            self.assertEqual(result["children"][1], right_ast)


if __name__ == "__main__":
    unittest.main()
