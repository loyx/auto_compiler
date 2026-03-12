# -*- coding: utf-8 -*-
"""Unit tests for handle_if_stmt function."""

import unittest
from unittest.mock import patch
from typing import Dict, Any

from .handle_if_stmt_src import handle_if_stmt


class TestHandleIfStmt(unittest.TestCase):
    """Test cases for handle_if_stmt function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.func_name = "test_func"
        self.label_counter: Dict[str, int] = {
            "while_cond": 0,
            "while_end": 0,
            "if_else": 0,
            "if_end": 0,
        }
        self.var_offsets: Dict[str, int] = {"x": 0, "y": 8}
        self.next_offset = 16

    def test_if_stmt_without_else_body(self) -> None:
        """Test IF statement with only then_body (no else)."""
        stmt: Dict[str, Any] = {
            "type": "if",
            "condition": {"type": "binary", "op": ">", "left": {"type": "var", "name": "x"}, "right": {"type": "literal", "value": 0}},
            "then_body": [{"type": "assign", "target": "y", "value": {"type": "literal", "value": 1}}],
        }

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr, patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code"
        ) as mock_gen_stmt:
            mock_gen_expr.return_value = ("mov x0, #1\n", 24)
            mock_gen_stmt.return_value = ("str x1, [sp, #8]\n", 32)

            code, offset = handle_if_stmt(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

            # Verify label counter was incremented
            self.assertEqual(self.label_counter["if_else"], 1)
            self.assertEqual(self.label_counter["if_end"], 1)

            # Verify generated code structure
            self.assertIn("mov x0, #1", code)
            self.assertIn("cbz x0, test_func_if_end_0", code)
            self.assertIn("str x1, [sp, #8]", code)
            self.assertIn("test_func_if_end_0:", code)

            # Verify offset was updated
            self.assertEqual(offset, 32)

            # Verify mocks were called correctly
            mock_gen_expr.assert_called_once()
            mock_gen_stmt.assert_called_once()

    def test_if_stmt_with_else_body(self) -> None:
        """Test IF statement with both then_body and else_body."""
        stmt: Dict[str, Any] = {
            "type": "if",
            "condition": {"type": "binary", "op": "==", "left": {"type": "var", "name": "x"}, "right": {"type": "literal", "value": 0}},
            "then_body": [{"type": "assign", "target": "y", "value": {"type": "literal", "value": 1}}],
            "else_body": [{"type": "assign", "target": "y", "value": {"type": "literal", "value": 2}}],
        }

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.handle_if_stmt_src.generate_expression_code"
        ) as mock_gen_expr, patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.handle_if_stmt_src.generate_statement_code"
        ) as mock_gen_stmt:
            mock_gen_expr.return_value = ("cmp x0, #0\n", 24)
            mock_gen_stmt.side_effect = [
                ("str x1, [sp, #8]\n", 32),  # then_body statement
                ("str x2, [sp, #8]\n", 40),  # else_body statement
            ]

            code, offset = handle_if_stmt(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

            # Verify label counter was incremented
            self.assertEqual(self.label_counter["if_else"], 1)
            self.assertEqual(self.label_counter["if_end"], 1)

            # Verify generated code structure
            self.assertIn("cmp x0, #0", code)
            self.assertIn("cbz x0, test_func_if_else_0", code)
            self.assertIn("str x1, [sp, #8]", code)
            self.assertIn("b test_func_if_end_0", code)
            self.assertIn("test_func_if_else_0:", code)
            self.assertIn("str x2, [sp, #8]", code)
            self.assertIn("test_func_if_end_0:", code)

            # Verify offset was updated
            self.assertEqual(offset, 40)

            # Verify mocks were called correctly (once for expr, twice for stmt)
            mock_gen_expr.assert_called_once()
            self.assertEqual(mock_gen_stmt.call_count, 2)

    def test_if_stmt_with_multiple_then_statements(self) -> None:
        """Test IF statement with multiple statements in then_body."""
        stmt: Dict[str, Any] = {
            "type": "if",
            "condition": {"type": "literal", "value": True},
            "then_body": [
                {"type": "assign", "target": "a", "value": {"type": "literal", "value": 1}},
                {"type": "assign", "target": "b", "value": {"type": "literal", "value": 2}},
                {"type": "assign", "target": "c", "value": {"type": "literal", "value": 3}},
            ],
        }

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.handle_if_stmt_src.generate_expression_code"
        ) as mock_gen_expr, patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.handle_if_stmt_src.generate_statement_code"
        ) as mock_gen_stmt:
            mock_gen_expr.return_value = ("mov x0, #1\n", 24)
            mock_gen_stmt.side_effect = [
                ("str x1, [sp, #0]\n", 32),
                ("str x2, [sp, #8]\n", 40),
                ("str x3, [sp, #16]\n", 48),
            ]

            code, offset = handle_if_stmt(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

            # Verify label counter was incremented
            self.assertEqual(self.label_counter["if_else"], 1)
            self.assertEqual(self.label_counter["if_end"], 1)

            # Verify offset was updated to last statement's offset
            self.assertEqual(offset, 48)

            # Verify generate_statement_code was called 3 times
            self.assertEqual(mock_gen_stmt.call_count, 3)

    def test_if_stmt_with_empty_then_body(self) -> None:
        """Test IF statement with empty then_body."""
        stmt: Dict[str, Any] = {
            "type": "if",
            "condition": {"type": "literal", "value": False},
            "then_body": [],
            "else_body": [{"type": "assign", "target": "y", "value": {"type": "literal", "value": 0}}],
        }

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.handle_if_stmt_src.generate_expression_code"
        ) as mock_gen_expr, patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.handle_if_stmt_src.generate_statement_code"
        ) as mock_gen_stmt:
            mock_gen_expr.return_value = ("mov x0, #0\n", 24)
            mock_gen_stmt.return_value = ("mov x1, #0\n", 32)

            code, offset = handle_if_stmt(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

            # Verify label counter was incremented
            self.assertEqual(self.label_counter["if_else"], 1)
            self.assertEqual(self.label_counter["if_end"], 1)

            # Verify generated code has else branch
            self.assertIn("cbz x0, test_func_if_else_0", code)
            self.assertIn("b test_func_if_end_0", code)
            self.assertIn("test_func_if_else_0:", code)
            self.assertIn("test_func_if_end_0:", code)

            self.assertEqual(offset, 32)

    def test_if_stmt_with_empty_else_body(self) -> None:
        """Test IF statement with empty else_body (treated as no else)."""
        stmt: Dict[str, Any] = {
            "type": "if",
            "condition": {"type": "literal", "value": True},
            "then_body": [{"type": "assign", "target": "x", "value": {"type": "literal", "value": 1}}],
            "else_body": [],
        }

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.handle_if_stmt_src.generate_expression_code"
        ) as mock_gen_expr, patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.handle_if_stmt_src.generate_statement_code"
        ) as mock_gen_stmt:
            mock_gen_expr.return_value = ("mov x0, #1\n", 24)
            mock_gen_stmt.return_value = ("str x1, [sp, #0]\n", 32)

            code, offset = handle_if_stmt(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

            # Verify label counter was incremented
            self.assertEqual(self.label_counter["if_else"], 1)
            self.assertEqual(self.label_counter["if_end"], 1)

            # Verify no else branch (jumps directly to end)
            self.assertIn("cbz x0, test_func_if_end_0", code)
            self.assertNotIn("test_func_if_else_0:", code)
            self.assertIn("test_func_if_end_0:", code)

            self.assertEqual(offset, 32)

    def test_label_counter_increments_correctly(self) -> None:
        """Test that label_counter is modified in-place correctly."""
        stmt: Dict[str, Any] = {
            "type": "if",
            "condition": {"type": "literal", "value": True},
            "then_body": [],
        }

        initial_if_else = self.label_counter["if_else"]
        initial_if_end = self.label_counter["if_end"]

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.handle_if_stmt_src.generate_expression_code"
        ) as mock_gen_expr, patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.handle_if_stmt_src.generate_statement_code"
        ) as mock_gen_stmt:
            mock_gen_expr.return_value = ("nop\n", self.next_offset)
            mock_gen_stmt.return_value = ("nop\n", self.next_offset)

            handle_if_stmt(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

            # Verify counters were incremented by 1
            self.assertEqual(self.label_counter["if_else"], initial_if_else + 1)
            self.assertEqual(self.label_counter["if_end"], initial_if_end + 1)

            # Other counters should remain unchanged
            self.assertEqual(self.label_counter["while_cond"], 0)
            self.assertEqual(self.label_counter["while_end"], 0)

    def test_label_names_include_func_name(self) -> None:
        """Test that generated labels include the function name."""
        stmt: Dict[str, Any] = {
            "type": "if",
            "condition": {"type": "literal", "value": True},
            "then_body": [],
        }

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.handle_if_stmt_src.generate_expression_code"
        ) as mock_gen_expr, patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.handle_if_stmt_src.generate_statement_code"
        ) as mock_gen_stmt:
            mock_gen_expr.return_value = ("nop\n", self.next_offset)
            mock_gen_stmt.return_value = ("nop\n", self.next_offset)

            code, _ = handle_if_stmt(stmt, "my_function", self.label_counter, self.var_offsets, self.next_offset)

            # Verify labels contain function name
            self.assertIn("my_function_if_else_0", code)
            self.assertIn("my_function_if_end_0", code)

    def test_offset_propagation_through_statements(self) -> None:
        """Test that offset is properly propagated through statement generation."""
        stmt: Dict[str, Any] = {
            "type": "if",
            "condition": {"type": "literal", "value": True},
            "then_body": [
                {"type": "assign", "target": "a", "value": {"type": "literal", "value": 1}},
                {"type": "assign", "target": "b", "value": {"type": "literal", "value": 2}},
            ],
        }

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.handle_if_stmt_src.generate_expression_code"
        ) as mock_gen_expr, patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.handle_if_stmt_src.generate_statement_code"
        ) as mock_gen_stmt:
            mock_gen_expr.return_value = ("nop\n", 24)
            mock_gen_stmt.side_effect = [
                ("stmt1\n", 32),
                ("stmt2\n", 40),
            ]

            _, offset = handle_if_stmt(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

            # Verify final offset is from last statement
            self.assertEqual(offset, 40)

            # Verify second statement was called with offset from first statement
            calls = mock_gen_stmt.call_args_list
            self.assertEqual(calls[0][0][4], 24)  # First call gets offset from generate_expression_code
            self.assertEqual(calls[1][0][4], 32)  # Second call gets offset from first statement

    def test_multiple_if_statements_sequential(self) -> None:
        """Test handling multiple IF statements sequentially (label counter increments)."""
        stmt: Dict[str, Any] = {
            "type": "if",
            "condition": {"type": "literal", "value": True},
            "then_body": [],
        }

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.handle_if_stmt_src.generate_expression_code"
        ) as mock_gen_expr, patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.handle_if_stmt_src.generate_statement_code"
        ) as mock_gen_stmt:
            mock_gen_expr.return_value = ("nop\n", self.next_offset)
            mock_gen_stmt.return_value = ("nop\n", self.next_offset)

            # First IF statement
            code1, _ = handle_if_stmt(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
            # Second IF statement
            code2, _ = handle_if_stmt(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

            # Verify unique labels for each IF
            self.assertIn("test_func_if_else_0", code1)
            self.assertIn("test_func_if_end_0", code1)
            self.assertIn("test_func_if_else_1", code2)
            self.assertIn("test_func_if_end_1", code2)

            # Verify counter was incremented twice
            self.assertEqual(self.label_counter["if_else"], 2)
            self.assertEqual(self.label_counter["if_end"], 2)


if __name__ == "__main__":
    unittest.main()
