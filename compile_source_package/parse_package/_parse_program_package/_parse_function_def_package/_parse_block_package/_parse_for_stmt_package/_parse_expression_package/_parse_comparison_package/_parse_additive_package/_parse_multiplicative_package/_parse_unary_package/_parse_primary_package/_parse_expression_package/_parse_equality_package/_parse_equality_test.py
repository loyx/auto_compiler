import unittest
from unittest.mock import patch
from typing import Dict, Any


class TestParseEquality(unittest.TestCase):
    """Test cases for _parse_equality function."""

    def test_single_comparison_no_equality_operator(self):
        """Test parsing a single comparison without equality operators."""
        from ._parse_equality_src import _parse_equality

        parser_state = {
            "tokens": [{"type": "NUMBER", "value": "42", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py"
        }

        mock_comparison = {"type": "Number", "value": 42, "line": 1, "column": 1}

        def mock_parse_comparison(state: Dict[str, Any]) -> Dict[str, Any]:
            state["pos"] = 1
            return mock_comparison

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package._parse_expression_package._parse_equality_package._parse_equality_src._parse_comparison",
            side_effect=mock_parse_comparison
        ):
            result = _parse_equality(parser_state)

            self.assertEqual(result, mock_comparison)
            self.assertEqual(parser_state["pos"], 1)
            self.assertNotIn("error", parser_state)

    def test_equality_operator_double_equals(self):
        """Test parsing equality with == operator."""
        from ._parse_equality_src import _parse_equality

        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "==", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        mock_left = {"type": "Number", "value": 1, "line": 1, "column": 1}
        mock_right = {"type": "Number", "value": 2, "line": 1, "column": 5}
        call_count = [0]

        def mock_parse_comparison(state: Dict[str, Any]) -> Dict[str, Any]:
            call_count[0] += 1
            if call_count[0] == 1:
                state["pos"] = 1
                return mock_left
            else:
                state["pos"] = 3
                return mock_right

        with patch(
            "_parse_equality_package._parse_equality_src._parse_comparison",
            side_effect=mock_parse_comparison
        ):
            result = _parse_equality(parser_state)

            self.assertEqual(result, mock_comparison)
            self.assertEqual(parser_state["pos"], 1)
            self.assertNotIn("error", parser_state)

    def test_equality_operator_double_equals(self):
        """Test parsing equality with == operator."""
        from ._parse_equality_src import _parse_equality

        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "==", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        mock_left = {"type": "Number", "value": 1, "line": 1, "column": 1}
        mock_right = {"type": "Number", "value": 2, "line": 1, "column": 5}
        call_count = [0]

        def mock_parse_comparison(state: Dict[str, Any]) -> Dict[str, Any]:
            call_count[0] += 1
            if call_count[0] == 1:
                state["pos"] = 1
                return mock_left
            else:
                state["pos"] = 3
                return mock_right

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package._parse_expression_package._parse_equality_package._parse_equality_src._parse_comparison",
            side_effect=mock_parse_comparison
        ):
            result = _parse_equality(parser_state)

            self.assertEqual(result["type"], "Binary")
            self.assertEqual(result["operator"], "==")
            self.assertEqual(result["left"], mock_left)
            self.assertEqual(result["right"], mock_right)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(parser_state["pos"], 3)

    def test_equality_operator_not_equals(self):
        """Test parsing equality with != operator."""
        from ._parse_equality_src import _parse_equality

        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "!=", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        mock_left = {"type": "Identifier", "value": "a", "line": 1, "column": 1}
        mock_right = {"type": "Identifier", "value": "b", "line": 1, "column": 5}
        call_count = [0]

        def mock_parse_comparison(state: Dict[str, Any]) -> Dict[str, Any]:
            call_count[0] += 1
            if call_count[0] == 1:
                state["pos"] = 1
                return mock_left
            else:
                state["pos"] = 3
                return mock_right

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package._parse_expression_package._parse_equality_package._parse_equality_src._parse_comparison",
            side_effect=mock_parse_comparison
        ):
            result = _parse_equality(parser_state)

            self.assertEqual(result["type"], "Binary")
            self.assertEqual(result["operator"], "!=")
            self.assertEqual(result["left"], mock_left)
            self.assertEqual(result["right"], mock_right)
            self.assertEqual(parser_state["pos"], 3)

    def test_multiple_equality_operators_left_associative(self):
        """Test parsing multiple equality operators (left-associative)."""
        from ._parse_equality_src import _parse_equality

        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "==", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "OPERATOR", "value": "!=", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        mock_1 = {"type": "Number", "value": 1, "line": 1, "column": 1}
        mock_2 = {"type": "Number", "value": 2, "line": 1, "column": 5}
        mock_3 = {"type": "Number", "value": 3, "line": 1, "column": 9}
        call_count = [0]

        def mock_parse_comparison(state: Dict[str, Any]) -> Dict[str, Any]:
            call_count[0] += 1
            if call_count[0] == 1:
                state["pos"] = 1
                return mock_1
            elif call_count[0] == 2:
                state["pos"] = 3
                return mock_2
            else:
                state["pos"] = 5
                return mock_3

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package._parse_expression_package._parse_equality_package._parse_equality_src._parse_comparison",
            side_effect=mock_parse_comparison
        ):
            result = _parse_equality(parser_state)

            # Should be left-associative: (1 == 2) != 3
            self.assertEqual(result["type"], "Binary")
            self.assertEqual(result["operator"], "!=")
            self.assertEqual(result["right"], mock_3)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 7)

            left_part = result["left"]
            self.assertEqual(left_part["type"], "Binary")
            self.assertEqual(left_part["operator"], "==")
            self.assertEqual(left_part["left"], mock_1)
            self.assertEqual(left_part["right"], mock_2)

            self.assertEqual(parser_state["pos"], 5)

    def test_error_in_left_comparison(self):
        """Test handling error from left comparison parsing."""
        from ._parse_equality_src import _parse_equality

        parser_state = {
            "tokens": [{"type": "NUMBER", "value": "1", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py"
        }

        mock_comparison = {"type": "Error", "value": None}

        def mock_parse_comparison(state: Dict[str, Any]) -> Dict[str, Any]:
            state["error"] = "Syntax error in comparison"
            return mock_comparison

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package._parse_expression_package._parse_equality_package._parse_equality_src._parse_comparison",
            side_effect=mock_parse_comparison
        ):
            result = _parse_equality(parser_state)

            self.assertEqual(result, mock_comparison)
            self.assertEqual(parser_state["error"], "Syntax error in comparison")

    def test_error_in_right_comparison(self):
        """Test handling error from right comparison parsing."""
        from ._parse_equality_src import _parse_equality

        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "==", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        mock_left = {"type": "Number", "value": 1, "line": 1, "column": 1}
        mock_right = {"type": "Error", "value": None}
        call_count = [0]

        def mock_parse_comparison(state: Dict[str, Any]) -> Dict[str, Any]:
            call_count[0] += 1
            if call_count[0] == 1:
                state["pos"] = 1
                return mock_left
            else:
                state["error"] = "Right side error"
                return mock_right

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package._parse_expression_package._parse_equality_package._parse_equality_src._parse_comparison",
            side_effect=mock_parse_comparison
        ):
            result = _parse_equality(parser_state)

            self.assertEqual(result, mock_left)
            self.assertEqual(parser_state["error"], "Right side error")

    def test_empty_tokens(self):
        """Test parsing with empty token list."""
        from ._parse_equality_src import _parse_equality

        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }

        mock_comparison = {"type": "Empty", "value": None}

        def mock_parse_comparison(state: Dict[str, Any]) -> Dict[str, Any]:
            return mock_comparison

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package._parse_expression_package._parse_equality_package._parse_equality_src._parse_comparison",
            side_effect=mock_parse_comparison
        ):
            result = _parse_equality(parser_state)

            self.assertEqual(result, mock_comparison)
            self.assertEqual(parser_state["pos"], 0)

    def test_non_equality_operator(self):
        """Test that non-equality operators are not consumed."""
        from ._parse_equality_src import _parse_equality

        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        mock_comparison = {"type": "Number", "value": 1, "line": 1, "column": 1}

        def mock_parse_comparison(state: Dict[str, Any]) -> Dict[str, Any]:
            state["pos"] = 1
            return mock_comparison

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package._parse_expression_package._parse_equality_package._parse_equality_src._parse_comparison",
            side_effect=mock_parse_comparison
        ):
            result = _parse_equality(parser_state)

            self.assertEqual(result, mock_comparison)
            self.assertEqual(parser_state["pos"], 1)

    def test_position_at_end_of_tokens(self):
        """Test when position is already at end of tokens."""
        from ._parse_equality_src import _parse_equality

        parser_state = {
            "tokens": [{"type": "NUMBER", "value": "1", "line": 1, "column": 1}],
            "pos": 1,
            "filename": "test.py"
        }

        mock_comparison = {"type": "Number", "value": 1, "line": 1, "column": 1}

        def mock_parse_comparison(state: Dict[str, Any]) -> Dict[str, Any]:
            return mock_comparison

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package._parse_expression_package._parse_equality_package._parse_equality_src._parse_comparison",
            side_effect=mock_parse_comparison
        ):
            result = _parse_equality(parser_state)

            self.assertEqual(result, mock_comparison)
            self.assertEqual(parser_state["pos"], 1)

    def test_mixed_equality_operators(self):
        """Test parsing with mixed == and != operators."""
        from ._parse_equality_src import _parse_equality

        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "==", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "OPERATOR", "value": "!=", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9},
                {"type": "OPERATOR", "value": "==", "line": 1, "column": 11},
                {"type": "IDENTIFIER", "value": "d", "line": 1, "column": 13}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        mock_a = {"type": "Identifier", "value": "a", "line": 1, "column": 1}
        mock_b = {"type": "Identifier", "value": "b", "line": 1, "column": 5}
        mock_c = {"type": "Identifier", "value": "c", "line": 1, "column": 9}
        mock_d = {"type": "Identifier", "value": "d", "line": 1, "column": 13}
        call_count = [0]

        def mock_parse_comparison(state: Dict[str, Any]) -> Dict[str, Any]:
            call_count[0] += 1
            if call_count[0] == 1:
                state["pos"] = 1
                return mock_a
            elif call_count[0] == 2:
                state["pos"] = 3
                return mock_b
            elif call_count[0] == 3:
                state["pos"] = 5
                return mock_c
            else:
                state["pos"] = 7
                return mock_d

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package._parse_expression_package._parse_equality_package._parse_equality_src._parse_comparison",
            side_effect=mock_parse_comparison
        ):
            result = _parse_equality(parser_state)

            # Should be left-associative: ((a == b) != c) == d
            self.assertEqual(result["type"], "Binary")
            self.assertEqual(result["operator"], "==")
            self.assertEqual(result["right"], mock_d)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 11)

            middle = result["left"]
            self.assertEqual(middle["type"], "Binary")
            self.assertEqual(middle["operator"], "!=")
            self.assertEqual(middle["right"], mock_c)
            self.assertEqual(middle["line"], 1)
            self.assertEqual(middle["column"], 7)

            leftmost = middle["left"]
            self.assertEqual(leftmost["type"], "Binary")
            self.assertEqual(leftmost["operator"], "==")
            self.assertEqual(leftmost["left"], mock_a)
            self.assertEqual(leftmost["right"], mock_b)

            self.assertEqual(parser_state["pos"], 7)

    def test_token_without_type_field(self):
        """Test handling token without type field."""
        from ._parse_equality_src import _parse_equality

        parser_state = {
            "tokens": [
                {"value": "1", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "==", "line": 1, "column": 3},
                {"value": "2", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        mock_comparison = {"type": "Number", "value": 1, "line": 1, "column": 1}
        call_count = [0]

        def mock_parse_comparison(state: Dict[str, Any]) -> Dict[str, Any]:
            call_count[0] += 1
            if call_count[0] == 1:
                state["pos"] = 1
                return mock_comparison
            else:
                state["pos"] = 3
                return mock_comparison

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package._parse_expression_package._parse_equality_package._parse_equality_src._parse_comparison",
            side_effect=mock_parse_comparison
        ):
            result = _parse_equality(parser_state)

            self.assertEqual(result, mock_comparison)
            self.assertEqual(parser_state["pos"], 1)

    def test_token_without_value_field(self):
        """Test handling token without value field."""
        from ._parse_equality_src import _parse_equality

        parser_state = {
            "tokens": [
                {"type": "NUMBER", "line": 1, "column": 1},
                {"type": "OPERATOR", "line": 1, "column": 3},
                {"type": "NUMBER", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        mock_comparison = {"type": "Number", "value": None, "line": 1, "column": 1}
        call_count = [0]

        def mock_parse_comparison(state: Dict[str, Any]) -> Dict[str, Any]:
            call_count[0] += 1
            if call_count[0] == 1:
                state["pos"] = 1
                return mock_comparison
            else:
                state["pos"] = 3
                return mock_comparison

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package._parse_expression_package._parse_equality_package._parse_equality_src._parse_comparison",
            side_effect=mock_parse_comparison
        ):
            result = _parse_equality(parser_state)

            self.assertEqual(result, mock_comparison)
            self.assertEqual(parser_state["pos"], 1)


if __name__ == "__main__":
    unittest.main()
