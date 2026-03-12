#!/usr/bin/env python3
"""Unit tests for evaluate_expression function."""

import unittest

from .evaluate_expression_src import evaluate_expression


class TestEvaluateExpressionLiteral(unittest.TestCase):
    """Tests for LITERAL expression type."""

    def test_literal_zero(self):
        """Test literal with value 0."""
        expr = {"type": "LITERAL", "value": 0}
        var_offsets = {}
        result = evaluate_expression(expr, var_offsets)
        self.assertEqual(result, "mov r0, #0")

    def test_literal_positive(self):
        """Test literal with positive value."""
        expr = {"type": "LITERAL", "value": 42}
        var_offsets = {}
        result = evaluate_expression(expr, var_offsets)
        self.assertEqual(result, "mov r0, #42")

    def test_literal_negative(self):
        """Test literal with negative value."""
        expr = {"type": "LITERAL", "value": -10}
        var_offsets = {}
        result = evaluate_expression(expr, var_offsets)
        self.assertEqual(result, "mov r0, #-10")

    def test_literal_large_value(self):
        """Test literal with large value."""
        expr = {"type": "LITERAL", "value": 1000000}
        var_offsets = {}
        result = evaluate_expression(expr, var_offsets)
        self.assertEqual(result, "mov r0, #1000000")

    def test_literal_missing_value(self):
        """Test literal with missing value field (defaults to 0)."""
        expr = {"type": "LITERAL"}
        var_offsets = {}
        result = evaluate_expression(expr, var_offsets)
        self.assertEqual(result, "mov r0, #0")


class TestEvaluateExpressionIdent(unittest.TestCase):
    """Tests for IDENT expression type."""

    def test_ident_existing_variable(self):
        """Test identifier with existing variable in var_offsets."""
        expr = {"type": "IDENT", "name": "x"}
        var_offsets = {"x": 8}
        result = evaluate_expression(expr, var_offsets)
        self.assertEqual(result, "ldr r0, [sp, #8]")

    def test_ident_zero_offset(self):
        """Test identifier with zero offset."""
        expr = {"type": "IDENT", "name": "y"}
        var_offsets = {"y": 0}
        result = evaluate_expression(expr, var_offsets)
        self.assertEqual(result, "ldr r0, [sp, #0]")

    def test_ident_missing_variable(self):
        """Test identifier with missing variable (defaults to offset 0)."""
        expr = {"type": "IDENT", "name": "z"}
        var_offsets = {"x": 4}
        result = evaluate_expression(expr, var_offsets)
        self.assertEqual(result, "ldr r0, [sp, #0]")

    def test_ident_missing_name(self):
        """Test identifier with missing name field (defaults to empty string)."""
        expr = {"type": "IDENT"}
        var_offsets = {}
        result = evaluate_expression(expr, var_offsets)
        self.assertEqual(result, "ldr r0, [sp, #0]")

    def test_ident_multiple_variables(self):
        """Test identifier with multiple variables in scope."""
        expr = {"type": "IDENT", "name": "b"}
        var_offsets = {"a": 0, "b": 4, "c": 8}
        result = evaluate_expression(expr, var_offsets)
        self.assertEqual(result, "ldr r0, [sp, #4]")


