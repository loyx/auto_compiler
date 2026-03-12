import unittest
from unittest.mock import patch

# Import UUT using relative import
from ._parse_and_expr_src import _parse_and_expr


class TestParseAndExpr(unittest.TestCase):
    """Test cases for _parse_and_expr function."""

    def test_single_comparison_no_and(self):
        """Test parsing a single comparison expression without && operator."""
        parser_state = {
            "tokens": [{"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.cc"
        }

        mock_comparison = {
            "type": "IDENTIFIER",
            "value": "a",
            "children": [],
            "line": 1,
            "column": 1
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_and_expr_package._parse_and_expr_src._parse_comparison_expr",
            return_value=mock_comparison
        ) as mock_parse_comp:
            result = _parse_and_expr(parser_state)

            self.assertEqual(result, mock_comparison)
            mock_parse_comp.assert_called_once_with(parser_state)
            self.assertEqual(parser_state["pos"], 0)

    def test_one_and_operator(self):
        """Test parsing expression with one && operator."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "AND", "value": "&&", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.cc"
        }

        left_operand = {
            "type": "IDENTIFIER",
            "value": "a",
            "children": [],
            "line": 1,
            "column": 1
        }

        right_operand = {
            "type": "IDENTIFIER",
            "value": "b",
            "children": [],
            "line": 1,
            "column": 6
        }

        with patch.object(_parse_and_expr_src, '_parse_comparison_expr') as mock_parse_comp:
            mock_parse_comp.side_effect = [left_operand, right_operand]
            result = _parse_and_expr(parser_state)

            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "&&")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0], left_operand)
            self.assertEqual(result["children"][1], right_operand)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(parser_state["pos"], 2)

    def test_multiple_and_operators_left_associative(self):
        """Test parsing expression with multiple && operators (left-associative)."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "AND", "value": "&&", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6},
                {"type": "AND", "value": "&&", "line": 1, "column": 8},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 11}
            ],
            "pos": 0,
            "filename": "test.cc"
        }

        operand_a = {
            "type": "IDENTIFIER",
            "value": "a",
            "children": [],
            "line": 1,
            "column": 1
        }

        operand_b = {
            "type": "IDENTIFIER",
            "value": "b",
            "children": [],
            "line": 1,
            "column": 6
        }

        operand_c = {
            "type": "IDENTIFIER",
            "value": "c",
            "children": [],
            "line": 1,
            "column": 11
        }

        with patch.object(_parse_and_expr_src, '_parse_comparison_expr') as mock_parse_comp:
            mock_parse_comp.side_effect = [operand_a, operand_b, operand_c]
            result = _parse_and_expr(parser_state)

            # Should be left-associative: ((a && b) && c)
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "&&")
            self.assertEqual(len(result["children"]), 2)

            # Left child should be (a && b)
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["value"], "&&")
            self.assertEqual(left_child["children"][0], operand_a)
            self.assertEqual(left_child["children"][1], operand_b)

            # Right child should be c
            self.assertEqual(result["children"][1], operand_c)
            self.assertEqual(parser_state["pos"], 4)

    def test_empty_tokens(self):
        """Test parsing with empty tokens list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.cc"
        }

        mock_comparison = {
            "type": "EMPTY",
            "value": None,
            "children": [],
            "line": 0,
            "column": 0
        }

        with patch.object(_parse_and_expr_src, '_parse_comparison_expr') as mock_parse_comp:
            mock_parse_comp.return_value = mock_comparison
            result = _parse_and_expr(parser_state)

            self.assertEqual(result, mock_comparison)
            mock_parse_comp.assert_called_once_with(parser_state)

    def test_position_at_end(self):
        """Test parsing when position is at end of tokens."""
        parser_state = {
            "tokens": [{"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}],
            "pos": 1,
            "filename": "test.cc"
        }

        mock_comparison = {
            "type": "IDENTIFIER",
            "value": "a",
            "children": [],
            "line": 1,
            "column": 1
        }

        with patch.object(_parse_and_expr_src, '_parse_comparison_expr') as mock_parse_comp:
            mock_parse_comp.return_value = mock_comparison
            result = _parse_and_expr(parser_state)

            self.assertEqual(result, mock_comparison)
            self.assertEqual(parser_state["pos"], 1)

    def test_and_at_end_missing_right_operand(self):
        """Test parsing && at end with missing right operand."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "AND", "value": "&&", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.cc"
        }

        left_operand = {
            "type": "IDENTIFIER",
            "value": "a",
            "children": [],
            "line": 1,
            "column": 1
        }

        right_operand = {
            "type": "ERROR",
            "value": "unexpected end",
            "children": [],
            "line": 0,
            "column": 0
        }

        with patch.object(_parse_and_expr_src, '_parse_comparison_expr') as mock_parse_comp:
            mock_parse_comp.side_effect = [left_operand, right_operand]
            result = _parse_and_expr(parser_state)

            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "&&")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0], left_operand)
            self.assertEqual(result["children"][1], right_operand)
            self.assertEqual(parser_state["pos"], 2)

    def test_non_and_token_after_comparison(self):
        """Test parsing stops when current token is not AND."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.cc"
        }

        mock_comparison = {
            "type": "IDENTIFIER",
            "value": "a",
            "children": [],
            "line": 1,
            "column": 1
        }

        with patch.object(_parse_and_expr_src, '_parse_comparison_expr') as mock_parse_comp:
            mock_parse_comp.return_value = mock_comparison
            result = _parse_and_expr(parser_state)

            self.assertEqual(result, mock_comparison)
            mock_parse_comp.assert_called_once_with(parser_state)
            self.assertEqual(parser_state["pos"], 0)

    def test_preserves_parser_state_fields(self):
        """Test that parser_state fields are preserved correctly."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "AND", "value": "&&", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.cc"
        }

        mock_comparison = {
            "type": "IDENTIFIER",
            "value": "mock",
            "children": [],
            "line": 1,
            "column": 1
        }

        with patch.object(_parse_and_expr_src, '_parse_comparison_expr') as mock_parse_comp:
            mock_parse_comp.return_value = mock_comparison
            _parse_and_expr(parser_state)

            self.assertEqual(parser_state["filename"], "test.cc")
            self.assertIn("tokens", parser_state)
            self.assertEqual(len(parser_state["tokens"]), 3)


if __name__ == "__main__":
    unittest.main()
