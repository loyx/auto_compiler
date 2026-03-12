#!/usr/bin/env python3
"""Unit tests for evaluate_expression function."""

import unittest
from typing import Any, Dict

from .evaluate_expression_src import evaluate_expression

VarOffsets = Dict[str, int]
Expr = Dict[str, Any]


class TestEvaluateExpressionLiteral(unittest.TestCase):
    """Test cases for literal expression type."""

    def test_literal_zero(self):
        """Test literal with value 0."""
        expr: Expr = {"type": "literal", "value": 0}
        var_offsets: VarOffsets = {}
        result = evaluate_expression(expr, var_offsets, "r0")
        self.assertEqual(result, "    mov r0, #0\n")

    def test_literal_positive(self):
        """Test literal with positive value."""
        expr: Expr = {"type": "literal", "value": 42}
        var_offsets: VarOffsets = {}
        result = evaluate_expression(expr, var_offsets, "r0")
        self.assertEqual(result, "    mov r0, #42\n")

    def test_literal_negative(self):
        """Test literal with negative value."""
        expr: Expr = {"type": "literal", "value": -10}
        var_offsets: VarOffsets = {}
        result = evaluate_expression(expr, var_offsets, "r0")
        self.assertEqual(result, "    mov r0, #-10\n")

    def test_literal_different_register(self):
        """Test literal with different target register."""
        expr: Expr = {"type": "literal", "value": 100}
        var_offsets: VarOffsets = {}
        result = evaluate_expression(expr, var_offsets, "r1")
        self.assertEqual(result, "    mov r1, #100\n")


class TestEvaluateExpressionIdentifier(unittest.TestCase):
    """Test cases for identifier expression type."""

    def test_identifier_simple(self):
        """Test simple identifier lookup."""
        expr: Expr = {"type": "identifier", "name": "x"}
        var_offsets: VarOffsets = {"x": 8}
        result = evaluate_expression(expr, var_offsets, "r0")
        self.assertEqual(result, "    ldr r0, [fp, #8]\n")

    def test_identifier_zero_offset(self):
        """Test identifier with zero offset."""
        expr: Expr = {"type": "identifier", "name": "y"}
        var_offsets: VarOffsets = {"y": 0}
        result = evaluate_expression(expr, var_offsets, "r0")
        self.assertEqual(result, "    ldr r0, [fp, #0]\n")

    def test_identifier_negative_offset(self):
        """Test identifier with negative offset."""
        expr: Expr = {"type": "identifier", "name": "z"}
        var_offsets: VarOffsets = {"z": -16}
        result = evaluate_expression(expr, var_offsets, "r0")
        self.assertEqual(result, "    ldr r0, [fp, #-16]\n")

    def test_identifier_different_register(self):
        """Test identifier with different target register."""
        expr: Expr = {"type": "identifier", "name": "a"}
        var_offsets: VarOffsets = {"a": 24}
        result = evaluate_expression(expr, var_offsets, "r1")
        self.assertEqual(result, "    ldr r1, [fp, #24]\n")


