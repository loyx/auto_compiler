# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any

# === import UUT ===
from ._parse_and_expr_src import _parse_and_expr


class TestParseAndExpr(unittest.TestCase):
    """Test cases for _parse_and_expr function."""

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        """Helper to create parser state."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast_node(self, node_type: str, **kwargs) -> Dict[str, Any]:
        """Helper to create an AST node."""
        node = {"type": node_type}
        node.update(kwargs)
        return node

    @patch('._parse_and_expr_src._parse_comparison_expr')
    def test_single_comparison_no_and(self, mock_parse_comparison):
        """Test parsing a single comparison expression without && operator."""
        expected_ast = self._create_ast_node("COMPARISON", value="a > b")
        mock_parse_comparison.return_value = expected_ast

        parser_state = self._create_parser_state([
            self._create_token("IDENTIFIER", "a"),
            self._create_token("OPERATOR", ">"),
            self._create_token("IDENTIFIER", "b")
        ])

        result = _parse_and_expr(parser_state)

        self.assertEqual(result["type"], "COMPARISON")
        self.assertEqual(result["value"], "a > b")
        mock_parse_comparison.assert_called_once_with(parser_state)
        self.assertEqual(parser_state["pos"], 0)

    @patch('._parse_and_expr_src._parse_comparison_expr')
    def test_two_and_expressions_left_associative(self, mock_parse_comparison):
        """Test parsing two expressions connected by && operator."""
        left_ast = self._create_ast_node("COMPARISON", value="a > b")
        right_ast = self._create_ast_node("COMPARISON", value="c < d")
        mock_parse_comparison.side_effect = [left_ast, right_ast]

        parser_state = self._create_parser_state([
            self._create_token("IDENTIFIER", "a"),
            self._create_token("AND", "&&", line=1, column=5),
            self._create_token("IDENTIFIER", "c")
        ])

        result = _parse_and_expr(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "&&")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0]["value"], "a > b")
        self.assertEqual(result["children"][1]["value"], "c < d")
        self.assertEqual(parser_state["pos"], 2)
        self.assertEqual(mock_parse_comparison.call_count, 2)

    @patch('._parse_and_expr_src._parse_comparison_expr')
    def test_three_and_expressions_left_associative(self, mock_parse_comparison):
        """Test parsing three expressions connected by && (left-associative)."""
        ast1 = self._create_ast_node("COMPARISON", value="a > b")
        ast2 = self._create_ast_node("COMPARISON", value="c < d")
        ast3 = self._create_ast_node("COMPARISON", value="e == f")
        mock_parse_comparison.side_effect = [ast1, ast2, ast3]

        parser_state = self._create_parser_state([
            self._create_token("IDENTIFIER", "a"),
            self._create_token("AND", "&&", line=1, column=5),
            self._create_token("IDENTIFIER", "c"),
            self._create_token("AND", "&&", line=1, column=10),
            self._create_token("IDENTIFIER", "e")
        ])

        result = _parse_and_expr(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "&&")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 10)
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][1]["value"], "e == f")
        self.assertEqual(result["children"][0]["type"], "BINARY_OP")
        self.assertEqual(result["children"][0]["children"][0]["value"], "a > b")
        self.assertEqual(result["children"][0]["children"][1]["value"], "c < d")
        self.assertEqual(parser_state["pos"], 4)
        self.assertEqual(mock_parse_comparison.call_count, 3)

    @patch('._parse_and_expr_src._parse_comparison_expr')
    def test_error_in_first_comparison(self, mock_parse_comparison):
        """Test handling when first _parse_comparison_expr sets an error."""
        error_ast = self._create_ast_node("ERROR", message="parse error")
        mock_parse_comparison.return_value = error_ast

        parser_state = self._create_parser_state([])
        parser_state["error"] = "parse error"

        result = _parse_and_expr(parser_state)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(parser_state["error"], "parse error")
        mock_parse_comparison.assert_called_once()

    @patch('._parse_and_expr_src._parse_comparison_expr')
    def test_error_in_second_comparison(self, mock_parse_comparison):
        """Test handling when second _parse_comparison_expr sets an error."""
        left_ast = self._create_ast_node("COMPARISON", value="a > b")
        error_ast = self._create_ast_node("ERROR", message="parse error")
        mock_parse_comparison.side_effect = [left_ast, error_ast]

        parser_state = self._create_parser_state([
            self._create_token("IDENTIFIER", "a"),
            self._create_token("AND", "&&", line=1, column=5),
            self._create_token("IDENTIFIER", "c")
        ])
        parser_state["error"] = "parse error"

        result = _parse_and_expr(parser_state)

        self.assertEqual(result["type"], "COMPARISON")
        self.assertEqual(result["value"], "a > b")
        self.assertEqual(parser_state["error"], "parse error")
        self.assertEqual(mock_parse_comparison.call_count, 2)

    @patch('._parse_and_expr_src._parse_comparison_expr')
    def test_empty_tokens(self, mock_parse_comparison):
        """Test parsing with empty token list."""
        empty_ast = self._create_ast_node("EMPTY", value="")
        mock_parse_comparison.return_value = empty_ast

        parser_state = self._create_parser_state([])

        result = _parse_and_expr(parser_state)

        self.assertEqual(result["type"], "EMPTY")
        self.assertEqual(parser_state["pos"], 0)
        mock_parse_comparison.assert_called_once()

    @patch('._parse_and_expr_src._parse_comparison_expr')
    def test_position_not_advanced_without_and(self, mock_parse_comparison):
        """Test that position is not advanced when no && token is present."""
        ast = self._create_ast_node("COMPARISON", value="a > b")
        mock_parse_comparison.return_value = ast

        parser_state = self._create_parser_state([
            self._create_token("IDENTIFIER", "a"),
            self._create_token("OR", "||", line=1, column=5),
            self._create_token("IDENTIFIER", "c")
        ])

        result = _parse_and_expr(parser_state)

        self.assertEqual(result["type"], "COMPARISON")
        self.assertEqual(parser_state["pos"], 0)

    @patch('._parse_and_expr_src._parse_comparison_expr')
    def test_line_column_from_and_token(self, mock_parse_comparison):
        """Test that line and column from AND token are preserved in AST."""
        left_ast = self._create_ast_node("COMPARISON", value="a > b")
        right_ast = self._create_ast_node("COMPARISON", value="c < d")
        mock_parse_comparison.side_effect = [left_ast, right_ast]

        parser_state = self._create_parser_state([
            self._create_token("IDENTIFIER", "a"),
            self._create_token("AND", "&&", line=5, column=15),
            self._create_token("IDENTIFIER", "c")
        ])

        result = _parse_and_expr(parser_state)

        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 15)

    @patch('._parse_and_expr_src._parse_comparison_expr')
    def test_and_at_end_consumed(self, mock_parse_comparison):
        """Test && at end of tokens is consumed."""
        left_ast = self._create_ast_node("COMPARISON", value="a > b")
        right_ast = self._create_ast_node("COMPARISON", value="")
        mock_parse_comparison.side_effect = [left_ast, right_ast]

        parser_state = self._create_parser_state([
            self._create_token("IDENTIFIER", "a"),
            self._create_token("AND", "&&", line=1, column=5)
        ])

        result = _parse_and_expr(parser_state)

        self.assertEqual(parser_state["pos"], 2)
        self.assertEqual(mock_parse_comparison.call_count, 2)


if __name__ == "__main__":
    unittest.main()
