import unittest
from typing import Dict

from generate_expression_code_src import generate_expression_code


class TestGenerateExpressionCode(unittest.TestCase):
    """Test cases for generate_expression_code function."""

    def test_literal_expression(self):
        """Test literal expression generates mov instruction."""
        expr = {"type": "literal", "value": 42}
        var_offsets: Dict[str, int] = {}
        code, next_offset = generate_expression_code(expr, var_offsets, 0)
        
        self.assertEqual(code, "mov x0, #42\n")
        self.assertEqual(next_offset, 0)

    def test_literal_negative_value(self):
        """Test literal expression with negative value."""
        expr = {"type": "literal", "value": -100}
        var_offsets: Dict[str, int] = {}
        code, next_offset = generate_expression_code(expr, var_offsets, 0)
        
        self.assertEqual(code, "mov x0, #-100\n")
        self.assertEqual(next_offset, 0)

    def test_literal_zero(self):
        """Test literal expression with zero value."""
        expr = {"type": "literal", "value": 0}
        var_offsets: Dict[str, int] = {}
        code, next_offset = generate_expression_code(expr, var_offsets, 0)
        
        self.assertEqual(code, "mov x0, #0\n")
        self.assertEqual(next_offset, 0)

    def test_variable_expression_defined(self):
        """Test variable expression with defined variable."""
        expr = {"type": "variable", "name": "x"}
        var_offsets = {"x": 8}
        code, next_offset = generate_expression_code(expr, var_offsets, 0)
        
        self.assertEqual(code, "ldr x0, [sp, #8]\n")
        self.assertEqual(next_offset, 0)

    def test_variable_expression_zero_offset(self):
        """Test variable expression with zero offset."""
        expr = {"type": "variable", "name": "y"}
        var_offsets = {"y": 0}
        code, next_offset = generate_expression_code(expr, var_offsets, 0)
        
        self.assertEqual(code, "ldr x0, [sp, #0]\n")
        self.assertEqual(next_offset, 0)

    def test_variable_expression_undefined(self):
        """Test variable expression raises KeyError for undefined variable."""
        expr = {"type": "variable", "name": "undefined_var"}
        var_offsets: Dict[str, int] = {}
        
        with self.assertRaises(KeyError) as context:
            generate_expression_code(expr, var_offsets, 0)
        
        self.assertIn("undefined_var", str(context.exception))

    def test_binary_op_add(self):
        """Test binary operation with add operator."""
        expr = {
            "type": "binary_op",
            "op": "add",
            "left": {"type": "literal", "value": 5},
            "right": {"type": "literal", "value": 3}
        }
        var_offsets: Dict[str, int] = {}
        code, next_offset = generate_expression_code(expr, var_offsets, 0)
        
        expected = (
            "mov x0, #5\n"
            "str x0, [sp, #0]\n"
            "mov x0, #3\n"
            "mov x1, x0\n"
            "ldr x0, [sp, #0]\n"
            "add x0, x0, x1\n"
        )
        self.assertEqual(code, expected)
        self.assertEqual(next_offset, 0)

    def test_binary_op_sub(self):
        """Test binary operation with sub operator."""
        expr = {
            "type": "binary_op",
            "op": "sub",
            "left": {"type": "literal", "value": 10},
            "right": {"type": "literal", "value": 4}
        }
        var_offsets: Dict[str, int] = {}
        code, next_offset = generate_expression_code(expr, var_offsets, 0)
        
        self.assertIn("sub x0, x0, x1\n", code)

    def test_binary_op_mul(self):
        """Test binary operation with mul operator."""
        expr = {
            "type": "binary_op",
            "op": "mul",
            "left": {"type": "literal", "value": 6},
            "right": {"type": "literal", "value": 7}
        }
        var_offsets: Dict[str, int] = {}
        code, next_offset = generate_expression_code(expr, var_offsets, 0)
        
        self.assertIn("mul x0, x0, x1\n", code)

    def test_binary_op_div(self):
        """Test binary operation with div operator (maps to sdiv)."""
        expr = {
            "type": "binary_op",
            "op": "div",
            "left": {"type": "literal", "value": 20},
            "right": {"type": "literal", "value": 4}
        }
        var_offsets: Dict[str, int] = {}
        code, next_offset = generate_expression_code(expr, var_offsets, 0)
        
        self.assertIn("sdiv x0, x0, x1\n", code)

    def test_binary_op_unsupported_operator(self):
        """Test binary operation raises ValueError for unsupported operator."""
        expr = {
            "type": "binary_op",
            "op": "mod",
            "left": {"type": "literal", "value": 10},
            "right": {"type": "literal", "value": 3}
        }
        var_offsets: Dict[str, int] = {}
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, var_offsets, 0)
        
        self.assertIn("mod", str(context.exception))

    def test_unsupported_expression_type(self):
        """Test raises ValueError for unsupported expression type."""
        expr = {"type": "unknown_type"}
        var_offsets: Dict[str, int] = {}
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, var_offsets, 0)
        
        self.assertIn("unknown_type", str(context.exception))

    def test_nested_binary_operations(self):
        """Test nested binary operations (a + b) * c."""
        expr = {
            "type": "binary_op",
            "op": "mul",
            "left": {
                "type": "binary_op",
                "op": "add",
                "left": {"type": "literal", "value": 2},
                "right": {"type": "literal", "value": 3}
            },
            "right": {"type": "literal", "value": 4}
        }
        var_offsets: Dict[str, int] = {}
        code, next_offset = generate_expression_code(expr, var_offsets, 0)
        
        # Should contain both add and mul operations
        self.assertIn("add x0, x0, x1\n", code)
        self.assertIn("mul x0, x0, x1\n", code)
        # Stack should be reclaimed
        self.assertEqual(next_offset, 0)

    def test_variable_in_binary_op(self):
        """Test binary operation with variable operand."""
        expr = {
            "type": "binary_op",
            "op": "add",
            "left": {"type": "variable", "name": "x"},
            "right": {"type": "literal", "value": 10}
        }
        var_offsets = {"x": 16}
        code, next_offset = generate_expression_code(expr, var_offsets, 0)
        
        self.assertIn("ldr x0, [sp, #16]\n", code)
        self.assertIn("add x0, x0, x1\n", code)

    def test_next_offset_increments_during_binary_op(self):
        """Test that next_offset increments when storing intermediate results."""
        expr = {
            "type": "binary_op",
            "op": "add",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 2}
        }
        var_offsets: Dict[str, int] = {}
        
        # During execution, offset should increment to 1, then decrement back to 0
        code, next_offset = generate_expression_code(expr, var_offsets, 0)
        
        # Final offset should be 0 (reclaimed)
        self.assertEqual(next_offset, 0)
        # But stack store should use offset 0
        self.assertIn("str x0, [sp, #0]\n", code)

    def test_multiple_variables_different_offsets(self):
        """Test expression with multiple variables at different offsets."""
        expr = {
            "type": "binary_op",
            "op": "sub",
            "left": {"type": "variable", "name": "a"},
            "right": {"type": "variable", "name": "b"}
        }
        var_offsets = {"a": 8, "b": 16}
        code, next_offset = generate_expression_code(expr, var_offsets, 0)
        
        self.assertIn("ldr x0, [sp, #8]\n", code)
        self.assertIn("ldr x0, [sp, #16]\n", code)
        self.assertIn("sub x0, x0, x1\n", code)

    def test_complex_nested_expression(self):
        """Test complex nested expression: (a + b) * (c - d)."""
        expr = {
            "type": "binary_op",
            "op": "mul",
            "left": {
                "type": "binary_op",
                "op": "add",
                "left": {"type": "variable", "name": "a"},
                "right": {"type": "variable", "name": "b"}
            },
            "right": {
                "type": "binary_op",
                "op": "sub",
                "left": {"type": "variable", "name": "c"},
                "right": {"type": "variable", "name": "d"}
            }
        }
        var_offsets = {"a": 0, "b": 8, "c": 16, "d": 24}
        code, next_offset = generate_expression_code(expr, var_offsets, 0)
        
        # Should contain all four variable loads
        self.assertIn("ldr x0, [sp, #0]\n", code)
        self.assertIn("ldr x0, [sp, #8]\n", code)
        self.assertIn("ldr x0, [sp, #16]\n", code)
        self.assertIn("ldr x0, [sp, #24]\n", code)
        # Should contain add, sub, and mul operations
        self.assertIn("add x0, x0, x1\n", code)
        self.assertIn("sub x0, x0, x1\n", code)
        self.assertIn("mul x0, x0, x1\n", code)
        # Stack should be fully reclaimed
        self.assertEqual(next_offset, 0)


if __name__ == "__main__":
    unittest.main()
