# === std / third-party imports ===
import unittest
from unittest.mock import patch

# === relative imports ===
from ._parse_multiplicative_expr_src import _parse_multiplicative_expr


class TestParseMultiplicativeExpr(unittest.TestCase):
    """Test cases for _parse_multiplicative_expr function."""

    def test_single_primary_expression_no_operator(self):
        """Test parsing a single primary expression without any multiplicative operators."""
        parser_state = {
            "tokens": [{"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py"
        }

        primary_node = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}

        with patch("._parse_multiplicative_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = primary_node

            result = _parse_multiplicative_expr(parser_state)

            self.assertEqual(result, primary_node)
            mock_primary.assert_called_once()

    def test_multiplication_expression(self):
        """Test parsing a multiplication expression (a * b)."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "STAR", "value": "*", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        left_node = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_node = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}

        call_count = [0]

        def primary_side_effect(state):
            result = left_node if call_count[0] == 0 else right_node
            call_count[0] += 1
            return result

        with patch("._parse_multiplicative_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.side_effect = primary_side_effect

            result = _parse_multiplicative_expr(parser_state)

            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "*")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0], left_node)
            self.assertEqual(result["children"][1], right_node)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(mock_primary.call_count, 2)

    def test_division_expression(self):
        """Test parsing a division expression (a / b)."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "SLASH", "value": "/", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        left_node = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_node = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}

        call_count = [0]

        def primary_side_effect(state):
            result = left_node if call_count[0] == 0 else right_node
            call_count[0] += 1
            return result

        with patch("._parse_multiplicative_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.side_effect = primary_side_effect

            result = _parse_multiplicative_expr(parser_state)

            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "/")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0], left_node)
            self.assertEqual(result["children"][1], right_node)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)

    def test_chained_operations_left_associative(self):
        """Test parsing chained operations (a * b / c) with left associativity."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "STAR", "value": "*", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "SLASH", "value": "/", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        nodes = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
        ]

        call_count = [0]

        def primary_side_effect(state):
            result = nodes[call_count[0]]
            call_count[0] += 1
            return result

        with patch("._parse_multiplicative_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.side_effect = primary_side_effect

            result = _parse_multiplicative_expr(parser_state)

            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "/")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 7)

            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["value"], "*")
            self.assertEqual(left_child["children"][0], nodes[0])
            self.assertEqual(left_child["children"][1], nodes[1])

            right_child = result["children"][1]
            self.assertEqual(right_child, nodes[2])

    def test_error_after_parsing_left(self):
        """Test that parsing stops when error is set after parsing left operand."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "STAR", "value": "*", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        error_node = {"type": "ERROR", "value": "error"}

        def primary_side_effect(state):
            state["error"] = "Test error"
            return error_node

        with patch("._parse_multiplicative_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.side_effect = primary_side_effect

            result = _parse_multiplicative_expr(parser_state)

            self.assertEqual(result, error_node)
            mock_primary.assert_called_once()

    def test_error_after_parsing_right(self):
        """Test that parsing stops and returns left when error is set after parsing right operand."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "STAR", "value": "*", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        left_node = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_node = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}

        call_count = [0]

        def primary_side_effect(state):
            result = left_node if call_count[0] == 0 else right_node
            call_count[0] += 1
            if call_count[0] == 2:
                state["error"] = "Error on right"
            return result

        with patch("._parse_multiplicative_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.side_effect = primary_side_effect

            result = _parse_multiplicative_expr(parser_state)

            self.assertEqual(result, left_node)
            self.assertEqual(mock_primary.call_count, 2)

    def test_empty_tokens(self):
        """Test parsing with empty token list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }

        empty_node = {"type": "EMPTY", "value": None}

        with patch("._parse_multiplicative_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = empty_node

            result = _parse_multiplicative_expr(parser_state)

            self.assertEqual(result, empty_node)

    def test_pos_at_end_of_tokens(self):
        """Test parsing when pos is already at end of tokens."""
        parser_state = {
            "tokens": [{"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}],
            "pos": 1,
            "filename": "test.py"
        }

        primary_node = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}

        with patch("._parse_multiplicative_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = primary_node

            result = _parse_multiplicative_expr(parser_state)

            self.assertEqual(result, primary_node)

    def test_preexisting_error(self):
        """Test that pre-existing error is respected."""
        parser_state = {
            "tokens": [{"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py",
            "error": "Pre-existing error"
        }

        primary_node = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}

        with patch("._parse_multiplicative_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = primary_node

            result = _parse_multiplicative_expr(parser_state)

            self.assertEqual(result, primary_node)
            mock_primary.assert_called_once()


if __name__ == "__main__":
    unittest.main()
