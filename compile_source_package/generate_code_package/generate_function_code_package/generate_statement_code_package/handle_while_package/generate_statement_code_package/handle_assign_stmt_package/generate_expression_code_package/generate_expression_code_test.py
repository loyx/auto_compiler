# === std / third-party imports ===
import unittest
from typing import Dict

# === sub function imports ===
from .generate_expression_code_src import generate_expression_code

# === Test Class ===
class TestGenerateExpressionCode(unittest.TestCase):
    """Unit tests for generate_expression_code function."""
    
    def test_const_expression_simple(self):
        """Test CONST expression with simple integer value."""
        expr = {"type": "CONST", "value": 42}
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        code, new_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("MOV R0, 42", code)
        self.assertIn("PUSH R0", code)
        self.assertEqual(new_offset, 0)
        self.assertEqual(len(var_offsets), 0)
    
    def test_const_expression_zero(self):
        """Test CONST expression with zero value."""
        expr = {"type": "CONST", "value": 0}
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        code, new_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("MOV R0, 0", code)
        self.assertEqual(new_offset, 0)
    
    def test_const_expression_negative(self):
        """Test CONST expression with negative value."""
        expr = {"type": "CONST", "value": -100}
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        code, new_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("MOV R0, -100", code)
        self.assertEqual(new_offset, 0)
    
    def test_var_expression_defined(self):
        """Test VAR expression with defined variable."""
        expr = {"type": "VAR", "name": "x"}
        var_offsets: Dict[str, int] = {"x": 16}
        next_offset = 0
        
        code, new_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("MOV R0, [RBP-16]", code)
        self.assertIn("PUSH R0", code)
        self.assertEqual(new_offset, 0)
        self.assertEqual(var_offsets["x"], 16)
    
    def test_var_expression_undefined(self):
        """Test VAR expression with undefined variable raises ValueError."""
        expr = {"type": "VAR", "name": "undefined_var"}
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("Undefined variable", str(context.exception))
    
    def test_binop_expression_addition(self):
        """Test BINOP expression with addition operator."""
        expr = {
            "type": "BINOP",
            "op": "+",
            "left": {"type": "CONST", "value": 5},
            "right": {"type": "CONST", "value": 3}
        }
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        code, new_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("ADD", code)
        self.assertIn("MOV R0, 5", code)
        self.assertIn("MOV R0, 3", code)
        self.assertEqual(new_offset, 16)
        self.assertEqual(len(var_offsets), 2)
    
    def test_binop_expression_subtraction(self):
        """Test BINOP expression with subtraction operator."""
        expr = {
            "type": "BINOP",
            "op": "-",
            "left": {"type": "CONST", "value": 10},
            "right": {"type": "CONST", "value": 4}
        }
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        code, new_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("SUB", code)
        self.assertEqual(new_offset, 16)
    
    def test_binop_expression_multiplication(self):
        """Test BINOP expression with multiplication operator."""
        expr = {
            "type": "BINOP",
            "op": "*",
            "left": {"type": "CONST", "value": 6},
            "right": {"type": "CONST", "value": 7}
        }
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        code, new_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("MUL", code)
        self.assertEqual(new_offset, 16)
    
    def test_binop_expression_division(self):
        """Test BINOP expression with division operator."""
        expr = {
            "type": "BINOP",
            "op": "/",
            "left": {"type": "CONST", "value": 20},
            "right": {"type": "CONST", "value": 4}
        }
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        code, new_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("DIV", code)
        self.assertEqual(new_offset, 16)
    
    def test_binop_expression_with_variables(self):
        """Test BINOP expression with variable operands."""
        expr = {
            "type": "BINOP",
            "op": "+",
            "left": {"type": "VAR", "name": "a"},
            "right": {"type": "VAR", "name": "b"}
        }
        var_offsets: Dict[str, int] = {"a": 8, "b": 16}
        next_offset = 0
        
        code, new_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("ADD", code)
        self.assertIn("MOV R0, [RBP-8]", code)
        self.assertIn("MOV R0, [RBP-16]", code)
        self.assertEqual(new_offset, 16)
    
    def test_binop_expression_nested(self):
        """Test nested BINOP expression (a + b) * c."""
        expr = {
            "type": "BINOP",
            "op": "*",
            "left": {
                "type": "BINOP",
                "op": "+",
                "left": {"type": "VAR", "name": "a"},
                "right": {"type": "VAR", "name": "b"}
            },
            "right": {"type": "VAR", "name": "c"}
        }
        var_offsets: Dict[str, int] = {"a": 8, "b": 16, "c": 24}
        next_offset = 0
        
        code, new_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("ADD", code)
        self.assertIn("MUL", code)
        self.assertGreater(new_offset, 16)
    
    def test_binop_var_offsets_modified_inplace(self):
        """Test that var_offsets is modified in-place with temporary variables."""
        expr = {
            "type": "BINOP",
            "op": "+",
            "left": {"type": "CONST", "value": 1},
            "right": {"type": "CONST", "value": 2}
        }
        var_offsets: Dict[str, int] = {"existing": 8}
        next_offset = 0
        original_id = id(var_offsets)
        
        code, new_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertEqual(id(var_offsets), original_id)
        self.assertIn("existing", var_offsets)
        self.assertTrue(any(k.startswith("_temp_") for k in var_offsets.keys()))
    
    def test_binop_next_offset_increments(self):
        """Test that next_offset increments by 8 for each temporary."""
        expr = {
            "type": "BINOP",
            "op": "+",
            "left": {"type": "CONST", "value": 1},
            "right": {"type": "CONST", "value": 2}
        }
        var_offsets: Dict[str, int] = {}
        next_offset = 100
        
        code, new_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertEqual(new_offset, 116)
    
    def test_unknown_expression_type(self):
        """Test unknown expression type raises ValueError."""
        expr = {"type": "UNKNOWN"}
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("Unknown expression type", str(context.exception))
    
    def test_empty_expr_dict(self):
        """Test empty expression dict raises ValueError."""
        expr: Dict = {}
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("Unknown expression type", str(context.exception))
    
    def test_binop_mixed_const_var(self):
        """Test BINOP with mixed constant and variable operands."""
        expr = {
            "type": "BINOP",
            "op": "-",
            "left": {"type": "CONST", "value": 100},
            "right": {"type": "VAR", "name": "x"}
        }
        var_offsets: Dict[str, int] = {"x": 32}
        next_offset = 0
        
        code, new_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("SUB", code)
        self.assertIn("MOV R0, 100", code)
        self.assertIn("MOV R0, [RBP-32]", code)
        self.assertEqual(new_offset, 16)
    
    def test_return_type_tuple(self):
        """Test that return type is tuple of (str, int)."""
        expr = {"type": "CONST", "value": 1}
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        result = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], str)
        self.assertIsInstance(result[1], int)


# === Main entry point ===
if __name__ == "__main__":
    unittest.main()
