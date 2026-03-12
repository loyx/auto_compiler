import unittest
from .generate_expression_code_src import generate_expression_code


class TestGenerateExpressionCode(unittest.TestCase):
    """Test cases for generate_expression_code function."""
    
    def test_literal_expression(self):
        """Test LITERAL expression type."""
        expr = {"type": "LITERAL", "value": 42}
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertEqual(code, "    mov x0, #42")
        self.assertEqual(updated_offset, 0)
        self.assertEqual(reg, "x0")
    
    def test_literal_zero(self):
        """Test LITERAL expression with zero value."""
        expr = {"type": "LITERAL", "value": 0}
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertEqual(code, "    mov x0, #0")
        self.assertEqual(updated_offset, 0)
        self.assertEqual(reg, "x0")
    
    def test_literal_negative(self):
        """Test LITERAL expression with negative value."""
        expr = {"type": "LITERAL", "value": -10}
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertEqual(code, "    mov x0, #-10")
        self.assertEqual(updated_offset, 0)
        self.assertEqual(reg, "x0")
    
    def test_ident_expression(self):
        """Test IDENT expression type."""
        expr = {"type": "IDENT", "name": "x"}
        var_offsets = {"x": 0}
        next_offset = 0
        
        code, updated_offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertEqual(code, "    ldr x0, [sp, #0]")
        self.assertEqual(updated_offset, 0)
        self.assertEqual(reg, "x0")
    
    def test_ident_expression_offset(self):
        """Test IDENT expression with non-zero offset."""
        expr = {"type": "IDENT", "name": "y"}
        var_offsets = {"y": 2}
        next_offset = 0
        
        code, updated_offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertEqual(code, "    ldr x0, [sp, #16]")
        self.assertEqual(updated_offset, 0)
        self.assertEqual(reg, "x0")
    
    def test_ident_undefined_variable(self):
        """Test IDENT expression with undefined variable."""
        expr = {"type": "IDENT", "name": "undefined_var"}
        var_offsets = {"x": 0}
        next_offset = 0
        
        with self.assertRaises(KeyError):
            generate_expression_code(expr, var_offsets, next_offset)
    
    def test_binary_add(self):
        """Test BINARY expression with addition."""
        expr = {
            "type": "BINARY",
            "op": "+",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 3}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        expected_lines = [
            "    mov x0, #5",
            "    mov x0, #3",
            "    add x0, x0, x1"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(updated_offset, 0)
        self.assertEqual(reg, "x0")
    
    def test_binary_subtract(self):
        """Test BINARY expression with subtraction."""
        expr = {
            "type": "BINARY",
            "op": "-",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 4}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        expected_lines = [
            "    mov x0, #10",
            "    mov x0, #4",
            "    sub x0, x0, x1"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(updated_offset, 0)
        self.assertEqual(reg, "x0")
    
    def test_binary_multiply(self):
        """Test BINARY expression with multiplication."""
        expr = {
            "type": "BINARY",
            "op": "*",
            "left": {"type": "LITERAL", "value": 6},
            "right": {"type": "LITERAL", "value": 7}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        expected_lines = [
            "    mov x0, #6",
            "    mov x0, #7",
            "    mul x0, x0, x1"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(updated_offset, 0)
        self.assertEqual(reg, "x0")
    
    def test_binary_divide(self):
        """Test BINARY expression with division."""
        expr = {
            "type": "BINARY",
            "op": "/",
            "left": {"type": "LITERAL", "value": 20},
            "right": {"type": "LITERAL", "value": 4}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        expected_lines = [
            "    mov x0, #20",
            "    mov x0, #4",
            "    udiv x0, x0, x1"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(updated_offset, 0)
        self.assertEqual(reg, "x0")
    
    def test_binary_equal(self):
        """Test BINARY expression with equality comparison."""
        expr = {
            "type": "BINARY",
            "op": "==",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        expected_lines = [
            "    mov x0, #5",
            "    mov x0, #5",
            "    cmp x0, x1",
            "    cset x0, eq"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(updated_offset, 0)
        self.assertEqual(reg, "x0")
    
    def test_binary_not_equal(self):
        """Test BINARY expression with not-equal comparison."""
        expr = {
            "type": "BINARY",
            "op": "!=",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 3}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        expected_lines = [
            "    mov x0, #5",
            "    mov x0, #3",
            "    cmp x0, x1",
            "    cset x0, ne"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(updated_offset, 0)
        self.assertEqual(reg, "x0")
    
    def test_binary_less_than(self):
        """Test BINARY expression with less-than comparison."""
        expr = {
            "type": "BINARY",
            "op": "<",
            "left": {"type": "LITERAL", "value": 3},
            "right": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        expected_lines = [
            "    mov x0, #3",
            "    mov x0, #5",
            "    cmp x0, x1",
            "    cset x0, lt"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(updated_offset, 0)
        self.assertEqual(reg, "x0")
    
    def test_binary_greater_than(self):
        """Test BINARY expression with greater-than comparison."""
        expr = {
            "type": "BINARY",
            "op": ">",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        expected_lines = [
            "    mov x0, #10",
            "    mov x0, #5",
            "    cmp x0, x1",
            "    cset x0, gt"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(updated_offset, 0)
        self.assertEqual(reg, "x0")
    
    def test_binary_less_than_or_equal(self):
        """Test BINARY expression with less-than-or-equal comparison."""
        expr = {
            "type": "BINARY",
            "op": "<=",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        expected_lines = [
            "    mov x0, #5",
            "    mov x0, #5",
            "    cmp x0, x1",
            "    cset x0, le"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(updated_offset, 0)
        self.assertEqual(reg, "x0")
    
    def test_binary_greater_than_or_equal(self):
        """Test BINARY expression with greater-than-or-equal comparison."""
        expr = {
            "type": "BINARY",
            "op": ">=",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        expected_lines = [
            "    mov x0, #10",
            "    mov x0, #5",
            "    cmp x0, x1",
            "    cset x0, ge"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(updated_offset, 0)
        self.assertEqual(reg, "x0")
    
    def test_binary_unsupported_operator(self):
        """Test BINARY expression with unsupported operator."""
        expr = {
            "type": "BINARY",
            "op": "%",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 3}
        }
        var_offsets = {}
        next_offset = 0
        
        with self.assertRaises(ValueError):
            generate_expression_code(expr, var_offsets, next_offset)
    
    def test_unary_neg(self):
        """Test UNARY expression with negation."""
        expr = {
            "type": "UNARY",
            "op": "neg",
            "operand": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        expected_lines = [
            "    mov x0, #5",
            "    neg x0, x0"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(updated_offset, 0)
        self.assertEqual(reg, "x0")
    
    def test_unary_not(self):
        """Test UNARY expression with logical not."""
        expr = {
            "type": "UNARY",
            "op": "not",
            "operand": {"type": "LITERAL", "value": 0}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        expected_lines = [
            "    mov x0, #0",
            "    cmp x0, #0",
            "    cset x0, eq"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(updated_offset, 0)
        self.assertEqual(reg, "x0")
    
    def test_unary_unsupported_operator(self):
        """Test UNARY expression with unsupported operator."""
        expr = {
            "type": "UNARY",
            "op": "abs",
            "operand": {"type": "LITERAL", "value": -5}
        }
        var_offsets = {}
        next_offset = 0
        
        with self.assertRaises(ValueError):
            generate_expression_code(expr, var_offsets, next_offset)
    
    def test_unsupported_expression_type(self):
        """Test unsupported expression type."""
        expr = {"type": "UNKNOWN"}
        var_offsets = {}
        next_offset = 0
        
        with self.assertRaises(ValueError):
            generate_expression_code(expr, var_offsets, next_offset)
    
    def test_nested_binary_expression(self):
        """Test nested BINARY expression."""
        expr = {
            "type": "BINARY",
            "op": "+",
            "left": {
                "type": "BINARY",
                "op": "*",
                "left": {"type": "LITERAL", "value": 2},
                "right": {"type": "LITERAL", "value": 3}
            },
            "right": {"type": "LITERAL", "value": 4}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("mov x0, #2", code)
        self.assertIn("mov x0, #3", code)
        self.assertIn("mul x0, x0, x1", code)
        self.assertIn("mov x0, #4", code)
        self.assertIn("add x0, x0, x1", code)
        self.assertEqual(updated_offset, 0)
        self.assertEqual(reg, "x0")
    
    def test_mixed_expression(self):
        """Test mixed expression with IDENT and LITERAL."""
        expr = {
            "type": "BINARY",
            "op": "+",
            "left": {"type": "IDENT", "name": "x"},
            "right": {"type": "LITERAL", "value": 10}
        }
        var_offsets = {"x": 1}
        next_offset = 0
        
        code, updated_offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        expected_lines = [
            "    ldr x0, [sp, #8]",
            "    mov x0, #10",
            "    add x0, x0, x1"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(updated_offset, 0)
        self.assertEqual(reg, "x0")
    
    def test_default_literal_value(self):
        """Test LITERAL expression with missing value (defaults to 0)."""
        expr = {"type": "LITERAL"}
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertEqual(code, "    mov x0, #0")
        self.assertEqual(updated_offset, 0)
        self.assertEqual(reg, "x0")
    
    def test_default_ident_name(self):
        """Test IDENT expression with missing name."""
        expr = {"type": "IDENT"}
        var_offsets = {}
        next_offset = 0
        
        with self.assertRaises(KeyError):
            generate_expression_code(expr, var_offsets, next_offset)


if __name__ == "__main__":
    unittest.main()
