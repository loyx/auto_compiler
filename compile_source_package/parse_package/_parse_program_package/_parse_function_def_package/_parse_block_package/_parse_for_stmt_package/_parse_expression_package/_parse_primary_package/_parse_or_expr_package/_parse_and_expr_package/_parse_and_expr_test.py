"""Unit tests for _parse_and_expr function."""

import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any

from ._parse_and_expr_src import _parse_and_expr


class TestParseAndExpr(unittest.TestCase):
    """Test cases for _parse_and_expr function."""

    def _create_parser_state(
        self,
        tokens: list,
        pos: int = 0,
        filename: str = "test.py"
    ) -> Dict[str, Any]:
        """Helper to create parser state dict."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_token(
        self,
        token_type: str,
        value: str,
        line: int = 1,
        column: int = 1
    ) -> Dict[str, Any]:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast_node(
        self,
        node_type: str,
        value: Any = None,
        children: list = None,
        line: int = 1,
        column: int = 1
    ) -> Dict[str, Any]:
        """Helper to create an AST node dict."""
        return {
            "type": node_type,
            "value": value,
            "children": children or [],
            "line": line,
            "column": column
        }

    @patch("projects.cc.files.main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_package._parse_or_expr_package._parse_and_expr_package._parse_and_expr_src._parse_not_expr")
    def test_single_operand_no_and(self, mock_parse_not_expr: MagicMock) -> None:
        """Test parsing single operand without AND operator."""
        # Setup
        operand_node = self._create_ast_node("IDENTIFIER", "x")
        
        def mock_not_expr_side_effect(state):
            state["pos"] += 1
            return operand_node
        
        mock_parse_not_expr.side_effect = mock_not_expr_side_effect
        
        tokens = [self._create_token("IDENTIFIER", "x")]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Execute
        result = _parse_and_expr(parser_state)
        
        # Verify
        self.assertEqual(result, operand_node)
        self.assertEqual(parser_state["pos"], 1)
        mock_parse_not_expr.assert_called_once_with(parser_state)

    @patch("projects.cc.files.main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_package._parse_or_expr_package._parse_and_expr_package._parse_and_expr_src._parse_not_expr")
    def test_simple_and_expression(self, mock_parse_not_expr: MagicMock) -> None:
        """Test parsing simple AND expression: a AND b."""
        # Setup
        left_operand = self._create_ast_node("IDENTIFIER", "a", line=1, column=1)
        right_operand = self._create_ast_node("IDENTIFIER", "b", line=1, column=5)
        
        mock_parse_not_expr.side_effect = [left_operand, right_operand]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", line=1, column=1),
            self._create_token("KEYWORD", "AND", line=1, column=3),
            self._create_token("IDENTIFIER", "b", line=1, column=5)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Execute
        result = _parse_and_expr(parser_state)
        
        # Verify
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "and")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0], left_operand)
        self.assertEqual(result["children"][1], right_operand)
        self.assertEqual(parser_state["pos"], 3)
        self.assertEqual(mock_parse_not_expr.call_count, 2)

    @patch("projects.cc.files.main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_package._parse_or_expr_package._parse_and_expr_package._parse_and_expr_src._parse_not_expr")
    def test_chained_and_expression(self, mock_parse_not_expr: MagicMock) -> None:
        """Test parsing chained AND expression: a AND b AND c (left-associative)."""
        # Setup
        operand_a = self._create_ast_node("IDENTIFIER", "a", line=1, column=1)
        operand_b = self._create_ast_node("IDENTIFIER", "b", line=1, column=5)
        operand_c = self._create_ast_node("IDENTIFIER", "c", line=1, column=9)
        
        mock_parse_not_expr.side_effect = [operand_a, operand_b, operand_c]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", line=1, column=1),
            self._create_token("KEYWORD", "AND", line=1, column=3),
            self._create_token("IDENTIFIER", "b", line=1, column=5),
            self._create_token("KEYWORD", "AND", line=1, column=7),
            self._create_token("IDENTIFIER", "c", line=1, column=9)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Execute
        result = _parse_and_expr(parser_state)
        
        # Verify left-associativity: (a AND b) AND c
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "and")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 7)  # Second AND token
        
        # Left child should be (a AND b)
        left_child = result["children"][0]
        self.assertEqual(left_child["type"], "BINARY_OP")
        self.assertEqual(left_child["value"], "and")
        self.assertEqual(left_child["line"], 1)
        self.assertEqual(left_child["column"], 3)  # First AND token
        self.assertEqual(left_child["children"][0], operand_a)
        self.assertEqual(left_child["children"][1], operand_b)
        
        # Right child should be c
        self.assertEqual(result["children"][1], operand_c)
        
        self.assertEqual(parser_state["pos"], 5)
        self.assertEqual(mock_parse_not_expr.call_count, 3)

    @patch("projects.cc.files.main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_package._parse_or_expr_package._parse_and_expr_package._parse_and_expr_src._parse_not_expr")
    def test_and_followed_by_non_and_token(self, mock_parse_not_expr: MagicMock) -> None:
        """Test parsing AND expression followed by non-AND token."""
        # Setup
        left_operand = self._create_ast_node("IDENTIFIER", "x", line=1, column=1)
        right_operand = self._create_ast_node("IDENTIFIER", "y", line=1, column=5)
        
        mock_parse_not_expr.side_effect = [left_operand, right_operand]
        
        tokens = [
            self._create_token("IDENTIFIER", "x", line=1, column=1),
            self._create_token("KEYWORD", "AND", line=1, column=3),
            self._create_token("IDENTIFIER", "y", line=1, column=5),
            self._create_token("KEYWORD", "OR", line=1, column=7),
            self._create_token("IDENTIFIER", "z", line=1, column=9)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Execute
        result = _parse_and_expr(parser_state)
        
        # Verify
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "and")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(parser_state["pos"], 3)  # Stops before OR token
        self.assertEqual(mock_parse_not_expr.call_count, 2)

    @patch("projects.cc.files.main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_package._parse_or_expr_package._parse_and_expr_package._parse_and_expr_src._parse_not_expr")
    def test_empty_tokens(self, mock_parse_not_expr: MagicMock) -> None:
        """Test parsing with empty token list."""
        # Setup
        empty_node = self._create_ast_node("EMPTY")
        mock_parse_not_expr.return_value = empty_node
        
        parser_state = self._create_parser_state([], pos=0)
        
        # Execute
        result = _parse_and_expr(parser_state)
        
        # Verify
        self.assertEqual(result, empty_node)
        self.assertEqual(parser_state["pos"], 0)
        mock_parse_not_expr.assert_called_once_with(parser_state)

    @patch("projects.cc.files.main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_package._parse_or_expr_package._parse_and_expr_package._parse_and_expr_src._parse_not_expr")
    def test_pos_at_end_of_tokens(self, mock_parse_not_expr: MagicMock) -> None:
        """Test parsing when pos is already at end of tokens."""
        # Setup
        operand_node = self._create_ast_node("IDENTIFIER", "x")
        mock_parse_not_expr.return_value = operand_node
        
        tokens = [self._create_token("IDENTIFIER", "x")]
        parser_state = self._create_parser_state(tokens, pos=1)
        
        # Execute
        result = _parse_and_expr(parser_state)
        
        # Verify
        self.assertEqual(result, operand_node)
        self.assertEqual(parser_state["pos"], 1)
        mock_parse_not_expr.assert_called_once_with(parser_state)

    @patch("projects.cc.files.main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_package._parse_or_expr_package._parse_and_expr_package._parse_and_expr_src._parse_not_expr")
    def test_and_token_position_tracking(self, mock_parse_not_expr: MagicMock) -> None:
        """Test that AND token line/column are correctly tracked in AST."""
        # Setup
        left_operand = self._create_ast_node("IDENTIFIER", "a", line=2, column=5)
        right_operand = self._create_ast_node("IDENTIFIER", "b", line=2, column=15)
        
        mock_parse_not_expr.side_effect = [left_operand, right_operand]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", line=2, column=5),
            self._create_token("KEYWORD", "AND", line=2, column=10),
            self._create_token("IDENTIFIER", "b", line=2, column=15)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Execute
        result = _parse_and_expr(parser_state)
        
        # Verify
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 10)  # AND token position
        self.assertEqual(result["children"][0]["line"], 2)
        self.assertEqual(result["children"][0]["column"], 5)
        self.assertEqual(result["children"][1]["line"], 2)
        self.assertEqual(result["children"][1]["column"], 15)

    @patch("projects.cc.files.main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_package._parse_or_expr_package._parse_and_expr_package._parse_and_expr_src._parse_not_expr")
    def test_complex_and_expression(self, mock_parse_not_expr: MagicMock) -> None:
        """Test parsing complex AND expression with multiple operands."""
        # Setup: a AND b AND c AND d
        operands = [
            self._create_ast_node("IDENTIFIER", chr(ord('a') + i), line=1, column=1 + i * 4)
            for i in range(4)
        ]
        mock_parse_not_expr.side_effect = operands
        
        tokens = []
        for i in range(4):
            tokens.append(self._create_token("IDENTIFIER", chr(ord('a') + i), line=1, column=1 + i * 4))
            if i < 3:
                tokens.append(self._create_token("KEYWORD", "AND", line=1, column=3 + i * 4))
        
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Execute
        result = _parse_and_expr(parser_state)
        
        # Verify structure: ((a AND b) AND c) AND d
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "and")
        self.assertEqual(result["column"], 9)  # Third AND
        
        # Verify left-associativity chain
        left_most = result["children"][0]["children"][0]["children"][0]
        self.assertEqual(left_most, operands[0])
        
        self.assertEqual(parser_state["pos"], 7)
        self.assertEqual(mock_parse_not_expr.call_count, 4)


if __name__ == "__main__":
    unittest.main()
