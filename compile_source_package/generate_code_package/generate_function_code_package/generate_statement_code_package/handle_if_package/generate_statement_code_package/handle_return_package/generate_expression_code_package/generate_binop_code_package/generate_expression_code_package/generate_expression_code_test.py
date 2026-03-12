import unittest
from unittest.mock import patch

from .generate_expression_code_src import generate_expression_code


class TestGenerateExpressionCode(unittest.TestCase):
    
    def test_var_expression(self):
        """Test VAR expression type - loads variable from stack"""
        expr = {"type": "VAR", "name": "x"}
        var_offsets = {"x": 16}
        next_offset = 32
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertEqual(code, "    ldr x0, [sp, #16]\n")
        self.assertEqual(updated_offset, 32)
        self.assertEqual(result_reg, "x0")
    
    def test_var_expression_zero_offset(self):
        """Test VAR expression with zero offset"""
        expr = {"type": "VAR", "name": "y"}
        var_offsets = {"y": 0}
        next_offset = 16
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertEqual(code, "    ldr x0, [sp, #0]\n")
        self.assertEqual(updated_offset, 16)
        self.assertEqual(result_reg, "x0")
    
    def test_var_not_found(self):
        """Test VAR expression when variable not in var_offsets"""
        expr = {"type": "VAR", "name": "missing_var"}
        var_offsets = {"x": 16}
        next_offset = 32
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("missing_var", str(context.exception))
        self.assertIn("not found", str(context.exception))
    
    def test_num_expression(self):
        """Test NUM expression type - emits mov instruction"""
        expr = {"type": "NUM", "value": 42}
        var_offsets = {}
        next_offset = 16
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertEqual(code, "    mov x0, #42\n")
        self.assertEqual(updated_offset, 16)
        self.assertEqual(result_reg, "x0")
    
    def test_num_expression_zero(self):
        """Test NUM expression with zero value"""
        expr = {"type": "NUM", "value": 0}
        var_offsets = {}
        next_offset = 16
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertEqual(code, "    mov x0, #0\n")
        self.assertEqual(updated_offset, 16)
        self.assertEqual(result_reg, "x0")
    
    def test_num_expression_negative(self):
        """Test NUM expression with negative value"""
        expr = {"type": "NUM", "value": -10}
        var_offsets = {}
        next_offset = 16
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertEqual(code, "    mov x0, #-10\n")
        self.assertEqual(updated_offset, 16)
        self.assertEqual(result_reg, "x0")
    
    def test_num_expression_large_value(self):
        """Test NUM expression with large value"""
        expr = {"type": "NUM", "value": 65535}
        var_offsets = {}
        next_offset = 16
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertEqual(code, "    mov x0, #65535\n")
        self.assertEqual(updated_offset, 16)
        self.assertEqual(result_reg, "x0")
    
    @patch('generate_expression_code_package.generate_binop_code_package.generate_binop_code_src.generate_binop_code')
    def test_binop_expression(self, mock_generate_binop_code):
        """Test BINOP expression type - delegates to generate_binop_code"""
        expr = {"type": "BINOP", "op": "ADD", "left": {"type": "NUM", "value": 1}, "right": {"type": "NUM", "value": 2}}
        var_offsets = {}
        next_offset = 16
        
        expected_code = "    add x0, x1, x2\n"
        expected_offset = 32
        expected_reg = "x0"
        mock_generate_binop_code.return_value = (expected_code, expected_offset, expected_reg)
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        mock_generate_binop_code.assert_called_once_with(expr, var_offsets, next_offset)
        self.assertEqual(code, expected_code)
        self.assertEqual(updated_offset, expected_offset)
        self.assertEqual(result_reg, expected_reg)
    
    @patch('generate_expression_code_package.generate_binop_code_package.generate_binop_code_src.generate_binop_code')
    def test_binop_expression_passes_arguments(self, mock_generate_binop_code):
        """Test BINOP expression passes correct arguments to generate_binop_code"""
        expr = {"type": "BINOP", "op": "MUL", "left": {"type": "VAR", "name": "a"}, "right": {"type": "NUM", "value": 5}}
        var_offsets = {"a": 24}
        next_offset = 48
        
        mock_generate_binop_code.return_value = ("    mul x0, x1, x2\n", 48, "x0")
        
        generate_expression_code(expr, var_offsets, next_offset)
        
        mock_generate_binop_code.assert_called_once_with(expr, var_offsets, next_offset)
    
    def test_unsupported_expression_type(self):
        """Test unsupported expression type raises ValueError"""
        expr = {"type": "UNKNOWN"}
        var_offsets = {}
        next_offset = 16
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("UNKNOWN", str(context.exception))
        self.assertIn("Unsupported expression type", str(context.exception))
    
    def test_empty_expr_type(self):
        """Test expression with missing type field"""
        expr = {}
        var_offsets = {}
        next_offset = 16
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("Unsupported expression type", str(context.exception))
    
    def test_var_multiple_variables(self):
        """Test VAR expression with multiple variables in var_offsets"""
        expr = {"type": "VAR", "name": "b"}
        var_offsets = {"a": 8, "b": 16, "c": 24}
        next_offset = 32
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertEqual(code, "    ldr x0, [sp, #16]\n")
        self.assertEqual(updated_offset, 32)
        self.assertEqual(result_reg, "x0")
    
    def test_num_does_not_modify_offset(self):
        """Test NUM expression does not modify next_offset"""
        expr = {"type": "NUM", "value": 100}
        var_offsets = {}
        next_offset = 100
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertEqual(updated_offset, next_offset)
    
    def test_var_does_not_modify_offset(self):
        """Test VAR expression does not modify next_offset"""
        expr = {"type": "VAR", "name": "x"}
        var_offsets = {"x": 8}
        next_offset = 100
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertEqual(updated_offset, next_offset)
    
    def test_code_has_proper_indentation(self):
        """Test that generated code has 4-space indentation"""
        expr_num = {"type": "NUM", "value": 5}
        expr_var = {"type": "VAR", "name": "x"}
        var_offsets = {"x": 8}
        
        code_num, _, _ = generate_expression_code(expr_num, {}, 0)
        code_var, _, _ = generate_expression_code(expr_var, var_offsets, 0)
        
        self.assertTrue(code_num.startswith("    "))
        self.assertTrue(code_var.startswith("    "))
    
    def test_code_ends_with_newline(self):
        """Test that generated code ends with newline"""
        expr_num = {"type": "NUM", "value": 5}
        expr_var = {"type": "VAR", "name": "x"}
        var_offsets = {"x": 8}
        
        code_num, _, _ = generate_expression_code(expr_num, {}, 0)
        code_var, _, _ = generate_expression_code(expr_var, var_offsets, 0)
        
        self.assertTrue(code_num.endswith("\n"))
        self.assertTrue(code_var.endswith("\n"))


if __name__ == "__main__":
    unittest.main()
