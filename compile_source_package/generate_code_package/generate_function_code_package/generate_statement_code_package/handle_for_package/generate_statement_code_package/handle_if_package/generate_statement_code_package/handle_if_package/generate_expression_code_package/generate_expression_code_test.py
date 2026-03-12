"""Unit tests for generate_expression_code function."""

import unittest
from typing import Dict, Any

from .generate_expression_code_src import generate_expression_code


class TestGenerateExpressionCode(unittest.TestCase):
    """Test cases for generate_expression_code function."""

    def test_literal_zero(self) -> None:
        """Test literal value 0 uses MOV instruction."""
        expr: Dict[str, Any] = {"type": "literal", "value": 0}
        asm, reg, offset = generate_expression_code(expr, {}, 0)
        self.assertEqual(asm, "MOV R0, #0\n")
        self.assertEqual(reg, 0)
        self.assertEqual(offset, 0)

    def test_literal_255(self) -> None:
        """Test literal value 255 uses MOV instruction."""
        expr: Dict[str, Any] = {"type": "literal", "value": 255}
        asm, reg, offset = generate_expression_code(expr, {}, 0)
        self.assertEqual(asm, "MOV R0, #255\n")
        self.assertEqual(reg, 0)
        self.assertEqual(offset, 0)

    def test_literal_256(self) -> None:
        """Test literal value 256 uses LDR instruction."""
        expr: Dict[str, Any] = {"type": "literal", "value": 256}
        asm, reg, offset = generate_expression_code(expr, {}, 0)
        self.assertEqual(asm, "LDR R0, =256\n")
        self.assertEqual(reg, 0)
        self.assertEqual(offset, 0)

    def test_literal_large_value(self) -> None:
        """Test large literal value uses LDR instruction."""
        expr: Dict[str, Any] = {"type": "literal", "value": 1000}
        asm, reg, offset = generate_expression_code(expr, {}, 0)
        self.assertEqual(asm, "LDR R0, =1000\n")
        self.assertEqual(reg, 0)
        self.assertEqual(offset, 0)

    def test_literal_negative(self) -> None:
        """Test negative literal value uses LDR instruction."""
        expr: Dict[str, Any] = {"type": "literal", "value": -5}
        asm, reg, offset = generate_expression_code(expr, {}, 0)
        self.assertEqual(asm, "LDR R0, =-5\n")
        self.assertEqual(reg, 0)
        self.assertEqual(offset, 0)

    def test_literal_float(self) -> None:
        """Test float literal value uses LDR instruction."""
        expr: Dict[str, Any] = {"type": "literal", "value": 3.14}
        asm, reg, offset = generate_expression_code(expr, {}, 0)
        self.assertEqual(asm, "LDR R0, =3.14\n")
        self.assertEqual(reg, 0)
        self.assertEqual(offset, 0)

    def test_variable_defined(self) -> None:
        """Test variable reference with defined variable."""
        expr: Dict[str, Any] = {"type": "variable", "var_name": "x"}
        var_offsets: Dict[str, int] = {"x": 8}
        asm, reg, offset = generate_expression_code(expr, var_offsets, 0)
        self.assertEqual(asm, "LDR R0, [SP, #8]\n")
        self.assertEqual(reg, 0)
        self.assertEqual(offset, 0)

    def test_variable_undefined(self) -> None:
        """Test variable reference with undefined variable raises ValueError."""
        expr: Dict[str, Any] = {"type": "variable", "var_name": "y"}
        var_offsets: Dict[str, int] = {"x": 8}
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, var_offsets, 0)
        self.assertIn("Undefined variable: y", str(context.exception))

    def test_binary_op_addition(self) -> None:
        """Test binary addition operation."""
        expr: Dict[str, Any] = {
            "type": "binary_op",
            "operator": "+",
            "left": {"type": "literal", "value": 5},
            "right": {"type": "literal", "value": 3},
        }
        asm, reg, offset = generate_expression_code(expr, {}, 0)
        self.assertIn("MOV R0, #5\n", asm)
        self.assertIn("STR R0, [SP, #0]\n", asm)
        self.assertIn("MOV R0, #3\n", asm)
        self.assertIn("LDR R1, [SP, #0]\n", asm)
        self.assertIn("ADD R0, R1, R0\n", asm)
        self.assertEqual(reg, 0)
        self.assertEqual(offset, 4)

    def test_binary_op_subtraction(self) -> None:
        """Test binary subtraction operation."""
        expr: Dict[str, Any] = {
            "type": "binary_op",
            "operator": "-",
            "left": {"type": "literal", "value": 10},
            "right": {"type": "literal", "value": 4},
        }
        asm, reg, offset = generate_expression_code(expr, {}, 0)
        self.assertIn("SUB R0, R1, R0\n", asm)
        self.assertEqual(reg, 0)

    def test_binary_op_multiplication(self) -> None:
        """Test binary multiplication operation."""
        expr: Dict[str, Any] = {
            "type": "binary_op",
            "operator": "*",
            "left": {"type": "literal", "value": 6},
            "right": {"type": "literal", "value": 7},
        }
        asm, reg, offset = generate_expression_code(expr, {}, 0)
        self.assertIn("MUL R0, R1, R0\n", asm)
        self.assertEqual(reg, 0)

    def test_binary_op_division(self) -> None:
        """Test binary division operation."""
        expr: Dict[str, Any] = {
            "type": "binary_op",
            "operator": "/",
            "left": {"type": "literal", "value": 20},
            "right": {"type": "literal", "value": 4},
        }
        asm, reg, offset = generate_expression_code(expr, {}, 0)
        self.assertIn("SDIV R0, R1, R0\n", asm)
        self.assertEqual(reg, 0)

    def test_binary_op_equal(self) -> None:
        """Test equality comparison operation."""
        expr: Dict[str, Any] = {
            "type": "binary_op",
            "operator": "==",
            "left": {"type": "literal", "value": 5},
            "right": {"type": "literal", "value": 5},
        }
        asm, reg, offset = generate_expression_code(expr, {}, 0)
        self.assertIn("CMP R1, R0\n", asm)
        self.assertIn("MOVEQ R0, #1\n", asm)
        self.assertIn("MOVNE R0, #0\n", asm)
        self.assertEqual(reg, 0)

    def test_binary_op_not_equal(self) -> None:
        """Test not equal comparison operation."""
        expr: Dict[str, Any] = {
            "type": "binary_op",
            "operator": "!=",
            "left": {"type": "literal", "value": 3},
            "right": {"type": "literal", "value": 5},
        }
        asm, reg, offset = generate_expression_code(expr, {}, 0)
        self.assertIn("CMP R1, R0\n", asm)
        self.assertIn("MOVNE R0, #1\n", asm)
        self.assertIn("MOVEQ R0, #0\n", asm)
        self.assertEqual(reg, 0)

    def test_binary_op_less_than(self) -> None:
        """Test less than comparison operation."""
        expr: Dict[str, Any] = {
            "type": "binary_op",
            "operator": "<",
            "left": {"type": "literal", "value": 3},
            "right": {"type": "literal", "value": 5},
        }
        asm, reg, offset = generate_expression_code(expr, {}, 0)
        self.assertIn("MOVLT R0, #1\n", asm)
        self.assertIn("MOVGE R0, #0\n", asm)
        self.assertEqual(reg, 0)

    def test_binary_op_greater_than(self) -> None:
        """Test greater than comparison operation."""
        expr: Dict[str, Any] = {
            "type": "binary_op",
            "operator": ">",
            "left": {"type": "literal", "value": 10},
            "right": {"type": "literal", "value": 5},
        }
        asm, reg, offset = generate_expression_code(expr, {}, 0)
        self.assertIn("MOVGT R0, #1\n", asm)
        self.assertIn("MOVLE R0, #0\n", asm)
        self.assertEqual(reg, 0)

    def test_binary_op_less_equal(self) -> None:
        """Test less than or equal comparison operation."""
        expr: Dict[str, Any] = {
            "type": "binary_op",
            "operator": "<=",
            "left": {"type": "literal", "value": 5},
            "right": {"type": "literal", "value": 5},
        }
        asm, reg, offset = generate_expression_code(expr, {}, 0)
        self.assertIn("MOVLE R0, #1\n", asm)
        self.assertIn("MOVGT R0, #0\n", asm)
        self.assertEqual(reg, 0)

    def test_binary_op_greater_equal(self) -> None:
        """Test greater than or equal comparison operation."""
        expr: Dict[str, Any] = {
            "type": "binary_op",
            "operator": ">=",
            "left": {"type": "literal", "value": 10},
            "right": {"type": "literal", "value": 5},
        }
        asm, reg, offset = generate_expression_code(expr, {}, 0)
        self.assertIn("MOVGE R0, #1\n", asm)
        self.assertIn("MOVLT R0, #0\n", asm)
        self.assertEqual(reg, 0)

    def test_binary_op_unknown_operator(self) -> None:
        """Test unknown binary operator raises ValueError."""
        expr: Dict[str, Any] = {
            "type": "binary_op",
            "operator": "%",
            "left": {"type": "literal", "value": 10},
            "right": {"type": "literal", "value": 3},
        }
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, {}, 0)
        self.assertIn("Unknown binary operator: %", str(context.exception))

    def test_binary_op_with_variables(self) -> None:
        """Test binary operation with variable operands."""
        expr: Dict[str, Any] = {
            "type": "binary_op",
            "operator": "+",
            "left": {"type": "variable", "var_name": "x"},
            "right": {"type": "variable", "var_name": "y"},
        }
        var_offsets: Dict[str, int] = {"x": 0, "y": 4}
        asm, reg, offset = generate_expression_code(expr, var_offsets, 0)
        self.assertIn("LDR R0, [SP, #0]\n", asm)
        self.assertIn("LDR R0, [SP, #4]\n", asm)
        self.assertIn("ADD R0, R1, R0\n", asm)
        self.assertEqual(reg, 0)

    def test_unary_op_negation(self) -> None:
        """Test unary negation operation."""
        expr: Dict[str, Any] = {
            "type": "unary_op",
            "operator": "-",
            "operand": {"type": "literal", "value": 5},
        }
        asm, reg, offset = generate_expression_code(expr, {}, 0)
        self.assertIn("MOV R0, #5\n", asm)
        self.assertIn("RSB R0, R0, #0\n", asm)
        self.assertEqual(reg, 0)
        self.assertEqual(offset, 0)

    def test_unary_op_not_zero(self) -> None:
        """Test logical NOT on zero produces 1."""
        expr: Dict[str, Any] = {
            "type": "unary_op",
            "operator": "not",
            "operand": {"type": "literal", "value": 0},
        }
        asm, reg, offset = generate_expression_code(expr, {}, 0)
        self.assertIn("CMP R0, #0\n", asm)
        self.assertIn("MOVEQ R0, #1\n", asm)
        self.assertIn("MOVNE R0, #0\n", asm)
        self.assertEqual(reg, 0)

    def test_unary_op_not_nonzero(self) -> None:
        """Test logical NOT on non-zero produces 0."""
        expr: Dict[str, Any] = {
            "type": "unary_op",
            "operator": "not",
            "operand": {"type": "literal", "value": 42},
        }
        asm, reg, offset = generate_expression_code(expr, {}, 0)
        self.assertIn("CMP R0, #0\n", asm)
        self.assertIn("MOVEQ R0, #1\n", asm)
        self.assertIn("MOVNE R0, #0\n", asm)
        self.assertEqual(reg, 0)

    def test_unary_op_unknown_operator(self) -> None:
        """Test unknown unary operator raises ValueError."""
        expr: Dict[str, Any] = {
            "type": "unary_op",
            "operator": "~",
            "operand": {"type": "literal", "value": 5},
        }
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, {}, 0)
        self.assertIn("Unknown unary operator: ~", str(context.exception))

    def test_unknown_expression_type(self) -> None:
        """Test unknown expression type raises ValueError."""
        expr: Dict[str, Any] = {"type": "unknown_type"}
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, {}, 0)
        self.assertIn("Unknown expression type: unknown_type", str(context.exception))

    def test_nested_binary_operations(self) -> None:
        """Test nested binary operations."""
        expr: Dict[str, Any] = {
            "type": "binary_op",
            "operator": "+",
            "left": {
                "type": "binary_op",
                "operator": "*",
                "left": {"type": "literal", "value": 2},
                "right": {"type": "literal", "value": 3},
            },
            "right": {"type": "literal", "value": 4},
        }
        asm, reg, offset = generate_expression_code(expr, {}, 0)
        self.assertIn("MOV R0, #2\n", asm)
        self.assertIn("MOV R0, #3\n", asm)
        self.assertIn("MUL R0, R1, R0\n", asm)
        self.assertIn("MOV R0, #4\n", asm)
        self.assertIn("ADD R0, R1, R0\n", asm)
        self.assertEqual(reg, 0)

    def test_unary_on_variable(self) -> None:
        """Test unary operation on variable."""
        expr: Dict[str, Any] = {
            "type": "unary_op",
            "operator": "-",
            "operand": {"type": "variable", "var_name": "x"},
        }
        var_offsets: Dict[str, int] = {"x": 12}
        asm, reg, offset = generate_expression_code(expr, var_offsets, 0)
        self.assertIn("LDR R0, [SP, #12]\n", asm)
        self.assertIn("RSB R0, R0, #0\n", asm)
        self.assertEqual(reg, 0)

    def test_comparison_result_in_r0(self) -> None:
        """Test that comparison operations produce result in R0."""
        expr: Dict[str, Any] = {
            "type": "binary_op",
            "operator": "==",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 1},
        }
        asm, reg, offset = generate_expression_code(expr, {}, 0)
        self.assertEqual(reg, 0)
        self.assertIn("MOVEQ R0, #1\n", asm)

    def test_temp_stack_allocation(self) -> None:
        """Test that temp stack space is allocated for binary operations."""
        expr: Dict[str, Any] = {
            "type": "binary_op",
            "operator": "+",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 2},
        }
        asm, reg, offset = generate_expression_code(expr, {}, 0)
        self.assertEqual(offset, 4)

    def test_multiple_nested_offsets(self) -> None:
        """Test offset tracking with multiple nested operations."""
        expr: Dict[str, Any] = {
            "type": "binary_op",
            "operator": "+",
            "left": {
                "type": "binary_op",
                "operator": "+",
                "left": {"type": "literal", "value": 1},
                "right": {"type": "literal", "value": 2},
            },
            "right": {
                "type": "binary_op",
                "operator": "+",
                "left": {"type": "literal", "value": 3},
                "right": {"type": "literal", "value": 4},
            },
        }
        asm, reg, offset = generate_expression_code(expr, {}, 0)
        self.assertEqual(reg, 0)
        self.assertGreater(offset, 0)


if __name__ == "__main__":
    unittest.main()
