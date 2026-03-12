import unittest
from unittest.mock import patch

from ._parse_additive_src import _parse_additive


class TestParseAdditive(unittest.TestCase):
    """Test cases for _parse_additive function."""

    def test_single_multiplicative_no_operator(self):
        """Test parsing a single multiplicative expression without + or - operators."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "5", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        mock_multiplicative = {
            "type": "LITERAL",
            "value": "5",
            "children": [],
            "line": 1,
            "column": 1
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_for_stmt_package."
            "_parse_expression_package._parse_comparison_package._parse_additive_package."
            "_parse_additive_src._parse_multiplicative",
            return_value=mock_multiplicative
        ) as mock_mul:
            result = _parse_additive(parser_state)

            self.assertEqual(result["type"], "LITERAL")
            self.assertEqual(result["value"], "5")
            self.assertEqual(parser_state["pos"], 0)
            mock_mul.assert_called_once_with(parser_state)

    def test_one_addition(self):
        """Test parsing a + b."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "5", "line": 1, "column": 1},
                {"type": "ADD", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        left_operand = {
            "type": "LITERAL",
            "value": "5",
            "children": [],
            "line": 1,
            "column": 1
        }

        right_operand = {
            "type": "LITERAL",
            "value": "3",
            "children": [],
            "line": 1,
            "column": 5
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_for_stmt_package."
            "_parse_expression_package._parse_comparison_package._parse_additive_package."
            "_parse_additive_src._parse_multiplicative",
            side_effect=[left_operand, right_operand]
        ) as mock_mul:
            result = _parse_additive(parser_state)

            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "+")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0], left_operand)
            self.assertEqual(result["children"][1], right_operand)
            self.assertEqual(parser_state["pos"], 3)
            self.assertEqual(mock_mul.call_count, 2)

    def test_one_subtraction(self):
        """Test parsing a - b."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "10", "line": 1, "column": 1},
                {"type": "SUB", "value": "-", "line": 1, "column": 4},
                {"type": "NUMBER", "value": "4", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        left_operand = {
            "type": "LITERAL",
            "value": "10",
            "children": [],
            "line": 1,
            "column": 1
        }

        right_operand = {
            "type": "LITERAL",
            "value": "4",
            "children": [],
            "line": 1,
            "column": 6
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_for_stmt_package."
            "_parse_expression_package._parse_comparison_package._parse_additive_package."
            "_parse_additive_src._parse_multiplicative",
            side_effect=[left_operand, right_operand]
        ):
            result = _parse_additive(parser_state)

            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(parser_state["pos"], 3)

    def test_multiple_additive_operations_left_associative(self):
        """Test left-associativity: a + b - c should be ((a + b) - c)."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "ADD", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "SUB", "value": "-", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        operand1 = {"type": "LITERAL", "value": "1", "children": [], "line": 1, "column": 1}
        operand2 = {"type": "LITERAL", "value": "2", "children": [], "line": 1, "column": 5}
        operand3 = {"type": "LITERAL", "value": "3", "children": [], "line": 1, "column": 9}

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_for_stmt_package."
            "_parse_expression_package._parse_comparison_package._parse_additive_package."
            "_parse_additive_src._parse_multiplicative",
            side_effect=[operand1, operand2, operand3]
        ):
            result = _parse_additive(parser_state)

            # Should be ((1 + 2) - 3)
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(len(result["children"]), 2)

            # Left child should be (1 + 2)
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["value"], "+")

            # Right child should be 3
            right_child = result["children"][1]
            self.assertEqual(right_child["type"], "LITERAL")
            self.assertEqual(right_child["value"], "3")

            self.assertEqual(parser_state["pos"], 5)

    def test_empty_tokens(self):
        """Test handling when tokens list is empty."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }

        mock_multiplicative = {
            "type": "LITERAL",
            "value": "0",
            "children": [],
            "line": 1,
            "column": 1
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_for_stmt_package."
            "_parse_expression_package._parse_comparison_package._parse_additive_package."
            "_parse_additive_src._parse_multiplicative",
            return_value=mock_multiplicative
        ):
            result = _parse_additive(parser_state)

            self.assertEqual(result["type"], "LITERAL")
            self.assertEqual(parser_state["pos"], 0)

    def test_position_at_end(self):
        """Test when position is already at end of tokens."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "5", "line": 1, "column": 1}
            ],
            "pos": 1,  # Already at end
            "filename": "test.py"
        }

        mock_multiplicative = {
            "type": "LITERAL",
            "value": "5",
            "children": [],
            "line": 1,
            "column": 1
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_for_stmt_package."
            "_parse_expression_package._parse_comparison_package._parse_additive_package."
            "_parse_additive_src._parse_multiplicative",
            return_value=mock_multiplicative
        ):
            result = _parse_additive(parser_state)

            self.assertEqual(result["type"], "LITERAL")
            self.assertEqual(parser_state["pos"], 1)

    def test_non_additive_operator_stops_loop(self):
        """Test that non-ADD/SUB token stops the parsing loop."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "5", "line": 1, "column": 1},
                {"type": "MUL", "value": "*", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        mock_multiplicative = {
            "type": "LITERAL",
            "value": "5",
            "children": [],
            "line": 1,
            "column": 1
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_for_stmt_package."
            "_parse_expression_package._parse_comparison_package._parse_additive_package."
            "_parse_additive_src._parse_multiplicative",
            return_value=mock_multiplicative
        ) as mock_mul:
            result = _parse_additive(parser_state)

            self.assertEqual(result["type"], "LITERAL")
            self.assertEqual(parser_state["pos"], 0)
            mock_mul.assert_called_once()

    def test_ast_node_preserves_line_column_from_left_operand(self):
        """Test that BINARY_OP node preserves line/column from left operand."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "5", "line": 2, "column": 10},
                {"type": "ADD", "value": "+", "line": 2, "column": 12},
                {"type": "NUMBER", "value": "3", "line": 2, "column": 14}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        left_operand = {
            "type": "LITERAL",
            "value": "5",
            "children": [],
            "line": 2,
            "column": 10
        }

        right_operand = {
            "type": "LITERAL",
            "value": "3",
            "children": [],
            "line": 2,
            "column": 14
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_for_stmt_package."
            "_parse_expression_package._parse_comparison_package._parse_additive_package."
            "_parse_additive_src._parse_multiplicative",
            side_effect=[left_operand, right_operand]
        ):
            result = _parse_additive(parser_state)

            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 10)

    def test_mixed_addition_subtraction_sequence(self):
        """Test complex sequence: a - b + c - d."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "10", "line": 1, "column": 1},
                {"type": "SUB", "value": "-", "line": 1, "column": 4},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 6},
                {"type": "ADD", "value": "+", "line": 1, "column": 8},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 10},
                {"type": "SUB", "value": "-", "line": 1, "column": 12},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 14}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        operands = [
            {"type": "LITERAL", "value": "10", "children": [], "line": 1, "column": 1},
            {"type": "LITERAL", "value": "5", "children": [], "line": 1, "column": 6},
            {"type": "LITERAL", "value": "3", "children": [], "line": 1, "column": 10},
            {"type": "LITERAL", "value": "2", "children": [], "line": 1, "column": 14}
        ]

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_for_stmt_package."
            "_parse_expression_package._parse_comparison_package._parse_additive_package."
            "_parse_additive_src._parse_multiplicative",
            side_effect=operands
        ):
            result = _parse_additive(parser_state)

            # Should be (((10 - 5) + 3) - 2)
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(parser_state["pos"], 7)

            # Verify left-associative structure
            left_most = result["children"][0]
            self.assertEqual(left_most["value"], "+")
            self.assertEqual(left_most["children"][0]["value"], "-")


if __name__ == "__main__":
    unittest.main()
