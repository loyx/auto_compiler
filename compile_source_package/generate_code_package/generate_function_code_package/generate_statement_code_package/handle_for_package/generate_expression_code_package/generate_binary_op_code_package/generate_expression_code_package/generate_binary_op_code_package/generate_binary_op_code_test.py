# -*- coding: utf-8 -*-
"""Unit tests for generate_binary_op_code function."""

import unittest
from unittest.mock import patch


class TestGenerateBinaryOpCode(unittest.TestCase):
    """Test cases for generate_binary_op_code function."""

    def test_and_operator_delegates_to_short_circuit_and(self):
        """Test AND operator delegates to generate_short_circuit_and."""
        from .generate_binary_op_code_src import generate_binary_op_code
        
        expr = {
            "operator": "AND",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 2}
        }
        func_name = "test_func"
        label_counter = {"skip": 0}
        var_offsets = {}
        next_offset = 10
        
        expected_code = "and_short_circuit_code"
        expected_offset = 15
        
        with patch("generate_binary_op_code_package.generate_short_circuit_and_package.generate_short_circuit_and_src.generate_short_circuit_and") as mock_and:
            mock_and.return_value = (expected_code, expected_offset)
            
            result_code, result_offset = generate_binary_op_code(
                expr, func_name, label_counter, var_offsets, next_offset
            )
            
            mock_and.assert_called_once_with(expr, func_name, label_counter, var_offsets, next_offset)
            self.assertEqual(result_code, expected_code)
            self.assertEqual(result_offset, expected_offset)

    def test_or_operator_delegates_to_short_circuit_or(self):
        """Test OR operator delegates to generate_short_circuit_or."""
        from .generate_binary_op_code_src import generate_binary_op_code
        
        expr = {
            "operator": "OR",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 2}
        }
        func_name = "test_func"
        label_counter = {"skip": 0}
        var_offsets = {}
        next_offset = 10
        
        expected_code = "or_short_circuit_code"
        expected_offset = 15
        
        with patch("generate_binary_op_code_package.generate_short_circuit_or_package.generate_short_circuit_or_src.generate_short_circuit_or") as mock_or:
            mock_or.return_value = (expected_code, expected_offset)
            
            result_code, result_offset = generate_binary_op_code(
                expr, func_name, label_counter, var_offsets, next_offset
            )
            
            mock_or.assert_called_once_with(expr, func_name, label_counter, var_offsets, next_offset)
            self.assertEqual(result_code, expected_code)
            self.assertEqual(result_offset, expected_offset)

    def test_add_operator_generates_correct_code(self):
        """Test ADD operator generates correct assembly code."""
        from .generate_binary_op_code_src import generate_binary_op_code
        
        expr = {
            "operator": "ADD",
            "left": {"type": "literal", "value": 5},
            "right": {"type": "literal", "value": 3}
        }
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 10
        
        left_code = "    ldr x0, [sp, #0]"
        right_code = "    ldr x0, [sp, #8]"
        op_instruction = "    add x0, x1, x0"
        
        with patch("generate_binary_op_code_package.generate_expr_code.generate_expr_code_src.generate_expr_code") as mock_expr:
            mock_expr.side_effect = [
                (left_code, 12),
                (right_code, 14)
            ]
            with patch("generate_binary_op_code_package.generate_arithmetic_comparison_code_package.generate_arithmetic_comparison_code_src.generate_arithmetic_comparison_code") as mock_arith:
                mock_arith.return_value = op_instruction
                
                result_code, result_offset = generate_binary_op_code(
                    expr, func_name, label_counter, var_offsets, next_offset
                )
                
                self.assertEqual(mock_expr.call_count, 2)
                mock_arith.assert_called_once_with("ADD", left_code, right_code)
                
                expected_full_code = "\n".join([
                    left_code,
                    "    mov x1, x0",
                    right_code,
                    op_instruction
                ])
                self.assertEqual(result_code, expected_full_code)
                self.assertEqual(result_offset, 14)

    def test_sub_operator_generates_correct_code(self):
        """Test SUB operator generates correct assembly code."""
        from .generate_binary_op_code_src import generate_binary_op_code
        
        expr = {
            "operator": "SUB",
            "left": {"type": "variable", "name": "a"},
            "right": {"type": "literal", "value": 1}
        }
        func_name = "test_func"
        label_counter = {}
        var_offsets = {"a": 0}
        next_offset = 5
        
        left_code = "    ldr x0, [sp, #0]"
        right_code = "    mov x0, #1"
        op_instruction = "    sub x0, x1, x0"
        
        with patch("generate_binary_op_code_package.generate_expr_code.generate_expr_code_src.generate_expr_code") as mock_expr:
            mock_expr.side_effect = [
                (left_code, 6),
                (right_code, 7)
            ]
            with patch("generate_binary_op_code_package.generate_arithmetic_comparison_code_package.generate_arithmetic_comparison_code_src.generate_arithmetic_comparison_code") as mock_arith:
                mock_arith.return_value = op_instruction
                
                result_code, result_offset = generate_binary_op_code(
                    expr, func_name, label_counter, var_offsets, next_offset
                )
                
                expected_full_code = "\n".join([
                    left_code,
                    "    mov x1, x0",
                    right_code,
                    op_instruction
                ])
                self.assertEqual(result_code, expected_full_code)

    def test_comparison_eq_operator(self):
        """Test EQ comparison operator."""
        from .generate_binary_op_code_src import generate_binary_op_code
        
        expr = {
            "operator": "EQ",
            "left": {"type": "variable", "name": "x"},
            "right": {"type": "literal", "value": 0}
        }
        func_name = "test_func"
        label_counter = {}
        var_offsets = {"x": 0}
        next_offset = 8
        
        left_code = "    ldr x0, [sp, #0]"
        right_code = "    mov x0, #0"
        op_instruction = "    cmp x1, x0\n    cset x0, eq"
        
        with patch("generate_binary_op_code_package.generate_expr_code.generate_expr_code_src.generate_expr_code") as mock_expr:
            mock_expr.side_effect = [
                (left_code, 9),
                (right_code, 10)
            ]
            with patch("generate_binary_op_code_package.generate_arithmetic_comparison_code_package.generate_arithmetic_comparison_code_src.generate_arithmetic_comparison_code") as mock_arith:
                mock_arith.return_value = op_instruction
                
                result_code, result_offset = generate_binary_op_code(
                    expr, func_name, label_counter, var_offsets, next_offset
                )
                
                mock_arith.assert_called_once_with("EQ", left_code, right_code)
                self.assertEqual(result_offset, 10)

    def test_comparison_lt_operator(self):
        """Test LT comparison operator."""
        from .generate_binary_op_code_src import generate_binary_op_code
        
        expr = {
            "operator": "LT",
            "left": {"type": "literal", "value": 10},
            "right": {"type": "literal", "value": 20}
        }
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 5
        
        left_code = "    mov x0, #10"
        right_code = "    mov x0, #20"
        op_instruction = "    cmp x1, x0\n    cset x0, lt"
        
        with patch("generate_binary_op_code_package.generate_expr_code.generate_expr_code_src.generate_expr_code") as mock_expr:
            mock_expr.side_effect = [
                (left_code, 6),
                (right_code, 7)
            ]
            with patch("generate_binary_op_code_package.generate_arithmetic_comparison_code_package.generate_arithmetic_comparison_code_src.generate_arithmetic_comparison_code") as mock_arith:
                mock_arith.return_value = op_instruction
                
                result_code, result_offset = generate_binary_op_code(
                    expr, func_name, label_counter, var_offsets, next_offset
                )
                
                mock_arith.assert_called_once_with("LT", left_code, right_code)

    def test_mul_operator(self):
        """Test MUL operator."""
        from .generate_binary_op_code_src import generate_binary_op_code
        
        expr = {
            "operator": "MUL",
            "left": {"type": "variable", "name": "a"},
            "right": {"type": "variable", "name": "b"}
        }
        func_name = "test_func"
        label_counter = {}
        var_offsets = {"a": 0, "b": 8}
        next_offset = 16
        
        left_code = "    ldr x0, [sp, #0]"
        right_code = "    ldr x0, [sp, #8]"
        op_instruction = "    mul x0, x1, x0"
        
        with patch("generate_binary_op_code_package.generate_expr_code.generate_expr_code_src.generate_expr_code") as mock_expr:
            mock_expr.side_effect = [
                (left_code, 17),
                (right_code, 18)
            ]
            with patch("generate_binary_op_code_package.generate_arithmetic_comparison_code_package.generate_arithmetic_comparison_code_src.generate_arithmetic_comparison_code") as mock_arith:
                mock_arith.return_value = op_instruction
                
                result_code, result_offset = generate_binary_op_code(
                    expr, func_name, label_counter, var_offsets, next_offset
                )
                
                mock_arith.assert_called_once_with("MUL", left_code, right_code)
                self.assertEqual(result_offset, 18)

    def test_div_operator(self):
        """Test DIV operator."""
        from .generate_binary_op_code_src import generate_binary_op_code
        
        expr = {
            "operator": "DIV",
            "left": {"type": "literal", "value": 100},
            "right": {"type": "literal", "value": 5}
        }
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 3
        
        left_code = "    mov x0, #100"
        right_code = "    mov x0, #5"
        op_instruction = "    sdiv x0, x1, x0"
        
        with patch("generate_binary_op_code_package.generate_expr_code.generate_expr_code_src.generate_expr_code") as mock_expr:
            mock_expr.side_effect = [
                (left_code, 4),
                (right_code, 5)
            ]
            with patch("generate_binary_op_code_package.generate_arithmetic_comparison_code_package.generate_arithmetic_comparison_code_src.generate_arithmetic_comparison_code") as mock_arith:
                mock_arith.return_value = op_instruction
                
                result_code, result_offset = generate_binary_op_code(
                    expr, func_name, label_counter, var_offsets, next_offset
                )
                
                mock_arith.assert_called_once_with("DIV", left_code, right_code)

    def test_ne_comparison_operator(self):
        """Test NE (not equal) comparison operator."""
        from .generate_binary_op_code_src import generate_binary_op_code
        
        expr = {
            "operator": "NE",
            "left": {"type": "variable", "name": "flag"},
            "right": {"type": "literal", "value": 0}
        }
        func_name = "test_func"
        label_counter = {}
        var_offsets = {"flag": 0}
        next_offset = 8
        
        left_code = "    ldr x0, [sp, #0]"
        right_code = "    mov x0, #0"
        op_instruction = "    cmp x1, x0\n    cset x0, ne"
        
        with patch("generate_binary_op_code_package.generate_expr_code.generate_expr_code_src.generate_expr_code") as mock_expr:
            mock_expr.side_effect = [
                (left_code, 9),
                (right_code, 10)
            ]
            with patch("generate_binary_op_code_package.generate_arithmetic_comparison_code_package.generate_arithmetic_comparison_code_src.generate_arithmetic_comparison_code") as mock_arith:
                mock_arith.return_value = op_instruction
                
                result_code, result_offset = generate_binary_op_code(
                    expr, func_name, label_counter, var_offsets, next_offset
                )
                
                mock_arith.assert_called_once_with("NE", left_code, right_code)

    def test_gt_comparison_operator(self):
        """Test GT (greater than) comparison operator."""
        from .generate_binary_op_code_src import generate_binary_op_code
        
        expr = {
            "operator": "GT",
            "left": {"type": "literal", "value": 50},
            "right": {"type": "literal", "value": 30}
        }
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 5
        
        left_code = "    mov x0, #50"
        right_code = "    mov x0, #30"
        op_instruction = "    cmp x1, x0\n    cset x0, gt"
        
        with patch("generate_binary_op_code_package.generate_expr_code.generate_expr_code_src.generate_expr_code") as mock_expr:
            mock_expr.side_effect = [
                (left_code, 6),
                (right_code, 7)
            ]
            with patch("generate_binary_op_code_package.generate_arithmetic_comparison_code_package.generate_arithmetic_comparison_code_src.generate_arithmetic_comparison_code") as mock_arith:
                mock_arith.return_value = op_instruction
                
                result_code, result_offset = generate_binary_op_code(
                    expr, func_name, label_counter, var_offsets, next_offset
                )
                
                mock_arith.assert_called_once_with("GT", left_code, right_code)

    def test_le_comparison_operator(self):
        """Test LE (less than or equal) comparison operator."""
        from .generate_binary_op_code_src import generate_binary_op_code
        
        expr = {
            "operator": "LE",
            "left": {"type": "variable", "name": "count"},
            "right": {"type": "literal", "value": 100}
        }
        func_name = "test_func"
        label_counter = {}
        var_offsets = {"count": 0}
        next_offset = 8
        
        left_code = "    ldr x0, [sp, #0]"
        right_code = "    mov x0, #100"
        op_instruction = "    cmp x1, x0\n    cset x0, le"
        
        with patch("generate_binary_op_code_package.generate_expr_code.generate_expr_code_src.generate_expr_code") as mock_expr:
            mock_expr.side_effect = [
                (left_code, 9),
                (right_code, 10)
            ]
            with patch("generate_binary_op_code_package.generate_arithmetic_comparison_code_package.generate_arithmetic_comparison_code_src.generate_arithmetic_comparison_code") as mock_arith:
                mock_arith.return_value = op_instruction
                
                result_code, result_offset = generate_binary_op_code(
                    expr, func_name, label_counter, var_offsets, next_offset
                )
                
                mock_arith.assert_called_once_with("LE", left_code, right_code)

    def test_ge_comparison_operator(self):
        """Test GE (greater than or equal) comparison operator."""
        from .generate_binary_op_code_src import generate_binary_op_code
        
        expr = {
            "operator": "GE",
            "left": {"type": "literal", "value": 0},
            "right": {"type": "variable", "name": "threshold"}
        }
        func_name = "test_func"
        label_counter = {}
        var_offsets = {"threshold": 0}
        next_offset = 8
        
        left_code = "    mov x0, #0"
        right_code = "    ldr x0, [sp, #0]"
        op_instruction = "    cmp x1, x0\n    cset x0, ge"
        
        with patch("generate_binary_op_code_package.generate_expr_code.generate_expr_code_src.generate_expr_code") as mock_expr:
            mock_expr.side_effect = [
                (left_code, 9),
                (right_code, 10)
            ]
            with patch("generate_binary_op_code_package.generate_arithmetic_comparison_code_package.generate_arithmetic_comparison_code_src.generate_arithmetic_comparison_code") as mock_arith:
                mock_arith.return_value = op_instruction
                
                result_code, result_offset = generate_binary_op_code(
                    expr, func_name, label_counter, var_offsets, next_offset
                )
                
                mock_arith.assert_called_once_with("GE", left_code, right_code)

    def test_empty_operator_defaults_to_empty_string(self):
        """Test that missing operator defaults to empty string and follows non-short-circuit path."""
        from .generate_binary_op_code_src import generate_binary_op_code
        
        expr = {
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 2}
        }
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 5
        
        left_code = "    mov x0, #1"
        right_code = "    mov x0, #2"
        op_instruction = "    add x0, x1, x0"
        
        with patch("generate_binary_op_code_package.generate_expr_code.generate_expr_code_src.generate_expr_code") as mock_expr:
            mock_expr.side_effect = [
                (left_code, 6),
                (right_code, 7)
            ]
            with patch("generate_binary_op_code_package.generate_arithmetic_comparison_code_package.generate_arithmetic_comparison_code_src.generate_arithmetic_comparison_code") as mock_arith:
                mock_arith.return_value = op_instruction
                
                result_code, result_offset = generate_binary_op_code(
                    expr, func_name, label_counter, var_offsets, next_offset
                )
                
                mock_arith.assert_called_once_with("", left_code, right_code)

    def test_nested_binary_expression(self):
        """Test nested binary expression (a + b) * c."""
        from .generate_binary_op_code_src import generate_binary_op_code
        
        expr = {
            "operator": "MUL",
            "left": {
                "operator": "ADD",
                "left": {"type": "variable", "name": "a"},
                "right": {"type": "variable", "name": "b"}
            },
            "right": {"type": "variable", "name": "c"}
        }
        func_name = "test_func"
        label_counter = {}
        var_offsets = {"a": 0, "b": 8, "c": 16}
        next_offset = 24
        
        left_inner_code = "    ldr x0, [sp, #0]"
        right_inner_code = "    ldr x0, [sp, #8]"
        inner_op = "    add x0, x1, x0"
        left_code = "\n".join([left_inner_code, "    mov x1, x0", right_inner_code, inner_op])
        right_code = "    ldr x0, [sp, #16]"
        outer_op = "    mul x0, x1, x0"
        
        with patch("generate_binary_op_code_package.generate_expr_code.generate_expr_code_src.generate_expr_code") as mock_expr:
            mock_expr.side_effect = [
                (left_code, 25),
                (right_code, 26)
            ]
            with patch("generate_binary_op_code_package.generate_arithmetic_comparison_code_package.generate_arithmetic_comparison_code_src.generate_arithmetic_comparison_code") as mock_arith:
                mock_arith.return_value = outer_op
                
                result_code, result_offset = generate_binary_op_code(
                    expr, func_name, label_counter, var_offsets, next_offset
                )
                
                self.assertEqual(result_offset, 26)
                self.assertIn("mul x0, x1, x0", result_code)

    def test_label_counter_not_modified_for_arithmetic_ops(self):
        """Test that label_counter is not modified for arithmetic operations."""
        from .generate_binary_op_code_src import generate_binary_op_code
        
        expr = {
            "operator": "ADD",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 2}
        }
        func_name = "test_func"
        label_counter = {"skip": 5, "true": 3}
        var_offsets = {}
        next_offset = 10
        
        original_counter = label_counter.copy()
        
        with patch("generate_binary_op_code_package.generate_expr_code.generate_expr_code_src.generate_expr_code") as mock_expr:
            mock_expr.side_effect = [
                ("    mov x0, #1", 11),
                ("    mov x0, #2", 12)
            ]
            with patch("generate_binary_op_code_package.generate_arithmetic_comparison_code_package.generate_arithmetic_comparison_code_src.generate_arithmetic_comparison_code") as mock_arith:
                mock_arith.return_value = "    add x0, x1, x0"
                
                generate_binary_op_code(
                    expr, func_name, label_counter, var_offsets, next_offset
                )
                
                self.assertEqual(label_counter, original_counter)

    def test_returns_tuple_with_code_and_offset(self):
        """Test that function returns a tuple of (code, offset)."""
        from .generate_binary_op_code_src import generate_binary_op_code
        
        expr = {
            "operator": "ADD",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 2}
        }
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 5
        
        with patch("generate_binary_op_code_package.generate_expr_code.generate_expr_code_src.generate_expr_code") as mock_expr:
            mock_expr.side_effect = [
                ("    mov x0, #1", 6),
                ("    mov x0, #2", 7)
            ]
            with patch("generate_binary_op_code_package.generate_arithmetic_comparison_code_package.generate_arithmetic_comparison_code_src.generate_arithmetic_comparison_code") as mock_arith:
                mock_arith.return_value = "    add x0, x1, x0"
                
                result = generate_binary_op_code(
                    expr, func_name, label_counter, var_offsets, next_offset
                )
                
                self.assertIsInstance(result, tuple)
                self.assertEqual(len(result), 2)
                self.assertIsInstance(result[0], str)
                self.assertIsInstance(result[1], int)


if __name__ == "__main__":
    unittest.main()
