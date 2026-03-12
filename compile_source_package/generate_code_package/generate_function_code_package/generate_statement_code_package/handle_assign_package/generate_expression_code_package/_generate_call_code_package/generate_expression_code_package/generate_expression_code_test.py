# === imports ===
import unittest


# === relative import of UUT ===
from .generate_expression_code_src import generate_expression_code


class TestGenerateExpressionCode(unittest.TestCase):
    """Test cases for generate_expression_code function."""

    def test_const_small_positive(self):
        """Test CONST expression with small positive value."""
        expr = {"type": "CONST", "value": 42}
        result = generate_expression_code(expr, "main", {})
        self.assertEqual(result, "mov x0, #42")

    def test_const_small_negative(self):
        """Test CONST expression with small negative value."""
        expr = {"type": "CONST", "value": -100}
        result = generate_expression_code(expr, "main", {})
        self.assertEqual(result, "mov x0, #-100")

    def test_const_boundary_min(self):
        """Test CONST expression at minimum boundary (-4096)."""
        expr = {"type": "CONST", "value": -4096}
        result = generate_expression_code(expr, "main", {})
        self.assertEqual(result, "mov x0, #-4096")

    def test_const_boundary_max(self):
        """Test CONST expression at maximum boundary (4095)."""
        expr = {"type": "CONST", "value": 4095}
        result = generate_expression_code(expr, "main", {})
        self.assertEqual(result, "mov x0, #4095")

    def test_const_large_value_high_zero(self):
        """Test CONST expression with large value where high 16 bits are zero."""
        expr = {"type": "CONST", "value": 0x0000FFFF}
        result = generate_expression_code(expr, "main", {})
        self.assertEqual(result, "movz x0, #65535")

    def test_const_large_value_both_parts(self):
        """Test CONST expression with large value requiring movz and movk."""
        expr = {"type": "CONST", "value": 0x12345678}
        result = generate_expression_code(expr, "main", {})
        expected = "movz x0, #4660, lsl #16\nmovk x0, #22136"
        self.assertEqual(result, expected)

    def test_var_simple(self):
        """Test VAR expression with simple variable."""
        expr = {"type": "VAR", "var_name": "x"}
        var_offsets = {"x": 16}
        result = generate_expression_code(expr, "main", var_offsets)
        self.assertEqual(result, "ldr x0, [sp, #16]")

    def test_var_zero_offset(self):
        """Test VAR expression with zero offset."""
        expr = {"type": "VAR", "var_name": "y"}
        var_offsets = {"y": 0}
        result = generate_expression_code(expr, "main", var_offsets)
        self.assertEqual(result, "ldr x0, [sp, #0]")

    def test_binop_add(self):
        """Test BINOP expression with addition."""
        expr = {
            "type": "BINOP",
            "op": "+",
            "left": {"type": "CONST", "value": 5},
            "right": {"type": "CONST", "value": 3}
        }
        result = generate_expression_code(expr, "main", {})
        expected = "mov x0, #5\nmov x9, x0\nmov x0, #3\nadd x0, x9, x0"
        self.assertEqual(result, expected)

    def test_binop_sub(self):
        """Test BINOP expression with subtraction."""
        expr = {
            "type": "BINOP",
            "op": "-",
            "left": {"type": "CONST", "value": 10},
            "right": {"type": "CONST", "value": 4}
        }
        result = generate_expression_code(expr, "main", {})
        expected = "mov x0, #10\nmov x9, x0\nmov x0, #4\nsub x0, x9, x0"
        self.assertEqual(result, expected)

    def test_binop_mul(self):
        """Test BINOP expression with multiplication."""
        expr = {
            "type": "BINOP",
            "op": "*",
            "left": {"type": "CONST", "value": 6},
            "right": {"type": "CONST", "value": 7}
        }
        result = generate_expression_code(expr, "main", {})
        expected = "mov x0, #6\nmov x9, x0\nmov x0, #7\nmul x0, x9, x0"
        self.assertEqual(result, expected)

    def test_binop_div(self):
        """Test BINOP expression with division."""
        expr = {
            "type": "BINOP",
            "op": "/",
            "left": {"type": "CONST", "value": 20},
            "right": {"type": "CONST", "value": 4}
        }
        result = generate_expression_code(expr, "main", {})
        expected = "mov x0, #20\nmov x9, x0\nmov x0, #4\nsdiv x0, x9, x0"
        self.assertEqual(result, expected)

    def test_binop_mod(self):
        """Test BINOP expression with modulo."""
        expr = {
            "type": "BINOP",
            "op": "%",
            "left": {"type": "CONST", "value": 17},
            "right": {"type": "CONST", "value": 5}
        }
        result = generate_expression_code(expr, "main", {})
        expected = "mov x0, #17\nmov x9, x0\nmov x0, #5\nsdiv x10, x9, x0\nmsub x0, x10, x0, x9"
        self.assertEqual(result, expected)

    def test_binop_eq(self):
        """Test BINOP expression with equality."""
        expr = {
            "type": "BINOP",
            "op": "==",
            "left": {"type": "CONST", "value": 1},
            "right": {"type": "CONST", "value": 1}
        }
        result = generate_expression_code(expr, "main", {})
        expected = "mov x0, #1\nmov x9, x0\nmov x0, #1\ncmp x9, x0\nmov x0, #0\ncset x0, eq"
        self.assertEqual(result, expected)

    def test_binop_ne(self):
        """Test BINOP expression with not equal."""
        expr = {
            "type": "BINOP",
            "op": "!=",
            "left": {"type": "CONST", "value": 1},
            "right": {"type": "CONST", "value": 2}
        }
        result = generate_expression_code(expr, "main", {})
        expected = "mov x0, #1\nmov x9, x0\nmov x0, #2\ncmp x9, x0\nmov x0, #0\ncset x0, ne"
        self.assertEqual(result, expected)

    def test_binop_lt(self):
        """Test BINOP expression with less than."""
        expr = {
            "type": "BINOP",
            "op": "<",
            "left": {"type": "CONST", "value": 3},
            "right": {"type": "CONST", "value": 5}
        }
        result = generate_expression_code(expr, "main", {})
        expected = "mov x0, #3\nmov x9, x0\nmov x0, #5\ncmp x9, x0\nmov x0, #0\ncset x0, lt"
        self.assertEqual(result, expected)

    def test_binop_le(self):
        """Test BINOP expression with less than or equal."""
        expr = {
            "type": "BINOP",
            "op": "<=",
            "left": {"type": "CONST", "value": 5},
            "right": {"type": "CONST", "value": 5}
        }
        result = generate_expression_code(expr, "main", {})
        expected = "mov x0, #5\nmov x9, x0\nmov x0, #5\ncmp x9, x0\nmov x0, #0\ncset x0, le"
        self.assertEqual(result, expected)

    def test_binop_gt(self):
        """Test BINOP expression with greater than."""
        expr = {
            "type": "BINOP",
            "op": ">",
            "left": {"type": "CONST", "value": 10},
            "right": {"type": "CONST", "value": 5}
        }
        result = generate_expression_code(expr, "main", {})
        expected = "mov x0, #10\nmov x9, x0\nmov x0, #5\ncmp x9, x0\nmov x0, #0\ncset x0, gt"
        self.assertEqual(result, expected)

    def test_binop_ge(self):
        """Test BINOP expression with greater than or equal."""
        expr = {
            "type": "BINOP",
            "op": ">=",
            "left": {"type": "CONST", "value": 10},
            "right": {"type": "CONST", "value": 10}
        }
        result = generate_expression_code(expr, "main", {})
        expected = "mov x0, #10\nmov x9, x0\nmov x0, #10\ncmp x9, x0\nmov x0, #0\ncset x0, ge"
        self.assertEqual(result, expected)

    def test_binop_and(self):
        """Test BINOP expression with bitwise AND."""
        expr = {
            "type": "BINOP",
            "op": "&",
            "left": {"type": "CONST", "value": 0xFF},
            "right": {"type": "CONST", "value": 0x0F}
        }
        result = generate_expression_code(expr, "main", {})
        expected = "mov x0, #255\nmov x9, x0\nmov x0, #15\nand x0, x9, x0"
        self.assertEqual(result, expected)

    def test_binop_or(self):
        """Test BINOP expression with bitwise OR."""
        expr = {
            "type": "BINOP",
            "op": "|",
            "left": {"type": "CONST", "value": 0xF0},
            "right": {"type": "CONST", "value": 0x0F}
        }
        result = generate_expression_code(expr, "main", {})
        expected = "mov x0, #240\nmov x9, x0\nmov x0, #15\norr x0, x9, x0"
        self.assertEqual(result, expected)

    def test_binop_xor(self):
        """Test BINOP expression with bitwise XOR."""
        expr = {
            "type": "BINOP",
            "op": "^",
            "left": {"type": "CONST", "value": 0xFF},
            "right": {"type": "CONST", "value": 0xFF}
        }
        result = generate_expression_code(expr, "main", {})
        expected = "mov x0, #255\nmov x9, x0\nmov x0, #255\neor x0, x9, x0"
        self.assertEqual(result, expected)

    def test_binop_with_var_operands(self):
        """Test BINOP expression with variable operands."""
        expr = {
            "type": "BINOP",
            "op": "+",
            "left": {"type": "VAR", "var_name": "a"},
            "right": {"type": "VAR", "var_name": "b"}
        }
        var_offsets = {"a": 8, "b": 16}
        result = generate_expression_code(expr, "main", var_offsets)
        expected = "ldr x0, [sp, #8]\nmov x9, x0\nldr x0, [sp, #16]\nadd x0, x9, x0"
        self.assertEqual(result, expected)

    def test_call_no_args(self):
        """Test CALL expression with no arguments."""
        expr = {"type": "CALL", "name": "foo", "args": []}
        result = generate_expression_code(expr, "main", {})
        self.assertEqual(result, "bl foo")

    def test_call_one_arg(self):
        """Test CALL expression with one argument."""
        expr = {
            "type": "CALL",
            "name": "bar",
            "args": [{"type": "CONST", "value": 42}]
        }
        result = generate_expression_code(expr, "main", {})
        expected = "mov x0, #42\nbl bar"
        self.assertEqual(result, expected)

    def test_call_multiple_args(self):
        """Test CALL expression with multiple arguments."""
        expr = {
            "type": "CALL",
            "name": "baz",
            "args": [
                {"type": "CONST", "value": 1},
                {"type": "CONST", "value": 2},
                {"type": "CONST", "value": 3}
            ]
        }
        result = generate_expression_code(expr, "main", {})
        expected = "mov x0, #1\nmov x0, x0\nmov x0, #2\nmov x1, x0\nmov x0, #3\nbl baz"
        self.assertEqual(result, expected)

    def test_call_with_var_args(self):
        """Test CALL expression with variable arguments."""
        expr = {
            "type": "CALL",
            "name": "func",
            "args": [
                {"type": "VAR", "var_name": "x"},
                {"type": "VAR", "var_name": "y"}
            ]
        }
        var_offsets = {"x": 0, "y": 8}
        result = generate_expression_code(expr, "main", var_offsets)
        expected = "ldr x0, [sp, #0]\nmov x0, x0\nldr x0, [sp, #8]\nbl func"
        self.assertEqual(result, expected)

    def test_nested_binop(self):
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
        result = generate_expression_code(expr, "main", {})
        expected = "mov x0, #2\nmov x9, x0\nmov x0, #3\nmul x0, x9, x0\nmov x9, x0\nmov x0, #4\nadd x0, x9, x0"
        self.assertEqual(result, expected)

    def test_nested_call_in_binop(self):
        """Test BINOP with nested CALL expression."""
        expr = {
            "type": "BINOP",
            "op": "+",
            "left": {
                "type": "CALL",
                "name": "get_value",
                "args": []
            },
            "right": {"type": "CONST", "value": 10}
        }
        result = generate_expression_code(expr, "main", {})
        expected = "bl get_value\nmov x9, x0\nmov x0, #10\nadd x0, x9, x0"
        self.assertEqual(result, expected)

    def test_nested_binop_in_call(self):
        """Test CALL with nested BINOP argument."""
        expr = {
            "type": "CALL",
            "name": "print_value",
            "args": [
                {
                    "type": "BINOP",
                    "op": "+",
                    "left": {"type": "CONST", "value": 5},
                    "right": {"type": "CONST", "value": 5}
                }
            ]
        }
        result = generate_expression_code(expr, "main", {})
        expected = "mov x0, #5\nmov x9, x0\nmov x0, #5\nadd x0, x9, x0\nbl print_value"
        self.assertEqual(result, expected)

    def test_deeply_nested_expression(self):
        """Test deeply nested expression with multiple levels."""
        expr = {
            "type": "BINOP",
            "op": "*",
            "left": {
                "type": "BINOP",
                "op": "+",
                "left": {"type": "CONST", "value": 1},
                "right": {"type": "CONST", "value": 2}
            },
            "right": {
                "type": "BINOP",
                "op": "-",
                "left": {"type": "CONST", "value": 4},
                "right": {"type": "CONST", "value": 1}
            }
        }
        result = generate_expression_code(expr, "main", {})
        expected = "mov x0, #1\nmov x9, x0\nmov x0, #2\nadd x0, x9, x0\nmov x9, x0\nmov x0, #4\nmov x9, x0\nmov x0, #1\nsub x0, x9, x0\nmul x0, x9, x0"
        self.assertEqual(result, expected)

    def test_unknown_expression_type(self):
        """Test error handling for unknown expression type."""
        expr = {"type": "UNKNOWN", "value": 42}
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, "main", {})
        self.assertIn("Unknown expression type: UNKNOWN", str(context.exception))

    def test_unknown_binop_operator(self):
        """Test error handling for unknown binary operator."""
        expr = {
            "type": "BINOP",
            "op": "**",
            "left": {"type": "CONST", "value": 2},
            "right": {"type": "CONST", "value": 3}
        }
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, "main", {})
        self.assertIn("Unknown binary operator: **", str(context.exception))

    def test_too_many_arguments(self):
        """Test error handling for too many function arguments."""
        expr = {
            "type": "CALL",
            "name": "func",
            "args": [
                {"type": "CONST", "value": i} for i in range(9)
            ]
        }
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, "main", {})
        self.assertIn("Too many arguments", str(context.exception))

    def test_call_with_eight_args_boundary(self):
        """Test CALL expression with exactly 8 arguments (boundary)."""
        expr = {
            "type": "CALL",
            "name": "func",
            "args": [{"type": "CONST", "value": i} for i in range(8)]
        }
        result = generate_expression_code(expr, "main", {})
        # Should generate code for all 8 args without error
        self.assertIn("bl func", result)
        # Check that all 8 args are processed (x0-x7)
        for i in range(7):
            self.assertIn(f"mov x{i}, x0", result)

    def test_var_missing_from_offsets(self):
        """Test error when variable not found in var_offsets."""
        expr = {"type": "VAR", "var_name": "missing_var"}
        var_offsets = {"other_var": 8}
        with self.assertRaises(KeyError):
            generate_expression_code(expr, "main", var_offsets)

    def test_call_missing_name(self):
        """Test error when CALL expression missing name field."""
        expr = {"type": "CALL", "args": []}
        with self.assertRaises(KeyError):
            generate_expression_code(expr, "main", {})

    def test_binop_missing_op(self):
        """Test error when BINOP expression missing op field."""
        expr = {
            "type": "BINOP",
            "left": {"type": "CONST", "value": 1},
            "right": {"type": "CONST", "value": 2}
        }
        with self.assertRaises(KeyError):
            generate_expression_code(expr, "main", {})

    def test_const_missing_value(self):
        """Test error when CONST expression missing value field."""
        expr = {"type": "CONST"}
        with self.assertRaises(KeyError):
            generate_expression_code(expr, "main", {})

    def test_var_missing_var_name(self):
        """Test error when VAR expression missing var_name field."""
        expr = {"type": "VAR"}
        with self.assertRaises(KeyError):
            generate_expression_code(expr, "main", {})


if __name__ == "__main__":
    unittest.main()
