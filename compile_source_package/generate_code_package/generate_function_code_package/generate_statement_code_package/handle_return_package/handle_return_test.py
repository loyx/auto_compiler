import unittest
from unittest.mock import patch

from .handle_return_src import handle_return


class TestHandleReturn(unittest.TestCase):
    
    def test_return_with_value_expression(self):
        """Test RETURN statement with a value expression"""
        stmt = {
            "type": "RETURN",
            "value": {"operation": "const", "operand": 42}
        }
        func_name = "test_func"
        var_offsets = {"x": 0}
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_return_package.handle_return_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = "mov x0, #42"
            
            result = handle_return(stmt, func_name, var_offsets)
            
            mock_gen_expr.assert_called_once_with({"operation": "const", "operand": 42}, "test_func", {"x": 0})
            self.assertEqual(result, "mov x0, #42\nb test_func_exit")
    
    def test_return_without_value(self):
        """Test RETURN statement without a value (None)"""
        stmt = {
            "type": "RETURN",
            "value": None
        }
        func_name = "test_func"
        var_offsets = {"x": 0}
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_return_package.handle_return_src.generate_expression_code") as mock_gen_expr:
            result = handle_return(stmt, func_name, var_offsets)
            
            mock_gen_expr.assert_not_called()
            self.assertEqual(result, "b test_func_exit")
    
    def test_return_with_empty_dict_value(self):
        """Test RETURN statement with empty dict value"""
        stmt = {
            "type": "RETURN",
            "value": {}
        }
        func_name = "test_func"
        var_offsets = {"x": 0}
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_return_package.handle_return_src.generate_expression_code") as mock_gen_expr:
            result = handle_return(stmt, func_name, var_offsets)
            
            mock_gen_expr.assert_not_called()
            self.assertEqual(result, "b test_func_exit")
    
    def test_return_with_empty_expression_code(self):
        """Test RETURN when generate_expression_code returns empty string"""
        stmt = {
            "type": "RETURN",
            "value": {"operation": "const", "operand": 0}
        }
        func_name = "my_func"
        var_offsets = {}
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_return_package.handle_return_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ""
            
            result = handle_return(stmt, func_name, var_offsets)
            
            mock_gen_expr.assert_called_once()
            self.assertEqual(result, "b my_func_exit")
    
    def test_return_with_multiple_lines(self):
        """Test RETURN with expression that generates multiple code lines"""
        stmt = {
            "type": "RETURN",
            "value": {"operation": "add", "left": 1, "right": 2}
        }
        func_name = "calculate"
        var_offsets = {"a": 0, "b": 1}
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_return_package.handle_return_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = "mov x0, #1\nmov x1, #2\nadd x0, x0, x1"
            
            result = handle_return(stmt, func_name, var_offsets)
            
            expected = "mov x0, #1\nmov x1, #2\nadd x0, x0, x1\nb calculate_exit"
            self.assertEqual(result, expected)
    
    def test_return_with_no_value_key(self):
        """Test RETURN statement without value key at all"""
        stmt = {
            "type": "RETURN"
        }
        func_name = "void_func"
        var_offsets = {}
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_return_package.handle_return_src.generate_expression_code") as mock_gen_expr:
            result = handle_return(stmt, func_name, var_offsets)
            
            mock_gen_expr.assert_not_called()
            self.assertEqual(result, "b void_func_exit")


if __name__ == "__main__":
    unittest.main()
