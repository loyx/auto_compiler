# -*- coding: utf-8 -*-
"""Unit tests for generate_expression_code function."""

import unittest

from .generate_expression_code_src import generate_expression_code


class TestGenerateExpressionCode(unittest.TestCase):
    """Test cases for generate_expression_code function."""

    def test_var_expression(self):
        """Test VAR type expression - loads variable from stack."""
        expr = {"type": "VAR", "var_name": "x"}
        var_offsets = {"x": 8}
        code, next_offset = generate_expression_code(expr, var_offsets, 0)
        
        self.assertEqual(code, "ldr x0, [sp, #8]")
        self.assertEqual(next_offset, 0)

    def test_var_expression_different_offset(self):
        """Test VAR type with different offset."""
        expr = {"type": "VAR", "var_name": "y"}
        var_offsets = {"y": 16}
        code, next_offset = generate_expression_code(expr, var_offsets, 0)
        
        self.assertEqual(code, "ldr x0, [sp, #16]")
        self.assertEqual(next_offset, 0)

    def test_const_small_value(self):
        """Test CONST type with small value (0-65535) - uses movz only."""
        expr = {"type": "CONST", "value": 100}
        code, next_offset = generate_expression_code(expr, {}, 0)
        
        self.assertEqual(code, "movz x0, #100")
        self.assertEqual(next_offset, 0)

    def test_const_zero(self):
        """Test CONST type with value 0."""
        expr = {"type": "CONST", "value": 0}
        code, next_offset = generate_expression_code(expr, {}, 0)
        
        self.assertEqual(code, "movz x0, #0")
        self.assertEqual(next_offset, 0)

    def test_const_max_small(self):
        """Test CONST type with max small value (65535)."""
        expr = {"type": "CONST", "value": 65535}
        code, next_offset = generate_expression_code(expr, {}, 0)
        
        self.assertEqual(code, "movz x0, #65535")
        self.assertEqual(next_offset, 0)

    def test_const_large_value(self):
        """Test CONST type with large value (>65535) - uses movz+movk."""
        expr = {"type": "CONST", "value": 100000}
        code, next_offset = generate_expression_code(expr, {}, 0)
        
        # 100000 = 0x186A0, low16 = 0x86A0 (34464), high16 = 0x1 (1)
        expected = "movz x0, #34464\nmovk x0, #1, lsl #16"
        self.assertEqual(code, expected)
        self.assertEqual(next_offset, 0)

    def test_const_very_large_value(self):
        """Test CONST type with very large value."""
        expr = {"type": "CONST", "value": 0x12345678}
        code, next_offset = generate_expression_code(expr, {}, 0)
        
        # 0x12345678: low16 = 0x5678 (22136), high16 = 0x1234 (4660)
        expected = "movz x0, #22136\nmovk x0, #4660, lsl #16"
        self.assertEqual(code, expected)
        self.assertEqual(next_offset, 0)

    def test_unop_negation(self):
        """Test UNOP type with negation operator."""
        expr = {"type": "UNOP", "op": "-", "operand": {"type": "CONST", "value": 5}}
        code, next_offset = generate_expression_code(expr, {}, 0)
        
        expected = "movz x0, #5\nneg x0, x0"
        self.assertEqual(code, expected)
        self.assertEqual(next_offset, 0)

    def test_unop_nested(self):
        """Test UNOP with nested expression."""
        expr = {
            "type": "UNOP",
            "op": "-",
            "operand": {"type": "VAR", "var_name": "a"}
        }
        var_offsets = {"a": 8}
        code, next_offset = generate_expression_code(expr, var_offsets, 0)
        
        expected = "ldr x0, [sp, #8]\nneg x0, x0"
        self.assertEqual(code, expected)
        self.assertEqual(next_offset, 0)

    def test_binop_add(self):
        """Test BINOP type with addition."""
        expr = {
            "type": "BINOP",
            "op": "+",
            "left": {"type": "CONST", "value": 10},
            "right": {"type": "CONST", "value": 20}
        }
        code, next_offset = generate_expression_code(expr, {}, 0)
        
        expected = "movz x0, #10\nmov x1, x0\nmovz x0, #20\nadd x0, x1, x0"
        self.assertEqual(code, expected)
        self.assertEqual(next_offset, 0)

    def test_binop_sub(self):
        """Test BINOP type with subtraction."""
        expr = {
            "type": "BINOP",
            "op": "-",
            "left": {"type": "CONST", "value": 30},
            "right": {"type": "CONST", "value": 10}
        }
        code, next_offset = generate_expression_code(expr, {}, 0)
        
        expected = "movz x0, #30\nmov x1, x0\nmovz x0, #10\nsub x0, x1, x0"
        self.assertEqual(code, expected)
        self.assertEqual(next_offset, 0)

    def test_binop_mul(self):
        """Test BINOP type with multiplication."""
        expr = {
            "type": "BINOP",
            "op": "*",
            "left": {"type": "CONST", "value": 5},
            "right": {"type": "CONST", "value": 6}
        }
        code, next_offset = generate_expression_code(expr, {}, 0)
        
        expected = "movz x0, #5\nmov x1, x0\nmovz x0, #6\nmul x0, x1, x0"
        self.assertEqual(code, expected)
        self.assertEqual(next_offset, 0)

    def test_binop_div(self):
        """Test BINOP type with division."""
        expr = {
            "type": "BINOP",
            "op": "/",
            "left": {"type": "CONST", "value": 100},
            "right": {"type": "CONST", "value": 4}
        }
        code, next_offset = generate_expression_code(expr, {}, 0)
        
        expected = "movz x0, #100\nmov x1, x0\nmovz x0, #4\nsdiv x0, x1, x0"
        self.assertEqual(code, expected)
        self.assertEqual(next_offset, 0)

    def test_binop_bitwise_and(self):
        """Test BINOP type with bitwise AND."""
        expr = {
            "type": "BINOP",
            "op": "&",
            "left": {"type": "CONST", "value": 15},
            "right": {"type": "CONST", "value": 7}
        }
        code, next_offset = generate_expression_code(expr, {}, 0)
        
        expected = "movz x0, #15\nmov x1, x0\nmovz x0, #7\nand x0, x1, x0"
        self.assertEqual(code, expected)
        self.assertEqual(next_offset, 0)

    def test_binop_bitwise_or(self):
        """Test BINOP type with bitwise OR."""
        expr = {
            "type": "BINOP",
            "op": "|",
            "left": {"type": "CONST", "value": 8},
            "right": {"type": "CONST", "value": 4}
        }
        code, next_offset = generate_expression_code(expr, {}, 0)
        
        expected = "movz x0, #8\nmov x1, x0\nmovz x0, #4\norr x0, x1, x0"
        self.assertEqual(code, expected)
        self.assertEqual(next_offset, 0)

    def test_binop_bitwise_xor(self):
        """Test BINOP type with bitwise XOR."""
        expr = {
            "type": "BINOP",
            "op": "^",
            "left": {"type": "CONST", "value": 12},
            "right": {"type": "CONST", "value": 5}
        }
        code, next_offset = generate_expression_code(expr, {}, 0)
        
        expected = "movz x0, #12\nmov x1, x0\nmovz x0, #5\neor x0, x1, x0"
        self.assertEqual(code, expected)
        self.assertEqual(next_offset, 0)

    def test_binop_eq(self):
        """Test BINOP type with equality comparison."""
        expr = {
            "type": "BINOP",
            "op": "==",
            "left": {"type": "VAR", "var_name": "a"},
            "right": {"type": "CONST", "value": 0}
        }
        var_offsets = {"a": 8}
        code, next_offset = generate_expression_code(expr, var_offsets, 0)
        
        expected = "ldr x0, [sp, #8]\nmov x1, x0\nmovz x0, #0\ncmp x1, x0\ncset x0, eq"
        self.assertEqual(code, expected)
        self.assertEqual(next_offset, 0)

    def test_binop_ne(self):
        """Test BINOP type with not-equal comparison."""
        expr = {
            "type": "BINOP",
            "op": "!=",
            "left": {"type": "VAR", "var_name": "x"},
            "right": {"type": "VAR", "var_name": "y"}
        }
        var_offsets = {"x": 8, "y": 16}
        code, next_offset = generate_expression_code(expr, var_offsets, 0)
        
        expected = "ldr x0, [sp, #8]\nmov x1, x0\nldr x0, [sp, #16]\ncmp x1, x0\ncset x0, ne"
        self.assertEqual(code, expected)
        self.assertEqual(next_offset, 0)

    def test_binop_lt(self):
        """Test BINOP type with less-than comparison."""
        expr = {
            "type": "BINOP",
            "op": "<",
            "left": {"type": "CONST", "value": 5},
            "right": {"type": "CONST", "value": 10}
        }
        code, next_offset = generate_expression_code(expr, {}, 0)
        
        expected = "movz x0, #5\nmov x1, x0\nmovz x0, #10\ncmp x1, x0\ncset x0, lt"
        self.assertEqual(code, expected)
        self.assertEqual(next_offset, 0)

    def test_binop_gt(self):
        """Test BINOP type with greater-than comparison."""
        expr = {
            "type": "BINOP",
            "op": ">",
            "left": {"type": "CONST", "value": 10},
            "right": {"type": "CONST", "value": 5}
        }
        code, next_offset = generate_expression_code(expr, {}, 0)
        
        expected = "movz x0, #10\nmov x1, x0\nmovz x0, #5\ncmp x1, x0\ncset x0, gt"
        self.assertEqual(code, expected)
        self.assertEqual(next_offset, 0)

    def test_binop_le(self):
        """Test BINOP type with less-than-or-equal comparison."""
        expr = {
            "type": "BINOP",
            "op": "<=",
            "left": {"type": "CONST", "value": 5},
            "right": {"type": "CONST", "value": 5}
        }
        code, next_offset = generate_expression_code(expr, {}, 0)
        
        expected = "movz x0, #5\nmov x1, x0\nmovz x0, #5\ncmp x1, x0\ncset x0, le"
        self.assertEqual(code, expected)
        self.assertEqual(next_offset, 0)

    def test_binop_ge(self):
        """Test BINOP type with greater-than-or-equal comparison."""
        expr = {
            "type": "BINOP",
            "op": ">=",
            "left": {"type": "CONST", "value": 10},
            "right": {"type": "CONST", "value": 10}
        }
        code, next_offset = generate_expression_code(expr, {}, 0)
        
        expected = "movz x0, #10\nmov x1, x0\nmovz x0, #10\ncmp x1, x0\ncset x0, ge"
        self.assertEqual(code, expected)
        self.assertEqual(next_offset, 0)

    def test_nested_binop(self):
        """Test nested BINOP expressions."""
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
        code, next_offset = generate_expression_code(expr, {}, 0)
        
        # Left: 2*3, Right: 4, then add
        expected = "movz x0, #2\nmov x1, x0\nmovz x0, #3\nmul x0, x1, x0\nmov x1, x0\nmovz x0, #4\nadd x0, x1, x0"
        self.assertEqual(code, expected)
        self.assertEqual(next_offset, 0)

    def test_complex_expression(self):
        """Test complex nested expression with VAR, CONST, BINOP, UNOP."""
        expr = {
            "type": "BINOP",
            "op": "+",
            "left": {
                "type": "UNOP",
                "op": "-",
                "operand": {"type": "VAR", "var_name": "x"}
            },
            "right": {"type": "CONST", "value": 10}
        }
        var_offsets = {"x": 8}
        code, next_offset = generate_expression_code(expr, var_offsets, 0)
        
        expected = "ldr x0, [sp, #8]\nneg x0, x0\nmov x1, x0\nmovz x0, #10\nadd x0, x1, x0"
        self.assertEqual(code, expected)
        self.assertEqual(next_offset, 0)

    def test_unknown_expression_type(self):
        """Test that unknown expression type raises ValueError."""
        expr = {"type": "UNKNOWN", "value": 42}
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, {}, 0)
        
        self.assertIn("Unknown expression type: UNKNOWN", str(context.exception))

    def test_next_offset_unchanged(self):
        """Test that next_offset is always returned unchanged."""
        expr = {"type": "CONST", "value": 100}
        code, next_offset = generate_expression_code(expr, {}, 999)
        
        self.assertEqual(next_offset, 999)

    def test_var_not_in_offsets(self):
        """Test that missing variable raises KeyError."""
        expr = {"type": "VAR", "var_name": "missing_var"}
        var_offsets = {"other": 8}
        
        with self.assertRaises(KeyError):
            generate_expression_code(expr, var_offsets, 0)


if __name__ == "__main__":
    unittest.main()
