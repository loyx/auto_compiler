"""Unit tests for _parse_term function."""
import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any

# Mock _parse_factor before importing _parse_term to avoid circular dependency
mock_parse_factor = MagicMock()
mock_parse_factor.return_value = {"type": "ERROR", "value": "Not mocked properly", "line": 0, "column": 0}

with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_term_package._parse_factor_package._parse_factor_src._parse_factor', mock_parse_factor):
    from ._parse_term_src import _parse_term


class TestParseTerm(unittest.TestCase):
    """Test cases for _parse_term function."""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast_node(self, node_type: str, value: Any = None, children: list = None, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create an AST node dict."""
        return {
            "type": node_type,
            "value": value,
            "children": children or [],
            "line": line,
            "column": column
        }

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_term_package._parse_factor_package._parse_factor_src._parse_factor')
    def test_single_factor_no_operator(self, mock_parse_factor: MagicMock):
        """Test parsing a single factor with no operators."""
        mock_factor_node = self._create_ast_node("IDENTIFIER", value="x", line=1, column=1)
        mock_parse_factor.return_value = mock_factor_node

        parser_state = {
            "tokens": [self._create_token("IDENTIFIER", "x")],
            "pos": 0,
            "filename": "test.py"
        }

        result = _parse_term(parser_state)

        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(parser_state["pos"], 0)
        mock_parse_factor.assert_called_once_with(parser_state)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_term_package._parse_factor_package._parse_factor_src._parse_factor')
    def test_multiplication_operator(self, mock_parse_factor: MagicMock):
        """Test parsing term with MULTI operator."""
        left_node = self._create_ast_node("IDENTIFIER", value="a", line=1, column=1)
        right_node = self._create_ast_node("IDENTIFIER", value="b", line=1, column=5)
        mock_parse_factor.side_effect = [left_node, right_node]

        parser_state = {
            "tokens": [
                self._create_token("IDENTIFIER", "a", column=1),
                self._create_token("MULTI", "*", column=3),
                self._create_token("IDENTIFIER", "b", column=5)
            ],
            "pos": 0,
            "filename": "test.py"
        }

        result = _parse_term(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "*")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0]["value"], "a")
        self.assertEqual(result["children"][1]["value"], "b")
        self.assertEqual(parser_state["pos"], 3)
        self.assertEqual(mock_parse_factor.call_count, 2)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_term_package._parse_factor_package._parse_factor_src._parse_factor')
    def test_division_operator(self, mock_parse_factor: MagicMock):
        """Test parsing term with DIV operator."""
        left_node = self._create_ast_node("LITERAL", value="10", line=1, column=1)
        right_node = self._create_ast_node("LITERAL", value="2", line=1, column=5)
        mock_parse_factor.side_effect = [left_node, right_node]

        parser_state = {
            "tokens": [
                self._create_token("LITERAL", "10", column=1),
                self._create_token("DIV", "/", column=4),
                self._create_token("LITERAL", "2", column=5)
            ],
            "pos": 0,
            "filename": "test.py"
        }

        result = _parse_term(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "/")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(parser_state["pos"], 3)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_term_package._parse_factor_package._parse_factor_src._parse_factor')
    def test_modulo_operator(self, mock_parse_factor: MagicMock):
        """Test parsing term with MOD operator."""
        left_node = self._create_ast_node("LITERAL", value="10", line=1, column=1)
        right_node = self._create_ast_node("LITERAL", value="3", line=1, column=5)
        mock_parse_factor.side_effect = [left_node, right_node]

        parser_state = {
            "tokens": [
                self._create_token("LITERAL", "10", column=1),
                self._create_token("MOD", "%", column=4),
                self._create_token("LITERAL", "3", column=5)
            ],
            "pos": 0,
            "filename": "test.py"
        }

        result = _parse_term(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "%")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(parser_state["pos"], 3)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_term_package._parse_factor_package._parse_factor_src._parse_factor')
    def test_left_associativity(self, mock_parse_factor: MagicMock):
        """Test that operators are left-associative: a * b / c = (a * b) / c."""
        factor_a = self._create_ast_node("IDENTIFIER", value="a", line=1, column=1)
        factor_b = self._create_ast_node("IDENTIFIER", value="b", line=1, column=5)
        factor_c = self._create_ast_node("IDENTIFIER", value="c", line=1, column=9)
        mock_parse_factor.side_effect = [factor_a, factor_b, factor_c]

        parser_state = {
            "tokens": [
                self._create_token("IDENTIFIER", "a", column=1),
                self._create_token("MULTI", "*", column=3),
                self._create_token("IDENTIFIER", "b", column=5),
                self._create_token("DIV", "/", column=7),
                self._create_token("IDENTIFIER", "c", column=9)
            ],
            "pos": 0,
            "filename": "test.py"
        }

        result = _parse_term(parser_state)

        # Should be ((a * b) / c)
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "/")
        self.assertEqual(len(result["children"]), 2)

        # Left child should be (a * b)
        left_child = result["children"][0]
        self.assertEqual(left_child["type"], "BINARY_OP")
        self.assertEqual(left_child["value"], "*")
        self.assertEqual(left_child["children"][0]["value"], "a")
        self.assertEqual(left_child["children"][1]["value"], "b")

        # Right child should be c
        right_child = result["children"][1]
        self.assertEqual(right_child["value"], "c")

        self.assertEqual(parser_state["pos"], 5)
        self.assertEqual(mock_parse_factor.call_count, 3)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_term_package._parse_factor_package._parse_factor_src._parse_factor')
    def test_factor_returns_error(self, mock_parse_factor: MagicMock):
        """Test that ERROR from _parse_factor is propagated."""
        error_node = {"type": "ERROR", "value": "Unexpected token", "line": 1, "column": 1}
        mock_parse_factor.return_value = error_node

        parser_state = {
            "tokens": [self._create_token("IDENTIFIER", "x")],
            "pos": 0,
            "filename": "test.py"
        }

        result = _parse_term(parser_state)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Unexpected token")
        mock_parse_factor.assert_called_once_with(parser_state)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_term_package._parse_factor_package._parse_factor_src._parse_factor')
    def test_right_factor_returns_error(self, mock_parse_factor: MagicMock):
        """Test that ERROR from right factor is propagated."""
        left_node = self._create_ast_node("IDENTIFIER", value="a", line=1, column=1)
        error_node = {"type": "ERROR", "value": "Expected factor", "line": 1, "column": 3}
        mock_parse_factor.side_effect = [left_node, error_node]

        parser_state = {
            "tokens": [
                self._create_token("IDENTIFIER", "a", column=1),
                self._create_token("MULTI", "*", column=3)
            ],
            "pos": 0,
            "filename": "test.py"
        }

        result = _parse_term(parser_state)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Expected factor")
        self.assertEqual(mock_parse_factor.call_count, 2)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_term_package._parse_factor_package._parse_factor_src._parse_factor')
    def test_empty_tokens(self, mock_parse_factor: MagicMock):
        """Test parsing with empty token list."""
        mock_parse_factor.return_value = {"type": "ERROR", "value": "No tokens", "line": 0, "column": 0}

        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }

        result = _parse_term(parser_state)

        self.assertEqual(result["type"], "ERROR")
        mock_parse_factor.assert_called_once_with(parser_state)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_term_package._parse_factor_package._parse_factor_src._parse_factor')
    def test_position_at_end(self, mock_parse_factor: MagicMock):
        """Test when position is already at end of tokens."""
        mock_parse_factor.return_value = {"type": "ERROR", "value": "No tokens", "line": 0, "column": 0}

        parser_state = {
            "tokens": [self._create_token("IDENTIFIER", "x")],
            "pos": 1,
            "filename": "test.py"
        }

        result = _parse_term(parser_state)

        self.assertEqual(result["type"], "ERROR")
        mock_parse_factor.assert_called_once_with(parser_state)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_term_package._parse_factor_package._parse_factor_src._parse_factor')
    def test_mixed_operators(self, mock_parse_factor: MagicMock):
        """Test parsing with mixed MULTI, DIV, MOD operators."""
        factors = [
            self._create_ast_node("LITERAL", "10", line=1, column=1),
            self._create_ast_node("LITERAL", "2", line=1, column=5),
            self._create_ast_node("LITERAL", "3", line=1, column=9),
            self._create_ast_node("LITERAL", "4", line=1, column=13)
        ]
        mock_parse_factor.side_effect = factors

        parser_state = {
            "tokens": [
                self._create_token("LITERAL", "10", column=1),
                self._create_token("MULTI", "*", column=4),
                self._create_token("LITERAL", "2", column=5),
                self._create_token("DIV", "/", column=7),
                self._create_token("LITERAL", "3", column=9),
                self._create_token("MOD", "%", column=11),
                self._create_token("LITERAL", "4", column=13)
            ],
            "pos": 0,
            "filename": "test.py"
        }

        result = _parse_term(parser_state)

        # Should be ((10 * 2) / 3) % 4
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "%")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][1]["value"], "4")

        # Left should be ((10 * 2) / 3)
        left = result["children"][0]
        self.assertEqual(left["value"], "/")
        self.assertEqual(left["children"][0]["value"], "*")
        self.assertEqual(left["children"][0]["children"][0]["value"], "10")
        self.assertEqual(left["children"][0]["children"][1]["value"], "2")
        self.assertEqual(left["children"][1]["value"], "3")

        self.assertEqual(parser_state["pos"], 7)
        self.assertEqual(mock_parse_factor.call_count, 4)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_term_package._parse_factor_package._parse_factor_src._parse_factor')
    def test_position_preserved_from_left_operand(self, mock_parse_factor: MagicMock):
        """Test that BINARY_OP node preserves position from left operand."""
        left_node = self._create_ast_node("IDENTIFIER", value="a", line=2, column=5)
        right_node = self._create_ast_node("IDENTIFIER", value="b", line=2, column=10)
        mock_parse_factor.side_effect = [left_node, right_node]

        parser_state = {
            "tokens": [
                self._create_token("IDENTIFIER", "a", line=2, column=5),
                self._create_token("MULTI", "*", line=2, column=7),
                self._create_token("IDENTIFIER", "b", line=2, column=10)
            ],
            "pos": 0,
            "filename": "test.py"
        }

        result = _parse_term(parser_state)

        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)

    @patch('main_package.compile_source_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_term_package._parse_factor_package._parse_factor_src._parse_factor')
    def test_non_operator_token_stops_loop(self, mock_parse_factor: MagicMock):
        """Test that non-operator token stops the operator loop."""
        left_node = self._create_ast_node("IDENTIFIER", value="a", line=1, column=1)
        right_node = self._create_ast_node("IDENTIFIER", value="b", line=1, column=5)
        mock_parse_factor.side_effect = [left_node, right_node]

        parser_state = {
            "tokens": [
                self._create_token("IDENTIFIER", "a", column=1),
                self._create_token("MULTI", "*", column=3),
                self._create_token("IDENTIFIER", "b", column=5),
                self._create_token("PLUS", "+", column=7),
                self._create_token("IDENTIFIER", "c", column=9)
            ],
            "pos": 0,
            "filename": "test.py"
        }

        result = _parse_term(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "*")
        self.assertEqual(parser_state["pos"], 3)
        self.assertEqual(mock_parse_factor.call_count, 2)


if __name__ == "__main__":
    unittest.main()
