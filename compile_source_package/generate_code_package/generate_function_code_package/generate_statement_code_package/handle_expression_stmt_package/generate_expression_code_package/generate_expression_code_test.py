# -*- coding: utf-8 -*-
"""Unit tests for generate_expression_code function."""

import unittest

from .generate_expression_code_src import generate_expression_code


class TestGenerateExpressionCodeConst(unittest.TestCase):
    """Test cases for CONST expression type."""

    def test_const_small_positive(self):
        """Test small positive constant (<= 4095)."""
        expr = {"type": "CONST", "value": 100}
        result = generate_expression_code(expr, "test_func", {})
        self.assertEqual(result, "mov x0, #100")

    def test_const_zero(self):
        """Test zero constant."""
        expr = {"type": "CONST", "value": 0}
        result = generate_expression_code(expr, "test_func", {})
        self.assertEqual(result, "mov x0, #0")

    def test_const_small_negative(self):
        """Test small negative constant (>= -4095)."""
        expr = {"type": "CONST", "value": -500}
        result = generate_expression_code(expr, "test_func", {})
        self.assertEqual(result, "mov x0, #-500")

    def test_const_boundary_4095(self):
        """Test constant at boundary 4095."""
        expr = {"type": "CONST", "value": 4095}
        result = generate_expression_code(expr, "test_func", {})
        self.assertEqual(result, "mov x0, #4095")

    def test_const_boundary_neg_4095(self):
        """Test constant at boundary -4095."""
        expr = {"type": "CONST", "value": -4095}
        result = generate_expression_code(expr, "test_func", {})
        self.assertEqual(result, "mov x0, #-4095")

    def test_const_large_positive(self):
        """Test large positive constant (> 4095)."""
        expr = {"type": "CONST", "value": 5000}
        result = generate_expression_code(expr, "test_func", {})
        self.assertEqual(result, "ldr x0, =5000")

    def test_const_large_negative(self):
        """Test large negative constant (< -4095)."""
        expr = {"type": "CONST", "value": -10000}
        result = generate_expression_code(expr, "test_func", {})
        self.assertEqual(result, "ldr x0, =-10000")

    def test_const_just_over_boundary(self):
        """Test constant just over boundary (4096)."""
        expr = {"type": "CONST", "value": 4096}
        result = generate_expression_code(expr, "test_func", {})
        self.assertEqual(result, "ldr x0, =4096")


class TestGenerateExpressionCodeVar(unittest.TestCase):
    """Test cases for VAR expression type."""

    def test_var_exists(self):
        """Test variable that exists in var_offsets."""
        expr = {"type": "VAR", "var_name": "x"}
        var_offsets = {"x": 16}
        result = generate_expression_code(expr, "test_func", var_offsets)
        self.assertEqual(result, "ldr x0, [sp, #16]")

    def test_var_zero_offset(self):
        """Test variable with zero offset."""
        expr = {"type": "VAR", "var_name": "y"}
        var_offsets = {"y": 0}
        result = generate_expression_code(expr, "test_func", var_offsets)
        self.assertEqual(result, "ldr x0, [sp, #0]")

    def test_var_large_offset(self):
        """Test variable with large offset."""
        expr = {"type": "VAR", "var_name": "z"}
        var_offsets = {"z": 128}
        result = generate_expression_code(expr, "test_func", var_offsets)
        self.assertEqual(result, "ldr x0, [sp, #128]")

    def test_var_not_found(self):
        """Test variable not in var_offsets raises KeyError."""
        expr = {"type": "VAR", "var_name": "missing"}
        var_offsets = {"x": 16}
        with self.assertRaises(KeyError) as context:
            generate_expression_code(expr, "test_func", var_offsets)
        self.assertIn("missing", str(context.exception))


