# === std / third-party imports ===
import unittest
from typing import Dict, Any

# === relative imports ===
from .generate_expression_code_src import (
    generate_expression_code,
    _generate_literal_code,
    _generate_var_code,
    _generate_binary_code,
    OP_MAP,
)

# === type aliases ===
VarOffsets = Dict[str, int]
Expr = Dict[str, Any]


class TestGenerateLiteralCode(unittest.TestCase):
    """Test cases for literal expression code generation."""

    def test_literal_integer(self):
        """Test generating code for an integer literal."""
        expr: Expr = {"type": "literal", "value": 42}
        code, result_offset, updated_offset = _generate_literal_code(expr, 0)
        
        self.assertEqual(code, "PUSH 42\n")
        self.assertEqual(result_offset, 0)
        self.assertEqual(updated_offset, 1)

    def test_literal_float(self):
        """Test generating code for a float literal."""
        expr: Expr = {"type": "literal", "value": 3.14}
        code, result_offset, updated_offset = _generate_literal_code(expr, 5)
        
        self.assertEqual(code, "PUSH 3.14\n")
        self.assertEqual(result_offset, 5)
        self.assertEqual(updated_offset, 6)

    def test_literal_zero(self):
        """Test generating code for zero literal."""
        expr: Expr = {"type": "literal", "value": 0}
        code, result_offset, updated_offset = _generate_literal_code(expr, 10)
        
        self.assertEqual(code, "PUSH 0\n")
        self.assertEqual(result_offset, 10)
        self.assertEqual(updated_offset, 11)

    def test_literal_negative(self):
        """Test generating code for a negative literal."""
        expr: Expr = {"type": "literal", "value": -5}
        code, result_offset, updated_offset = _generate_literal_code(expr, 0)
        
        self.assertEqual(code, "PUSH -5\n")
        self.assertEqual(result_offset, 0)
        self.assertEqual(updated_offset, 1)


class TestGenerateVarCode(unittest.TestCase):
    """Test cases for variable reference code generation."""

    def test_var_defined(self):
        """Test generating code for a defined variable."""
        expr: Expr = {"type": "var", "name": "x"}
        var_offsets: VarOffsets = {"x": 3, "y": 4}
        code, result_offset, updated_offset = _generate_var_code(expr, var_offsets, 0)
        
        self.assertEqual(code, "LOAD 3\n")
        self.assertEqual(result_offset, 0)
        self.assertEqual(updated_offset, 1)

    def test_var_different_offset(self):
        """Test generating code with different starting offset."""
        expr: Expr = {"type": "var", "name": "y"}
        var_offsets: VarOffsets = {"x": 0, "y": 5}
        code, result_offset, updated_offset = _generate_var_code(expr, var_offsets, 10)
        
        self.assertEqual(code, "LOAD 5\n")
        self.assertEqual(result_offset, 10)
        self.assertEqual(updated_offset, 11)

    def test_var_undefined(self):
        """Test that undefined variable raises ValueError."""
        expr: Expr = {"type": "var", "name": "undefined_var"}
        var_offsets: VarOffsets = {"x": 0}
        
        with self.assertRaises(ValueError) as context:
            _generate_var_code(expr, var_offsets, 0)
        
        self.assertIn("Undefined variable: undefined_var", str(context.exception))


