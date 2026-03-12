import unittest
from unittest.mock import patch

# Relative import from the same package
from .handle_if_src import handle_if


class TestHandleIf(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.func_name = "test_func"
        self.label_counter = {"if_else": 0, "if_end": 0}
        self.var_offsets = {"x": 0, "y": 1}
        self.next_offset = 10
    
    def test_handle_if_with_else_body(self):
        """Test IF statement with both then and else bodies."""
        stmt = {
            "type": "IF",
            "condition": {"type": "EQ", "left": {"type": "VAR", "name": "x"}, "right": {"type": "NUM", "value": 0}},
            "then_body": [{"type": "ASSIGN", "target": "y", "value": {"type": "NUM", "value": 1}}],
            "else_body": [{"type": "ASSIGN", "target": "y", "value": {"type": "NUM", "value": 2}}]
        }
        
        label_counter = {"if_else": 0, "if_end": 0}
        
        with patch('generate_expression_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_expr, \
             patch('generate_expression_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code') as mock_stmt:
            mock_expr.return_value = ("    LOAD x\n    PUSH 0\n    EQ", 11, 12)
            mock_stmt.side_effect = [
                ("    LOAD 1\n    STORE y", 13),
                ("    LOAD 2\n    STORE y", 14)
            ]
            
            code, next_offset = handle_if(stmt, self.func_name, label_counter, self.var_offsets, self.next_offset)
        
        # Verify labels are generated
        self.assertIn("test_func_if_else_0:", code)
        self.assertIn("test_func_if_end_0:", code)
        # Verify JZ and JMP instructions
        self.assertIn("JZ test_func_if_else_0", code)
        self.assertIn("JMP test_func_if_end_0", code)
        # Verify label counter is updated
        self.assertEqual(label_counter["if_else"], 1)
        self.assertEqual(label_counter["if_end"], 1)
        self.assertEqual(next_offset, 14)
    
    def test_handle_if_without_else_body(self):
        """Test IF statement with only then body (no else)."""
        stmt = {
            "type": "IF",
            "condition": {"type": "GT", "left": {"type": "VAR", "name": "x"}, "right": {"type": "NUM", "value": 5}},
            "then_body": [{"type": "ASSIGN", "target": "y", "value": {"type": "NUM", "value": 10}}],
            "else_body": []
        }
        
        label_counter = {"if_else": 0, "if_end": 0}
        
        with patch('generate_expression_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_expr, \
             patch('generate_expression_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code') as mock_stmt:
            mock_expr.return_value = ("    LOAD x\n    PUSH 5\n    GT", 11, 12)
            mock_stmt.return_value = ("    LOAD 10\n    STORE y", 13)
            
            code, next_offset = handle_if(stmt, self.func_name, label_counter, self.var_offsets, self.next_offset)
        
        # Verify labels are generated
        self.assertIn("test_func_if_end_0:", code)
        # Should NOT have if_else label since there's no else body
        self.assertNotIn("test_func_if_else_0", code)
        # Should have JZ but no JMP
        self.assertIn("JZ test_func_if_end_0", code)
        self.assertNotIn("JMP", code)
        # Label counter should be updated
        self.assertEqual(label_counter["if_else"], 1)
        self.assertEqual(label_counter["if_end"], 1)
    
    def test_handle_if_empty_then_body(self):
        """Test IF statement with empty then body."""
        stmt = {
            "type": "IF",
            "condition": {"type": "LT", "left": {"type": "VAR", "name": "x"}, "right": {"type": "NUM", "value": 0}},
            "then_body": [],
            "else_body": [{"type": "ASSIGN", "target": "y", "value": {"type": "NUM", "value": -1}}]
        }
        
        label_counter = {"if_else": 5, "if_end": 3}
        
        with patch('generate_expression_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_expr, \
             patch('generate_expression_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code') as mock_stmt:
            mock_expr.return_value = ("    LOAD x\n    PUSH 0\n    LT", 11, 12)
            mock_stmt.return_value = ("    LOAD -1\n    STORE y", 13)
            
            code, next_offset = handle_if(stmt, self.func_name, label_counter, self.var_offsets, self.next_offset)
        
        # Verify labels use the counter values
        self.assertIn("test_func_if_else_5:", code)
        self.assertIn("test_func_if_end_3:", code)
        # Counter should be incremented
        self.assertEqual(label_counter["if_else"], 6)
        self.assertEqual(label_counter["if_end"], 4)
    
    def test_handle_if_multiple_then_statements(self):
        """Test IF statement with multiple statements in then body."""
        stmt = {
            "type": "IF",
            "condition": {"type": "NEQ", "left": {"type": "VAR", "name": "x"}, "right": {"type": "NUM", "value": 0}},
            "then_body": [
                {"type": "ASSIGN", "target": "a", "value": {"type": "NUM", "value": 1}},
                {"type": "ASSIGN", "target": "b", "value": {"type": "NUM", "value": 2}},
                {"type": "ASSIGN", "target": "c", "value": {"type": "NUM", "value": 3}}
            ],
            "else_body": []
        }
        
        label_counter = {"if_else": 0, "if_end": 0}
        
        with patch('generate_expression_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_expr, \
             patch('generate_expression_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code') as mock_stmt:
            mock_expr.return_value = ("    LOAD x\n    PUSH 0\n    NEQ", 11, 12)
            mock_stmt.side_effect = [
                ("    LOAD 1\n    STORE a", 13),
                ("    LOAD 2\n    STORE b", 14),
                ("    LOAD 3\n    STORE c", 15)
            ]
            
            code, next_offset = handle_if(stmt, self.func_name, label_counter, self.var_offsets, self.next_offset)
        
        # Verify generate_statement_code was called 3 times
        self.assertEqual(mock_stmt.call_count, 3)
        # Verify offset is updated correctly
        self.assertEqual(next_offset, 15)
    
    def test_handle_if_multiple_else_statements(self):
        """Test IF statement with multiple statements in else body."""
        stmt = {
            "type": "IF",
            "condition": {"type": "EQ", "left": {"type": "VAR", "name": "x"}, "right": {"type": "NUM", "value": 0}},
            "then_body": [{"type": "ASSIGN", "target": "y", "value": {"type": "NUM", "value": 0}}],
            "else_body": [
                {"type": "ASSIGN", "target": "a", "value": {"type": "NUM", "value": 1}},
                {"type": "ASSIGN", "target": "b", "value": {"type": "NUM", "value": 2}}
            ]
        }
        
        label_counter = {"if_else": 0, "if_end": 0}
        
        with patch('generate_expression_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_expr, \
             patch('generate_expression_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code') as mock_stmt:
            mock_expr.return_value = ("    LOAD x\n    PUSH 0\n    EQ", 11, 12)
            mock_stmt.side_effect = [
                ("    LOAD 0\n    STORE y", 13),
                ("    LOAD 1\n    STORE a", 14),
                ("    LOAD 2\n    STORE b", 15)
            ]
            
            code, next_offset = handle_if(stmt, self.func_name, label_counter, self.var_offsets, self.next_offset)
        
        # Verify generate_statement_code was called 3 times (1 then + 2 else)
        self.assertEqual(mock_stmt.call_count, 3)
        # Verify JMP is present (since else exists)
        self.assertIn("JMP test_func_if_end_0", code)
    
    def test_handle_if_empty_bodies(self):
        """Test IF statement with both empty then and else bodies."""
        stmt = {
            "type": "IF",
            "condition": {"type": "BOOL", "value": True},
            "then_body": [],
            "else_body": []
        }
        
        label_counter = {"if_else": 0, "if_end": 0}
        
        with patch('generate_expression_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_expr:
            mock_expr.return_value = ("    PUSH 1", 11, 11)
            
            code, next_offset = handle_if(stmt, self.func_name, label_counter, self.var_offsets, self.next_offset)
        
        # Should still generate labels
        self.assertIn("test_func_if_end_0:", code)
        # No JMP since else_body is empty
        self.assertNotIn("JMP", code)
        # JZ should jump to if_end
        self.assertIn("JZ test_func_if_end_0", code)
    
    def test_handle_if_label_counter_increment(self):
        """Test that label counter is properly incremented."""
        stmt = {
            "type": "IF",
            "condition": {"type": "BOOL", "value": True},
            "then_body": [],
            "else_body": []
        }
        
        label_counter = {"if_else": 10, "if_end": 20}
        
        with patch('generate_expression_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_expr:
            mock_expr.return_value = ("    PUSH 1", 11, 11)
            
            handle_if(stmt, self.func_name, label_counter, self.var_offsets, self.next_offset)
        
        # Verify counters are incremented
        self.assertEqual(label_counter["if_else"], 11)
        self.assertEqual(label_counter["if_end"], 21)
    
    def test_handle_if_missing_condition(self):
        """Test IF statement with missing condition (should use default)."""
        stmt = {
            "type": "IF",
            "then_body": [],
            "else_body": []
        }
        
        label_counter = {"if_else": 0, "if_end": 0}
        
        with patch('generate_expression_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_expr:
            mock_expr.return_value = ("", 10, 10)
            
            code, next_offset = handle_if(stmt, self.func_name, label_counter, self.var_offsets, self.next_offset)
        
        # Should still work with empty condition
        self.assertIn("test_func_if_end_0:", code)
        # generate_expression_code should be called with empty dict
        mock_expr.assert_called_once()
        args = mock_expr.call_args[0]
        self.assertEqual(args[0], {})  # condition is empty dict
    
    def test_handle_if_missing_then_body(self):
        """Test IF statement with missing then_body (should use default)."""
        stmt = {
            "type": "IF",
            "condition": {"type": "BOOL", "value": True},
            "else_body": [{"type": "ASSIGN", "target": "x", "value": {"type": "NUM", "value": 0}}]
        }
        
        label_counter = {"if_else": 0, "if_end": 0}
        
        with patch('generate_expression_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_expr, \
             patch('generate_expression_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code') as mock_stmt:
            mock_expr.return_value = ("    PUSH 1", 11, 11)
            mock_stmt.return_value = ("    LOAD 0\n    STORE x", 12)
            
            code, next_offset = handle_if(stmt, self.func_name, label_counter, self.var_offsets, self.next_offset)
        
        # Should have else label and jump
        self.assertIn("test_func_if_else_0:", code)
        self.assertIn("JMP test_func_if_end_0", code)
        # generate_statement_code should be called once for else body
        self.assertEqual(mock_stmt.call_count, 1)
    
    def test_handle_if_missing_else_body(self):
        """Test IF statement with missing else_body key."""
        stmt = {
            "type": "IF",
            "condition": {"type": "BOOL", "value": True},
            "then_body": [{"type": "ASSIGN", "target": "x", "value": {"type": "NUM", "value": 1}}]
        }
        
        label_counter = {"if_else": 0, "if_end": 0}
        
        with patch('generate_expression_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_expr, \
             patch('generate_expression_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code') as mock_stmt:
            mock_expr.return_value = ("    PUSH 1", 11, 11)
            mock_stmt.return_value = ("    LOAD 1\n    STORE x", 12)
            
            code, next_offset = handle_if(stmt, self.func_name, label_counter, self.var_offsets, self.next_offset)
        
        # Should not have else label or JMP
        self.assertNotIn("test_func_if_else_0", code)
        self.assertNotIn("JMP", code)
        # Should have if_end label
        self.assertIn("test_func_if_end_0:", code)


if __name__ == '__main__':
    unittest.main()
