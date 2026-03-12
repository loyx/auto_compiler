import unittest
from unittest.mock import patch

from .handle_assign_src import handle_assign


class TestHandleAssign(unittest.TestCase):
    
    @patch('handle_assign_package.handle_assign_src.generate_expression_code')
    def test_handle_assign_with_value(self, mock_gen_expr):
        """Test normal ASSIGN with value expression"""
        mock_gen_expr.return_value = "mov x0, #42"
        
        stmt = {
            "type": "ASSIGN",
            "target": "x",
            "value": {"type": "literal", "value": 42}
        }
        func_name = "main"
        var_offsets = {"x": 8}
        
        result = handle_assign(stmt, func_name, var_offsets)
        
        mock_gen_expr.assert_called_once_with(
            {"type": "literal", "value": 42},
            "main",
            {"x": 8}
        )
        self.assertEqual(result, "mov x0, #42\nstr x0, [sp, #8]")
    
    @patch('handle_assign_package.handle_assign_src.generate_expression_code')
    def test_handle_assign_without_value(self, mock_gen_expr):
        """Test ASSIGN without value (None)"""
        stmt = {
            "type": "ASSIGN",
            "target": "y",
            "value": None
        }
        func_name = "main"
        var_offsets = {"y": 16}
        
        result = handle_assign(stmt, func_name, var_offsets)
        
        mock_gen_expr.assert_not_called()
        self.assertEqual(result, "str x0, [sp, #16]")
    
    @patch('handle_assign_package.handle_assign_src.generate_expression_code')
    def test_handle_assign_target_not_in_offsets(self, mock_gen_expr):
        """Test when target variable is not in var_offsets (defaults to 0)"""
        mock_gen_expr.return_value = "mov x0, #10"
        
        stmt = {
            "type": "ASSIGN",
            "target": "z",
            "value": {"type": "literal", "value": 10}
        }
        func_name = "main"
        var_offsets = {"x": 8}
        
        result = handle_assign(stmt, func_name, var_offsets)
        
        self.assertEqual(result, "mov x0, #10\nstr x0, [sp, #0]")
    
    @patch('handle_assign_package.handle_assign_src.generate_expression_code')
    def test_handle_assign_zero_offset(self, mock_gen_expr):
        """Test when target variable has offset 0"""
        mock_gen_expr.return_value = "mov x0, #5"
        
        stmt = {
            "type": "ASSIGN",
            "target": "a",
            "value": {"type": "literal", "value": 5}
        }
        func_name = "main"
        var_offsets = {"a": 0}
        
        result = handle_assign(stmt, func_name, var_offsets)
        
        self.assertEqual(result, "mov x0, #5\nstr x0, [sp, #0]")
    
    @patch('handle_assign_package.handle_assign_src.generate_expression_code')
    def test_handle_assign_empty_var_offsets(self, mock_gen_expr):
        """Test with empty var_offsets dict"""
        mock_gen_expr.return_value = "mov x0, #100"
        
        stmt = {
            "type": "ASSIGN",
            "target": "temp",
            "value": {"type": "literal", "value": 100}
        }
        func_name = "test_func"
        var_offsets = {}
        
        result = handle_assign(stmt, func_name, var_offsets)
        
        self.assertEqual(result, "mov x0, #100\nstr x0, [sp, #0]")
    
    @patch('handle_assign_package.handle_assign_src.generate_expression_code')
    def test_handle_assign_large_offset(self, mock_gen_expr):
        """Test with large offset value"""
        mock_gen_expr.return_value = "mov x0, #1"
        
        stmt = {
            "type": "ASSIGN",
            "target": "big_var",
            "value": {"type": "literal", "value": 1}
        }
        func_name = "main"
        var_offsets = {"big_var": 256}
        
        result = handle_assign(stmt, func_name, var_offsets)
        
        self.assertEqual(result, "mov x0, #1\nstr x0, [sp, #256]")
    
    @patch('handle_assign_package.handle_assign_src.generate_expression_code')
    def test_handle_assign_complex_expression(self, mock_gen_expr):
        """Test with complex expression code"""
        mock_gen_expr.return_value = "ldr x1, [sp, #8]\nadd x0, x1, #5"
        
        stmt = {
            "type": "ASSIGN",
            "target": "result",
            "value": {"type": "binop", "op": "add", "left": {"type": "var", "name": "x"}, "right": {"type": "literal", "value": 5}}
        }
        func_name = "compute"
        var_offsets = {"result": 24, "x": 8}
        
        result = handle_assign(stmt, func_name, var_offsets)
        
        mock_gen_expr.assert_called_once()
        self.assertEqual(result, "ldr x1, [sp, #8]\nadd x0, x1, #5\nstr x0, [sp, #24]")
    
    @patch('handle_assign_package.handle_assign_src.generate_expression_code')
    def test_handle_assign_multiline_expression(self, mock_gen_expr):
        """Test expression code with multiple lines"""
        mock_gen_expr.return_value = "mov x0, #10\nmov x1, #20\nadd x0, x0, x1"
        
        stmt = {
            "type": "ASSIGN",
            "target": "sum",
            "value": {"type": "binop", "op": "add"}
        }
        func_name = "main"
        var_offsets = {"sum": 32}
        
        result = handle_assign(stmt, func_name, var_offsets)
        
        self.assertEqual(result, "mov x0, #10\nmov x1, #20\nadd x0, x0, x1\nstr x0, [sp, #32]")


if __name__ == "__main__":
    unittest.main()