class TestGenerateBinaryCode(unittest.TestCase):
    """Test cases for binary operation code generation."""

    def test_binary_addition(self):
        """Test generating code for addition operation."""
        expr: Expr = {
            "type": "binary",
            "op": "+",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 2},
        }
        var_offsets: VarOffsets = {}
        code, result_offset, updated_offset = _generate_binary_code(expr, var_offsets, 0)
        
        self.assertEqual(code, "PUSH 1\nPUSH 2\nADD\n")
        self.assertEqual(result_offset, 2)
        self.assertEqual(updated_offset, 3)

    def test_binary_subtraction(self):
        """Test generating code for subtraction operation."""
        expr: Expr = {
            "type": "binary",
            "op": "-",
            "left": {"type": "literal", "value": 10},
            "right": {"type": "literal", "value": 3},
        }
        var_offsets: VarOffsets = {}
        code, result_offset, updated_offset = _generate_binary_code(expr, var_offsets, 0)
        
        self.assertEqual(code, "PUSH 10\nPUSH 3\nSUB\n")
        self.assertEqual(result_offset, 2)
        self.assertEqual(updated_offset, 3)

    def test_binary_multiplication(self):
        """Test generating code for multiplication operation."""
        expr: Expr = {
            "type": "binary",
            "op": "*",
            "left": {"type": "literal", "value": 4},
            "right": {"type": "literal", "value": 5},
        }
        var_offsets: VarOffsets = {}
        code, result_offset, updated_offset = _generate_binary_code(expr, var_offsets, 0)
        
        self.assertEqual(code, "PUSH 4\nPUSH 5\nMUL\n")
        self.assertEqual(result_offset, 2)
        self.assertEqual(updated_offset, 3)

    def test_binary_division(self):
        """Test generating code for division operation."""
        expr: Expr = {
            "type": "binary",
            "op": "/",
            "left": {"type": "literal", "value": 20},
            "right": {"type": "literal", "value": 4},
        }
        var_offsets: VarOffsets = {}
        code, result_offset, updated_offset = _generate_binary_code(expr, var_offsets, 0)
        
        self.assertEqual(code, "PUSH 20\nPUSH 4\nDIV\n")
        self.assertEqual(result_offset, 2)
        self.assertEqual(updated_offset, 3)

    def test_binary_comparison_lt(self):
        """Test generating code for less-than comparison."""
        expr: Expr = {
            "type": "binary",
            "op": "<",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 2},
        }
        var_offsets: VarOffsets = {}
        code, result_offset, updated_offset = _generate_binary_code(expr, var_offsets, 0)
        
        self.assertEqual(code, "PUSH 1\nPUSH 2\nLT\n")
        self.assertEqual(result_offset, 2)
        self.assertEqual(updated_offset, 3)

    def test_binary_comparison_gt(self):
        """Test generating code for greater-than comparison."""
        expr: Expr = {
            "type": "binary",
            "op": ">",
            "left": {"type": "literal", "value": 5},
            "right": {"type": "literal", "value": 3},
        }
        var_offsets: VarOffsets = {}
        code, result_offset, updated_offset = _generate_binary_code(expr, var_offsets, 0)
        
        self.assertEqual(code, "PUSH 5\nPUSH 3\nGT\n")
        self.assertEqual(result_offset, 2)
        self.assertEqual(updated_offset, 3)

    def test_binary_comparison_le(self):
        """Test generating code for less-than-or-equal comparison."""
        expr: Expr = {
            "type": "binary",
            "op": "<=",
            "left": {"type": "literal", "value": 3},
            "right": {"type": "literal", "value": 3},
        }
        var_offsets: VarOffsets = {}
        code, result_offset, updated_offset = _generate_binary_code(expr, var_offsets, 0)
        
        self.assertEqual(code, "PUSH 3\nPUSH 3\nLE\n")
        self.assertEqual(result_offset, 2)
        self.assertEqual(updated_offset, 3)

    def test_binary_comparison_ge(self):
        """Test generating code for greater-than-or-equal comparison."""
        expr: Expr = {
            "type": "binary",
            "op": ">=",
            "left": {"type": "literal", "value": 5},
            "right": {"type": "literal", "value": 5},
        }
        var_offsets: VarOffsets = {}
        code, result_offset, updated_offset = _generate_binary_code(expr, var_offsets, 0)
        
        self.assertEqual(code, "PUSH 5\nPUSH 5\nGE\n")
        self.assertEqual(result_offset, 2)
        self.assertEqual(updated_offset, 3)

    def test_binary_comparison_eq(self):
        """Test generating code for equality comparison."""
        expr: Expr = {
            "type": "binary",
            "op": "==",
            "left": {"type": "literal", "value": 7},
            "right": {"type": "literal", "value": 7},
        }
        var_offsets: VarOffsets = {}
        code, result_offset, updated_offset = _generate_binary_code(expr, var_offsets, 0)
        
        self.assertEqual(code, "PUSH 7\nPUSH 7\nEQ\n")
        self.assertEqual(result_offset, 2)
        self.assertEqual(updated_offset, 3)

    def test_binary_comparison_ne(self):
        """Test generating code for not-equal comparison."""
        expr: Expr = {
            "type": "binary",
            "op": "!=",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 2},
        }
        var_offsets: VarOffsets = {}
        code, result_offset, updated_offset = _generate_binary_code(expr, var_offsets, 0)
        
        self.assertEqual(code, "PUSH 1\nPUSH 2\nNE\n")
        self.assertEqual(result_offset, 2)
        self.assertEqual(updated_offset, 3)

    def test_binary_unknown_operator(self):
        """Test that unknown operator raises ValueError."""
        expr: Expr = {
            "type": "binary",
            "op": "UNKNOWN",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 2},
        }
        var_offsets: VarOffsets = {}
        
        with self.assertRaises(ValueError) as context:
            _generate_binary_code(expr, var_offsets, 0)
        
        self.assertIn("Unknown operator: UNKNOWN", str(context.exception))

    def test_binary_with_variables(self):
        """Test generating code for binary operation with variables."""
        expr: Expr = {
            "type": "binary",
            "op": "+",
            "left": {"type": "var", "name": "x"},
            "right": {"type": "var", "name": "y"},
        }
        var_offsets: VarOffsets = {"x": 0, "y": 1}
        code, result_offset, updated_offset = _generate_binary_code(expr, var_offsets, 0)
        
        self.assertEqual(code, "LOAD 0\nLOAD 1\nADD\n")
        self.assertEqual(result_offset, 2)
        self.assertEqual(updated_offset, 3)


