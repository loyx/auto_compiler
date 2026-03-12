import unittest
from unittest.mock import patch

from .handle_expression_stmt_src import handle_expression_stmt


class TestHandleExpressionStmt(unittest.TestCase):
    """Test cases for handle_expression_stmt function."""
    
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_expression_stmt_package.handle_expression_stmt_src.generate_expression_code')
    def test_empty_args(self, mock_gen_expr):
        """Test EXPRESSION statement with no arguments."""
        stmt = {
            "type": "EXPRESSION",
            "func_name": "my_function",
            "args": []
        }
        result = handle_expression_stmt(stmt, "current_func", {})
        
        # Should only generate the bl instruction
        self.assertEqual(result, "bl my_function")
        mock_gen_expr.assert_not_called()
    
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_expression_stmt_package.handle_expression_stmt_src.generate_expression_code')
    def test_single_argument(self, mock_gen_expr):
        """Test EXPRESSION statement with one argument."""
        mock_gen_expr.return_value = "ldr x0, [sp, #0]"
        
        stmt = {
            "type": "EXPRESSION",
            "func_name": "my_function",
            "args": [{"type": "CONST", "value": 42}]
        }
        result = handle_expression_stmt(stmt, "current_func", {})
        
        # Should generate arg code + bl instruction (no mov for single arg)
        self.assertEqual(result, "ldr x0, [sp, #0]\nbl my_function")
        mock_gen_expr.assert_called_once_with({"type": "CONST", "value": 42}, "current_func", {})
    
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_expression_stmt_package.handle_expression_stmt_src.generate_expression_code')
    def test_two_arguments(self, mock_gen_expr):
        """Test EXPRESSION statement with two arguments."""
        mock_gen_expr.return_value = "ldr x0, [sp, #0]"
        
        stmt = {
            "type": "EXPRESSION",
            "func_name": "add_func",
            "args": [
                {"type": "CONST", "value": 1},
                {"type": "CONST", "value": 2}
            ]
        }
        result = handle_expression_stmt(stmt, "current_func", {})
        
        # First arg in x0, mov to x1, second arg in x0, then bl
        expected = "ldr x0, [sp, #0]\nmov x1, x0\nldr x0, [sp, #0]\nbl add_func"
        self.assertEqual(result, expected)
        self.assertEqual(mock_gen_expr.call_count, 2)
    
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_expression_stmt_package.handle_expression_stmt_src.generate_expression_code')
    def test_eight_arguments(self, mock_gen_expr):
        """Test EXPRESSION statement with exactly 8 arguments (ARM64 limit)."""
        mock_gen_expr.return_value = "ldr x0, [sp, #0]"
        
        args = [{"type": "CONST", "value": i} for i in range(8)]
        stmt = {
            "type": "EXPRESSION",
            "func_name": "eight_arg_func",
            "args": args
        }
        
        result = handle_expression_stmt(stmt, "current_func", {})
        
        # Should generate 8 arg loads + 7 mov instructions + bl
        expected_lines = ["ldr x0, [sp, #0]"]  # arg 0
        for i in range(1, 8):
            expected_lines.append("mov x{}, x0".format(i))  # mov to x1-x7
            expected_lines.append("ldr x0, [sp, #0]")  # arg i
        
        expected_lines.append("bl eight_arg_func")
        expected = "\n".join(expected_lines)
        
        self.assertEqual(result, expected)
        self.assertEqual(mock_gen_expr.call_count, 8)
    
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_expression_stmt_package.handle_expression_stmt_src.generate_expression_code')
    def test_more_than_eight_arguments(self, mock_gen_expr):
        """Test EXPRESSION statement with more than 8 arguments (should only process first 8)."""
        mock_gen_expr.return_value = "ldr x0, [sp, #0]"
        
        args = [{"type": "CONST", "value": i} for i in range(10)]
        stmt = {
            "type": "EXPRESSION",
            "func_name": "many_arg_func",
            "args": args
        }
        
        result = handle_expression_stmt(stmt, "current_func", {})
        
        # Should only process first 8 arguments
        self.assertEqual(mock_gen_expr.call_count, 8)
        
        # Verify bl instruction is present
        self.assertIn("bl many_arg_func", result)
    
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_expression_stmt_package.handle_expression_stmt_src.generate_expression_code')
    def test_missing_func_name(self, mock_gen_expr):
        """Test EXPRESSION statement with missing func_name."""
        stmt = {
            "type": "EXPRESSION",
            "args": []
        }
        
        result = handle_expression_stmt(stmt, "current_func", {})
        
        # Should use empty string for func_name
        self.assertEqual(result, "bl ")
    
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_expression_stmt_package.handle_expression_stmt_src.generate_expression_code')
    def test_missing_args(self, mock_gen_expr):
        """Test EXPRESSION statement with missing args."""
        stmt = {
            "type": "EXPRESSION",
            "func_name": "my_function"
        }
        
        result = handle_expression_stmt(stmt, "current_func", {})
        
        # Should use empty list for args
        self.assertEqual(result, "bl my_function")
        mock_gen_expr.assert_not_called()
    
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_expression_stmt_package.handle_expression_stmt_src.generate_expression_code')
    def test_var_offsets_passed_to_generate_expression_code(self, mock_gen_expr):
        """Test that var_offsets are passed correctly to generate_expression_code."""
        mock_gen_expr.return_value = "ldr x0, [sp, #0]"
        
        var_offsets = {"x": 0, "y": 8}
        stmt = {
            "type": "EXPRESSION",
            "func_name": "my_function",
            "args": [{"type": "VAR", "name": "x"}]
        }
        
        handle_expression_stmt(stmt, "current_func", var_offsets)
        
        mock_gen_expr.assert_called_once_with({"type": "VAR", "name": "x"}, "current_func", var_offsets)
    
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_expression_stmt_package.handle_expression_stmt_src.generate_expression_code')
    def test_func_name_context_passed_to_generate_expression_code(self, mock_gen_expr):
        """Test that func_name context is passed correctly to generate_expression_code."""
        mock_gen_expr.return_value = "ldr x0, [sp, #0]"
        
        stmt = {
            "type": "EXPRESSION",
            "func_name": "my_function",
            "args": [{"type": "CONST", "value": 42}]
        }
        
        handle_expression_stmt(stmt, "enclosing_function", {})
        
        mock_gen_expr.assert_called_once_with({"type": "CONST", "value": 42}, "enclosing_function", {})
    
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_expression_stmt_package.handle_expression_stmt_src.generate_expression_code')
    def test_different_expression_types(self, mock_gen_expr):
        """Test EXPRESSION statement with different expression types."""
        mock_gen_expr.side_effect = [
            "ldr x0, [sp, #0]",  # CONST
            "ldr x0, [x19, #0]",  # VAR
            "add x0, x1, x2"  # BINOP
        ]
        
        stmt = {
            "type": "EXPRESSION",
            "func_name": "mixed_func",
            "args": [
                {"type": "CONST", "value": 42},
                {"type": "VAR", "name": "x"},
                {"type": "BINOP", "op": "+", "left": {"type": "VAR", "name": "a"}, "right": {"type": "VAR", "name": "b"}}
            ]
        }
        
        result = handle_expression_stmt(stmt, "current_func", {"x": 0, "a": 8, "b": 16})
        
        self.assertEqual(mock_gen_expr.call_count, 3)
        self.assertIn("bl mixed_func", result)


if __name__ == '__main__':
    unittest.main()