class TestEvaluateExpressionUnop(unittest.TestCase):
    """Tests for UNOP expression type."""

    def test_unop_negate_literal(self):
        """Test unary minus on literal."""
        expr = {"type": "UNOP", "op": "-", "operand": {"type": "LITERAL", "value": 5}}
        var_offsets = {}
        result = evaluate_expression(expr, var_offsets)
        self.assertEqual(result, "mov r0, #5\n    rsb r0, r0, #0")

    def test_unop_negate_ident(self):
        """Test unary minus on identifier."""
        expr = {"type": "UNOP", "op": "-", "operand": {"type": "IDENT", "name": "x"}}
        var_offsets = {"x": 4}
        result = evaluate_expression(expr, var_offsets)
        self.assertEqual(result, "ldr r0, [sp, #4]\n    rsb r0, r0, #0")

    def test_unop_not_literal_zero(self):
        """Test logical not on literal zero (should be 1)."""
        expr = {"type": "UNOP", "op": "!", "operand": {"type": "LITERAL", "value": 0}}
        var_offsets = {}
        result = evaluate_expression(expr, var_offsets)
        self.assertEqual(result, "mov r0, #0\n    cmp r0, #0\n    moveq r0, #1\n    movne r0, #0")

    def test_unop_not_literal_nonzero(self):
        """Test logical not on non-zero literal (should be 0)."""
        expr = {"type": "UNOP", "op": "!", "operand": {"type": "LITERAL", "value": 42}}
        var_offsets = {}
        result = evaluate_expression(expr, var_offsets)
        self.assertEqual(result, "mov r0, #42\n    cmp r0, #0\n    moveq r0, #1\n    movne r0, #0")

    def test_unop_nested_negate(self):
        """Test double negation."""
        expr = {
            "type": "UNOP",
            "op": "-",
            "operand": {
                "type": "UNOP",
                "op": "-",
                "operand": {"type": "LITERAL", "value": 10}
            }
        }
        var_offsets = {}
        result = evaluate_expression(expr, var_offsets)
        expected = "mov r0, #10\n    rsb r0, r0, #0\n    rsb r0, r0, #0"
        self.assertEqual(result, expected)

    def test_unop_not_nested(self):
        """Test logical not on nested expression."""
        expr = {
            "type": "UNOP",
            "op": "!",
            "operand": {
                "type": "BINOP",
                "op": "+",
                "left": {"type": "LITERAL", "value": 1},
                "right": {"type": "LITERAL", "value": 2}
            }
        }
        var_offsets = {}
        result = evaluate_expression(expr, var_offsets)
        self.assertIn("cmp r0, #0", result)
        self.assertIn("moveq r0, #1", result)

    def test_unop_unknown_op(self):
        """Test unary operator with unknown op (returns operand code only)."""
        expr = {"type": "UNOP", "op": "~", "operand": {"type": "LITERAL", "value": 5}}
        var_offsets = {}
        result = evaluate_expression(expr, var_offsets)
        self.assertEqual(result, "mov r0, #5")

    def test_unop_missing_operand(self):
        """Test unary operator with missing operand."""
        expr = {"type": "UNOP", "op": "-"}
        var_offsets = {}
        result = evaluate_expression(expr, var_offsets)
        self.assertEqual(result, "rsb r0, r0, #0")


class TestEvaluateExpressionBinopArithmetic(unittest.TestCase):
    """Tests for BINOP arithmetic operators."""

    def test_binop_add_literals(self):
        """Test addition of two literals."""
        expr = {
            "type": "BINOP",
            "op": "+",
            "left": {"type": "LITERAL", "value": 3},
            "right": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        result = evaluate_expression(expr, var_offsets)
        self.assertIn("mov r0, #3", result)
        self.assertIn("mov r1, r0", result)
        self.assertIn("mov r0, #5", result)
        self.assertIn("add r0, r1, r0", result)

    def test_binop_sub_literals(self):
        """Test subtraction of two literals."""
        expr = {
            "type": "BINOP",
            "op": "-",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 4}
        }
        var_offsets = {}
        result = evaluate_expression(expr, var_offsets)
        self.assertIn("sub r0, r1, r0", result)

    def test_binop_mul_literals(self):
        """Test multiplication of two literals."""
        expr = {
            "type": "BINOP",
            "op": "*",
            "left": {"type": "LITERAL", "value": 6},
            "right": {"type": "LITERAL", "value": 7}
        }
        var_offsets = {}
        result = evaluate_expression(expr, var_offsets)
        self.assertIn("mul r0, r1, r0", result)

    def test_binop_div_literals(self):
        """Test division of two literals."""
        expr = {
            "type": "BINOP",
            "op": "/",
            "left": {"type": "LITERAL", "value": 20},
            "right": {"type": "LITERAL", "value": 4}
        }
        var_offsets = {}
        result = evaluate_expression(expr, var_offsets)
        self.assertIn("sdiv r0, r1, r0", result)

    def test_binop_add_idents(self):
        """Test addition of two identifiers."""
        expr = {
            "type": "BINOP",
            "op": "+",
            "left": {"type": "IDENT", "name": "a"},
            "right": {"type": "IDENT", "name": "b"}
        }
        var_offsets = {"a": 0, "b": 4}
        result = evaluate_expression(expr, var_offsets)
        self.assertIn("ldr r0, [sp, #0]", result)
        self.assertIn("ldr r0, [sp, #4]", result)
        self.assertIn("add r0, r1, r0", result)

    def test_binop_mixed_ident_literal(self):
        """Test operation between identifier and literal."""
        expr = {
            "type": "BINOP",
            "op": "+",
            "left": {"type": "IDENT", "name": "x"},
            "right": {"type": "LITERAL", "value": 1}
        }
        var_offsets = {"x": 8}
        result = evaluate_expression(expr, var_offsets)
        self.assertIn("ldr r0, [sp, #8]", result)
        self.assertIn("mov r0, #1", result)


