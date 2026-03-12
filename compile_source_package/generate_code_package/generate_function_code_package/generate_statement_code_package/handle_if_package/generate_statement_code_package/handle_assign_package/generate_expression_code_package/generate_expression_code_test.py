import unittest

# Relative import from the package
from .generate_expression_code_src import generate_expression_code


class TestGenerateExpressionCode(unittest.TestCase):
    """Test cases for generate_expression_code function."""
    
    def test_literal_int(self):
        """Test LITERAL expression with integer value."""
        expr = {"type": "LITERAL", "value": 42}
        var_offsets = {}
        next_offset = 0
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("mov x0, #42", code)
        self.assertEqual(offset, 0)
        self.assertEqual(reg, "x0")
    
    def test_literal_float(self):
        """Test LITERAL expression with float value."""
        expr = {"type": "LITERAL", "value": 3.14}
        var_offsets = {}
        next_offset = 0
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertTrue("fmov v0" in code or "ldr v0" in code)
        self.assertEqual(offset, 0)
        self.assertEqual(reg, "v0")
    
    def test_literal_negative_int(self):
        """Test LITERAL expression with negative integer value."""
        expr = {"type": "LITERAL", "value": -10}
        var_offsets = {}
        next_offset = 0
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("mov x0, #-10", code)
        self.assertEqual(offset, 0)
        self.assertEqual(reg, "x0")
    
    def test_ident_defined_variable(self):
        """Test IDENT expression with defined variable."""
        expr = {"type": "IDENT", "name": "x"}
        var_offsets = {"x": 0}
        next_offset = 5
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("ldr x0, [sp, #0]", code)
        self.assertEqual(offset, 5)
        self.assertEqual(reg, "x0")
    
    def test_ident_undefined_variable(self):
        """Test IDENT expression with undefined variable raises ValueError."""
        expr = {"type": "IDENT", "name": "undefined_var"}
        var_offsets = {"x": 0}
        next_offset = 0
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("undefined_var", str(context.exception))
    
    def test_binary_addition(self):
        """Test BINARY expression with addition operator."""
        expr = {
            "type": "BINARY",
            "op": "+",
            "left": {"type": "LITERAL", "value": 3},
            "right": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        next_offset = 0
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("add x0", code)
        self.assertEqual(reg, "x0")
    
    def test_binary_subtraction(self):
        """Test BINARY expression with subtraction operator."""
        expr = {
            "type": "BINARY",
            "op": "-",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 3}
        }
        var_offsets = {}
        next_offset = 0
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("sub x0", code)
        self.assertEqual(reg, "x0")
    
    def test_binary_multiplication(self):
        """Test BINARY expression with multiplication operator."""
        expr = {
            "type": "BINARY",
            "op": "*",
            "left": {"type": "LITERAL", "value": 4},
            "right": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        next_offset = 0
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("mul x0", code)
        self.assertEqual(reg, "x0")
    
    def test_binary_division(self):
        """Test BINARY expression with division operator."""
        expr = {
            "type": "BINARY",
            "op": "/",
            "left": {"type": "LITERAL", "value": 20},
            "right": {"type": "LITERAL", "value": 4}
        }
        var_offsets = {}
        next_offset = 0
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("sdiv x0", code)
        self.assertEqual(reg, "x0")
    
    def test_binary_equality(self):
        """Test BINARY expression with equality operator."""
        expr = {
            "type": "BINARY",
            "op": "==",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        next_offset = 0
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("cmp x", code)
        self.assertEqual(reg, "x0")
    
    def test_binary_inequality(self):
        """Test BINARY expression with inequality operator."""
        expr = {
            "type": "BINARY",
            "op": "!=",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 3}
        }
        var_offsets = {}
        next_offset = 0
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("cmp x", code)
        self.assertEqual(reg, "x0")
    
    def test_binary_less_than(self):
        """Test BINARY expression with less than operator."""
        expr = {
            "type": "BINARY",
            "op": "<",
            "left": {"type": "LITERAL", "value": 3},
            "right": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        next_offset = 0
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("cmp x", code)
        self.assertEqual(reg, "x0")
    
    def test_binary_greater_than(self):
        """Test BINARY expression with greater than operator."""
        expr = {
            "type": "BINARY",
            "op": ">",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        next_offset = 0
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("cmp x", code)
        self.assertEqual(reg, "x0")
    
    def test_binary_less_equal(self):
        """Test BINARY expression with less than or equal operator."""
        expr = {
            "type": "BINARY",
            "op": "<=",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        next_offset = 0
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("cmp x", code)
        self.assertEqual(reg, "x0")
    
    def test_binary_greater_equal(self):
        """Test BINARY expression with greater than or equal operator."""
        expr = {
            "type": "BINARY",
            "op": ">=",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        next_offset = 0
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("cmp x", code)
        self.assertEqual(reg, "x0")
    
    def test_binary_logical_and(self):
        """Test BINARY expression with logical AND operator."""
        expr = {
            "type": "BINARY",
            "op": "&&",
            "left": {"type": "LITERAL", "value": 1},
            "right": {"type": "LITERAL", "value": 0}
        }
        var_offsets = {}
        next_offset = 0
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("and x0", code)
        self.assertEqual(reg, "x0")
    
    def test_binary_logical_or(self):
        """Test BINARY expression with logical OR operator."""
        expr = {
            "type": "BINARY",
            "op": "||",
            "left": {"type": "LITERAL", "value": 1},
            "right": {"type": "LITERAL", "value": 0}
        }
        var_offsets = {}
        next_offset = 0
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("orr x0", code)
        self.assertEqual(reg, "x0")
    
    def test_binary_with_ident_operands(self):
        """Test BINARY expression with variable operands."""
        expr = {
            "type": "BINARY",
            "op": "+",
            "left": {"type": "IDENT", "name": "x"},
            "right": {"type": "IDENT", "name": "y"}
        }
        var_offsets = {"x": 0, "y": 1}
        next_offset = 2
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("ldr x0, [sp, #0]", code)
        self.assertIn("ldr x", code)
        self.assertIn("add x0", code)
        self.assertEqual(reg, "x0")
    
    def test_unary_negation(self):
        """Test UNARY expression with negation operator."""
        expr = {
            "type": "UNARY",
            "op": "-",
            "operand": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        next_offset = 0
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("neg x0, x0", code)
        self.assertEqual(reg, "x0")
    
    def test_unary_logical_not(self):
        """Test UNARY expression with logical NOT operator."""
        expr = {
            "type": "UNARY",
            "op": "!",
            "operand": {"type": "LITERAL", "value": 0}
        }
        var_offsets = {}
        next_offset = 0
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertTrue("not" in code.lower() or "cmp" in code or "mvn" in code)
        self.assertEqual(reg, "x0")
    
    def test_unary_with_ident_operand(self):
        """Test UNARY expression with variable operand."""
        expr = {
            "type": "UNARY",
            "op": "-",
            "operand": {"type": "IDENT", "name": "x"}
        }
        var_offsets = {"x": 0}
        next_offset = 1
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("ldr x0, [sp, #0]", code)
        self.assertIn("neg x0, x0", code)
        self.assertEqual(reg, "x0")
    
    def test_nested_expression(self):
        """Test nested expression: (3 + 5) * 2."""
        expr = {
            "type": "BINARY",
            "op": "*",
            "left": {
                "type": "BINARY",
                "op": "+",
                "left": {"type": "LITERAL", "value": 3},
                "right": {"type": "LITERAL", "value": 5}
            },
            "right": {"type": "LITERAL", "value": 2}
        }
        var_offsets = {}
        next_offset = 0
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("add x", code)
        self.assertIn("mul x0", code)
        self.assertEqual(reg, "x0")
    
    def test_complex_nested_expression(self):
        """Test complex nested expression: -(a + b)."""
        expr = {
            "type": "UNARY",
            "op": "-",
            "operand": {
                "type": "BINARY",
                "op": "+",
                "left": {"type": "IDENT", "name": "a"},
                "right": {"type": "IDENT", "name": "b"}
            }
        }
        var_offsets = {"a": 0, "b": 1}
        next_offset = 2
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("ldr x", code)
        self.assertIn("add x", code)
        self.assertIn("neg x0, x0", code)
        self.assertEqual(reg, "x0")
    
    def test_unknown_expression_type(self):
        """Test unknown expression type raises ValueError."""
        expr = {"type": "UNKNOWN_TYPE", "value": 42}
        var_offsets = {}
        next_offset = 0
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("UNKNOWN_TYPE", str(context.exception))
    
    def test_assembly_code_indentation(self):
        """Test that all assembly lines are indented with 4 spaces."""
        expr = {"type": "LITERAL", "value": 10}
        var_offsets = {}
        next_offset = 0
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        lines = code.strip().split('\n')
        for line in lines:
            if line.strip():
                self.assertTrue(line.startswith("    "), f"Line not properly indented: {repr(line)}")
    
    def test_var_offsets_not_modified_for_literal(self):
        """Test that var_offsets is not modified for LITERAL expressions."""
        expr = {"type": "LITERAL", "value": 42}
        var_offsets = {"x": 0}
        original_offsets = var_offsets.copy()
        next_offset = 0
        
        generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertEqual(var_offsets, original_offsets)
    
    def test_var_offsets_not_modified_for_binary(self):
        """Test that var_offsets is not modified for BINARY expressions."""
        expr = {
            "type": "BINARY",
            "op": "+",
            "left": {"type": "LITERAL", "value": 1},
            "right": {"type": "LITERAL", "value": 2}
        }
        var_offsets = {"x": 0}
        original_offsets = var_offsets.copy()
        next_offset = 0
        
        generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertEqual(var_offsets, original_offsets)


if __name__ == "__main__":
    unittest.main()