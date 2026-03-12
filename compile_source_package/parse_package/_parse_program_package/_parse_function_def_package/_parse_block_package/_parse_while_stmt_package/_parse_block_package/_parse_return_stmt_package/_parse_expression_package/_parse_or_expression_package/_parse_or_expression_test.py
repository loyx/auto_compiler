# -*- coding: utf-8 -*-
"""Unit tests for _parse_or_expression function."""

import unittest
from unittest.mock import patch
from typing import Dict, Any

from ._parse_or_expression_src import _parse_or_expression


class TestParseOrExpression(unittest.TestCase):
    """Test cases for _parse_or_expression function."""

    def setUp(self):
        """Set up test fixtures."""
        self.base_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dictionary."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast_node(self, node_type: str, value: Any = None, children: list = None, line: int = 0, column: int = 0) -> Dict[str, Any]:
        """Helper to create an AST node dictionary."""
        return {
            "type": node_type,
            "value": value,
            "children": children if children is not None else [],
            "line": line,
            "column": column
        }

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_or_expression_package._parse_or_expression_src._parse_comparison')
    def test_no_logical_operator(self, mock_parse_comparison):
        """Test expression without logical operators - returns left operand as-is."""
        left_ast = self._create_ast_node("LITERAL", value=42, line=1, column=1)
        mock_parse_comparison.return_value = (left_ast, self.base_state)

        result_ast, result_state = _parse_or_expression(self.base_state)

        self.assertEqual(result_ast, left_ast)
        self.assertEqual(result_state, self.base_state)
        mock_parse_comparison.assert_called_once_with(self.base_state)

    @patch('_parse_or_expression_package._parse_or_expression_src._parse_comparison')
    def test_simple_or_operator(self, mock_parse_comparison):
        """Test expression with 'or' operator."""
        tokens = [
            self._create_token("LITERAL", "true", 1, 1),
            self._create_token("KEYWORD", "or", 1, 6),
            self._create_token("LITERAL", "false", 1, 9),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        left_ast = self._create_ast_node("LITERAL", value="true", line=1, column=1)
        right_ast = self._create_ast_node("LITERAL", value="false", line=1, column=9)
        intermediate_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        final_state = {
            "tokens": tokens,
            "pos": 2,
            "filename": "test.py",
            "error": ""
        }

        mock_parse_comparison.side_effect = [
            (left_ast, intermediate_state),
            (right_ast, final_state)
        ]

        result_ast, result_state = _parse_or_expression(parser_state)

        self.assertEqual(result_ast["type"], "BINARY_OP")
        self.assertEqual(result_ast["value"], "or")
        self.assertEqual(len(result_ast["children"]), 2)
        self.assertEqual(result_ast["children"][0], left_ast)
        self.assertEqual(result_ast["children"][1], right_ast)
        self.assertEqual(result_ast["line"], 1)
        self.assertEqual(result_ast["column"], 6)
        self.assertEqual(result_state["pos"], 2)

    @patch('_parse_or_expression_package._parse_or_expression_src._parse_comparison')
    def test_simple_and_operator(self, mock_parse_comparison):
        """Test expression with 'and' operator."""
        tokens = [
            self._create_token("LITERAL", "true", 1, 1),
            self._create_token("KEYWORD", "and", 1, 6),
            self._create_token("NUMBER", "1", 1, 10),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        left_ast = self._create_ast_node("LITERAL", value="true", line=1, column=1)
        right_ast = self._create_ast_node("NUMBER", value="1", line=1, column=10)
        intermediate_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        final_state = {
            "tokens": tokens,
            "pos": 2,
            "filename": "test.py",
            "error": ""
        }

        mock_parse_comparison.side_effect = [
            (left_ast, intermediate_state),
            (right_ast, final_state)
        ]

        result_ast, result_state = _parse_or_expression(parser_state)

        self.assertEqual(result_ast["type"], "BINARY_OP")
        self.assertEqual(result_ast["value"], "and")
        self.assertEqual(len(result_ast["children"]), 2)
        self.assertEqual(result_ast["children"][0], left_ast)
        self.assertEqual(result_ast["children"][1], right_ast)
        self.assertEqual(result_ast["line"], 1)
        self.assertEqual(result_ast["column"], 6)
        self.assertEqual(result_state["pos"], 2)

    @patch('_parse_or_expression_package._parse_or_expression_src._parse_comparison')
    def test_left_associativity(self, mock_parse_comparison):
        """Test chained logical operators are left-associative: a or b or c => ((a or b) or c)."""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("KEYWORD", "or", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 6),
            self._create_token("KEYWORD", "or", 1, 8),
            self._create_token("IDENTIFIER", "c", 1, 11),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        ast_a = self._create_ast_node("IDENTIFIER", value="a", line=1, column=1)
        ast_b = self._create_ast_node("IDENTIFIER", value="b", line=1, column=6)
        ast_c = self._create_ast_node("IDENTIFIER", value="c", line=1, column=11)

        state_1 = {"tokens": tokens, "pos": 1, "filename": "test.py", "error": ""}
        state_2 = {"tokens": tokens, "pos": 2, "filename": "test.py", "error": ""}
        state_3 = {"tokens": tokens, "pos": 3, "filename": "test.py", "error": ""}
        state_4 = {"tokens": tokens, "pos": 4, "filename": "test.py", "error": ""}
        state_5 = {"tokens": tokens, "pos": 5, "filename": "test.py", "error": ""}

        mock_parse_comparison.side_effect = [
            (ast_a, state_1),
            (ast_b, state_3),
            (ast_c, state_5)
        ]

        result_ast, result_state = _parse_or_expression(parser_state)

        self.assertEqual(result_ast["type"], "BINARY_OP")
        self.assertEqual(result_ast["value"], "or")
        self.assertEqual(result_ast["line"], 1)
        self.assertEqual(result_ast["column"], 8)
        self.assertEqual(len(result_ast["children"]), 2)
        self.assertEqual(result_ast["children"][1], ast_c)

        left_child = result_ast["children"][0]
        self.assertEqual(left_child["type"], "BINARY_OP")
        self.assertEqual(left_child["value"], "or")
        self.assertEqual(left_child["line"], 1)
        self.assertEqual(left_child["column"], 3)
        self.assertEqual(left_child["children"][0], ast_a)
        self.assertEqual(left_child["children"][1], ast_b)

        self.assertEqual(result_state["pos"], 5)

    @patch('_parse_or_expression_package._parse_or_expression_src._parse_comparison')
    def test_empty_tokens(self, mock_parse_comparison):
        """Test with empty token list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        left_ast = self._create_ast_node("LITERAL", value=None)
        mock_parse_comparison.return_value = (left_ast, parser_state)

        result_ast, result_state = _parse_or_expression(parser_state)

        self.assertEqual(result_ast, left_ast)
        self.assertEqual(result_state["pos"], 0)

    @patch('_parse_or_expression_package._parse_or_expression_src._parse_comparison')
    def test_at_end_of_tokens(self, mock_parse_comparison):
        """Test when position is at end of tokens."""
        tokens = [self._create_token("LITERAL", "x", 1, 1)]
        parser_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }

        left_ast = self._create_ast_node("IDENTIFIER", value="x", line=1, column=1)
        mock_parse_comparison.return_value = (left_ast, parser_state)

        result_ast, result_state = _parse_or_expression(parser_state)

        self.assertEqual(result_ast, left_ast)
        self.assertEqual(result_state["pos"], 1)

    @patch('_parse_or_expression_package._parse_or_expression_src._parse_comparison')
    def test_non_keyword_token(self, mock_parse_comparison):
        """Test when current token is not a KEYWORD type."""
        tokens = [
            self._create_token("LITERAL", "a", 1, 1),
            self._create_token("OPERATOR", "or", 1, 3),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        left_ast = self._create_ast_node("IDENTIFIER", value="a", line=1, column=1)
        intermediate_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        mock_parse_comparison.return_value = (left_ast, intermediate_state)

        result_ast, result_state = _parse_or_expression(parser_state)

        self.assertEqual(result_ast, left_ast)
        self.assertEqual(result_state["pos"], 1)

    @patch('_parse_or_expression_package._parse_or_expression_src._parse_comparison')
    def test_keyword_but_not_or_and(self, mock_parse_comparison):
        """Test when current token is KEYWORD but value is not 'or' or 'and'."""
        tokens = [
            self._create_token("LITERAL", "a", 1, 1),
            self._create_token("KEYWORD", "if", 1, 3),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        left_ast = self._create_ast_node("IDENTIFIER", value="a", line=1, column=1)
        intermediate_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        mock_parse_comparison.return_value = (left_ast, intermediate_state)

        result_ast, result_state = _parse_or_expression(parser_state)

        self.assertEqual(result_ast, left_ast)
        self.assertEqual(result_state["pos"], 1)

    @patch('_parse_or_expression_package._parse_or_expression_src._parse_comparison')
    def test_mixed_and_or_operators(self, mock_parse_comparison):
        """Test expression with mixed and/or operators respecting precedence."""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("KEYWORD", "or", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 6),
            self._create_token("KEYWORD", "and", 1, 8),
            self._create_token("IDENTIFIER", "c", 1, 12),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        ast_a = self._create_ast_node("IDENTIFIER", value="a", line=1, column=1)
        ast_b = self._create_ast_node("IDENTIFIER", value="b", line=1, column=6)
        ast_c = self._create_ast_node("IDENTIFIER", value="c", line=1, column=12)

        state_1 = {"tokens": tokens, "pos": 1, "filename": "test.py", "error": ""}
        state_2 = {"tokens": tokens, "pos": 2, "filename": "test.py", "error": ""}
        state_3 = {"tokens": tokens, "pos": 3, "filename": "test.py", "error": ""}
        state_4 = {"tokens": tokens, "pos": 4, "filename": "test.py", "error": ""}
        state_5 = {"tokens": tokens, "pos": 5, "filename": "test.py", "error": ""}

        mock_parse_comparison.side_effect = [
            (ast_a, state_1),
            (ast_b, state_3),
            (ast_c, state_5)
        ]

        result_ast, result_state = _parse_or_expression(parser_state)

        self.assertEqual(result_ast["type"], "BINARY_OP")
        self.assertEqual(result_ast["value"], "or")
        self.assertEqual(result_ast["line"], 1)
        self.assertEqual(result_ast["column"], 3)
        self.assertEqual(len(result_ast["children"]), 2)

        left_child = result_ast["children"][0]
        self.assertEqual(left_child, ast_a)

        right_child = result_ast["children"][1]
        self.assertEqual(right_child["type"], "BINARY_OP")
        self.assertEqual(right_child["value"], "and")
        self.assertEqual(right_child["line"], 1)
        self.assertEqual(right_child["column"], 8)
        self.assertEqual(right_child["children"][0], ast_b)
        self.assertEqual(right_child["children"][1], ast_c)

        self.assertEqual(result_state["pos"], 5)

    @patch('_parse_or_expression_package._parse_or_expression_src._parse_comparison')
    def test_token_missing_type_field(self, mock_parse_comparison):
        """Test when token is missing 'type' field."""
        tokens = [
            self._create_token("LITERAL", "a", 1, 1),
            {"value": "or", "line": 1, "column": 3},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        left_ast = self._create_ast_node("IDENTIFIER", value="a", line=1, column=1)
        intermediate_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        mock_parse_comparison.return_value = (left_ast, intermediate_state)

        result_ast, result_state = _parse_or_expression(parser_state)

        self.assertEqual(result_ast, left_ast)
        self.assertEqual(result_state["pos"], 1)

    @patch('_parse_or_expression_package._parse_or_expression_src._parse_comparison')
    def test_token_missing_value_field(self, mock_parse_comparison):
        """Test when token is missing 'value' field."""
        tokens = [
            self._create_token("LITERAL", "a", 1, 1),
            {"type": "KEYWORD", "line": 1, "column": 3},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        left_ast = self._create_ast_node("IDENTIFIER", value="a", line=1, column=1)
        intermediate_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        mock_parse_comparison.return_value = (left_ast, intermediate_state)

        result_ast, result_state = _parse_or_expression(parser_state)

        self.assertEqual(result_ast, left_ast)
        self.assertEqual(result_state["pos"], 1)


if __name__ == "__main__":
    unittest.main()
