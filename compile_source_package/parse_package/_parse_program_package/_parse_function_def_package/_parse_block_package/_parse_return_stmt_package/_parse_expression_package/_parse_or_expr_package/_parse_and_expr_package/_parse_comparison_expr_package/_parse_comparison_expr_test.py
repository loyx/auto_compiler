# -*- coding: utf-8 -*-
"""
Unit tests for _parse_comparison_expr function.
Tests comparison expression parsing (<, >, <=, >=, ==, !=).
"""

import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any

# Import the function under test using relative import
from ._parse_comparison_expr_src import _parse_comparison_expr


class TestParseComparisonExpr(unittest.TestCase):
    """Test cases for _parse_comparison_expr function."""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        """Helper to create a parser_state dict."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_ast_node(self, node_type: str, value: Any = None, children: list = None, line: int = 0, column: int = 0) -> Dict[str, Any]:
        """Helper to create an AST node dict."""
        return {
            "type": node_type,
            "value": value,
            "children": children if children is not None else [],
            "line": line,
            "column": column
        }

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_parse_lt_comparison(self, mock_additive_expr: MagicMock):
        """Test parsing 'less than' comparison: a < b"""
        # Setup: left operand (a), operator (<), right operand (b)
        left_node = self._create_ast_node("IDENTIFIER", "a", line=1, column=0)
        right_node = self._create_ast_node("IDENTIFIER", "b", line=1, column=4)
        
        # Mock _parse_additive_expr to return left then right
        mock_additive_expr.side_effect = [left_node, right_node]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 0),
            self._create_token("LT", "<", 1, 2),
            self._create_token("IDENTIFIER", "b", 1, 4),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Execute
        result = _parse_comparison_expr(parser_state)
        
        # Verify
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "<")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 2)
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0], left_node)
        self.assertEqual(result["children"][1], right_node)
        self.assertEqual(parser_state["pos"], 3)  # Should consume all 3 tokens
        self.assertEqual(mock_additive_expr.call_count, 2)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_parse_gt_comparison(self, mock_additive_expr: MagicMock):
        """Test parsing 'greater than' comparison: a > b"""
        left_node = self._create_ast_node("IDENTIFIER", "a", line=1, column=0)
        right_node = self._create_ast_node("IDENTIFIER", "b", line=1, column=4)
        
        mock_additive_expr.side_effect = [left_node, right_node]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 0),
            self._create_token("GT", ">", 1, 2),
            self._create_token("IDENTIFIER", "b", 1, 4),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], ">")
        self.assertEqual(result["column"], 2)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_parse_le_comparison(self, mock_additive_expr: MagicMock):
        """Test parsing 'less than or equal' comparison: a <= b"""
        left_node = self._create_ast_node("IDENTIFIER", "a", line=1, column=0)
        right_node = self._create_ast_node("IDENTIFIER", "b", line=1, column=5)
        
        mock_additive_expr.side_effect = [left_node, right_node]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 0),
            self._create_token("LE", "<=", 1, 2),
            self._create_token("IDENTIFIER", "b", 1, 5),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "<=")

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_parse_ge_comparison(self, mock_additive_expr: MagicMock):
        """Test parsing 'greater than or equal' comparison: a >= b"""
        left_node = self._create_ast_node("IDENTIFIER", "a", line=1, column=0)
        right_node = self._create_ast_node("IDENTIFIER", "b", line=1, column=5)
        
        mock_additive_expr.side_effect = [left_node, right_node]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 0),
            self._create_token("GE", ">=", 1, 2),
            self._create_token("IDENTIFIER", "b", 1, 5),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], ">=")

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_parse_eq_comparison(self, mock_additive_expr: MagicMock):
        """Test parsing 'equal' comparison: a == b"""
        left_node = self._create_ast_node("IDENTIFIER", "a", line=1, column=0)
        right_node = self._create_ast_node("IDENTIFIER", "b", line=1, column=5)
        
        mock_additive_expr.side_effect = [left_node, right_node]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 0),
            self._create_token("EQ", "==", 1, 2),
            self._create_token("IDENTIFIER", "b", 1, 5),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "==")

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_parse_ne_comparison(self, mock_additive_expr: MagicMock):
        """Test parsing 'not equal' comparison: a != b"""
        left_node = self._create_ast_node("IDENTIFIER", "a", line=1, column=0)
        right_node = self._create_ast_node("IDENTIFIER", "b", line=1, column=5)
        
        mock_additive_expr.side_effect = [left_node, right_node]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 0),
            self._create_token("NE", "!=", 1, 2),
            self._create_token("IDENTIFIER", "b", 1, 5),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "!=")

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_no_comparison_operator(self, mock_additive_expr: MagicMock):
        """Test when there's no comparison operator - should return left operand only"""
        left_node = self._create_ast_node("IDENTIFIER", "a", line=1, column=0)
        
        mock_additive_expr.return_value = left_node
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 0),
            self._create_token("SEMICOLON", ";", 1, 1),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_comparison_expr(parser_state)
        
        # Should return left operand as-is (not wrapped in BINARY_OP)
        self.assertEqual(result, left_node)
        self.assertEqual(parser_state["pos"], 0)  # Should not consume any token
        mock_additive_expr.assert_called_once()

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_empty_tokens(self, mock_additive_expr: MagicMock):
        """Test with empty token list - boundary condition"""
        left_node = self._create_ast_node("IDENTIFIER", "a", line=1, column=0)
        mock_additive_expr.return_value = left_node
        
        parser_state = self._create_parser_state([], pos=0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result, left_node)
        self.assertEqual(parser_state["pos"], 0)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_pos_at_end_of_tokens(self, mock_additive_expr: MagicMock):
        """Test when pos is already at end of tokens"""
        left_node = self._create_ast_node("IDENTIFIER", "a", line=1, column=0)
        mock_additive_expr.return_value = left_node
        
        tokens = [self._create_token("IDENTIFIER", "a", 1, 0)]
        parser_state = self._create_parser_state(tokens, pos=1)  # pos at end
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result, left_node)
        self.assertEqual(parser_state["pos"], 1)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_left_operand_error(self, mock_additive_expr: MagicMock):
        """Test when left operand parsing returns an error"""
        error_node = self._create_ast_node("ERROR", "parse error")
        parser_state_with_error = {
            "tokens": [],
            "pos": 0,
            "error": "parse error"
        }
        mock_additive_expr.return_value = error_node
        mock_additive_expr.side_effect = lambda ps: ps.update({"error": "parse error"}) or error_node if False else error_node
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 0),
            self._create_token("LT", "<", 1, 2),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        parser_state["error"] = None  # Initially no error
        
        # Mock to set error after first call
        def side_effect(ps):
            ps["error"] = "parse error"
            return error_node
        
        mock_additive_expr.side_effect = side_effect
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result, error_node)
        self.assertEqual(parser_state["error"], "parse error")
        mock_additive_expr.assert_called_once()

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_right_operand_error(self, mock_additive_expr: MagicMock):
        """Test when right operand parsing returns an error"""
        left_node = self._create_ast_node("IDENTIFIER", "a", line=1, column=0)
        error_node = self._create_ast_node("ERROR", "parse error")
        
        def side_effect(ps):
            if mock_additive_expr.call_count == 1:
                return left_node
            else:
                ps["error"] = "parse error"
                return error_node
        
        mock_additive_expr.side_effect = side_effect
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 0),
            self._create_token("LT", "<", 1, 2),
            self._create_token("IDENTIFIER", "b", 1, 4),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result, error_node)
        self.assertEqual(parser_state["error"], "parse error")
        self.assertEqual(mock_additive_expr.call_count, 2)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_no_chained_comparison(self, mock_additive_expr: MagicMock):
        """Test that chained comparisons are not supported - only first comparison is parsed"""
        left_node = self._create_ast_node("IDENTIFIER", "a", line=1, column=0)
        right_node = self._create_ast_node("IDENTIFIER", "b", line=1, column=4)
        
        mock_additive_expr.side_effect = [left_node, right_node]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 0),
            self._create_token("LT", "<", 1, 2),
            self._create_token("IDENTIFIER", "b", 1, 4),
            self._create_token("LT", "<", 1, 6),
            self._create_token("IDENTIFIER", "c", 1, 8),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_comparison_expr(parser_state)
        
        # Should only parse a < b, not the chained comparison
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "<")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(parser_state["pos"], 3)  # Only consumed 3 tokens
        self.assertEqual(mock_additive_expr.call_count, 2)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_complex_expressions_as_operands(self, mock_additive_expr: MagicMock):
        """Test with complex expressions as operands (e.g., a + b < c - d)"""
        left_expr = self._create_ast_node("BINARY_OP", "+", children=[
            self._create_ast_node("IDENTIFIER", "a"),
            self._create_ast_node("IDENTIFIER", "b")
        ], line=1, column=0)
        right_expr = self._create_ast_node("BINARY_OP", "-", children=[
            self._create_ast_node("IDENTIFIER", "c"),
            self._create_ast_node("IDENTIFIER", "d")
        ], line=1, column=6)
        
        mock_additive_expr.side_effect = [left_expr, right_expr]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 0),
            self._create_token("PLUS", "+", 1, 2),
            self._create_token("IDENTIFIER", "b", 1, 4),
            self._create_token("LT", "<", 1, 6),
            self._create_token("IDENTIFIER", "c", 1, 8),
            self._create_token("MINUS", "-", 1, 10),
            self._create_token("IDENTIFIER", "d", 1, 12),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "<")
        self.assertEqual(result["children"][0], left_expr)
        self.assertEqual(result["children"][1], right_expr)


if __name__ == "__main__":
    unittest.main()