class TestEvaluateExpressionBinaryArithmetic(unittest.TestCase):
    """Test cases for binary arithmetic operations."""

    def test_binary_add(self):
        """Test binary addition."""
        expr: Expr = {
            "type": "binary",
            "op": "add",
            "left": {"type": "literal", "value": 5},
            "right": {"type": "literal", "value": 3}
        }
        var_offsets: VarOffsets = {}
        result = evaluate_expression(expr, var_offsets, "r0")
        expected = (
            "    mov r0, #5\n"
            "    mov r1, #3\n"
            "    add r0, r0, r1\n"
        )
        self.assertEqual(result, expected)

    def test_binary_sub(self):
        """Test binary subtraction."""
        expr: Expr = {
            "type": "binary",
            "op": "sub",
            "left": {"type": "literal", "value": 10},
            "right": {"type": "literal", "value": 4}
        }
        var_offsets: VarOffsets = {}
        result = evaluate_expression(expr, var_offsets, "r0")
        expected = (
            "    mov r0, #10\n"
            "    mov r1, #4\n"
            "    sub r0, r0, r1\n"
        )
        self.assertEqual(result, expected)

    def test_binary_mul(self):
        """Test binary multiplication."""
        expr: Expr = {
            "type": "binary",
            "op": "mul",
            "left": {"type": "literal", "value": 6},
            "right": {"type": "literal", "value": 7}
        }
        var_offsets: VarOffsets = {}
        result = evaluate_expression(expr, var_offsets, "r0")
        expected = (
            "    mov r0, #6\n"
            "    mov r1, #7\n"
            "    mul r0, r0, r1\n"
        )
        self.assertEqual(result, expected)

    def test_binary_div(self):
        """Test binary division."""
        expr: Expr = {
            "type": "binary",
            "op": "div",
            "left": {"type": "literal", "value": 20},
            "right": {"type": "literal", "value": 4}
        }
        var_offsets: VarOffsets = {}
        result = evaluate_expression(expr, var_offsets, "r0")
        expected = (
            "    mov r0, #20\n"
            "    mov r1, #4\n"
            "    sdiv r0, r0, r1\n"
        )
        self.assertEqual(result, expected)


class TestEvaluateExpressionBinaryComparison(unittest.TestCase):
    """Test cases for binary comparison operations."""

    def test_binary_lt(self):
        """Test less than comparison."""
        expr: Expr = {
            "type": "binary",
            "op": "lt",
            "left": {"type": "literal", "value": 3},
            "right": {"type": "literal", "value": 5}
        }
        var_offsets: VarOffsets = {}
        result = evaluate_expression(expr, var_offsets, "r0")
        expected = (
            "    mov r0, #3\n"
            "    mov r1, #5\n"
            "    cmp r0, r1\n"
            "    movlt r0, #1\n"
            "    movge r0, #0\n"
        )
        self.assertEqual(result, expected)

    def test_binary_gt(self):
        """Test greater than comparison."""
        expr: Expr = {
            "type": "binary",
            "op": "gt",
            "left": {"type": "literal", "value": 10},
            "right": {"type": "literal", "value": 2}
        }
        var_offsets: VarOffsets = {}
        result = evaluate_expression(expr, var_offsets, "r0")
        expected = (
            "    mov r0, #10\n"
            "    mov r1, #2\n"
            "    cmp r0, r1\n"
            "    movgt r0, #1\n"
            "    movle r0, #0\n"
        )
        self.assertEqual(result, expected)

    def test_binary_le(self):
        """Test less than or equal comparison."""
        expr: Expr = {
            "type": "binary",
            "op": "le",
            "left": {"type": "literal", "value": 5},
            "right": {"type": "literal", "value": 5}
        }
        var_offsets: VarOffsets = {}
        result = evaluate_expression(expr, var_offsets, "r0")
        expected = (
            "    mov r0, #5\n"
            "    mov r1, #5\n"
            "    cmp r0, r1\n"
            "    movle r0, #1\n"
            "    movgt r0, #0\n"
        )
        self.assertEqual(result, expected)

    def test_binary_ge(self):
        """Test greater than or equal comparison."""
        expr: Expr = {
            "type": "binary",
            "op": "ge",
            "left": {"type": "literal", "value": 8},
            "right": {"type": "literal", "value": 3}
        }
        var_offsets: VarOffsets = {}
        result = evaluate_expression(expr, var_offsets, "r0")
        expected = (
            "    mov r0, #8\n"
            "    mov r1, #3\n"
            "    cmp r0, r1\n"
            "    movge r0, #1\n"
            "    movlt r0, #0\n"
        )
        self.assertEqual(result, expected)

    def test_binary_eq(self):
        """Test equality comparison."""
        expr: Expr = {
            "type": "binary",
            "op": "eq",
            "left": {"type": "literal", "value": 7},
            "right": {"type": "literal", "value": 7}
        }
        var_offsets: VarOffsets = {}
        result = evaluate_expression(expr, var_offsets, "r0")
        expected = (
            "    mov r0, #7\n"
            "    mov r1, #7\n"
            "    cmp r0, r1\n"
            "    moveq r0, #1\n"
            "    movne r0, #0\n"
        )
        self.assertEqual(result, expected)

    def test_binary_ne(self):
        """Test not equal comparison."""
        expr: Expr = {
            "type": "binary",
            "op": "ne",
            "left": {"type": "literal", "value": 4},
            "right": {"type": "literal", "value": 9}
        }
        var_offsets: VarOffsets = {}
        result = evaluate_expression(expr, var_offsets, "r0")
        expected = (
            "    mov r0, #4\n"
            "    mov r1, #9\n"
            "    cmp r0, r1\n"
            "    movne r0, #1\n"
            "    moveq r0, #0\n"
        )
        self.assertEqual(result, expected)