class TestGenerateExpressionCodeBinop(unittest.TestCase):
    """Test cases for BINOP expression type."""

    def test_binop_add_constants(self):
        """Test ADD operation with two constants."""
        expr = {
            "type": "BINOP",
            "op": "ADD",
            "left": {"type": "CONST", "value": 5},
            "right": {"type": "CONST", "value": 3},
        }
        result = generate_expression_code(expr, "test_func", {})
        expected = "mov x0, #5\nmov x1, x0\nmov x0, #3\nadd x0, x1, x0"
        self.assertEqual(result, expected)

    def test_binop_sub_constants(self):
        """Test SUB operation with two constants."""
        expr = {
            "type": "BINOP",
            "op": "SUB",
            "left": {"type": "CONST", "value": 10},
            "right": {"type": "CONST", "value": 4},
        }
        result = generate_expression_code(expr, "test_func", {})
        expected = "mov x0, #10\nmov x1, x0\nmov x0, #4\nsub x0, x1, x0"
        self.assertEqual(result, expected)

    def test_binop_mul_constants(self):
        """Test MUL operation with two constants."""
        expr = {
            "type": "BINOP",
            "op": "MUL",
            "left": {"type": "CONST", "value": 6},
            "right": {"type": "CONST", "value": 7},
        }
        result = generate_expression_code(expr, "test_func", {})
        expected = "mov x0, #6\nmov x1, x0\nmov x0, #7\nmul x0, x1, x0"
        self.assertEqual(result, expected)

    def test_binop_div_constants(self):
        """Test DIV operation with two constants."""
        expr = {
            "type": "BINOP",
            "op": "DIV",
            "left": {"type": "CONST", "value": 20},
            "right": {"type": "CONST", "value": 4},
        }
        result = generate_expression_code(expr, "test_func", {})
        expected = "mov x0, #20\nmov x1, x0\nmov x0, #4\nsdiv x0, x1, x0"
        self.assertEqual(result, expected)

    def test_binop_and_constants(self):
        """Test AND operation with two constants."""
        expr = {
            "type": "BINOP",
            "op": "AND",
            "left": {"type": "CONST", "value": 15},
            "right": {"type": "CONST", "value": 7},
        }
        result = generate_expression_code(expr, "test_func", {})
        expected = "mov x0, #15\nmov x1, x0\nmov x0, #7\nand x0, x1, x0"
        self.assertEqual(result, expected)

    def test_binop_or_constants(self):
        """Test OR operation with two constants."""
        expr = {
            "type": "BINOP",
            "op": "OR",
            "left": {"type": "CONST", "value": 8},
            "right": {"type": "CONST", "value": 4},
        }
        result = generate_expression_code(expr, "test_func", {})
        expected = "mov x0, #8\nmov x1, x0\nmov x0, #4\norr x0, x1, x0"
        self.assertEqual(result, expected)

    def test_binop_xor_constants(self):
        """Test XOR operation with two constants."""
        expr = {
            "type": "BINOP",
            "op": "XOR",
            "left": {"type": "CONST", "value": 12},
            "right": {"type": "CONST", "value": 5},
        }
        result = generate_expression_code(expr, "test_func", {})
        expected = "mov x0, #12\nmov x1, x0\nmov x0, #5\neor x0, x1, x0"
        self.assertEqual(result, expected)

    def test_binop_cmp_constants(self):
        """Test CMP operation with two constants."""
        expr = {
            "type": "BINOP",
            "op": "CMP",
            "left": {"type": "CONST", "value": 10},
            "right": {"type": "CONST", "value": 5},
        }
        result = generate_expression_code(expr, "test_func", {})
        expected = "mov x0, #10\nmov x1, x0\nmov x0, #5\ncmp x1, x0"
        self.assertEqual(result, expected)

    def test_binop_nested_expression(self):
        """Test BINOP with nested expressions."""
        expr = {
            "type": "BINOP",
            "op": "ADD",
            "left": {
                "type": "BINOP",
                "op": "MUL",
                "left": {"type": "CONST", "value": 2},
                "right": {"type": "CONST", "value": 3},
            },
            "right": {"type": "CONST", "value": 1},
        }
        result = generate_expression_code(expr, "test_func", {})
        expected_lines = [
            "mov x0, #2",
            "mov x1, x0",
            "mov x0, #3",
            "mul x0, x1, x0",
            "mov x1, x0",
            "mov x0, #1",
            "add x0, x1, x0",
        ]
        self.assertEqual(result, "\n".join(expected_lines))

    def test_binop_with_variables(self):
        """Test BINOP with variable operands."""
        expr = {
            "type": "BINOP",
            "op": "ADD",
            "left": {"type": "VAR", "var_name": "a"},
            "right": {"type": "VAR", "var_name": "b"},
        }
        var_offsets = {"a": 8, "b": 16}
        result = generate_expression_code(expr, "test_func", var_offsets)
        expected = "ldr x0, [sp, #8]\nmov x1, x0\nldr x0, [sp, #16]\nadd x0, x1, x0"
        self.assertEqual(result, expected)

    def test_binop_unknown_operator(self):
        """Test BINOP with unknown operator raises ValueError."""
        expr = {
            "type": "BINOP",
            "op": "MOD",
            "left": {"type": "CONST", "value": 10},
            "right": {"type": "CONST", "value": 3},
        }
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, "test_func", {})
        self.assertIn("MOD", str(context.exception))


