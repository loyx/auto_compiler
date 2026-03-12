# -*- coding: utf-8 -*-
"""Unit tests for generate_expression_code function."""

import unittest

from .generate_expression_code_src import generate_expression_code


class TestGenerateExpressionCode(unittest.TestCase):
    """Test cases for generate_expression_code function."""

    def test_const_expression(self):
        """Test CONST expression type."""
        expr = {"type": "CONST", "value": 42}
        var_offsets = {}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        self.assertEqual(code, "    LOAD_CONST R0, 42\n")
        self.assertEqual(offset, 1)
        self.assertEqual(reg, "R0")

    def test_const_expression_string(self):
        """Test CONST expression with string value."""
        expr = {"type": "CONST", "value": "hello"}
        var_offsets = {}
        code, offset, reg = generate_expression_code(expr, var_offsets, 5)
        
        self.assertEqual(code, "    LOAD_CONST R5, 'hello'\n")
        self.assertEqual(offset, 6)
        self.assertEqual(reg, "R5")

    def test_const_expression_float(self):
        """Test CONST expression with float value."""
        expr = {"type": "CONST", "value": 3.14}
        var_offsets = {}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        self.assertEqual(code, "    LOAD_CONST R0, 3.14\n")
        self.assertEqual(offset, 1)
        self.assertEqual(reg, "R0")

    def test_var_expression_defined(self):
        """Test VAR expression with defined variable."""
        expr = {"type": "VAR", "var_name": "x"}
        var_offsets = {"x": 0}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        self.assertEqual(code, "    LOAD_VAR R0, [0]\n")
        self.assertEqual(offset, 1)
        self.assertEqual(reg, "R0")

    def test_var_expression_different_offset(self):
        """Test VAR expression with different variable offset."""
        expr = {"type": "VAR", "var_name": "y"}
        var_offsets = {"y": 3}
        code, offset, reg = generate_expression_code(expr, var_offsets, 2)
        
        self.assertEqual(code, "    LOAD_VAR R2, [3]\n")
        self.assertEqual(offset, 3)
        self.assertEqual(reg, "R2")

    def test_var_expression_undefined(self):
        """Test VAR expression with undefined variable raises ValueError."""
        expr = {"type": "VAR", "var_name": "undefined_var"}
        var_offsets = {"x": 0}
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, var_offsets, 0)
        
        self.assertIn("Undefined variable: undefined_var", str(context.exception))

    def test_binop_add(self):
        """Test BINOP expression with addition."""
        expr = {
            "type": "BINOP",
            "op": "+",
            "left": {"type": "CONST", "value": 1},
            "right": {"type": "CONST", "value": 2}
        }
        var_offsets = {}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        expected = (
            "    LOAD_CONST R0, 1\n"
            "    LOAD_CONST R1, 2\n"
            "    ADD R2, R0, R1\n"
        )
        self.assertEqual(code, expected)
        self.assertEqual(offset, 3)
        self.assertEqual(reg, "R2")

    def test_binop_sub(self):
        """Test BINOP expression with subtraction."""
        expr = {
            "type": "BINOP",
            "op": "-",
            "left": {"type": "CONST", "value": 10},
            "right": {"type": "CONST", "value": 3}
        }
        var_offsets = {}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        expected = (
            "    LOAD_CONST R0, 10\n"
            "    LOAD_CONST R1, 3\n"
            "    SUB R2, R0, R1\n"
        )
        self.assertEqual(code, expected)
        self.assertEqual(offset, 3)
        self.assertEqual(reg, "R2")

    def test_binop_mul(self):
        """Test BINOP expression with multiplication."""
        expr = {
            "type": "BINOP",
            "op": "*",
            "left": {"type": "CONST", "value": 4},
            "right": {"type": "CONST", "value": 5}
        }
        var_offsets = {}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        expected = (
            "    LOAD_CONST R0, 4\n"
            "    LOAD_CONST R1, 5\n"
            "    MUL R2, R0, R1\n"
        )
        self.assertEqual(code, expected)
        self.assertEqual(offset, 3)
        self.assertEqual(reg, "R2")

    def test_binop_div(self):
        """Test BINOP expression with division."""
        expr = {
            "type": "BINOP",
            "op": "/",
            "left": {"type": "CONST", "value": 20},
            "right": {"type": "CONST", "value": 4}
        }
        var_offsets = {}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        expected = (
            "    LOAD_CONST R0, 20\n"
            "    LOAD_CONST R1, 4\n"
            "    DIV R2, R0, R1\n"
        )
        self.assertEqual(code, expected)
        self.assertEqual(offset, 3)
        self.assertEqual(reg, "R2")

    def test_binop_comparison_eq(self):
        """Test BINOP expression with equality comparison."""
        expr = {
            "type": "BINOP",
            "op": "==",
            "left": {"type": "VAR", "var_name": "a"},
            "right": {"type": "CONST", "value": 0}
        }
        var_offsets = {"a": 0}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        expected = (
            "    LOAD_VAR R0, [0]\n"
            "    LOAD_CONST R1, 0\n"
            "    EQ R2, R0, R1\n"
        )
        self.assertEqual(code, expected)
        self.assertEqual(offset, 3)
        self.assertEqual(reg, "R2")

    def test_binop_comparison_ne(self):
        """Test BINOP expression with not-equal comparison."""
        expr = {
            "type": "BINOP",
            "op": "!=",
            "left": {"type": "VAR", "var_name": "x"},
            "right": {"type": "VAR", "var_name": "y"}
        }
        var_offsets = {"x": 0, "y": 1}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        expected = (
            "    LOAD_VAR R0, [0]\n"
            "    LOAD_VAR R1, [1]\n"
            "    NE R2, R0, R1\n"
        )
        self.assertEqual(code, expected)
        self.assertEqual(offset, 3)
        self.assertEqual(reg, "R2")

    def test_binop_comparison_lt(self):
        """Test BINOP expression with less-than comparison."""
        expr = {
            "type": "BINOP",
            "op": "<",
            "left": {"type": "CONST", "value": 5},
            "right": {"type": "CONST", "value": 10}
        }
        var_offsets = {}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        expected = (
            "    LOAD_CONST R0, 5\n"
            "    LOAD_CONST R1, 10\n"
            "    LT R2, R0, R1\n"
        )
        self.assertEqual(code, expected)
        self.assertEqual(offset, 3)
        self.assertEqual(reg, "R2")

    def test_binop_comparison_gt(self):
        """Test BINOP expression with greater-than comparison."""
        expr = {
            "type": "BINOP",
            "op": ">",
            "left": {"type": "CONST", "value": 10},
            "right": {"type": "CONST", "value": 5}
        }
        var_offsets = {}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        expected = (
            "    LOAD_CONST R0, 10\n"
            "    LOAD_CONST R1, 5\n"
            "    GT R2, R0, R1\n"
        )
        self.assertEqual(code, expected)
        self.assertEqual(offset, 3)
        self.assertEqual(reg, "R2")

    def test_binop_comparison_le(self):
        """Test BINOP expression with less-than-or-equal comparison."""
        expr = {
            "type": "BINOP",
            "op": "<=",
            "left": {"type": "CONST", "value": 5},
            "right": {"type": "CONST", "value": 5}
        }
        var_offsets = {}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        expected = (
            "    LOAD_CONST R0, 5\n"
            "    LOAD_CONST R1, 5\n"
            "    LE R2, R0, R1\n"
        )
        self.assertEqual(code, expected)
        self.assertEqual(offset, 3)
        self.assertEqual(reg, "R2")

    def test_binop_comparison_ge(self):
        """Test BINOP expression with greater-than-or-equal comparison."""
        expr = {
            "type": "BINOP",
            "op": ">=",
            "left": {"type": "CONST", "value": 10},
            "right": {"type": "CONST", "value": 5}
        }
        var_offsets = {}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        expected = (
            "    LOAD_CONST R0, 10\n"
            "    LOAD_CONST R1, 5\n"
            "    GE R2, R0, R1\n"
        )
        self.assertEqual(code, expected)
        self.assertEqual(offset, 3)
        self.assertEqual(reg, "R2")

    def test_binop_logical_and(self):
        """Test BINOP expression with logical AND."""
        expr = {
            "type": "BINOP",
            "op": "and",
            "left": {"type": "VAR", "var_name": "a"},
            "right": {"type": "VAR", "var_name": "b"}
        }
        var_offsets = {"a": 0, "b": 1}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        expected = (
            "    LOAD_VAR R0, [0]\n"
            "    LOAD_VAR R1, [1]\n"
            "    AND R2, R0, R1\n"
        )
        self.assertEqual(code, expected)
        self.assertEqual(offset, 3)
        self.assertEqual(reg, "R2")

    def test_binop_logical_or(self):
        """Test BINOP expression with logical OR."""
        expr = {
            "type": "BINOP",
            "op": "or",
            "left": {"type": "VAR", "var_name": "x"},
            "right": {"type": "CONST", "value": True}
        }
        var_offsets = {"x": 0}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        expected = (
            "    LOAD_VAR R0, [0]\n"
            "    LOAD_CONST R1, True\n"
            "    OR R2, R0, R1\n"
        )
        self.assertEqual(code, expected)
        self.assertEqual(offset, 3)
        self.assertEqual(reg, "R2")

    def test_binop_unknown_operator(self):
        """Test BINOP expression with unknown operator raises ValueError."""
        expr = {
            "type": "BINOP",
            "op": "**",
            "left": {"type": "CONST", "value": 2},
            "right": {"type": "CONST", "value": 3}
        }
        var_offsets = {}
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, var_offsets, 0)
        
        self.assertIn("Unknown binary operator: **", str(context.exception))

    def test_binop_nested(self):
        """Test nested BINOP expression."""
        expr = {
            "type": "BINOP",
            "op": "+",
            "left": {
                "type": "BINOP",
                "op": "*",
                "left": {"type": "CONST", "value": 2},
                "right": {"type": "CONST", "value": 3}
            },
            "right": {"type": "CONST", "value": 4}
        }
        var_offsets = {}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        expected = (
            "    LOAD_CONST R0, 2\n"
            "    LOAD_CONST R1, 3\n"
            "    MUL R2, R0, R1\n"
            "    LOAD_CONST R3, 4\n"
            "    ADD R4, R2, R3\n"
        )
        self.assertEqual(code, expected)
        self.assertEqual(offset, 5)
        self.assertEqual(reg, "R4")

    def test_unop_neg(self):
        """Test UNOP expression with negation."""
        expr = {
            "type": "UNOP",
            "op": "-",
            "operand": {"type": "CONST", "value": 5}
        }
        var_offsets = {}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        expected = (
            "    LOAD_CONST R0, 5\n"
            "    NEG R1, R0\n"
        )
        self.assertEqual(code, expected)
        self.assertEqual(offset, 2)
        self.assertEqual(reg, "R1")

    def test_unop_not(self):
        """Test UNOP expression with logical NOT."""
        expr = {
            "type": "UNOP",
            "op": "not",
            "operand": {"type": "VAR", "var_name": "flag"}
        }
        var_offsets = {"flag": 0}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        expected = (
            "    LOAD_VAR R0, [0]\n"
            "    NOT R1, R0\n"
        )
        self.assertEqual(code, expected)
        self.assertEqual(offset, 2)
        self.assertEqual(reg, "R1")

    def test_unop_unknown_operator(self):
        """Test UNOP expression with unknown operator raises ValueError."""
        expr = {
            "type": "UNOP",
            "op": "~",
            "operand": {"type": "CONST", "value": 5}
        }
        var_offsets = {}
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, var_offsets, 0)
        
        self.assertIn("Unknown unary operator: ~", str(context.exception))

    def test_unop_nested(self):
        """Test nested UNOP expression."""
        expr = {
            "type": "UNOP",
            "op": "-",
            "operand": {
                "type": "UNOP",
                "op": "-",
                "operand": {"type": "CONST", "value": 10}
            }
        }
        var_offsets = {}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        expected = (
            "    LOAD_CONST R0, 10\n"
            "    NEG R1, R0\n"
            "    NEG R2, R1\n"
        )
        self.assertEqual(code, expected)
        self.assertEqual(offset, 3)
        self.assertEqual(reg, "R2")

    def test_call_no_args(self):
        """Test CALL expression with no arguments."""
        expr = {
            "type": "CALL",
            "func_name": "print",
            "args": []
        }
        var_offsets = {}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        expected = "    CALL R0, print, 0, \n"
        self.assertEqual(code, expected)
        self.assertEqual(offset, 1)
        self.assertEqual(reg, "R0")

    def test_call_single_arg(self):
        """Test CALL expression with single argument."""
        expr = {
            "type": "CALL",
            "func_name": "len",
            "args": [{"type": "CONST", "value": [1, 2, 3]}]
        }
        var_offsets = {}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        expected = (
            "    LOAD_CONST R0, [1, 2, 3]\n"
            "    CALL R1, len, 1, R0\n"
        )
        self.assertEqual(code, expected)
        self.assertEqual(offset, 2)
        self.assertEqual(reg, "R1")

    def test_call_multiple_args(self):
        """Test CALL expression with multiple arguments."""
        expr = {
            "type": "CALL",
            "func_name": "max",
            "args": [
                {"type": "CONST", "value": 1},
                {"type": "CONST", "value": 2},
                {"type": "CONST", "value": 3}
            ]
        }
        var_offsets = {}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        expected = (
            "    LOAD_CONST R0, 1\n"
            "    LOAD_CONST R1, 2\n"
            "    LOAD_CONST R2, 3\n"
            "    CALL R3, max, 3, R0, R1, R2\n"
        )
        self.assertEqual(code, expected)
        self.assertEqual(offset, 4)
        self.assertEqual(reg, "R3")

    def test_call_with_var_args(self):
        """Test CALL expression with variable arguments."""
        expr = {
            "type": "CALL",
            "func_name": "add",
            "args": [
                {"type": "VAR", "var_name": "x"},
                {"type": "VAR", "var_name": "y"}
            ]
        }
        var_offsets = {"x": 0, "y": 1}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        expected = (
            "    LOAD_VAR R0, [0]\n"
            "    LOAD_VAR R1, [1]\n"
            "    CALL R2, add, 2, R0, R1\n"
        )
        self.assertEqual(code, expected)
        self.assertEqual(offset, 3)
        self.assertEqual(reg, "R2")

    def test_call_nested_expression(self):
        """Test CALL expression with nested expression as argument."""
        expr = {
            "type": "CALL",
            "func_name": "print",
            "args": [
                {
                    "type": "BINOP",
                    "op": "+",
                    "left": {"type": "VAR", "var_name": "a"},
                    "right": {"type": "VAR", "var_name": "b"}
                }
            ]
        }
        var_offsets = {"a": 0, "b": 1}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        expected = (
            "    LOAD_VAR R0, [0]\n"
            "    LOAD_VAR R1, [1]\n"
            "    ADD R2, R0, R1\n"
            "    CALL R3, print, 1, R2\n"
        )
        self.assertEqual(code, expected)
        self.assertEqual(offset, 4)
        self.assertEqual(reg, "R3")

    def test_complex_expression(self):
        """Test complex nested expression combining multiple types."""
        expr = {
            "type": "BINOP",
            "op": ">",
            "left": {
                "type": "CALL",
                "func_name": "len",
                "args": [{"type": "VAR", "var_name": "items"}]
            },
            "right": {"type": "CONST", "value": 0}
        }
        var_offsets = {"items": 0}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        expected = (
            "    LOAD_VAR R0, [0]\n"
            "    CALL R1, len, 1, R0\n"
            "    LOAD_CONST R2, 0\n"
            "    GT R3, R1, R2\n"
        )
        self.assertEqual(code, expected)
        self.assertEqual(offset, 4)
        self.assertEqual(reg, "R3")

    def test_unknown_expression_type(self):
        """Test unknown expression type raises ValueError."""
        expr = {"type": "UNKNOWN", "value": 42}
        var_offsets = {}
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, var_offsets, 0)
        
        self.assertIn("Unknown expression type: UNKNOWN", str(context.exception))

    def test_starting_offset_not_zero(self):
        """Test that function works correctly with non-zero starting offset."""
        expr = {"type": "CONST", "value": 100}
        var_offsets = {}
        code, offset, reg = generate_expression_code(expr, var_offsets, 10)
        
        self.assertEqual(code, "    LOAD_CONST R10, 100\n")
        self.assertEqual(offset, 11)
        self.assertEqual(reg, "R10")

    def test_empty_var_offsets_with_const(self):
        """Test CONST expression with empty var_offsets."""
        expr = {"type": "CONST", "value": "test"}
        var_offsets = {}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        self.assertEqual(code, "    LOAD_CONST R0, 'test'\n")
        self.assertEqual(offset, 1)
        self.assertEqual(reg, "R0")


if __name__ == "__main__":
    unittest.main()
