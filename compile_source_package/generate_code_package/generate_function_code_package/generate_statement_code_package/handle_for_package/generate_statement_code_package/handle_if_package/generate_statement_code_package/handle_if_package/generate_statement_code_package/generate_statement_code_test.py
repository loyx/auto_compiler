# -*- coding: utf-8 -*-
"""Unit tests for generate_statement_code function."""

import unittest
from unittest.mock import patch
from typing import Dict


class TestGenerateStatementCode(unittest.TestCase):
    """Test cases for generate_statement_code function."""

    def setUp(self):
        """Set up test fixtures."""
        self.func_name = "test_func"
        self.label_counter: Dict[str, int] = {"if_else": 0, "if_end": 0, "while_start": 0, "while_end": 0}
        self.var_offsets: Dict[str, int] = {}
        self.next_offset = 0

    def _import_uut(self):
        """Import the unit under test."""
        from .generate_statement_code_src import generate_statement_code
        return generate_statement_code

    # ==================== Assignment Statement Tests ====================

    def test_assignment_new_variable(self):
        """Test assignment statement with a new variable."""
        generate_statement_code = self._import_uut()
        stmt = {
            "type": "assignment",
            "var_name": "x",
            "value": {"type": "literal", "value": 42}
        }

        with patch('generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_gen_expr:
            mock_gen_expr.return_value = "    LDR R0, =42\n"

            asm, offset = generate_statement_code(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

            self.assertIn("LDR R0, =42", asm)
            self.assertIn("STR R0, [SP, #0]", asm)
            self.assertEqual(offset, 4)
            self.assertEqual(self.var_offsets["x"], 0)

    def test_assignment_existing_variable(self):
        """Test assignment statement with an existing variable."""
        generate_statement_code = self._import_uut()
        self.var_offsets = {"x": 8}
        stmt = {
            "type": "assignment",
            "var_name": "x",
            "value": {"type": "literal", "value": 100}
        }

        with patch('generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_gen_expr:
            mock_gen_expr.return_value = "    LDR R0, =100\n"

            asm, offset = generate_statement_code(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

            self.assertIn("LDR R0, =100", asm)
            self.assertIn("STR R0, [SP, #8]", asm)
            self.assertEqual(offset, 0)
            self.assertEqual(self.var_offsets["x"], 8)

    def test_assignment_complex_expression(self):
        """Test assignment with a complex expression."""
        generate_statement_code = self._import_uut()
        stmt = {
            "type": "assignment",
            "var_name": "y",
            "value": {"type": "add", "left": {"type": "var", "name": "a"}, "right": {"type": "var", "name": "b"}}
        }

        with patch('generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_gen_expr:
            mock_gen_expr.return_value = "    LDR R0, [SP, #0]\n    LDR R1, [SP, #4]\n    ADD R0, R0, R1\n"

            asm, offset = generate_statement_code(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

            self.assertIn("ADD R0, R0, R1", asm)
            self.assertIn("STR R0, [SP, #0]", asm)
            self.assertEqual(offset, 4)

    # ==================== If Statement Tests ====================

    def test_if_statement_delegates_to_handler(self):
        """Test if statement delegates to handle_if_statement."""
        generate_statement_code = self._import_uut()
        stmt = {
            "type": "if",
            "condition": {"type": "literal", "value": 1},
            "then_body": [],
            "else_body": []
        }

        with patch('generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_statement_package.handle_if_statement_src.handle_if_statement') as mock_handle_if:
            mock_handle_if.return_value = ("    ; if code\n", 8)

            asm, offset = generate_statement_code(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

            mock_handle_if.assert_called_once_with(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
            self.assertEqual(asm, "    ; if code\n")
            self.assertEqual(offset, 8)

    # ==================== While Statement Tests ====================

    def test_while_statement_delegates_to_handler(self):
        """Test while statement delegates to handle_while_statement."""
        generate_statement_code = self._import_uut()
        stmt = {
            "type": "while",
            "condition": {"type": "literal", "value": 1},
            "body": []
        }

        with patch('generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_while_statement_package.handle_while_statement_src.handle_while_statement') as mock_handle_while:
            mock_handle_while.return_value = ("    ; while code\n", 0)

            asm, offset = generate_statement_code(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

            mock_handle_while.assert_called_once_with(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
            self.assertEqual(asm, "    ; while code\n")
            self.assertEqual(offset, 0)

    # ==================== Return Statement Tests ====================

    def test_return_statement_with_value(self):
        """Test return statement with a value."""
        generate_statement_code = self._import_uut()
        stmt = {
            "type": "return",
            "value": {"type": "literal", "value": 42}
        }

        with patch('generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_gen_expr:
            mock_gen_expr.return_value = "    LDR R0, =42\n"

            asm, offset = generate_statement_code(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

            self.assertIn("LDR R0, =42", asm)
            self.assertIn("STR R0, [SP, #-4]!", asm)
            self.assertIn("LDR PC, [SP], #4", asm)
            self.assertEqual(offset, 0)

    def test_return_statement_without_value(self):
        """Test return statement without a value."""
        generate_statement_code = self._import_uut()
        stmt = {
            "type": "return",
            "value": None
        }

        asm, offset = generate_statement_code(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

        self.assertEqual(asm, "    LDR PC, [SP], #4\n")
        self.assertEqual(offset, 0)

    def test_return_statement_no_value_key(self):
        """Test return statement with no 'value' key."""
        generate_statement_code = self._import_uut()
        stmt = {
            "type": "return"
        }

        asm, offset = generate_statement_code(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

        self.assertEqual(asm, "    LDR PC, [SP], #4\n")
        self.assertEqual(offset, 0)

    # ==================== Expression Statement Tests ====================

    def test_expression_statement(self):
        """Test standalone expression statement."""
        generate_statement_code = self._import_uut()
        stmt = {
            "type": "expression",
            "expression": {"type": "add", "left": {"type": "literal", "value": 1}, "right": {"type": "literal", "value": 2}}
        }

        with patch('generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_gen_expr:
            mock_gen_expr.return_value = "    LDR R0, =1\n    LDR R1, =2\n    ADD R0, R0, R1\n"

            asm, offset = generate_statement_code(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

            mock_gen_expr.assert_called_once_with(stmt["expression"], self.var_offsets)
            self.assertIn("ADD R0, R0, R1", asm)
            self.assertEqual(offset, 0)

    # ==================== Unknown Statement Type Tests ====================

    def test_unknown_statement_type(self):
        """Test unknown statement type returns empty code."""
        generate_statement_code = self._import_uut()
        stmt = {
            "type": "unknown_type",
            "data": "some data"
        }

        asm, offset = generate_statement_code(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

        self.assertEqual(asm, "")
        self.assertEqual(offset, 0)

    def test_empty_statement_type(self):
        """Test statement with empty type returns empty code."""
        generate_statement_code = self._import_uut()
        stmt = {
            "type": ""
        }

        asm, offset = generate_statement_code(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

        self.assertEqual(asm, "")
        self.assertEqual(offset, 0)

    def test_statement_without_type_key(self):
        """Test statement without 'type' key returns empty code."""
        generate_statement_code = self._import_uut()
        stmt = {
            "data": "some data"
        }

        asm, offset = generate_statement_code(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

        self.assertEqual(asm, "")
        self.assertEqual(offset, 0)

    # ==================== Edge Cases and Boundary Tests ====================

    def test_multiple_assignments_accumulate_offsets(self):
        """Test multiple assignments properly accumulate variable offsets."""
        generate_statement_code = self._import_uut()

        stmt1 = {"type": "assignment", "var_name": "a", "value": {"type": "literal", "value": 1}}
        stmt2 = {"type": "assignment", "var_name": "b", "value": {"type": "literal", "value": 2}}
        stmt3 = {"type": "assignment", "var_name": "c", "value": {"type": "literal", "value": 3}}

        with patch('generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_gen_expr:
            mock_gen_expr.return_value = "    LDR R0, =1\n"

            offset = 0
            for stmt in [stmt1, stmt2, stmt3]:
                _, offset = generate_statement_code(stmt, self.func_name, self.label_counter, self.var_offsets, offset)

            self.assertEqual(self.var_offsets["a"], 0)
            self.assertEqual(self.var_offsets["b"], 4)
            self.assertEqual(self.var_offsets["c"], 8)
            self.assertEqual(offset, 12)

    def test_var_offsets_mutation_persists(self):
        """Test that var_offsets mutations persist across calls."""
        generate_statement_code = self._import_uut()
        stmt = {"type": "assignment", "var_name": "x", "value": {"type": "literal", "value": 42}}

        with patch('generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_gen_expr:
            mock_gen_expr.return_value = "    LDR R0, =42\n"

            generate_statement_code(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

            self.assertIn("x", self.var_offsets)
            self.assertEqual(self.var_offsets["x"], 0)

    def test_label_counter_not_mutated_for_non_control_flow(self):
        """Test that label_counter is not mutated for assignment/expression/return."""
        generate_statement_code = self._import_uut()
        initial_counter = self.label_counter.copy()

        stmt_assign = {"type": "assignment", "var_name": "x", "value": {"type": "literal", "value": 1}}
        with patch('generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_gen_expr:
            mock_gen_expr.return_value = "    LDR R0, =1\n"
            generate_statement_code(stmt_assign, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

        self.assertEqual(self.label_counter, initial_counter)

        stmt_expr = {"type": "expression", "expression": {"type": "literal", "value": 1}}
        with patch('generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_gen_expr:
            mock_gen_expr.return_value = "    LDR R0, =1\n"
            generate_statement_code(stmt_expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

        self.assertEqual(self.label_counter, initial_counter)

    def test_next_offset_unchanged_for_non_assignment(self):
        """Test that next_offset is unchanged for non-assignment statements."""
        generate_statement_code = self._import_uut()
        initial_offset = 100

        stmt_expr = {"type": "expression", "expression": {"type": "literal", "value": 1}}
        with patch('generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_gen_expr:
            mock_gen_expr.return_value = "    LDR R0, =1\n"
            _, offset = generate_statement_code(stmt_expr, self.func_name, self.label_counter, self.var_offsets, initial_offset)
            self.assertEqual(offset, initial_offset)

        stmt_return = {"type": "return", "value": {"type": "literal", "value": 1}}
        with patch('generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_gen_expr:
            mock_gen_expr.return_value = "    LDR R0, =1\n"
            _, offset = generate_statement_code(stmt_return, self.func_name, self.label_counter, self.var_offsets, initial_offset)
            self.assertEqual(offset, initial_offset)


if __name__ == "__main__":
    unittest.main()
