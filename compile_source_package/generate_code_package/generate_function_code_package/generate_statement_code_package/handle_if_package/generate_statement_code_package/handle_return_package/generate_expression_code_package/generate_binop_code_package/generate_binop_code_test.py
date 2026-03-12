# -*- coding: utf-8 -*-
"""Unit tests for generate_binop_code function."""

import unittest
from unittest.mock import patch

from .generate_binop_code_src import generate_binop_code


class TestGenerateBinopCode(unittest.TestCase):
    """Test cases for generate_binop_code function."""

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_return_package.generate_expression_code_package.generate_binop_code_package.generate_expression_code_src.generate_expression_code')
    def test_add_operation(self, mock_gen_expr):
        """Test ADD operation generates correct assembly code."""
        mock_gen_expr.side_effect = [
            ("    mov x1, #5\n", 16, "x1"),
            ("    mov x2, #3\n", 16, "x2"),
        ]
        
        expr = {
            "type": "BINOP",
            "op": "ADD",
            "left": {"type": "NUM", "value": 5},
            "right": {"type": "NUM", "value": 3},
        }
        var_offsets = {"x": 0}
        next_offset = 16
        
        code, updated_offset, result_reg = generate_binop_code(expr, var_offsets, next_offset)
        
        self.assertIn("add x0, x1, x2", code)
        self.assertEqual(updated_offset, 16)
        self.assertEqual(result_reg, "x0")
        self.assertEqual(mock_gen_expr.call_count, 2)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_return_package.generate_expression_code_package.generate_binop_code_package.generate_expression_code_src.generate_expression_code')
    def test_sub_operation(self, mock_gen_expr):
        """Test SUB operation generates correct assembly code."""
        mock_gen_expr.side_effect = [
            ("    mov x1, #10\n", 16, "x1"),
            ("    mov x2, #4\n", 16, "x2"),
        ]
        
        expr = {
            "type": "BINOP",
            "op": "SUB",
            "left": {"type": "NUM", "value": 10},
            "right": {"type": "NUM", "value": 4},
        }
        
        code, updated_offset, result_reg = generate_binop_code(expr, {}, 16)
        
        self.assertIn("sub x0, x1, x2", code)
        self.assertEqual(result_reg, "x0")

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_return_package.generate_expression_code_package.generate_binop_code_package.generate_expression_code_src.generate_expression_code')
    def test_mul_operation(self, mock_gen_expr):
        """Test MUL operation generates correct assembly code."""
        mock_gen_expr.side_effect = [
            ("    mov x1, #6\n", 16, "x1"),
            ("    mov x2, #7\n", 16, "x2"),
        ]
        
        expr = {
            "type": "BINOP",
            "op": "MUL",
            "left": {"type": "NUM", "value": 6},
            "right": {"type": "NUM", "value": 7},
        }
        
        code, updated_offset, result_reg = generate_binop_code(expr, {}, 16)
        
        self.assertIn("mul x0, x1, x2", code)
        self.assertEqual(result_reg, "x0")

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_return_package.generate_expression_code_package.generate_binop_code_package.generate_expression_code_src.generate_expression_code')
    def test_div_operation(self, mock_gen_expr):
        """Test DIV operation generates correct assembly code (sdiv)."""
        mock_gen_expr.side_effect = [
            ("    mov x1, #20\n", 16, "x1"),
            ("    mov x2, #4\n", 16, "x2"),
        ]
        
        expr = {
            "type": "BINOP",
            "op": "DIV",
            "left": {"type": "NUM", "value": 20},
            "right": {"type": "NUM", "value": 4},
        }
        
        code, updated_offset, result_reg = generate_binop_code(expr, {}, 16)
        
        self.assertIn("sdiv x0, x1, x2", code)
        self.assertEqual(result_reg, "x0")

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_return_package.generate_expression_code_package.generate_binop_code_package.generate_expression_code_src.generate_expression_code')
    def test_unsupported_operator(self, mock_gen_expr):
        """Test that unsupported operator raises ValueError."""
        expr = {
            "type": "BINOP",
            "op": "MOD",
            "left": {"type": "NUM", "value": 10},
            "right": {"type": "NUM", "value": 3},
        }
        
        with self.assertRaises(ValueError) as context:
            generate_binop_code(expr, {}, 16)
        
        self.assertIn("Unsupported binary operator: MOD", str(context.exception))
        mock_gen_expr.assert_not_called()

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_return_package.generate_expression_code_package.generate_binop_code_package.generate_expression_code_src.generate_expression_code')
    def test_nested_binop_expression(self, mock_gen_expr):
        """Test nested binary operation expressions."""
        mock_gen_expr.side_effect = [
            ("    mov x1, #2\n    add x1, x1, #3\n", 16, "x1"),
            ("    mov x2, #4\n", 16, "x2"),
        ]
        
        expr = {
            "type": "BINOP",
            "op": "MUL",
            "left": {
                "type": "BINOP",
                "op": "ADD",
                "left": {"type": "NUM", "value": 2},
                "right": {"type": "NUM", "value": 3},
            },
            "right": {"type": "NUM", "value": 4},
        }
        
        code, updated_offset, result_reg = generate_binop_code(expr, {}, 16)
        
        self.assertIn("mul x0, x1, x2", code)
        self.assertEqual(mock_gen_expr.call_count, 2)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_return_package.generate_expression_code_package.generate_binop_code_package.generate_expression_code_src.generate_expression_code')
    def test_next_offset_propagation(self, mock_gen_expr):
        """Test that next_offset is properly propagated through calls."""
        mock_gen_expr.side_effect = [
            ("    mov x1, #5\n", 32, "x1"),
            ("    mov x2, #3\n", 48, "x2"),
        ]
        
        expr = {
            "type": "BINOP",
            "op": "ADD",
            "left": {"type": "NUM", "value": 5},
            "right": {"type": "NUM", "value": 3},
        }
        
        code, updated_offset, result_reg = generate_binop_code(expr, {}, 16)
        
        self.assertEqual(updated_offset, 48)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_return_package.generate_expression_code_package.generate_binop_code_package.generate_expression_code_src.generate_expression_code')
    def test_code_concatenation_order(self, mock_gen_expr):
        """Test that code is concatenated in correct order: left, right, operation."""
        mock_gen_expr.side_effect = [
            ("    LEFT_CODE\n", 16, "x1"),
            ("    RIGHT_CODE\n", 16, "x2"),
        ]
        
        expr = {
            "type": "BINOP",
            "op": "ADD",
            "left": {"type": "NUM", "value": 1},
            "right": {"type": "NUM", "value": 2},
        }
        
        code, updated_offset, result_reg = generate_binop_code(expr, {}, 16)
        
        left_pos = code.find("LEFT_CODE")
        right_pos = code.find("RIGHT_CODE")
        op_pos = code.find("add x0")
        
        self.assertLess(left_pos, right_pos)
        self.assertLess(right_pos, op_pos)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_return_package.generate_expression_code_package.generate_binop_code_package.generate_expression_code_src.generate_expression_code')
    def test_var_operand_left(self, mock_gen_expr):
        """Test binary operation with variable as left operand."""
        mock_gen_expr.side_effect = [
            ("    ldr x1, [sp, #0]\n", 16, "x1"),
            ("    mov x2, #5\n", 16, "x2"),
        ]
        
        expr = {
            "type": "BINOP",
            "op": "ADD",
            "left": {"type": "VAR", "name": "x"},
            "right": {"type": "NUM", "value": 5},
        }
        var_offsets = {"x": 0}
        
        code, updated_offset, result_reg = generate_binop_code(expr, var_offsets, 16)
        
        self.assertIn("add x0, x1, x2", code)
        self.assertEqual(result_reg, "x0")

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_return_package.generate_expression_code_package.generate_binop_code_package.generate_expression_code_src.generate_expression_code')
    def test_empty_var_offsets(self, mock_gen_expr):
        """Test binary operation with empty var_offsets dict."""
        mock_gen_expr.side_effect = [
            ("    mov x1, #10\n", 16, "x1"),
            ("    mov x2, #20\n", 16, "x2"),
        ]
        
        expr = {
            "type": "BINOP",
            "op": "ADD",
            "left": {"type": "NUM", "value": 10},
            "right": {"type": "NUM", "value": 20},
        }
        
        code, updated_offset, result_reg = generate_binop_code(expr, {}, 16)
        
        self.assertIn("add x0, x1, x2", code)
        self.assertEqual(updated_offset, 16)


if __name__ == "__main__":
    unittest.main()
