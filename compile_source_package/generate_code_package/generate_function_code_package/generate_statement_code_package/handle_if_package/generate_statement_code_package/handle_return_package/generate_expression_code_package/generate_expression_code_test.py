import unittest
from unittest.mock import patch

# Relative import from the same package
from .generate_expression_code_src import generate_expression_code


class TestGenerateExpressionCode(unittest.TestCase):
    """Test cases for generate_expression_code function."""
    
    @patch('generate_expression_code_package.generate_num_code_package.generate_num_code_src.generate_num_code')
    def test_num_expression(self, mock_generate_num_code):
        """Test NUM expression type delegation"""
        mock_generate_num_code.return_value = ("mov x0, #42", 0, "x0")
        
        expr = {"type": "NUM", "value": 42}
        var_offsets = {}
        next_offset = 0
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        mock_generate_num_code.assert_called_once_with(expr, next_offset)
        self.assertEqual(code, "mov x0, #42")
        self.assertEqual(offset, 0)
        self.assertEqual(reg, "x0")
    
    @patch('generate_expression_code_package.generate_var_code_package.generate_var_code_src.generate_var_code')
    def test_var_expression(self, mock_generate_var_code):
        """Test VAR expression type delegation"""
        mock_generate_var_code.return_value = ("ldr x0, [sp, #8]", 0, "x0")
        
        expr = {"type": "VAR", "name": "x"}
        var_offsets = {"x": 8}
        next_offset = 0
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        mock_generate_var_code.assert_called_once_with(expr, var_offsets, next_offset)
        self.assertEqual(code, "ldr x0, [sp, #8]")
        self.assertEqual(offset, 0)
        self.assertEqual(reg, "x0")
    
    @patch('generate_expression_code_package.generate_binop_code_package.generate_binop_code_src.generate_binop_code')
    def test_binop_expression(self, mock_generate_binop_code):
        """Test BINOP expression type delegation"""
        mock_generate_binop_code.return_value = ("add x0, x1, x2", 0, "x0")
        
        expr = {
            "type": "BINOP",
            "op": "ADD",
            "left": {"type": "NUM", "value": 3},
            "right": {"type": "NUM", "value": 2}
        }
        var_offsets = {}
        next_offset = 0
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        mock_generate_binop_code.assert_called_once_with(expr, var_offsets, next_offset)
        self.assertEqual(code, "add x0, x1, x2")
        self.assertEqual(offset, 0)
        self.assertEqual(reg, "x0")
    
    @patch('generate_expression_code_package.generate_call_code_package.generate_call_code_src.generate_call_code')
    def test_call_expression(self, mock_generate_call_code):
        """Test CALL expression type delegation"""
        mock_generate_call_code.return_value = ("bl func", 0, "x0")
        
        expr = {
            "type": "CALL",
            "func_name": "func",
            "args": [{"type": "NUM", "value": 1}]
        }
        var_offsets = {}
        next_offset = 0
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        mock_generate_call_code.assert_called_once_with(expr, var_offsets, next_offset)
        self.assertEqual(code, "bl func")
        self.assertEqual(offset, 0)
        self.assertEqual(reg, "x0")
    
    def test_unknown_expression_type(self):
        """Test error handling for unknown expression type"""
        expr = {"type": "UNKNOWN"}
        var_offsets = {}
        next_offset = 0
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("Unknown expression type: UNKNOWN", str(context.exception))
    
    @patch('generate_expression_code_package.generate_num_code_package.generate_num_code_src.generate_num_code')
    def test_num_expression_with_offset(self, mock_generate_num_code):
        """Test NUM expression with non-zero offset"""
        mock_generate_num_code.return_value = ("mov x0, #100", 16, "x0")
        
        expr = {"type": "NUM", "value": 100}
        var_offsets = {"x": 8}
        next_offset = 16
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        mock_generate_num_code.assert_called_once_with(expr, next_offset)
        self.assertEqual(offset, 16)
    
    @patch('generate_expression_code_package.generate_var_code_package.generate_var_code_src.generate_var_code')
    def test_var_expression_with_multiple_vars(self, mock_generate_var_code):
        """Test VAR expression with multiple variables in var_offsets"""
        mock_generate_var_code.return_value = ("ldr x0, [sp, #16]", 0, "x0")
        
        expr = {"type": "VAR", "name": "z"}
        var_offsets = {"x": 8, "y": 16, "z": 16}
        next_offset = 24
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        mock_generate_var_code.assert_called_once_with(expr, var_offsets, next_offset)
        self.assertEqual(reg, "x0")
    
    @patch('generate_expression_code_package.generate_binop_code_package.generate_binop_code_src.generate_binop_code')
    def test_binop_expression_nested(self, mock_generate_binop_code):
        """Test BINOP expression with nested operations"""
        mock_generate_binop_code.return_value = ("mul x0, x1, x2", 0, "x0")
        
        expr = {
            "type": "BINOP",
            "op": "MUL",
            "left": {
                "type": "BINOP",
                "op": "ADD",
                "left": {"type": "NUM", "value": 1},
                "right": {"type": "NUM", "value": 2}
            },
            "right": {"type": "NUM", "value": 3}
        }
        var_offsets = {}
        next_offset = 0
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        mock_generate_binop_code.assert_called_once_with(expr, var_offsets, next_offset)
        self.assertEqual(reg, "x0")
    
    @patch('generate_expression_code_package.generate_call_code_package.generate_call_code_src.generate_call_code')
    def test_call_expression_multiple_args(self, mock_generate_call_code):
        """Test CALL expression with multiple arguments"""
        mock_generate_call_code.return_value = ("bl multi_arg_func", 0, "x0")
        
        expr = {
            "type": "CALL",
            "func_name": "multi_arg_func",
            "args": [
                {"type": "NUM", "value": 1},
                {"type": "NUM", "value": 2},
                {"type": "NUM", "value": 3}
            ]
        }
        var_offsets = {}
        next_offset = 0
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        mock_generate_call_code.assert_called_once_with(expr, var_offsets, next_offset)
        self.assertEqual(code, "bl multi_arg_func")
    
    @patch('generate_expression_code_package.generate_num_code_package.generate_num_code_src.generate_num_code')
    def test_num_expression_negative_value(self, mock_generate_num_code):
        """Test NUM expression with negative value"""
        mock_generate_num_code.return_value = ("mov x0, #-5", 0, "x0")
        
        expr = {"type": "NUM", "value": -5}
        var_offsets = {}
        next_offset = 0
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        mock_generate_num_code.assert_called_once_with(expr, next_offset)
        self.assertEqual(code, "mov x0, #-5")
    
    @patch('generate_expression_code_package.generate_num_code_package.generate_num_code_src.generate_num_code')
    def test_num_expression_zero_value(self, mock_generate_num_code):
        """Test NUM expression with zero value"""
        mock_generate_num_code.return_value = ("mov x0, #0", 0, "x0")
        
        expr = {"type": "NUM", "value": 0}
        var_offsets = {}
        next_offset = 0
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        mock_generate_num_code.assert_called_once_with(expr, next_offset)
        self.assertEqual(code, "mov x0, #0")
    
    def test_missing_type_field(self):
        """Test error handling when type field is missing"""
        expr = {"value": 42}
        var_offsets = {}
        next_offset = 0
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("Unknown expression type: None", str(context.exception))
    
    @patch('generate_expression_code_package.generate_num_code_package.generate_num_code_src.generate_num_code')
    def test_num_expression_preserves_var_offsets(self, mock_generate_num_code):
        """Test that NUM expression doesn't modify var_offsets"""
        mock_generate_num_code.return_value = ("mov x0, #1", 0, "x0")
        
        expr = {"type": "NUM", "value": 1}
        var_offsets = {"x": 8, "y": 16}
        next_offset = 24
        
        generate_expression_code(expr, var_offsets, next_offset)
        
        mock_generate_num_code.assert_called_once_with(expr, next_offset)
    
    @patch('generate_expression_code_package.generate_call_code_package.generate_call_code_src.generate_call_code')
    def test_call_expression_no_args(self, mock_generate_call_code):
        """Test CALL expression with no arguments"""
        mock_generate_call_code.return_value = ("bl no_arg_func", 0, "x0")
        
        expr = {
            "type": "CALL",
            "func_name": "no_arg_func",
            "args": []
        }
        var_offsets = {}
        next_offset = 0
        
        code, offset, reg = generate_expression_code(expr, var_offsets, next_offset)
        
        mock_generate_call_code.assert_called_once_with(expr, var_offsets, next_offset)
        self.assertEqual(code, "bl no_arg_func")


if __name__ == '__main__':
    unittest.main()
