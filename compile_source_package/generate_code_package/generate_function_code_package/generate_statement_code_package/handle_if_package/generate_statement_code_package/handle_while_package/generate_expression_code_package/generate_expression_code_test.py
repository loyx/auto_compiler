# === std / third-party imports ===
import unittest
from unittest.mock import patch

# === sub function imports ===
from .generate_expression_code_src import (
    generate_expression_code,
    _generate_const_code,
    _generate_var_code,
    _generate_binop_code,
    _emit_operation,
)


class TestGenerateConstCode(unittest.TestCase):
    """Tests for _generate_const_code helper function."""

    def test_const_integer(self):
        """Test generating code for integer constant."""
        expr = {"type": "CONST", "value": 42}
        code, offset, reg = _generate_const_code(expr, 0)
        self.assertEqual(code, "    mov x0, #42\n")
        self.assertEqual(offset, 1)
        self.assertEqual(reg, "x0")

    def test_const_zero(self):
        """Test generating code for zero constant."""
        expr = {"type": "CONST", "value": 0}
        code, offset, reg = _generate_const_code(expr, 5)
        self.assertEqual(code, "    mov x5, #0\n")
        self.assertEqual(offset, 6)
        self.assertEqual(reg, "x5")

    def test_const_negative(self):
        """Test generating code for negative constant."""
        expr = {"type": "CONST", "value": -10}
        code, offset, reg = _generate_const_code(expr, 3)
        self.assertEqual(code, "    mov x3, #-10\n")
        self.assertEqual(offset, 4)
        self.assertEqual(reg, "x3")


class TestGenerateVarCode(unittest.TestCase):
    """Tests for _generate_var_code helper function."""

    def test_var_found(self):
        """Test generating code for existing variable."""
        expr = {"type": "VAR", "name": "x"}
        var_offsets = {"x": 8, "y": 16}
        code, offset, reg = _generate_var_code(expr, var_offsets, 2)
        self.assertEqual(code, "    ldr x2, [sp, #8]\n")
        self.assertEqual(offset, 3)
        self.assertEqual(reg, "x2")

    def test_var_not_found(self):
        """Test error when variable not in var_offsets."""
        expr = {"type": "VAR", "name": "z"}
        var_offsets = {"x": 8}
        with self.assertRaises(ValueError) as context:
            _generate_var_code(expr, var_offsets, 0)
        self.assertIn("Variable 'z' not found", str(context.exception))

    def test_var_offset_zero(self):
        """Test generating code for variable at offset 0."""
        expr = {"type": "VAR", "name": "a"}
        var_offsets = {"a": 0}
        code, offset, reg = _generate_var_code(expr, var_offsets, 10)
        self.assertEqual(code, "    ldr x10, [sp, #0]\n")
        self.assertEqual(offset, 11)
        self.assertEqual(reg, "x10")


class TestEmitOperation(unittest.TestCase):
    """Tests for _emit_operation helper function."""

    def test_arithmetic_add(self):
        """Test ADD operation."""
        code, offset = _emit_operation("+", "x0", "x1", "x2", 3)
        self.assertEqual(code, "    add x2, x0, x1\n")
        self.assertEqual(offset, 4)

    def test_arithmetic_sub(self):
        """Test SUB operation."""
        code, offset = _emit_operation("-", "x0", "x1", "x2", 3)
        self.assertEqual(code, "    sub x2, x0, x1\n")
        self.assertEqual(offset, 4)

    def test_arithmetic_mul(self):
        """Test MUL operation."""
        code, offset = _emit_operation("*", "x0", "x1", "x2", 3)
        self.assertEqual(code, "    mul x2, x0, x1\n")
        self.assertEqual(offset, 4)

    def test_arithmetic_div(self):
        """Test SDIV operation."""
        code, offset = _emit_operation("/", "x0", "x1", "x2", 3)
        self.assertEqual(code, "    sdiv x2, x0, x1\n")
        self.assertEqual(offset, 4)

    def test_comparison_eq(self):
        """Test EQ comparison."""
        code, offset = _emit_operation("==", "x0", "x1", "x2", 3)
        expected = "    cmp x0, x1\n    cset x2, eq\n"
        self.assertEqual(code, expected)
        self.assertEqual(offset, 4)

    def test_comparison_ne(self):
        """Test NE comparison."""
        code, offset = _emit_operation("!=", "x0", "x1", "x2", 3)
        expected = "    cmp x0, x1\n    cset x2, ne\n"
        self.assertEqual(code, expected)
        self.assertEqual(offset, 4)

    def test_comparison_lt(self):
        """Test LT comparison."""
        code, offset = _emit_operation("<", "x0", "x1", "x2", 3)
        expected = "    cmp x0, x1\n    cset x2, lt\n"
        self.assertEqual(code, expected)
        self.assertEqual(offset, 4)

    def test_comparison_gt(self):
        """Test GT comparison."""
        code, offset = _emit_operation(">", "x0", "x1", "x2", 3)
        expected = "    cmp x0, x1\n    cset x2, gt\n"
        self.assertEqual(code, expected)
        self.assertEqual(offset, 4)

    def test_comparison_le(self):
        """Test LE comparison."""
        code, offset = _emit_operation("<=", "x0", "x1", "x2", 3)
        expected = "    cmp x0, x1\n    cset x2, le\n"
        self.assertEqual(code, expected)
        self.assertEqual(offset, 4)

    def test_comparison_ge(self):
        """Test GE comparison."""
        code, offset = _emit_operation(">=", "x0", "x1", "x2", 3)
        expected = "    cmp x0, x1\n    cset x2, ge\n"
        self.assertEqual(code, expected)
        self.assertEqual(offset, 4)

    def test_logical_and(self):
        """Test AND operation."""
        code, offset = _emit_operation("and", "x0", "x1", "x2", 3)
        self.assertEqual(code, "    and x2, x0, x1\n")
        self.assertEqual(offset, 4)

    def test_logical_or(self):
        """Test ORR operation."""
        code, offset = _emit_operation("or", "x0", "x1", "x2", 3)
        self.assertEqual(code, "    orr x2, x0, x1\n")
        self.assertEqual(offset, 4)

    def test_unknown_operator(self):
        """Test error for unknown operator."""
        with self.assertRaises(ValueError) as context:
            _emit_operation("%", "x0", "x1", "x2", 3)
        self.assertIn("Unknown operator: %", str(context.exception))


