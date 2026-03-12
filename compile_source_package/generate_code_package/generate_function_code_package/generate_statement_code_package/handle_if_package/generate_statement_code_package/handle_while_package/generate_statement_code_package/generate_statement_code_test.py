import unittest
from unittest.mock import patch

# Relative import from the same package
from .generate_statement_code_src import generate_statement_code


class TestGenerateStatementCode(unittest.TestCase):
    """Test cases for generate_statement_code function."""
    
    def test_decl_without_init(self):
        """Test DECL statement without initialization value."""
        stmt = {"type": "DECL", "name": "x"}
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 5
        
        code, offset = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)
        
        self.assertEqual(var_offsets["x"], 5)
        self.assertEqual(offset, 6)
        self.assertEqual(code, "")
    
    def test_decl_with_init(self):
        """Test DECL statement with initialization value."""
        stmt = {"type": "DECL", "name": "x", "init_value": {"type": "CONST", "value": 10}}
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 5
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.generate_statement_code_src.generate_expression_code') as mock_gen_expr:
            mock_gen_expr.return_value = ("    mov x1, #10", "x1")
            
            code, offset = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)
            
            self.assertEqual(var_offsets["x"], 5)
            self.assertEqual(offset, 6)
            self.assertIn("mov x1, #10", code)
            self.assertIn("str x1, [sp, 40]", code)
    
    def test_assign(self):
        """Test ASSIGN statement."""
        stmt = {"type": "ASSIGN", "name": "x", "value": {"type": "CONST", "value": 20}}
        func_name = "test_func"
        label_counter = {}
        var_offsets = {"x": 3}
        next_offset = 5
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.generate_statement_code_src.generate_expression_code') as mock_gen_expr:
            mock_gen_expr.return_value = ("    mov x1, #20", "x1")
            
            code, offset = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)
            
            self.assertEqual(offset, 5)
            self.assertIn("mov x1, #20", code)
            self.assertIn("str x1, [sp, 24]", code)
    
    def test_assign_variable_not_found(self):
        """Test ASSIGN statement with non-existent variable raises KeyError."""
        stmt = {"type": "ASSIGN", "name": "x", "value": {"type": "CONST", "value": 20}}
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 5
        
        with self.assertRaises(KeyError):
            generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)
    
    def test_if_without_else(self):
        """Test IF statement without else body."""
        stmt = {
            "type": "IF",
            "condition": {"type": "CONST", "value": 1},
            "body": [{"type": "DECL", "name": "y"}],
        }
        func_name = "test_func"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {}
        next_offset = 5
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.generate_statement_code_src.generate_expression_code') as mock_gen_expr:
            mock_gen_expr.return_value = ("    mov x1, #1", "x1")
            
            code, offset = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)
            
            self.assertEqual(label_counter["if_else"], 1)
            self.assertEqual(label_counter["if_end"], 1)
            self.assertIn("cbz x1, test_func_if_else_0", code)
            self.assertIn("test_func_if_else_0:", code)
    
    def test_if_with_else(self):
        """Test IF statement with else body."""
        stmt = {
            "type": "IF",
            "condition": {"type": "CONST", "value": 1},
            "body": [{"type": "DECL", "name": "y"}],
            "else_body": [{"type": "DECL", "name": "z"}]
        }
        func_name = "test_func"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {}
        next_offset = 5
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.generate_statement_code_src.generate_expression_code') as mock_gen_expr:
            mock_gen_expr.return_value = ("    mov x1, #1", "x1")
            
            code, offset = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)
            
            self.assertIn("cbz x1, test_func_if_else_0", code)
            self.assertIn("b test_func_if_end_0", code)
            self.assertIn("test_func_if_else_0:", code)
            self.assertIn("test_func_if_end_0:", code)
    
    def test_if_nested_statements(self):
        """Test IF statement with nested statements in body."""
        stmt = {
            "type": "IF",
            "condition": {"type": "CONST", "value": 1},
            "body": [
                {"type": "DECL", "name": "a"},
                {"type": "ASSIGN", "name": "a", "value": {"type": "CONST", "value": 5}}
            ],
        }
        func_name = "test_func"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {}
        next_offset = 5
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.generate_statement_code_src.generate_expression_code') as mock_gen_expr:
            mock_gen_expr.return_value = ("    mov x1, #1", "x1")
            
            code, offset = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)
            
            self.assertEqual(var_offsets["a"], 5)
            self.assertIn("cbz x1, test_func_if_else_0", code)
    
    def test_while(self):
        """Test WHILE statement."""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "CONST", "value": 1},
            "body": []
        }
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 5
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.generate_statement_code_src.handle_while') as mock_handle_while:
            mock_handle_while.return_value = ("while_code", 6)
            
            code, offset = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)
            
            mock_handle_while.assert_called_once_with(stmt, func_name, label_counter, var_offsets, next_offset)
            self.assertEqual(code, "while_code")
            self.assertEqual(offset, 6)
    
    def test_break_inside_loop(self):
        """Test BREAK statement inside a loop."""
        stmt = {"type": "BREAK"}
        func_name = "test_func"
        label_counter = {"loop_stack": ["test_func_while_end_0"]}
        var_offsets = {}
        next_offset = 5
        
        code, offset = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)
        
        self.assertEqual(code, "    b test_func_while_end_0")
        self.assertEqual(offset, 5)
    
    def test_break_outside_loop(self):
        """Test BREAK statement outside a loop should raise error."""
        stmt = {"type": "BREAK"}
        func_name = "test_func"
        label_counter = {"loop_stack": []}
        var_offsets = {}
        next_offset = 5
        
        with self.assertRaises(RuntimeError) as context:
            generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)
        
        self.assertIn("BREAK outside of loop", str(context.exception))
    
    def test_break_no_loop_stack(self):
        """Test BREAK statement when loop_stack key doesn't exist."""
        stmt = {"type": "BREAK"}
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 5
        
        with self.assertRaises(RuntimeError) as context:
            generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)
        
        self.assertIn("BREAK outside of loop", str(context.exception))
    
    def test_return_with_value(self):
        """Test RETURN statement with value."""
        stmt = {"type": "RETURN", "value": {"type": "CONST", "value": 42}}
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 5
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.generate_statement_code_src.generate_expression_code') as mock_gen_expr:
            mock_gen_expr.return_value = ("    mov x1, #42", "x1")
            
            code, offset = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)
            
            self.assertIn("mov x1, #42", code)
            self.assertIn("mov x0, x1", code)
            self.assertIn("b test_func_epilogue", code)
            self.assertEqual(offset, 5)
    
    def test_return_without_value(self):
        """Test RETURN statement without value."""
        stmt = {"type": "RETURN", "value": None}
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 5
        
        code, offset = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)
        
        self.assertEqual(code, "    b test_func_epilogue")
        self.assertEqual(offset, 5)
    
    def test_return_missing_value_key(self):
        """Test RETURN statement without value key."""
        stmt = {"type": "RETURN"}
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 5
        
        code, offset = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)
        
        self.assertEqual(code, "    b test_func_epilogue")
        self.assertEqual(offset, 5)
    
    def test_unknown_statement_type(self):
        """Test unknown statement type should raise ValueError."""
        stmt = {"type": "UNKNOWN"}
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 5
        
        with self.assertRaises(ValueError) as context:
            generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)
        
        self.assertIn("Unknown statement type: UNKNOWN", str(context.exception))
    
    def test_decl_updates_var_offsets(self):
        """Test that DECL statement properly updates var_offsets dict."""
        stmt = {"type": "DECL", "name": "var1"}
        func_name = "test_func"
        label_counter = {}
        var_offsets = {"existing": 0}
        next_offset = 10
        
        code, offset = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)
        
        self.assertEqual(var_offsets["existing"], 0)
        self.assertEqual(var_offsets["var1"], 10)
        self.assertEqual(offset, 11)
    
    def test_if_updates_label_counter(self):
        """Test that IF statement properly updates label_counter."""
        stmt = {
            "type": "IF",
            "condition": {"type": "CONST", "value": 1},
            "body": []
        }
        func_name = "test_func"
        label_counter = {"if_else": 5, "if_end": 3}
        var_offsets = {}
        next_offset = 5
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.generate_statement_code_src.generate_expression_code') as mock_gen_expr:
            mock_gen_expr.return_value = ("    mov x1, #1", "x1")
            
            code, offset = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)
            
            self.assertEqual(label_counter["if_else"], 6)
            self.assertEqual(label_counter["if_end"], 4)
            self.assertIn("test_func_if_else_5", code)
            self.assertIn("test_func_if_end_3", code)


if __name__ == '__main__':
    unittest.main()