class TestGenerateExpressionCodeErrors(unittest.TestCase):
    """Test cases for error handling."""

    def test_unknown_expr_type(self):
        """Test unknown expression type raises ValueError."""
        expr = {"type": "UNKNOWN", "value": 42}
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, "test_func", {})
        self.assertIn("UNKNOWN", str(context.exception))

    def test_empty_expr_type(self):
        """Test empty expression type raises ValueError."""
        expr = {"type": ""}
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, "test_func", {})
        self.assertIn("", str(context.exception))

    def test_missing_type_field(self):
        """Test missing type field raises appropriate error."""
        expr = {"value": 42}
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, "test_func", {})
        self.assertIn("None", str(context.exception))


class TestGenerateExpressionCodeEdgeCases(unittest.TestCase):
    """Test cases for edge cases and special scenarios."""

    def test_func_name_unused(self):
        """Test that func_name parameter doesn't affect output."""
        expr = {"type": "CONST", "value": 42}
        result1 = generate_expression_code(expr, "func1", {})
        result2 = generate_expression_code(expr, "func2", {})
        self.assertEqual(result1, result2)

    def test_empty_var_offsets_with_const(self):
        """Test CONST expression with empty var_offsets."""
        expr = {"type": "CONST", "value": 100}
        result = generate_expression_code(expr, "test_func", {})
        self.assertEqual(result, "mov x0, #100")

    def test_mixed_const_var_in_binop(self):
        """Test BINOP with mixed CONST and VAR operands."""
        expr = {
            "type": "BINOP",
            "op": "SUB",
            "left": {"type": "VAR", "var_name": "x"},
            "right": {"type": "CONST", "value": 1},
        }
        var_offsets = {"x": 24}
        result = generate_expression_code(expr, "test_func", var_offsets)
        expected = "ldr x0, [sp, #24]\nmov x1, x0\nmov x0, #1\nsub x0, x1, x0"
        self.assertEqual(result, expected)

    def test_deeply_nested_expression(self):
        """Test deeply nested expression (3 levels)."""
        expr = {
            "type": "BINOP",
            "op": "ADD",
            "left": {
                "type": "BINOP",
                "op": "ADD",
                "left": {
                    "type": "BINOP",
                    "op": "ADD",
                    "left": {"type": "CONST", "value": 1},
                    "right": {"type": "CONST", "value": 2},
                },
                "right": {"type": "CONST", "value": 3},
            },
            "right": {"type": "CONST", "value": 4},
        }
        result = generate_expression_code(expr, "test_func", {})
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
        self.assertTrue(result.endswith("add x0, x1, x0"))


if __name__ == "__main__":
    unittest.main()