class TestGenerateExpressionCode(unittest.TestCase):
    """Test cases for the main generate_expression_code function."""

    def test_expression_literal(self):
        """Test main function with literal expression."""
        expr: Expr = {"type": "literal", "value": 100}
        var_offsets: VarOffsets = {}
        code, result_offset, updated_offset = generate_expression_code(expr, var_offsets, 0)
        
        self.assertEqual(code, "PUSH 100\n")
        self.assertEqual(result_offset, 0)
        self.assertEqual(updated_offset, 1)

    def test_expression_var(self):
        """Test main function with variable expression."""
        expr: Expr = {"type": "var", "name": "counter"}
        var_offsets: VarOffsets = {"counter": 5}
        code, result_offset, updated_offset = generate_expression_code(expr, var_offsets, 0)
        
        self.assertEqual(code, "LOAD 5\n")
        self.assertEqual(result_offset, 0)
        self.assertEqual(updated_offset, 1)

    def test_expression_binary_simple(self):
        """Test main function with simple binary expression."""
        expr: Expr = {
            "type": "binary",
            "op": "+",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 1},
        }
        var_offsets: VarOffsets = {}
        code, result_offset, updated_offset = generate_expression_code(expr, var_offsets, 0)
        
        self.assertEqual(code, "PUSH 1\nPUSH 1\nADD\n")
        self.assertEqual(result_offset, 2)
        self.assertEqual(updated_offset, 3)

    def test_expression_nested_binary(self):
        """Test main function with nested binary expression: (1 + 2) * 3."""
        expr: Expr = {
            "type": "binary",
            "op": "*",
            "left": {
                "type": "binary",
                "op": "+",
                "left": {"type": "literal", "value": 1},
                "right": {"type": "literal", "value": 2},
            },
            "right": {"type": "literal", "value": 3},
        }
        var_offsets: VarOffsets = {}
        code, result_offset, updated_offset = generate_expression_code(expr, var_offsets, 0)
        
        # Expected: PUSH 1, PUSH 2, ADD, PUSH 3, MUL
        self.assertEqual(code, "PUSH 1\nPUSH 2\nADD\nPUSH 3\nMUL\n")
        self.assertEqual(result_offset, 4)
        self.assertEqual(updated_offset, 5)

    def test_expression_complex_nested(self):
        """Test main function with complex nested expression: (a + b) * (c - d)."""
        expr: Expr = {
            "type": "binary",
            "op": "*",
            "left": {
                "type": "binary",
                "op": "+",
                "left": {"type": "var", "name": "a"},
                "right": {"type": "var", "name": "b"},
            },
            "right": {
                "type": "binary",
                "op": "-",
                "left": {"type": "var", "name": "c"},
                "right": {"type": "var", "name": "d"},
            },
        }
        var_offsets: VarOffsets = {"a": 0, "b": 1, "c": 2, "d": 3}
        code, result_offset, updated_offset = generate_expression_code(expr, var_offsets, 0)
        
        # Expected: LOAD 0, LOAD 1, ADD, LOAD 2, LOAD 3, SUB, MUL
        self.assertEqual(code, "LOAD 0\nLOAD 1\nADD\nLOAD 2\nLOAD 3\nSUB\nMUL\n")
        self.assertEqual(result_offset, 6)
        self.assertEqual(updated_offset, 7)

    def test_expression_unknown_type(self):
        """Test that unknown expression type raises ValueError."""
        expr: Expr = {"type": "unknown_type"}
        var_offsets: VarOffsets = {}
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, var_offsets, 0)
        
        self.assertIn("Unknown expression type: unknown_type", str(context.exception))

    def test_expression_var_undefined(self):
        """Test that undefined variable raises ValueError through main function."""
        expr: Expr = {"type": "var", "name": "not_defined"}
        var_offsets: VarOffsets = {"x": 0}
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, var_offsets, 0)
        
        self.assertIn("Undefined variable: not_defined", str(context.exception))

    def test_expression_with_non_zero_offset(self):
        """Test expression generation starting from non-zero offset."""
        expr: Expr = {"type": "literal", "value": 42}
        var_offsets: VarOffsets = {}
        code, result_offset, updated_offset = generate_expression_code(expr, var_offsets, 10)
        
        self.assertEqual(code, "PUSH 42\n")
        self.assertEqual(result_offset, 10)
        self.assertEqual(updated_offset, 11)

    def test_expression_deeply_nested(self):
        """Test deeply nested expression: ((1 + 2) * (3 + 4)) - 5."""
        expr: Expr = {
            "type": "binary",
            "op": "-",
            "left": {
                "type": "binary",
                "op": "*",
                "left": {
                    "type": "binary",
                    "op": "+",
                    "left": {"type": "literal", "value": 1},
                    "right": {"type": "literal", "value": 2},
                },
                "right": {
                    "type": "binary",
                    "op": "+",
                    "left": {"type": "literal", "value": 3},
                    "right": {"type": "literal", "value": 4},
                },
            },
            "right": {"type": "literal", "value": 5},
        }
        var_offsets: VarOffsets = {}
        code, result_offset, updated_offset = generate_expression_code(expr, var_offsets, 0)
        
        # Expected sequence of operations
        expected_code = (
            "PUSH 1\nPUSH 2\nADD\n"  # 1 + 2
            "PUSH 3\nPUSH 4\nADD\n"  # 3 + 4
            "MUL\n"                   # (1+2) * (3+4)
            "PUSH 5\n"                # 5
            "SUB\n"                   # ((1+2)*(3+4)) - 5
        )
        self.assertEqual(code, expected_code)
        self.assertEqual(result_offset, 8)
        self.assertEqual(updated_offset, 9)

    def test_expression_mixed_var_literal(self):
        """Test expression mixing variables and literals: x + 10."""
        expr: Expr = {
            "type": "binary",
            "op": "+",
            "left": {"type": "var", "name": "x"},
            "right": {"type": "literal", "value": 10},
        }
        var_offsets: VarOffsets = {"x": 0}
        code, result_offset, updated_offset = generate_expression_code(expr, var_offsets, 0)
        
        self.assertEqual(code, "LOAD 0\nPUSH 10\nADD\n")
        self.assertEqual(result_offset, 2)
        self.assertEqual(updated_offset, 3)


class TestOpMap(unittest.TestCase):
    """Test cases for operator mapping."""

    def test_op_map_completeness(self):
        """Test that OP_MAP contains all expected operators."""
        expected_ops = ["+", "-", "*", "/", "<", ">", "<=", ">=", "==", "!="]
        for op in expected_ops:
            self.assertIn(op, OP_MAP)

    def test_op_map_values(self):
        """Test that OP_MAP values are valid assembly instructions."""
        expected_instructions = ["ADD", "SUB", "MUL", "DIV", "LT", "GT", "LE", "GE", "EQ", "NE"]
        for instruction in OP_MAP.values():
            self.assertIn(instruction, expected_instructions)


if __name__ == "__main__":
    unittest.main()