class TestEvaluateExpressionBinaryNested(unittest.TestCase):
    """Test cases for nested binary expressions."""

    def test_nested_arithmetic(self):
        """Test nested arithmetic expression: (5 + 3) * 2."""
        expr: Expr = {
            "type": "binary",
            "op": "mul",
            "left": {
                "type": "binary",
                "op": "add",
                "left": {"type": "literal", "value": 5},
                "right": {"type": "literal", "value": 3}
            },
            "right": {"type": "literal", "value": 2}
        }
        var_offsets: VarOffsets = {}
        result = evaluate_expression(expr, var_offsets, "r0")
        expected = (
            "    mov r0, #5\n"
            "    mov r1, #3\n"
            "    add r0, r0, r1\n"
            "    mov r1, #2\n"
            "    mul r0, r0, r1\n"
        )
        self.assertEqual(result, expected)

    def test_mixed_identifier_and_literal(self):
        """Test expression with identifier and literal: x + 10."""
        expr: Expr = {
            "type": "binary",
            "op": "add",
            "left": {"type": "identifier", "name": "x"},
            "right": {"type": "literal", "value": 10}
        }
        var_offsets: VarOffsets = {"x": 16}
        result = evaluate_expression(expr, var_offsets, "r0")
        expected = (
            "    ldr r0, [fp, #16]\n"
            "    mov r1, #10\n"
            "    add r0, r0, r1\n"
        )
        self.assertEqual(result, expected)

    def test_two_identifiers(self):
        """Test expression with two identifiers: a - b."""
        expr: Expr = {
            "type": "binary",
            "op": "sub",
            "left": {"type": "identifier", "name": "a"},
            "right": {"type": "identifier", "name": "b"}
        }
        var_offsets: VarOffsets = {"a": 8, "b": 12}
        result = evaluate_expression(expr, var_offsets, "r0")
        expected = (
            "    ldr r0, [fp, #8]\n"
            "    ldr r1, [fp, #12]\n"
            "    sub r0, r0, r1\n"
        )
        self.assertEqual(result, expected)


class TestEvaluateExpressionTargetRegister(unittest.TestCase):
    """Test cases for different target registers."""

    def test_target_r1(self):
        """Test with r1 as target register."""
        expr: Expr = {
            "type": "binary",
            "op": "add",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 2}
        }
        var_offsets: VarOffsets = {}
        result = evaluate_expression(expr, var_offsets, "r1")
        expected = (
            "    mov r1, #1\n"
            "    mov r1, #2\n"
            "    add r1, r1, r1\n"
        )
        self.assertEqual(result, expected)


class TestEvaluateExpressionInvalidInput(unittest.TestCase):
    """Test cases for invalid inputs."""

    def test_unknown_expression_type(self):
        """Test with unknown expression type."""
        expr: Expr = {"type": "unknown_type"}
        var_offsets: VarOffsets = {}
        with self.assertRaises(AssertionError) as context:
            evaluate_expression(expr, var_offsets, "r0")
        self.assertIn("Unknown expression type", str(context.exception))

    def test_unknown_binary_operator(self):
        """Test with unknown binary operator."""
        expr: Expr = {
            "type": "binary",
            "op": "unknown_op",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 2}
        }
        var_offsets: VarOffsets = {}
        with self.assertRaises(AssertionError) as context:
            evaluate_expression(expr, var_offsets, "r0")
        self.assertIn("Unknown binary operator", str(context.exception))


if __name__ == "__main__":
    unittest.main()
