# -*- coding: utf-8 -*-
"""Unit tests for evaluate_expression function."""

import unittest

from .evaluate_expression_src import evaluate_expression


class TestEvaluateExpressionLiteral(unittest.TestCase):
    """Tests for LITERAL expression type."""

    def test_literal_zero(self):
        """Test literal expression with value 0."""
        expr = {"type": "LITERAL", "value": 0}
        code, next_offset = evaluate_expression(
            expr, "main", {}, {}, 0
        )
        self.assertEqual(code, "    mov r0, #0\n")
        self.assertEqual(next_offset, 0)

    def test_literal_positive(self):
        """Test literal expression with positive value."""
        expr = {"type": "LITERAL", "value": 42}
        code, next_offset = evaluate_expression(
            expr, "main", {}, {}, 0
        )
        self.assertEqual(code, "    mov r0, #42\n")
        self.assertEqual(next_offset, 0)

    def test_literal_negative(self):
        """Test literal expression with negative value."""
        expr = {"type": "LITERAL", "value": -10}
        code, next_offset = evaluate_expression(
            expr, "main", {}, {}, 0
        )
        self.assertEqual(code, "    mov r0, #-10\n")
        self.assertEqual(next_offset, 0)

    def test_literal_large_value(self):
        """Test literal expression with large value."""
        expr = {"type": "LITERAL", "value": 999999}
        code, next_offset = evaluate_expression(
            expr, "main", {}, {}, 0
        )
        self.assertEqual(code, "    mov r0, #999999\n")
        self.assertEqual(next_offset, 0)

    def test_literal_with_non_zero_offset(self):
        """Test literal expression with non-zero next_offset."""
        expr = {"type": "LITERAL", "value": 5}
        code, next_offset = evaluate_expression(
            expr, "main", {}, {}, 10
        )
        self.assertEqual(code, "    mov r0, #5\n")
        self.assertEqual(next_offset, 10)


class TestEvaluateExpressionVar(unittest.TestCase):
    """Tests for VAR expression type."""

    def test_var_defined(self):
        """Test variable expression with defined variable."""
        expr = {"type": "VAR", "value": "x"}
        var_offsets = {"x": 4}
        code, next_offset = evaluate_expression(
            expr, "main", {}, var_offsets, 0
        )
        self.assertEqual(code, "    ldr r0, [sp, #4]\n")
        self.assertEqual(next_offset, 0)

    def test_var_offset_zero(self):
        """Test variable at stack offset 0."""
        expr = {"type": "VAR", "value": "y"}
        var_offsets = {"y": 0}
        code, next_offset = evaluate_expression(
            expr, "main", {}, var_offsets, 0
        )
        self.assertEqual(code, "    ldr r0, [sp, #0]\n")
        self.assertEqual(next_offset, 0)

    def test_var_large_offset(self):
        """Test variable at large stack offset."""
        expr = {"type": "VAR", "value": "z"}
        var_offsets = {"z": 100}
        code, next_offset = evaluate_expression(
            expr, "main", {}, var_offsets, 0
        )
        self.assertEqual(code, "    ldr r0, [sp, #100]\n")
        self.assertEqual(next_offset, 0)

    def test_var_undefined_raises(self):
        """Test undefined variable raises ValueError."""
        expr = {"type": "VAR", "value": "undefined_var"}
        var_offsets = {"x": 4}
        with self.assertRaises(ValueError) as context:
            evaluate_expression(expr, "main", {}, var_offsets, 0)
        self.assertIn("Undefined variable: undefined_var", str(context.exception))

    def test_var_empty_var_offsets_raises(self):
        """Test variable with empty var_offsets raises ValueError."""
        expr = {"type": "VAR", "value": "any_var"}
        with self.assertRaises(ValueError) as context:
            evaluate_expression(expr, "main", {}, {}, 0)
        self.assertIn("Undefined variable: any_var", str(context.exception))


