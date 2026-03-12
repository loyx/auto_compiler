import unittest
from unittest.mock import patch

from .generate_statement_code_src import generate_statement_code


class TestGenerateStatementCode(unittest.TestCase):
    """Test cases for generate_statement_code function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.func_name = "test_func"
        self.label_counter = {
            "while_cond": 0,
            "while_end": 0,
            "if_else": 0,
            "if_end": 0,
        }
        self.var_offsets = {"x": 0, "y": 1, "z": 2}
        self.next_offset = 3
    
    def test_assign_statement(self):
        """Test assignment statement code generation."""
        stmt = {
            "type": "assign",
            "target": "x",
            "value": {"type": "literal", "value": 42}
        }
        
        with patch('generate_statement_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_gen_expr:
            mock_gen_expr.return_value = ("    PUSH 42\n", 3, 4)
            
            code, new_offset = generate_statement_code(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
            
            self.assertIn("STORE 0", code)
            self.assertEqual(new_offset, 4)
            mock_gen_expr.assert_called_once()
    
    def test_assign_statement_unknown_variable(self):
        """Test assignment to unknown variable returns empty code."""
        stmt = {
            "type": "assign",
            "target": "unknown_var",
            "value": {"type": "literal", "value": 42}
        }
        
        code, new_offset = generate_statement_code(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        self.assertEqual(code, "")
        self.assertEqual(new_offset, self.next_offset)
    
    def test_while_statement(self):
        """Test while statement delegates to handle_while_stmt."""
        stmt = {
            "type": "while",
            "condition": {"type": "binary", "op": "<", "left": {"type": "var", "name": "i"}, "right": {"type": "literal", "value": 10}},
            "body": [{"type": "assign", "target": "i", "value": {"type": "binary", "op": "+", "left": {"type": "var", "name": "i"}, "right": {"type": "literal", "value": 1}}}]
        }
        
        expected_code = "    ; while loop code\n"
        expected_offset = 10
        
        with patch('generate_statement_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.generate_expression_code_package.generate_expression_code_src.handle_while_stmt') as mock_handle_while:
            mock_handle_while.return_value = (expected_code, expected_offset)
            
            code, new_offset = generate_statement_code(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
            
            self.assertEqual(code, expected_code)
            self.assertEqual(new_offset, expected_offset)
            mock_handle_while.assert_called_once_with(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
    
    def test_if_statement_without_else(self):
        """Test IF statement without else branch."""
        stmt = {
            "type": "if",
            "condition": {"type": "binary", "op": ">", "left": {"type": "var", "name": "x"}, "right": {"type": "literal", "value": 0}},
            "body": [{"type": "assign", "target": "y", "value": {"type": "literal", "value": 1}}],
            "else_body": []
        }
        
        with patch('generate_statement_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_gen_expr, \
             patch('generate_statement_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.generate_expression_code_package.generate_expression_code_src.generate_statement_code') as mock_gen_stmt:
            
            mock_gen_expr.return_value = ("    PUSH 0\n", 5, 6)
            mock_gen_stmt.return_value = ("    ; body code\n", 7)
            
            code, new_offset = generate_statement_code(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
            
            self.assertIn("test_func_if_else_0", code)
            self.assertIn("test_func_if_end_0", code)
            self.assertIn("JUMP_IF_FALSE 5", code)
            self.assertEqual(self.label_counter["if_else"], 1)
            self.assertEqual(self.label_counter["if_end"], 1)
    
    def test_if_statement_with_else(self):
        """Test IF statement with else branch."""
        stmt = {
            "type": "if",
            "condition": {"type": "binary", "op": "==", "left": {"type": "var", "name": "x"}, "right": {"type": "literal", "value": 0}},
            "body": [{"type": "assign", "target": "y", "value": {"type": "literal", "value": 1}}],
            "else_body": [{"type": "assign", "target": "y", "value": {"type": "literal", "value": 2}}]
        }
        
        with patch('generate_statement_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_gen_expr, \
             patch('generate_statement_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.generate_expression_code_package.generate_expression_code_src.generate_statement_code') as mock_gen_stmt:
            
            mock_gen_expr.return_value = ("    PUSH 0\n", 5, 6)
            mock_gen_stmt.side_effect = [("    ; then body\n", 7), ("    ; else body\n", 8)]
            
            code, new_offset = generate_statement_code(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
            
            self.assertIn("test_func_if_else_0", code)
            self.assertIn("test_func_if_end_0", code)
            self.assertIn("JUMP_IF_FALSE 5", code)
            self.assertIn("JUMP test_func_if_end_0", code)
    
    def test_return_statement_with_expression(self):
        """Test RETURN statement with expression."""
        stmt = {
            "type": "return",
            "expression": {"type": "var", "name": "x"}
        }
        
        with patch('generate_statement_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_gen_expr:
            mock_gen_expr.return_value = ("    LOAD 0\n", 0, 4)
            
            code, new_offset = generate_statement_code(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
            
            self.assertIn("RETURN 0", code)
            self.assertEqual(new_offset, 4)
    
    def test_return_statement_without_expression(self):
        """Test RETURN statement without expression (void return)."""
        stmt = {
            "type": "return",
            "expression": {}
        }
        
        code, new_offset = generate_statement_code(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        self.assertEqual(code, "    RETURN\n")
        self.assertEqual(new_offset, self.next_offset)
    
    def test_break_statement_with_label(self):
        """Test BREAK statement with custom label."""
        stmt = {
            "type": "break",
            "label": "my_loop_end"
        }
        
        code, new_offset = generate_statement_code(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        self.assertEqual(code, "    JUMP my_loop_end\n")
        self.assertEqual(new_offset, self.next_offset)
    
    def test_break_statement_without_label(self):
        """Test BREAK statement without label uses default."""
        stmt = {
            "type": "break"
        }
        
        code, new_offset = generate_statement_code(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        self.assertEqual(code, "    JUMP loop_end\n")
        self.assertEqual(new_offset, self.next_offset)
    
    def test_continue_statement_with_label(self):
        """Test CONTINUE statement with custom label."""
        stmt = {
            "type": "continue",
            "label": "my_loop_cond"
        }
        
        code, new_offset = generate_statement_code(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        self.assertEqual(code, "    JUMP my_loop_cond\n")
        self.assertEqual(new_offset, self.next_offset)
    
    def test_continue_statement_without_label(self):
        """Test CONTINUE statement without label uses default."""
        stmt = {
            "type": "continue"
        }
        
        code, new_offset = generate_statement_code(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        self.assertEqual(code, "    JUMP loop_cond\n")
        self.assertEqual(new_offset, self.next_offset)
    
    def test_unknown_statement_type(self):
        """Test unknown statement type returns empty code."""
        stmt = {
            "type": "unknown_type",
            "data": "some_data"
        }
        
        code, new_offset = generate_statement_code(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        self.assertEqual(code, "")
        self.assertEqual(new_offset, self.next_offset)
    
    def test_empty_statement_type(self):
        """Test empty statement type returns empty code."""
        stmt = {
            "type": ""
        }
        
        code, new_offset = generate_statement_code(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        self.assertEqual(code, "")
        self.assertEqual(new_offset, self.next_offset)
    
    def test_statement_missing_type_field(self):
        """Test statement without type field returns empty code."""
        stmt = {
            "data": "some_data"
        }
        
        code, new_offset = generate_statement_code(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        self.assertEqual(code, "")
        self.assertEqual(new_offset, self.next_offset)
    
    def test_label_counter_not_modified_for_non_if_while(self):
        """Test label counter is not modified for non-if/while statements."""
        original_counter = self.label_counter.copy()
        
        stmt = {
            "type": "assign",
            "target": "x",
            "value": {"type": "literal", "value": 42}
        }
        
        with patch('generate_statement_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code'):
            generate_statement_code(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
        
        self.assertEqual(self.label_counter, original_counter)


if __name__ == '__main__':
    unittest.main()
