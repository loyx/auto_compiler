# === std / third-party imports ===
import unittest
from typing import Dict

# === relative import for UUT ===
from generate_expression_code_src import generate_expression_code


class TestGenerateExpressionCode(unittest.TestCase):
    """Unit tests for generate_expression_code function."""

    def test_literal_expression(self):
        """Test LITERAL expression type - loads immediate value."""
        expr = {"type": "LITERAL", "value": 42}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)

        self.assertEqual(code, "    LOAD_IMM R0, 42\n")
        self.assertEqual(updated_offset, 1)
        self.assertEqual(result_reg, "R0")

    def test_literal_expression_with_offset(self):
        """Test LITERAL expression with non-zero starting offset."""
        expr = {"type": "LITERAL", "value": 100}
        var_offsets: Dict[str, int] = {}
        next_offset = 5

        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)

        self.assertEqual(code, "    LOAD_IMM R5, 100\n")
        self.assertEqual(updated_offset, 6)
        self.assertEqual(result_reg, "R5")

    def test_ident_expression(self):
        """Test IDENT expression type - loads variable from stack."""
        expr = {"type": "IDENT", "name": "x"}
        var_offsets: Dict[str, int] = {"x": 3}
        next_offset = 0

        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)

        self.assertEqual(code, "    LOAD_STACK R0, 3\n")
        self.assertEqual(updated_offset, 1)
        self.assertEqual(result_reg, "R0")

    def test_ident_expression_different_variable(self):
        """Test IDENT expression with different variable."""
        expr = {"type": "IDENT", "name": "y"}
        var_offsets: Dict[str, int] = {"x": 0, "y": 5, "z": 10}
        next_offset = 2

        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)

        self.assertEqual(code, "    LOAD_STACK R2, 5\n")
        self.assertEqual(updated_offset, 3)
        self.assertEqual(result_reg, "R2")

    def test_binary_add_expression(self):
        """Test BINARY expression with ADD operator."""
        expr = {
            "type": "BINARY",
            "op": "ADD",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 20}
        }
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)

        expected_code = (
            "    LOAD_IMM R0, 10\n"
            "    LOAD_IMM R1, 20\n"
            "    ADD R2, R0, R1\n"
        )
        self.assertEqual(code, expected_code)
        self.assertEqual(updated_offset, 3)
        self.assertEqual(result_reg, "R2")

    def test_binary_sub_expression(self):
        """Test BINARY expression with SUB operator."""
        expr = {
            "type": "BINARY",
            "op": "SUB",
            "left": {"type": "IDENT", "name": "a"},
            "right": {"type": "LITERAL", "value": 5}
        }
        var_offsets: Dict[str, int] = {"a": 0}
        next_offset = 0

        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)

        expected_code = (
            "    LOAD_STACK R0, 0\n"
            "    LOAD_IMM R1, 5\n"
            "    SUB R2, R0, R1\n"
        )
        self.assertEqual(code, expected_code)
        self.assertEqual(updated_offset, 3)
        self.assertEqual(result_reg, "R2")

    def test_binary_mul_expression(self):
        """Test BINARY expression with MUL operator."""
        expr = {
            "type": "BINARY",
            "op": "MUL",
            "left": {"type": "LITERAL", "value": 3},
            "right": {"type": "IDENT", "name": "b"}
        }
        var_offsets: Dict[str, int] = {"b": 2}
        next_offset = 1

        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)

        expected_code = (
            "    LOAD_IMM R1, 3\n"
            "    LOAD_STACK R2, 2\n"
            "    MUL R3, R1, R2\n"
        )
        self.assertEqual(code, expected_code)
        self.assertEqual(updated_offset, 4)
        self.assertEqual(result_reg, "R3")

    def test_unary_not_expression(self):
        """Test UNARY expression with NOT operator."""
        expr = {
            "type": "UNARY",
            "op": "NOT",
            "expr": {"type": "LITERAL", "value": 1}
        }
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)

        expected_code = (
            "    LOAD_IMM R0, 1\n"
            "    NOT R1, R0\n"
        )
        self.assertEqual(code, expected_code)
        self.assertEqual(updated_offset, 2)
        self.assertEqual(result_reg, "R1")

    def test_unary_neg_expression(self):
        """Test UNARY expression with NEG operator."""
        expr = {
            "type": "UNARY",
            "op": "NEG",
            "expr": {"type": "IDENT", "name": "x"}
        }
        var_offsets: Dict[str, int] = {"x": 4}
        next_offset = 0

        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)

        expected_code = (
            "    LOAD_STACK R0, 4\n"
            "    NEG R1, R0\n"
        )
        self.assertEqual(code, expected_code)
        self.assertEqual(updated_offset, 2)
        self.assertEqual(result_reg, "R1")

    def test_nested_binary_expression(self):
        """Test nested BINARY expression: (1 + 2) * 3."""
        expr = {
            "type": "BINARY",
            "op": "MUL",
            "left": {
                "type": "BINARY",
                "op": "ADD",
                "left": {"type": "LITERAL", "value": 1},
                "right": {"type": "LITERAL", "value": 2}
            },
            "right": {"type": "LITERAL", "value": 3}
        }
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)

        expected_code = (
            "    LOAD_IMM R0, 1\n"
            "    LOAD_IMM R1, 2\n"
            "    ADD R2, R0, R1\n"
            "    LOAD_IMM R3, 3\n"
            "    MUL R4, R2, R3\n"
        )
        self.assertEqual(code, expected_code)
        self.assertEqual(updated_offset, 5)
        self.assertEqual(result_reg, "R4")

    def test_nested_unary_expression(self):
        """Test nested UNARY expression: NOT(NOT(x))."""
        expr = {
            "type": "UNARY",
            "op": "NOT",
            "expr": {
                "type": "UNARY",
                "op": "NOT",
                "expr": {"type": "IDENT", "name": "flag"}
            }
        }
        var_offsets: Dict[str, int] = {"flag": 1}
        next_offset = 0

        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)

        expected_code = (
            "    LOAD_STACK R0, 1\n"
            "    NOT R1, R0\n"
            "    NOT R2, R1\n"
        )
        self.assertEqual(code, expected_code)
        self.assertEqual(updated_offset, 3)
        self.assertEqual(result_reg, "R2")

    def test_complex_mixed_expression(self):
        """Test complex expression: (a + 5) * (NOT b)."""
        expr = {
            "type": "BINARY",
            "op": "MUL",
            "left": {
                "type": "BINARY",
                "op": "ADD",
                "left": {"type": "IDENT", "name": "a"},
                "right": {"type": "LITERAL", "value": 5}
            },
            "right": {
                "type": "UNARY",
                "op": "NOT",
                "expr": {"type": "IDENT", "name": "b"}
            }
        }
        var_offsets: Dict[str, int] = {"a": 0, "b": 1}
        next_offset = 0

        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)

        expected_code = (
            "    LOAD_STACK R0, 0\n"
            "    LOAD_IMM R1, 5\n"
            "    ADD R2, R0, R1\n"
            "    LOAD_STACK R3, 1\n"
            "    NOT R4, R3\n"
            "    MUL R5, R2, R4\n"
        )
        self.assertEqual(code, expected_code)
        self.assertEqual(updated_offset, 6)
        self.assertEqual(result_reg, "R5")

    def test_unknown_expression_type_raises_error(self):
        """Test that unknown expression type raises ValueError."""
        expr = {"type": "UNKNOWN", "value": 42}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, var_offsets, next_offset)

        self.assertIn("Unknown expression type: UNKNOWN", str(context.exception))

    def test_multiple_variables_in_expression(self):
        """Test expression with multiple different variables."""
        expr = {
            "type": "BINARY",
            "op": "ADD",
            "left": {"type": "IDENT", "name": "x"},
            "right": {"type": "IDENT", "name": "y"}
        }
        var_offsets: Dict[str, int] = {"x": 10, "y": 20, "z": 30}
        next_offset = 0

        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)

        expected_code = (
            "    LOAD_STACK R0, 10\n"
            "    LOAD_STACK R1, 20\n"
            "    ADD R2, R0, R1\n"
        )
        self.assertEqual(code, expected_code)
        self.assertEqual(updated_offset, 3)
        self.assertEqual(result_reg, "R2")

    def test_deeply_nested_expression(self):
        """Test deeply nested expression: ((1 + 2) + (3 + 4))."""
        expr = {
            "type": "BINARY",
            "op": "ADD",
            "left": {
                "type": "BINARY",
                "op": "ADD",
                "left": {"type": "LITERAL", "value": 1},
                "right": {"type": "LITERAL", "value": 2}
            },
            "right": {
                "type": "BINARY",
                "op": "ADD",
                "left": {"type": "LITERAL", "value": 3},
                "right": {"type": "LITERAL", "value": 4}
            }
        }
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)

        expected_code = (
            "    LOAD_IMM R0, 1\n"
            "    LOAD_IMM R1, 2\n"
            "    ADD R2, R0, R1\n"
            "    LOAD_IMM R3, 3\n"
            "    LOAD_IMM R4, 4\n"
            "    ADD R5, R3, R4\n"
            "    ADD R6, R2, R5\n"
        )
        self.assertEqual(code, expected_code)
        self.assertEqual(updated_offset, 7)
        self.assertEqual(result_reg, "R6")


if __name__ == "__main__":
    unittest.main()