class TestEvaluateExpressionBinop(unittest.TestCase):
    """Tests for BINOP expression type."""

    def test_binop_add_simple(self):
        """Test simple addition of two literals."""
        expr = {
            "type": "BINOP",
            "op": "add",
            "left": {"type": "LITERAL", "value": 3},
            "right": {"type": "LITERAL", "value": 5},
        }
        code, next_offset = evaluate_expression(
            expr, "main", {}, {}, 0
        )
        expected = (
            "    mov r0, #3\n"
            "    str r0, [sp, #0]\n"
            "    mov r0, #5\n"
            "    ldr r1, [sp, #0]\n"
            "    add r0, r1, r0\n"
        )
        self.assertEqual(code, expected)
        self.assertEqual(next_offset, 1)

    def test_binop_sub_simple(self):
        """Test simple subtraction of two literals."""
        expr = {
            "type": "BINOP",
            "op": "sub",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 3},
        }
        code, next_offset = evaluate_expression(
            expr, "main", {}, {}, 0
        )
        expected = (
            "    mov r0, #10\n"
            "    str r0, [sp, #0]\n"
            "    mov r0, #3\n"
            "    ldr r1, [sp, #0]\n"
            "    sub r0, r1, r0\n"
        )
        self.assertEqual(code, expected)
        self.assertEqual(next_offset, 1)

    def test_binop_mul_simple(self):
        """Test simple multiplication of two literals."""
        expr = {
            "type": "BINOP",
            "op": "mul",
            "left": {"type": "LITERAL", "value": 4},
            "right": {"type": "LITERAL", "value": 7},
        }
        code, next_offset = evaluate_expression(
            expr, "main", {}, {}, 0
        )
        expected = (
            "    mov r0, #4\n"
            "    str r0, [sp, #0]\n"
            "    mov r0, #7\n"
            "    ldr r1, [sp, #0]\n"
            "    mul r0, r1, r0\n"
        )
        self.assertEqual(code, expected)
        self.assertEqual(next_offset, 1)

    def test_binop_div_simple(self):
        """Test simple division of two literals."""
        expr = {
            "type": "BINOP",
            "op": "div",
            "left": {"type": "LITERAL", "value": 20},
            "right": {"type": "LITERAL", "value": 4},
        }
        code, next_offset = evaluate_expression(
            expr, "main", {}, {}, 0
        )
        expected = (
            "    mov r0, #20\n"
            "    str r0, [sp, #0]\n"
            "    mov r0, #4\n"
            "    ldr r1, [sp, #0]\n"
            "    sdiv r0, r1, r0\n"
        )
        self.assertEqual(code, expected)
        self.assertEqual(next_offset, 1)

    def test_binop_unsupported_op_raises(self):
        """Test unsupported operator raises ValueError."""
        expr = {
            "type": "BINOP",
            "op": "mod",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 3},
        }
        with self.assertRaises(ValueError) as context:
            evaluate_expression(expr, "main", {}, {}, 0)
        self.assertIn("Unsupported binary operator: mod", str(context.exception))

    def test_binop_with_vars(self):
        """Test binary operation with variables."""
        expr = {
            "type": "BINOP",
            "op": "add",
            "left": {"type": "VAR", "value": "a"},
            "right": {"type": "VAR", "value": "b"},
        }
        var_offsets = {"a": 4, "b": 8}
        code, next_offset = evaluate_expression(
            expr, "main", {}, var_offsets, 0
        )
        expected = (
            "    ldr r0, [sp, #4]\n"
            "    str r0, [sp, #0]\n"
            "    ldr r0, [sp, #8]\n"
            "    ldr r1, [sp, #0]\n"
            "    add r0, r1, r0\n"
        )
        self.assertEqual(code, expected)
        self.assertEqual(next_offset, 1)

    def test_binop_nested_left(self):
        """Test binary operation with nested expression on left."""
        expr = {
            "type": "BINOP",
            "op": "add",
            "left": {
                "type": "BINOP",
                "op": "mul",
                "left": {"type": "LITERAL", "value": 2},
                "right": {"type": "LITERAL", "value": 3},
            },
            "right": {"type": "LITERAL", "value": 10},
        }
        code, next_offset = evaluate_expression(
            expr, "main", {}, {}, 0
        )
        # Left side: 2 * 3, stored at offset 0
        # Right side: 10, evaluated at offset 2
        # Then add them
        self.assertIn("mov r0, #2\n", code)
        self.assertIn("mov r0, #3\n", code)
        self.assertIn("mul r0, r1, r0\n", code)
        self.assertIn("mov r0, #10\n", code)
        self.assertIn("add r0, r1, r0\n", code)
        self.assertEqual(next_offset, 3)

    def test_binop_nested_right(self):
        """Test binary operation with nested expression on right."""
        expr = {
            "type": "BINOP",
            "op": "sub",
            "left": {"type": "LITERAL", "value": 100},
            "right": {
                "type": "BINOP",
                "op": "div",
                "left": {"type": "LITERAL", "value": 20},
                "right": {"type": "LITERAL", "value": 4},
            },
        }
        code, next_offset = evaluate_expression(
            expr, "main", {}, {}, 0
        )
        self.assertIn("mov r0, #100\n", code)
        self.assertIn("mov r0, #20\n", code)
        self.assertIn("mov r0, #4\n", code)
        self.assertIn("sdiv r0, r1, r0\n", code)
        self.assertIn("sub r0, r1, r0\n", code)
        self.assertEqual(next_offset, 3)

    def test_binop_deeply_nested(self):
        """Test deeply nested binary operations."""
        expr = {
            "type": "BINOP",
            "op": "add",
            "left": {
                "type": "BINOP",
                "op": "add",
                "left": {"type": "LITERAL", "value": 1},
                "right": {"type": "LITERAL", "value": 2},
            },
            "right": {
                "type": "BINOP",
                "op": "add",
                "left": {"type": "LITERAL", "value": 3},
                "right": {"type": "LITERAL", "value": 4},
            },
        }
        code, next_offset = evaluate_expression(
            expr, "main", {}, {}, 0
        )
        # Should contain all four literal loads and three add operations
        self.assertEqual(code.count("mov r0, #"), 4)
        self.assertEqual(code.count("add r0, r1, r0\n"), 3)
        self.assertEqual(code.count("str r0, [sp,"), 3)
        self.assertEqual(code.count("ldr r1, [sp,"), 3)
        self.assertEqual(next_offset, 5)

    def test_binop_mixed_var_and_literal(self):
        """Test binary operation mixing variable and literal."""
        expr = {
            "type": "BINOP",
            "op": "mul",
            "left": {"type": "VAR", "value": "x"},
            "right": {"type": "LITERAL", "value": 2},
        }
        var_offsets = {"x": 12}
        code, next_offset = evaluate_expression(
            expr, "main", {}, var_offsets, 0
        )
        expected = (
            "    ldr r0, [sp, #12]\n"
            "    str r0, [sp, #0]\n"
            "    mov r0, #2\n"
            "    ldr r1, [sp, #0]\n"
            "    mul r0, r1, r0\n"
        )
        self.assertEqual(code, expected)
        self.assertEqual(next_offset, 1)

    def test_binop_with_non_zero_start_offset(self):
        """Test binary operation starting with non-zero offset."""
        expr = {
            "type": "BINOP",
            "op": "add",
            "left": {"type": "LITERAL", "value": 1},
            "right": {"type": "LITERAL", "value": 2},
        }
        code, next_offset = evaluate_expression(
            expr, "main", {}, {}, 5
        )
        # Stack temp should be saved at offset 5
        self.assertIn("str r0, [sp, #5]\n", code)
        self.assertEqual(next_offset, 6)