class TestGenerateBinopCode(unittest.TestCase):
    """Tests for _generate_binop_code helper function."""

    @patch('projects.cc.files.main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_while_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_binop_simple(self, mock_gen):
        """Test binary operation with mocked recursive calls."""
        # Setup mock returns for left and right operands
        mock_gen.side_effect = [
            ("    mov x0, #5\n", 1, "x0"),  # left operand
            ("    mov x1, #3\n", 2, "x1"),  # right operand
        ]
        
        expr = {"type": "BINOP", "operator": "+", "left": {}, "right": {}}
        var_offsets = {}
        code, offset, reg = _generate_binop_code(expr, var_offsets, 0)
        
        self.assertIn("add x2, x0, x1", code)
        self.assertEqual(offset, 3)
        self.assertEqual(reg, "x2")
        self.assertEqual(mock_gen.call_count, 2)

    @patch('projects.cc.files.main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_while_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_binop_comparison(self, mock_gen):
        """Test binary comparison operation."""
        mock_gen.side_effect = [
            ("    mov x0, #5\n", 1, "x0"),
            ("    mov x1, #3\n", 2, "x1"),
        ]
        
        expr = {"type": "BINOP", "operator": ">", "left": {}, "right": {}}
        var_offsets = {}
        code, offset, reg = _generate_binop_code(expr, var_offsets, 0)
        
        self.assertIn("cmp x0, x1", code)
        self.assertIn("cset x2, gt", code)
        self.assertEqual(offset, 3)


class TestGenerateExpressionCode(unittest.TestCase):
    """Tests for main generate_expression_code function."""

    def test_const_expression(self):
        """Test CONST expression type."""
        expr = {"type": "CONST", "value": 100}
        var_offsets = {}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        self.assertEqual(code, "    mov x0, #100\n")
        self.assertEqual(offset, 1)
        self.assertEqual(reg, "x0")

    def test_var_expression(self):
        """Test VAR expression type."""
        expr = {"type": "VAR", "name": "counter"}
        var_offsets = {"counter": 24}
        code, offset, reg = generate_expression_code(expr, var_offsets, 5)
        self.assertEqual(code, "    ldr x5, [sp, #24]\n")
        self.assertEqual(offset, 6)
        self.assertEqual(reg, "x5")

    def test_binop_arithmetic_expression(self):
        """Test BINOP arithmetic expression."""
        expr = {
            "type": "BINOP",
            "operator": "+",
            "left": {"type": "CONST", "value": 10},
            "right": {"type": "CONST", "value": 20},
        }
        var_offsets = {}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        self.assertIn("mov x0, #10", code)
        self.assertIn("mov x1, #20", code)
        self.assertIn("add x2, x0, x1", code)
        self.assertEqual(offset, 3)
        self.assertEqual(reg, "x2")

    def test_binop_comparison_expression(self):
        """Test BINOP comparison expression."""
        expr = {
            "type": "BINOP",
            "operator": "==",
            "left": {"type": "VAR", "name": "a"},
            "right": {"type": "VAR", "name": "b"},
        }
        var_offsets = {"a": 0, "b": 8}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        self.assertIn("ldr x0, [sp, #0]", code)
        self.assertIn("ldr x1, [sp, #8]", code)
        self.assertIn("cmp x0, x1", code)
        self.assertIn("cset x2, eq", code)
        self.assertEqual(offset, 3)
        self.assertEqual(reg, "x2")

    def test_nested_binop_expression(self):
        """Test nested binary operations."""
        expr = {
            "type": "BINOP",
            "operator": "*",
            "left": {
                "type": "BINOP",
                "operator": "+",
                "left": {"type": "CONST", "value": 1},
                "right": {"type": "CONST", "value": 2},
            },
            "right": {"type": "CONST", "value": 3},
        }
        var_offsets = {}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        # Should evaluate (1 + 2) * 3
        self.assertIn("mov x0, #1", code)
        self.assertIn("mov x1, #2", code)
        self.assertIn("add x2, x0, x1", code)
        self.assertIn("mov x3, #3", code)
        self.assertIn("mul x4, x2, x3", code)
        self.assertEqual(offset, 5)
        self.assertEqual(reg, "x4")

    def test_complex_mixed_expression(self):
        """Test complex expression with vars and constants."""
        expr = {
            "type": "BINOP",
            "operator": "and",
            "left": {
                "type": "BINOP",
                "operator": ">",
                "left": {"type": "VAR", "name": "x"},
                "right": {"type": "CONST", "value": 0},
            },
            "right": {
                "type": "BINOP",
                "operator": "<",
                "left": {"type": "VAR", "name": "x"},
                "right": {"type": "CONST", "value": 100},
            },
        }
        var_offsets = {"x": 16}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        # Check all components are present
        self.assertIn("ldr x0, [sp, #16]", code)  # load x
        self.assertIn("mov x1, #0", code)  # load 0
        self.assertIn("cmp x0, x1", code)  # compare x > 0
        self.assertIn("cset x2, gt", code)
        self.assertIn("ldr x3, [sp, #16]", code)  # load x again
        self.assertIn("mov x4, #100", code)  # load 100
        self.assertIn("cmp x3, x4", code)  # compare x < 100
        self.assertIn("cset x5, lt", code)
        self.assertIn("and x6, x2, x5", code)  # combine results
        self.assertEqual(offset, 7)
        self.assertEqual(reg, "x6")

    def test_unknown_expression_type(self):
        """Test error for unknown expression type."""
        expr = {"type": "UNKNOWN", "value": 42}
        var_offsets = {}
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, var_offsets, 0)
        self.assertIn("Unknown expression type: UNKNOWN", str(context.exception))

    def test_division_operation(self):
        """Test division operation."""
        expr = {
            "type": "BINOP",
            "operator": "/",
            "left": {"type": "CONST", "value": 100},
            "right": {"type": "CONST", "value": 5},
        }
        var_offsets = {}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        self.assertIn("sdiv x2, x0, x1", code)
        self.assertEqual(offset, 3)

    def test_logical_or_operation(self):
        """Test logical OR operation."""
        expr = {
            "type": "BINOP",
            "operator": "or",
            "left": {"type": "CONST", "value": 1},
            "right": {"type": "CONST", "value": 0},
        }
        var_offsets = {}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        self.assertIn("orr x2, x0, x1", code)
        self.assertEqual(offset, 3)

    def test_subtraction_operation(self):
        """Test subtraction operation."""
        expr = {
            "type": "BINOP",
            "operator": "-",
            "left": {"type": "CONST", "value": 50},
            "right": {"type": "CONST", "value": 30},
        }
        var_offsets = {}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        self.assertIn("sub x2, x0, x1", code)
        self.assertEqual(offset, 3)

    def test_not_equal_comparison(self):
        """Test not equal comparison."""
        expr = {
            "type": "BINOP",
            "operator": "!=",
            "left": {"type": "VAR", "name": "a"},
            "right": {"type": "CONST", "value": 0},
        }
        var_offsets = {"a": 32}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        self.assertIn("cset x2, ne", code)
        self.assertEqual(offset, 3)

    def test_less_equal_comparison(self):
        """Test less than or equal comparison."""
        expr = {
            "type": "BINOP",
            "operator": "<=",
            "left": {"type": "CONST", "value": 5},
            "right": {"type": "VAR", "name": "limit"},
        }
        var_offsets = {"limit": 40}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        self.assertIn("cset x2, le", code)
        self.assertEqual(offset, 3)

    def test_greater_equal_comparison(self):
        """Test greater than or equal comparison."""
        expr = {
            "type": "BINOP",
            "operator": ">=",
            "left": {"type": "VAR", "name": "value"},
            "right": {"type": "CONST", "value": 10},
        }
        var_offsets = {"value": 48}
        code, offset, reg = generate_expression_code(expr, var_offsets, 0)
        
        self.assertIn("cset x2, ge", code)
        self.assertEqual(offset, 3)


if __name__ == "__main__":
    unittest.main()