class TestEvaluateExpressionBinopComparison(unittest.TestCase):
    """Tests for BINOP comparison operators."""

    def test_binop_eq_true(self):
        """Test equality comparison that would be true."""
        expr = {
            "type": "BINOP",
            "op": "==",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        result = evaluate_expression(expr, var_offsets)
        self.assertIn("cmp r1, r0", result)
        self.assertIn("moveq r0, #1", result)
        self.assertIn("movne r0, #0", result)

    def test_binop_ne_true(self):
        """Test not-equal comparison that would be true."""
        expr = {
            "type": "BINOP",
            "op": "!=",
            "left": {"type": "LITERAL", "value": 3},
            "right": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        result = evaluate_expression(expr, var_offsets)
        self.assertIn("movne r0, #1", result)
        self.assertIn("moveq r0, #0", result)

    def test_binop_lt_true(self):
        """Test less-than comparison that would be true."""
        expr = {
            "type": "BINOP",
            "op": "<",
            "left": {"type": "LITERAL", "value": 3},
            "right": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        result = evaluate_expression(expr, var_offsets)
        self.assertIn("movlt r0, #1", result)
        self.assertIn("movge r0, #0", result)

    def test_binop_gt_true(self):
        """Test greater-than comparison that would be true."""
        expr = {
            "type": "BINOP",
            "op": ">",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        result = evaluate_expression(expr, var_offsets)
        self.assertIn("movgt r0, #1", result)
        self.assertIn("movle r0, #0", result)

    def test_binop_le_true(self):
        """Test less-than-or-equal comparison."""
        expr = {
            "type": "BINOP",
            "op": "<=",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        result = evaluate_expression(expr, var_offsets)
        self.assertIn("movle r0, #1", result)
        self.assertIn("movgt r0, #0", result)

    def test_binop_ge_true(self):
        """Test greater-than-or-equal comparison."""
        expr = {
            "type": "BINOP",
            "op": ">=",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        result = evaluate_expression(expr, var_offsets)
        self.assertIn("movge r0, #1", result)
        self.assertIn("movlt r0, #0", result)


class TestEvaluateExpressionBinopLogical(unittest.TestCase):
    """Tests for BINOP logical operators."""

    def test_binop_and(self):
        """Test logical AND operator."""
        expr = {
            "type": "BINOP",
            "op": "&&",
            "left": {"type": "LITERAL", "value": 1},
            "right": {"type": "LITERAL", "value": 1}
        }
        var_offsets = {}
        result = evaluate_expression(expr, var_offsets)
        self.assertIn("cmp r0, #0", result)
        self.assertIn("and r0, r0, r1", result)

    def test_binop_or(self):
        """Test logical OR operator."""
        expr = {
            "type": "BINOP",
            "op": "||",
            "left": {"type": "LITERAL", "value": 0},
            "right": {"type": "LITERAL", "value": 1}
        }
        var_offsets = {}
        result = evaluate_expression(expr, var_offsets)
        self.assertIn("orr r0, r1, r0", result)


class TestEvaluateExpressionNested(unittest.TestCase):
    """Tests for deeply nested expressions."""

    def test_nested_arithmetic(self):
        """Test nested arithmetic expression: (1 + 2) * 3."""
        expr = {
            "type": "BINOP",
            "op": "*",
            "left": {
                "type": "BINOP",
                "op": "+",
                "left": {"type": "LITERAL", "value": 1},
                "right": {"type": "LITERAL", "value": 2}
            },
            "right": {"type": "LITERAL", "value": 3}
        }
        var_offsets = {}
        result = evaluate_expression(expr, var_offsets)
        self.assertIn("add r0, r1, r0", result)
        self.assertIn("mul r0, r1, r0", result)

    def test_nested_comparison_in_unop(self):
        """Test negation of comparison: !(a == b)."""
        expr = {
            "type": "UNOP",
            "op": "!",
            "operand": {
                "type": "BINOP",
                "op": "==",
                "left": {"type": "IDENT", "name": "a"},
                "right": {"type": "IDENT", "name": "b"}
            }
        }
        var_offsets = {"a": 0, "b": 4}
        result = evaluate_expression(expr, var_offsets)
        self.assertIn("ldr r0, [sp, #0]", result)
        self.assertIn("ldr r0, [sp, #4]", result)
        self.assertIn("cmp r1, r0", result)
        self.assertIn("cmp r0, #0", result)

    def test_complex_expression(self):
        """Test complex expression: (a + b) > (c * 2)."""
        expr = {
            "type": "BINOP",
            "op": ">",
            "left": {
                "type": "BINOP",
                "op": "+",
                "left": {"type": "IDENT", "name": "a"},
                "right": {"type": "IDENT", "name": "b"}
            },
            "right": {
                "type": "BINOP",
                "op": "*",
                "left": {"type": "IDENT", "name": "c"},
                "right": {"type": "LITERAL", "value": 2}
            }
        }
        var_offsets = {"a": 0, "b": 4, "c": 8}
        result = evaluate_expression(expr, var_offsets)
        self.assertIn("add r0, r1, r0", result)
        self.assertIn("mul r0, r1, r0", result)
        self.assertIn("cmp r1, r0", result)
        self.assertIn("movgt r0, #1", result)


class TestEvaluateExpressionEdgeCases(unittest.TestCase):
    """Tests for edge cases and error handling."""

    def test_empty_expr(self):
        """Test empty expression dict."""
        expr = {}
        var_offsets = {}
        result = evaluate_expression(expr, var_offsets)
        self.assertEqual(result, "")

    def test_unknown_type(self):
        """Test expression with unknown type."""
        expr = {"type": "UNKNOWN"}
        var_offsets = {}
        result = evaluate_expression(expr, var_offsets)
        self.assertEqual(result, "")

    def test_binop_unknown_op(self):
        """Test binary operator with unknown op."""
        expr = {
            "type": "BINOP",
            "op": "^",
            "left": {"type": "LITERAL", "value": 1},
            "right": {"type": "LITERAL", "value": 2}
        }
        var_offsets = {}
        result = evaluate_expression(expr, var_offsets)
        self.assertEqual(result, "")

    def test_var_offsets_not_modified(self):
        """Test that var_offsets is not modified."""
        expr = {"type": "IDENT", "name": "x"}
        var_offsets = {"x": 4, "y": 8}
        original = dict(var_offsets)
        evaluate_expression(expr, var_offsets)
        self.assertEqual(var_offsets, original)

    def test_none_var_offsets(self):
        """Test with None as var_offsets (should handle gracefully)."""
        expr = {"type": "LITERAL", "value": 5}
        var_offsets = None
        with self.assertRaises((AttributeError, TypeError)):
            evaluate_expression(expr, var_offsets)


class TestEvaluateExpressionIntegration(unittest.TestCase):
    """Integration tests for realistic expression scenarios."""

    def test_variable_increment_pattern(self):
        """Test pattern: x = x + 1."""
        expr = {
            "type": "BINOP",
            "op": "+",
            "left": {"type": "IDENT", "name": "x"},
            "right": {"type": "LITERAL", "value": 1}
        }
        var_offsets = {"x": 0}
        result = evaluate_expression(expr, var_offsets)
        self.assertIn("ldr r0, [sp, #0]", result)
        self.assertIn("mov r0, #1", result)
        self.assertIn("add r0, r1, r0", result)

    def test_comparison_for_if_statement(self):
        """Test comparison typical for if condition: x > 0."""
        expr = {
            "type": "BINOP",
            "op": ">",
            "left": {"type": "IDENT", "name": "x"},
            "right": {"type": "LITERAL", "value": 0}
        }
        var_offsets = {"x": 4}
        result = evaluate_expression(expr, var_offsets)
        self.assertIn("ldr r0, [sp, #4]", result)
        self.assertIn("mov r0, #0", result)
        self.assertIn("cmp r1, r0", result)
        self.assertIn("movgt r0, #1", result)

    def test_logical_and_chain(self):
        """Test logical AND: (a > 0) && (b > 0)."""
        expr = {
            "type": "BINOP",
            "op": "&&",
            "left": {
                "type": "BINOP",
                "op": ">",
                "left": {"type": "IDENT", "name": "a"},
                "right": {"type": "LITERAL", "value": 0}
            },
            "right": {
                "type": "BINOP",
                "op": ">",
                "left": {"type": "IDENT", "name": "b"},
                "right": {"type": "LITERAL", "value": 0}
            }
        }
        var_offsets = {"a": 0, "b": 4}
        result = evaluate_expression(expr, var_offsets)
        self.assertIn("and r0, r0, r1", result)

    def test_negate_variable(self):
        """Test negation: -x."""
        expr = {
            "type": "UNOP",
            "op": "-",
            "operand": {"type": "IDENT", "name": "x"}
        }
        var_offsets = {"x": 12}
        result = evaluate_expression(expr, var_offsets)
        self.assertEqual(result, "ldr r0, [sp, #12]\n    rsb r0, r0, #0")


if __name__ == "__main__":
    unittest.main()