class TestEvaluateExpressionUnknown(unittest.TestCase):
    """Tests for unknown expression types."""

    def test_unknown_type_raises(self):
        """Test unknown expression type raises ValueError."""
        expr = {"type": "UNKNOWN", "value": 42}
        with self.assertRaises(ValueError) as context:
            evaluate_expression(expr, "main", {}, {}, 0)
        self.assertIn("Unknown expression type: UNKNOWN", str(context.exception))

    def test_empty_expr_raises(self):
        """Test empty expression dict raises error."""
        expr = {}
        with self.assertRaises(ValueError) as context:
            evaluate_expression(expr, "main", {}, {}, 0)
        self.assertIn("Unknown expression type: None", str(context.exception))

    def test_missing_type_key_raises(self):
        """Test expression without type key raises error."""
        expr = {"value": 42}
        with self.assertRaises(ValueError) as context:
            evaluate_expression(expr, "main", {}, {}, 0)
        self.assertIn("Unknown expression type: None", str(context.exception))


class TestEvaluateExpressionEdgeCases(unittest.TestCase):
    """Edge case tests for evaluate_expression."""

    def test_binop_missing_op_raises(self):
        """Test BINOP without op key raises error."""
        expr = {
            "type": "BINOP",
            "left": {"type": "LITERAL", "value": 1},
            "right": {"type": "LITERAL", "value": 2},
        }
        with self.assertRaises(KeyError):
            evaluate_expression(expr, "main", {}, {}, 0)

    def test_binop_missing_left_raises(self):
        """Test BINOP without left key raises error."""
        expr = {
            "type": "BINOP",
            "op": "add",
            "right": {"type": "LITERAL", "value": 2},
        }
        with self.assertRaises(KeyError):
            evaluate_expression(expr, "main", {}, {}, 0)

    def test_binop_missing_right_raises(self):
        """Test BINOP without right key raises error."""
        expr = {
            "type": "BINOP",
            "op": "add",
            "left": {"type": "LITERAL", "value": 1},
        }
        with self.assertRaises(KeyError):
            evaluate_expression(expr, "main", {}, {}, 0)

    def test_var_missing_value_raises(self):
        """Test VAR without value key raises error."""
        expr = {"type": "VAR"}
        with self.assertRaises(KeyError):
            evaluate_expression(expr, "main", {}, {}, 0)

    def test_literal_missing_value_raises(self):
        """Test LITERAL without value key raises error."""
        expr = {"type": "LITERAL"}
        with self.assertRaises(KeyError):
            evaluate_expression(expr, "main", {}, {}, 0)

    def test_func_name_unused(self):
        """Test that func_name parameter doesn't affect output."""
        expr = {"type": "LITERAL", "value": 42}
        code1, _ = evaluate_expression(expr, "func1", {}, {}, 0)
        code2, _ = evaluate_expression(expr, "func2", {}, {}, 0)
        self.assertEqual(code1, code2)

    def test_label_counter_unused(self):
        """Test that label_counter parameter doesn't affect output."""
        expr = {"type": "LITERAL", "value": 42}
        code1, _ = evaluate_expression(expr, "main", {}, {}, 0)
        code2, _ = evaluate_expression(expr, "main", {"while_cond": 0}, {}, 0)
        self.assertEqual(code1, code2)


if __name__ == "__main__":
    unittest.main()
