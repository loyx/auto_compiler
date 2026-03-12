# === std / third-party imports ===
import unittest

# === sub function imports ===
from .generate_expression_code_src import generate_expression_code


class TestGenerateExpressionCode(unittest.TestCase):
    """Test cases for generate_expression_code function."""

    def test_literal_positive(self):
        """Test LITERAL expression with positive value."""
        expr = {"type": "LITERAL", "value": 42}
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertEqual(code, "MOV x0, #42")
        self.assertEqual(updated_offset, 0)

    def test_literal_zero(self):
        """Test LITERAL expression with zero value."""
        expr = {"type": "LITERAL", "value": 0}
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertEqual(code, "MOV x0, #0")
        self.assertEqual(updated_offset, 0)

    def test_literal_negative(self):
        """Test LITERAL expression with negative value."""
        expr = {"type": "LITERAL", "value": -10}
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertEqual(code, "MOV x0, #-10")
        self.assertEqual(updated_offset, 0)

    def test_var_simple(self):
        """Test VAR expression with single variable."""
        expr = {"type": "VAR", "name": "x"}
        var_offsets = {"x": 16}
        next_offset = 0
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertEqual(code, "LOAD_OFFSET x0, 16")
        self.assertEqual(updated_offset, 0)

    def test_var_multiple_vars(self):
        """Test VAR expression with multiple variables in offsets."""
        expr = {"type": "VAR", "name": "y"}
        var_offsets = {"x": 0, "y": 8, "z": 16}
        next_offset = 0
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertEqual(code, "LOAD_OFFSET x0, 8")
        self.assertEqual(updated_offset, 0)

    def test_binop_add_simple(self):
        """Test BINOP expression with ADD operator."""
        expr = {
            "type": "BINOP",
            "op": "ADD",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 3}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        expected_lines = [
            "MOV x0, #5",
            "STORE_OFFSET 0, x0",
            "MOV x0, #3",
            "LOAD_OFFSET x1, 0",
            "ADD x0, x1"
        ]
        expected_code = "\n".join(expected_lines)
        
        self.assertEqual(code, expected_code)
        self.assertEqual(updated_offset, 8)

    def test_binop_sub(self):
        """Test BINOP expression with SUB operator."""
        expr = {
            "type": "BINOP",
            "op": "SUB",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 4}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        expected_lines = [
            "MOV x0, #10",
            "STORE_OFFSET 0, x0",
            "MOV x0, #4",
            "LOAD_OFFSET x1, 0",
            "SUB x0, x1"
        ]
        expected_code = "\n".join(expected_lines)
        
        self.assertEqual(code, expected_code)
        self.assertEqual(updated_offset, 8)

    def test_binop_mul(self):
        """Test BINOP expression with MUL operator."""
        expr = {
            "type": "BINOP",
            "op": "MUL",
            "left": {"type": "LITERAL", "value": 6},
            "right": {"type": "LITERAL", "value": 7}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        expected_lines = [
            "MOV x0, #6",
            "STORE_OFFSET 0, x0",
            "MOV x0, #7",
            "LOAD_OFFSET x1, 0",
            "MUL x0, x1"
        ]
        expected_code = "\n".join(expected_lines)
        
        self.assertEqual(code, expected_code)
        self.assertEqual(updated_offset, 8)

    def test_binop_div(self):
        """Test BINOP expression with DIV operator."""
        expr = {
            "type": "BINOP",
            "op": "DIV",
            "left": {"type": "LITERAL", "value": 20},
            "right": {"type": "LITERAL", "value": 4}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        expected_lines = [
            "MOV x0, #20",
            "STORE_OFFSET 0, x0",
            "MOV x0, #4",
            "LOAD_OFFSET x1, 0",
            "DIV x0, x1"
        ]
        expected_code = "\n".join(expected_lines)
        
        self.assertEqual(code, expected_code)
        self.assertEqual(updated_offset, 8)

    def test_binop_with_vars(self):
        """Test BINOP expression with variable operands."""
        expr = {
            "type": "BINOP",
            "op": "ADD",
            "left": {"type": "VAR", "name": "a"},
            "right": {"type": "VAR", "name": "b"}
        }
        var_offsets = {"a": 0, "b": 8}
        next_offset = 16
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        expected_lines = [
            "LOAD_OFFSET x0, 0",
            "STORE_OFFSET 16, x0",
            "LOAD_OFFSET x0, 8",
            "LOAD_OFFSET x1, 16",
            "ADD x0, x1"
        ]
        expected_code = "\n".join(expected_lines)
        
        self.assertEqual(code, expected_code)
        self.assertEqual(updated_offset, 24)

    def test_binop_nested(self):
        """Test BINOP expression with nested BINOP."""
        expr = {
            "type": "BINOP",
            "op": "ADD",
            "left": {
                "type": "BINOP",
                "op": "MUL",
                "left": {"type": "LITERAL", "value": 2},
                "right": {"type": "LITERAL", "value": 3}
            },
            "right": {"type": "LITERAL", "value": 4}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        # Inner MUL uses offset 0, outer ADD uses offset 8
        expected_lines = [
            "MOV x0, #2",
            "STORE_OFFSET 0, x0",
            "MOV x0, #3",
            "LOAD_OFFSET x1, 0",
            "MUL x0, x1",
            "STORE_OFFSET 8, x0",
            "MOV x0, #4",
            "LOAD_OFFSET x1, 8",
            "ADD x0, x1"
        ]
        expected_code = "\n".join(expected_lines)
        
        self.assertEqual(code, expected_code)
        self.assertEqual(updated_offset, 16)

    def test_unop_neg_literal(self):
        """Test UNOP expression with NEG operator on literal."""
        expr = {
            "type": "UNOP",
            "op": "NEG",
            "operand": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        expected_lines = [
            "MOV x0, #5",
            "NEG x0"
        ]
        expected_code = "\n".join(expected_lines)
        
        self.assertEqual(code, expected_code)
        self.assertEqual(updated_offset, 0)

    def test_unop_neg_var(self):
        """Test UNOP expression with NEG operator on variable."""
        expr = {
            "type": "UNOP",
            "op": "NEG",
            "operand": {"type": "VAR", "name": "x"}
        }
        var_offsets = {"x": 24}
        next_offset = 0
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        expected_lines = [
            "LOAD_OFFSET x0, 24",
            "NEG x0"
        ]
        expected_code = "\n".join(expected_lines)
        
        self.assertEqual(code, expected_code)
        self.assertEqual(updated_offset, 0)

    def test_unop_neg_nested_binop(self):
        """Test UNOP expression with NEG operator on nested BINOP."""
        expr = {
            "type": "UNOP",
            "op": "NEG",
            "operand": {
                "type": "BINOP",
                "op": "ADD",
                "left": {"type": "LITERAL", "value": 1},
                "right": {"type": "LITERAL", "value": 2}
            }
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        expected_lines = [
            "MOV x0, #1",
            "STORE_OFFSET 0, x0",
            "MOV x0, #2",
            "LOAD_OFFSET x1, 0",
            "ADD x0, x1",
            "NEG x0"
        ]
        expected_code = "\n".join(expected_lines)
        
        self.assertEqual(code, expected_code)
        self.assertEqual(updated_offset, 8)

    def test_unknown_expression_type(self):
        """Test error handling for unknown expression type."""
        expr = {"type": "UNKNOWN", "value": 42}
        var_offsets = {}
        next_offset = 0
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("Unknown expression type", str(context.exception))
        self.assertIn("UNKNOWN", str(context.exception))

    def test_unknown_unary_operator(self):
        """Test error handling for unknown unary operator."""
        expr = {
            "type": "UNOP",
            "op": "UNKNOWN_OP",
            "operand": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        next_offset = 0
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("Unknown unary operator", str(context.exception))
        self.assertIn("UNKNOWN_OP", str(context.exception))

    def test_next_offset_monotonic_binop_chain(self):
        """Test that next_offset increases monotonically for chained BINOPs."""
        expr = {
            "type": "BINOP",
            "op": "ADD",
            "left": {
                "type": "BINOP",
                "op": "ADD",
                "left": {"type": "LITERAL", "value": 1},
                "right": {"type": "LITERAL", "value": 2}
            },
            "right": {
                "type": "BINOP",
                "op": "ADD",
                "left": {"type": "LITERAL", "value": 3},
                "right": {"type": "LITERAL", "value": 4}
            }
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        # Three BINOPs should use offsets 0, 8, 16
        self.assertEqual(updated_offset, 24)
        self.assertIn("STORE_OFFSET 0, x0", code)
        self.assertIn("STORE_OFFSET 8, x0", code)
        self.assertIn("STORE_OFFSET 16, x0", code)

    def test_complex_expression(self):
        """Test complex expression: (a + b) * (c - d)."""
        expr = {
            "type": "BINOP",
            "op": "MUL",
            "left": {
                "type": "BINOP",
                "op": "ADD",
                "left": {"type": "VAR", "name": "a"},
                "right": {"type": "VAR", "name": "b"}
            },
            "right": {
                "type": "BINOP",
                "op": "SUB",
                "left": {"type": "VAR", "name": "c"},
                "right": {"type": "VAR", "name": "d"}
            }
        }
        var_offsets = {"a": 0, "b": 8, "c": 16, "d": 24}
        next_offset = 32
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        # Should use offsets 32, 40, 48 for the three BINOP temp slots
        self.assertEqual(updated_offset, 56)
        self.assertIn("LOAD_OFFSET x0, 0", code)  # load a
        self.assertIn("LOAD_OFFSET x0, 8", code)  # load b
        self.assertIn("ADD x0, x1", code)
        self.assertIn("LOAD_OFFSET x0, 16", code)  # load c
        self.assertIn("LOAD_OFFSET x0, 24", code)  # load d
        self.assertIn("SUB x0, x1", code)
        self.assertIn("MUL x0, x1", code)


if __name__ == "__main__":
    unittest.main()
