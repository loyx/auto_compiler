# -*- coding: utf-8 -*-
"""Unit tests for handle_assign function."""

import unittest
from unittest.mock import patch

from .handle_assign_src import handle_assign


class TestHandleAssign(unittest.TestCase):
    """Test cases for handle_assign function."""

    def test_handle_assign_simple_literal(self):
        """Test ASSIGN with simple literal expression."""
        stmt = {
            "type": "ASSIGN",
            "var_name": "x",
            "expression": {
                "type": "LITERAL",
                "value": 42
            }
        }
        func_name = "main"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {"x": 8}
        next_offset = 0

        with patch("handle_assign_package.handle_assign_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("MOV R0, #42", 0)

            asm_code, updated_offset = handle_assign(
                stmt, func_name, label_counter, var_offsets, next_offset
            )

            expected_asm = "MOV R0, #42\nSTR R0, [FP, #8]"
            self.assertEqual(asm_code, expected_asm)
            self.assertEqual(updated_offset, 0)
            mock_gen_expr.assert_called_once_with(
                stmt["expression"], func_name, label_counter, var_offsets, next_offset
            )

    def test_handle_assign_identifier_expression(self):
        """Test ASSIGN with identifier expression (variable copy)."""
        stmt = {
            "type": "ASSIGN",
            "var_name": "y",
            "expression": {
                "type": "IDENTIFIER",
                "name": "x"
            }
        }
        func_name = "main"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {"x": 8, "y": 12}
        next_offset = 0

        with patch("handle_assign_package.handle_assign_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("LDR R0, [FP, #8]", 0)

            asm_code, updated_offset = handle_assign(
                stmt, func_name, label_counter, var_offsets, next_offset
            )

            expected_asm = "LDR R0, [FP, #8]\nSTR R0, [FP, #12]"
            self.assertEqual(asm_code, expected_asm)
            self.assertEqual(updated_offset, 0)

    def test_handle_assign_binary_expression(self):
        """Test ASSIGN with binary operation expression."""
        stmt = {
            "type": "ASSIGN",
            "var_name": "z",
            "expression": {
                "type": "BINARY_OP",
                "op": "ADD",
                "left": {"type": "IDENTIFIER", "name": "x"},
                "right": {"type": "LITERAL", "value": 1}
            }
        }
        func_name = "main"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {"x": 8, "z": 16}
        next_offset = 0

        with patch("handle_assign_package.handle_assign_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("LDR R0, [FP, #8]\nMOV R1, #1\nADD R0, R0, R1", 0)

            asm_code, updated_offset = handle_assign(
                stmt, func_name, label_counter, var_offsets, next_offset
            )

            expected_asm = "LDR R0, [FP, #8]\nMOV R1, #1\nADD R0, R0, R1\nSTR R0, [FP, #16]"
            self.assertEqual(asm_code, expected_asm)
            self.assertEqual(updated_offset, 0)

    def test_handle_assign_function_call_expression(self):
        """Test ASSIGN with function call expression."""
        stmt = {
            "type": "ASSIGN",
            "var_name": "result",
            "expression": {
                "type": "CALL",
                "func_name": "foo",
                "args": [{"type": "LITERAL", "value": 5}]
            }
        }
        func_name = "main"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {"result": 20}
        next_offset = 0

        with patch("handle_assign_package.handle_assign_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("MOV R0, #5\nBL foo", 0)

            asm_code, updated_offset = handle_assign(
                stmt, func_name, label_counter, var_offsets, next_offset
            )

            expected_asm = "MOV R0, #5\nBL foo\nSTR R0, [FP, #20]"
            self.assertEqual(asm_code, expected_asm)
            self.assertEqual(updated_offset, 0)

    def test_handle_assign_with_offset_increment(self):
        """Test ASSIGN where expression evaluation increases next_offset."""
        stmt = {
            "type": "ASSIGN",
            "var_name": "temp",
            "expression": {
                "type": "BINARY_OP",
                "op": "MUL",
                "left": {"type": "LITERAL", "value": 2},
                "right": {"type": "LITERAL", "value": 3}
            }
        }
        func_name = "main"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {"temp": 24}
        next_offset = 0

        with patch("handle_assign_package.handle_assign_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("MOV R0, #2\nMOV R1, #3\nMUL R0, R0, R1", 8)

            asm_code, updated_offset = handle_assign(
                stmt, func_name, label_counter, var_offsets, next_offset
            )

            expected_asm = "MOV R0, #2\nMOV R1, #3\nMUL R0, R0, R1\nSTR R0, [FP, #24]"
            self.assertEqual(asm_code, expected_asm)
            self.assertEqual(updated_offset, 8)

    def test_handle_assign_zero_offset(self):
        """Test ASSIGN with variable at offset 0."""
        stmt = {
            "type": "ASSIGN",
            "var_name": "a",
            "expression": {
                "type": "LITERAL",
                "value": 0
            }
        }
        func_name = "main"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {"a": 0}
        next_offset = 0

        with patch("handle_assign_package.handle_assign_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("MOV R0, #0", 0)

            asm_code, updated_offset = handle_assign(
                stmt, func_name, label_counter, var_offsets, next_offset
            )

            expected_asm = "MOV R0, #0\nSTR R0, [FP, #0]"
            self.assertEqual(asm_code, expected_asm)
            self.assertEqual(updated_offset, 0)

    def test_handle_assign_negative_offset(self):
        """Test ASSIGN with negative offset (if supported by var_offsets)."""
        stmt = {
            "type": "ASSIGN",
            "var_name": "param",
            "expression": {
                "type": "LITERAL",
                "value": 100
            }
        }
        func_name = "main"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {"param": -8}
        next_offset = 0

        with patch("handle_assign_package.handle_assign_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("MOV R0, #100", 0)

            asm_code, updated_offset = handle_assign(
                stmt, func_name, label_counter, var_offsets, next_offset
            )

            expected_asm = "MOV R0, #100\nSTR R0, [FP, #-8]"
            self.assertEqual(asm_code, expected_asm)
            self.assertEqual(updated_offset, 0)

    def test_handle_assign_missing_var_in_offsets(self):
        """Test ASSIGN raises KeyError when var_name not in var_offsets."""
        stmt = {
            "type": "ASSIGN",
            "var_name": "undefined_var",
            "expression": {
                "type": "LITERAL",
                "value": 1
            }
        }
        func_name = "main"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {"x": 8}
        next_offset = 0

        with self.assertRaises(KeyError):
            handle_assign(stmt, func_name, label_counter, var_offsets, next_offset)

    def test_handle_assign_empty_expression_code(self):
        """Test ASSIGN with empty expression code from generate_expression_code."""
        stmt = {
            "type": "ASSIGN",
            "var_name": "x",
            "expression": {
                "type": "LITERAL",
                "value": 5
            }
        }
        func_name = "main"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {"x": 8}
        next_offset = 0

        with patch("handle_assign_package.handle_assign_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("", 0)

            asm_code, updated_offset = handle_assign(
                stmt, func_name, label_counter, var_offsets, next_offset
            )

            expected_asm = "\nSTR R0, [FP, #8]"
            self.assertEqual(asm_code, expected_asm)
            self.assertEqual(updated_offset, 0)

    def test_handle_assign_multiline_expression_code(self):
        """Test ASSIGN with multi-line expression code."""
        stmt = {
            "type": "ASSIGN",
            "var_name": "result",
            "expression": {
                "type": "BINARY_OP",
                "op": "ADD",
                "left": {
                    "type": "BINARY_OP",
                    "op": "MUL",
                    "left": {"type": "LITERAL", "value": 2},
                    "right": {"type": "LITERAL", "value": 3}
                },
                "right": {"type": "LITERAL", "value": 1}
            }
        }
        func_name = "main"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {"result": 12}
        next_offset = 0

        with patch("handle_assign_package.handle_assign_src.generate_expression_code") as mock_gen_expr:
            expr_code = "MOV R0, #2\nMOV R1, #3\nMUL R0, R0, R1\nMOV R1, #1\nADD R0, R0, R1"
            mock_gen_expr.return_value = (expr_code, 0)

            asm_code, updated_offset = handle_assign(
                stmt, func_name, label_counter, var_offsets, next_offset
            )

            expected_asm = expr_code + "\nSTR R0, [FP, #12]"
            self.assertEqual(asm_code, expected_asm)
            self.assertEqual(updated_offset, 0)

    def test_handle_assign_preserves_label_counter(self):
        """Test that handle_assign does not modify label_counter."""
        stmt = {
            "type": "ASSIGN",
            "var_name": "x",
            "expression": {
                "type": "LITERAL",
                "value": 1
            }
        }
        func_name = "main"
        label_counter = {"if_else": 5, "if_end": 10}
        var_offsets = {"x": 8}
        next_offset = 0

        original_label_counter = label_counter.copy()

        with patch("handle_assign_package.handle_assign_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("MOV R0, #1", 0)

            handle_assign(stmt, func_name, label_counter, var_offsets, next_offset)

            self.assertEqual(label_counter, original_label_counter)

    def test_handle_assign_preserves_var_offsets(self):
        """Test that handle_assign does not modify var_offsets."""
        stmt = {
            "type": "ASSIGN",
            "var_name": "x",
            "expression": {
                "type": "LITERAL",
                "value": 1
            }
        }
        func_name = "main"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {"x": 8}
        next_offset = 0

        original_var_offsets = var_offsets.copy()

        with patch("handle_assign_package.handle_assign_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("MOV R0, #1", 0)

            handle_assign(stmt, func_name, label_counter, var_offsets, next_offset)

            self.assertEqual(var_offsets, original_var_offsets)

    def test_handle_assign_returns_correct_offset_from_expression(self):
        """Test that handle_assign returns the offset from generate_expression_code."""
        stmt = {
            "type": "ASSIGN",
            "var_name": "x",
            "expression": {
                "type": "LITERAL",
                "value": 1
            }
        }
        func_name = "main"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {"x": 8}
        next_offset = 16

        with patch("handle_assign_package.handle_assign_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("MOV R0, #1", 32)

            _, updated_offset = handle_assign(stmt, func_name, label_counter, var_offsets, next_offset)

            self.assertEqual(updated_offset, 32)


if __name__ == "__main__":
    unittest.main()
