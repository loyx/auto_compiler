import unittest
from unittest.mock import patch, MagicMock
import sys

# Mock the dependencies before importing handle_for
sys.modules['main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_expression_code_src'] = MagicMock()
sys.modules['main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.generate_statement_code_src'] = MagicMock()

from .handle_for_src import handle_for


class TestHandleFor(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.func_name = "test_func"
        self.label_counter = {"for_cond": 0, "for_end": 0, "for_update": 0}
        self.var_offsets = {"x": 0, "y": 4}
        self.next_offset = 8
    
    def test_complete_for_statement(self):
        """Test complete FOR statement with all components."""
        stmt = {
            "type": "FOR",
            "init": {"type": "ASSIGN", "var": "i", "value": 0},
            "condition": {"type": "BINOP", "op": "<", "left": "i", "right": 10},
            "update": {"type": "ASSIGN", "var": "i", "value": "i+1"},
            "body": [{"type": "PRINT", "value": "i"}]
        }
        
        label_counter = {"for_cond": 0, "for_end": 0, "for_update": 0}
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.handle_for_src.generate_expression_code') as mock_gen_expr, \
             patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.handle_for_src.generate_statement_code') as mock_gen_stmt:
            
            mock_gen_expr.return_value = ("cmp x0, x1", 8)
            mock_gen_stmt.side_effect = [
                ("mov x0, #0", 8),  # init
                ("bl print", 8),  # body
                ("add x0, x0, #1", 8)  # update
            ]
            
            code, next_offset = handle_for(stmt, self.func_name, label_counter, self.var_offsets, self.next_offset)
            
            # Verify label counter was updated
            self.assertEqual(label_counter["for_cond"], 1)
            self.assertEqual(label_counter["for_end"], 1)
            self.assertEqual(label_counter["for_update"], 1)
            
            # Verify generated code structure
            self.assertIn(f"{self.func_name}_for_cond_0:", code)
            self.assertIn(f"{self.func_name}_for_end_0:", code)
            self.assertIn(f"{self.func_name}_for_update_0:", code)
            self.assertIn(f"cbz x0, {self.func_name}_for_end_0", code)
            self.assertIn(f"b {self.func_name}_for_cond_0", code)
    
    def test_for_without_init(self):
        """Test FOR statement without init."""
        stmt = {
            "type": "FOR",
            "condition": {"type": "BINOP", "op": "<", "left": "i", "right": 10},
            "body": []
        }
        
        label_counter = {"for_cond": 0, "for_end": 0, "for_update": 0}
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.handle_for_src.generate_expression_code') as mock_gen_expr, \
             patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.handle_for_src.generate_statement_code') as mock_gen_stmt:
            
            mock_gen_expr.return_value = ("cmp x0, x1", 8)
            
            code, next_offset = handle_for(stmt, self.func_name, label_counter, self.var_offsets, self.next_offset)
            
            # Should not call generate_statement_code for init
            init_calls = [call for call in mock_gen_stmt.call_args_list if call[0][0].get("type") == "ASSIGN"]
            self.assertEqual(len(init_calls), 0)
            
            # Should still have condition label
            self.assertIn(f"{self.func_name}_for_cond_0:", code)
    
    def test_for_without_condition(self):
        """Test FOR statement without condition (infinite loop)."""
        stmt = {
            "type": "FOR",
            "init": {"type": "ASSIGN", "var": "i", "value": 0},
            "body": []
        }
        
        label_counter = {"for_cond": 0, "for_end": 0, "for_update": 0}
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.handle_for_src.generate_statement_code') as mock_gen_stmt:
            
            mock_gen_stmt.return_value = ("mov x0, #0", 8)
            
            code, next_offset = handle_for(stmt, self.func_name, label_counter, self.var_offsets, self.next_offset)
            
            # Should not have cbz instruction
            self.assertNotIn("cbz", code)
            
            # Should still have condition label and loop back
            self.assertIn(f"{self.func_name}_for_cond_0:", code)
            self.assertIn(f"b {self.func_name}_for_cond_0", code)
    
    def test_for_without_update(self):
        """Test FOR statement without update."""
        stmt = {
            "type": "FOR",
            "init": {"type": "ASSIGN", "var": "i", "value": 0},
            "condition": {"type": "BINOP", "op": "<", "left": "i", "right": 10},
            "body": []
        }
        
        label_counter = {"for_cond": 0, "for_end": 0, "for_update": 0}
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.handle_for_src.generate_expression_code') as mock_gen_expr, \
             patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.handle_for_src.generate_statement_code') as mock_gen_stmt:
            
            mock_gen_expr.return_value = ("cmp x0, x1", 8)
            mock_gen_stmt.return_value = ("mov x0, #0", 8)
            
            code, next_offset = handle_for(stmt, self.func_name, label_counter, self.var_offsets, self.next_offset)
            
            # Should have update label but no update code generation call
            self.assertIn(f"{self.func_name}_for_update_0:", code)
            
            # Verify update code was not generated (only init call, body is empty)
            self.assertEqual(mock_gen_stmt.call_count, 1)  # init only
    
    def test_for_with_empty_body(self):
        """Test FOR statement with empty body."""
        stmt = {
            "type": "FOR",
            "init": {"type": "ASSIGN", "var": "i", "value": 0},
            "condition": {"type": "BINOP", "op": "<", "left": "i", "right": 10},
            "update": {"type": "ASSIGN", "var": "i", "value": "i+1"},
            "body": []
        }
        
        label_counter = {"for_cond": 0, "for_end": 0, "for_update": 0}
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.handle_for_src.generate_expression_code') as mock_gen_expr, \
             patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.handle_for_src.generate_statement_code') as mock_gen_stmt:
            
            mock_gen_expr.return_value = ("cmp x0, x1", 8)
            mock_gen_stmt.side_effect = [
                ("mov x0, #0", 8),  # init
                ("add x0, x0, #1", 8)  # update
            ]
            
            code, next_offset = handle_for(stmt, self.func_name, label_counter, self.var_offsets, self.next_offset)
            
            # Should still have all labels
            self.assertIn(f"{self.func_name}_for_cond_0:", code)
            self.assertIn(f"{self.func_name}_for_update_0:", code)
            self.assertIn(f"{self.func_name}_for_end_0:", code)
            
            # Should have loop back
            self.assertIn(f"b {self.func_name}_for_cond_0", code)
    
    def test_for_with_multiple_body_statements(self):
        """Test FOR statement with multiple body statements."""
        stmt = {
            "type": "FOR",
            "init": {"type": "ASSIGN", "var": "i", "value": 0},
            "condition": {"type": "BINOP", "op": "<", "left": "i", "right": 10},
            "update": {"type": "ASSIGN", "var": "i", "value": "i+1"},
            "body": [
                {"type": "PRINT", "value": "i"},
                {"type": "PRINT", "value": "i*2"},
                {"type": "ASSIGN", "var": "j", "value": "i"}
            ]
        }
        
        label_counter = {"for_cond": 0, "for_end": 0, "for_update": 0}
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.handle_for_src.generate_expression_code') as mock_gen_expr, \
             patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.handle_for_src.generate_statement_code') as mock_gen_stmt:
            
            mock_gen_expr.return_value = ("cmp x0, x1", 8)
            mock_gen_stmt.side_effect = [
                ("mov x0, #0", 8),  # init
                ("bl print", 8),  # body 1
                ("bl print", 8),  # body 2
                ("mov x1, x0", 8),  # body 3
                ("add x0, x0, #1", 8)  # update
            ]
            
            code, next_offset = handle_for(stmt, self.func_name, label_counter, self.var_offsets, self.next_offset)
            
            # Should call generate_statement_code for init, 3 body statements, and update
            self.assertEqual(mock_gen_stmt.call_count, 5)
    
    def test_label_counter_increment(self):
        """Test that label counter is incremented correctly."""
        stmt = {
            "type": "FOR",
            "condition": {"type": "BINOP", "op": "<", "left": "i", "right": 10},
            "body": []
        }
        
        label_counter = {"for_cond": 5, "for_end": 3, "for_update": 7}
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.handle_for_src.generate_expression_code') as mock_gen_expr:
            
            mock_gen_expr.return_value = ("cmp x0, x1", 8)
            
            code, next_offset = handle_for(stmt, self.func_name, label_counter, self.var_offsets, self.next_offset)
            
            # Verify labels use the old counts
            self.assertIn(f"{self.func_name}_for_cond_5:", code)
            self.assertIn(f"{self.func_name}_for_end_3:", code)
            self.assertIn(f"{self.func_name}_for_update_7:", code)
            
            # Verify counter was incremented
            self.assertEqual(label_counter["for_cond"], 6)
            self.assertEqual(label_counter["for_end"], 4)
            self.assertEqual(label_counter["for_update"], 8)
    
    def test_next_offset_propagation(self):
        """Test that next_offset is properly propagated through calls."""
        stmt = {
            "type": "FOR",
            "init": {"type": "ASSIGN", "var": "i", "value": 0},
            "condition": {"type": "BINOP", "op": "<", "left": "i", "right": 10},
            "update": {"type": "ASSIGN", "var": "i", "value": "i+1"},
            "body": [{"type": "ASSIGN", "var": "j", "value": "i"}]
        }
        
        label_counter = {"for_cond": 0, "for_end": 0, "for_update": 0}
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.handle_for_src.generate_expression_code') as mock_gen_expr, \
             patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.handle_for_src.generate_statement_code') as mock_gen_stmt:
            
            # Simulate offset increasing with each call
            mock_gen_expr.return_value = ("cmp x0, x1", 16)
            mock_gen_stmt.side_effect = [
                ("mov x0, #0", 16),  # init
                ("mov x1, x0", 24),  # body
                ("add x0, x0, #1", 32)  # update
            ]
            
            code, next_offset = handle_for(stmt, self.func_name, label_counter, self.var_offsets, 8)
            
            # Final offset should be from the last call (update)
            self.assertEqual(next_offset, 32)
    
    def test_empty_init_condition_update(self):
        """Test FOR statement with None/empty init, condition, and update."""
        stmt = {
            "type": "FOR",
            "init": None,
            "condition": None,
            "update": None,
            "body": []
        }
        
        label_counter = {"for_cond": 0, "for_end": 0, "for_update": 0}
        
        code, next_offset = handle_for(stmt, self.func_name, label_counter, self.var_offsets, self.next_offset)
        
        # Should still have labels and loop
        self.assertIn(f"{self.func_name}_for_cond_0:", code)
        self.assertIn(f"{self.func_name}_for_update_0:", code)
        self.assertIn(f"{self.func_name}_for_end_0:", code)
        self.assertIn(f"b {self.func_name}_for_cond_0", code)
        
        # Should not have cbz (no condition)
        self.assertNotIn("cbz", code)
    
    def test_minimal_for_statement(self):
        """Test minimal FOR statement with only type."""
        stmt = {
            "type": "FOR"
        }
        
        label_counter = {"for_cond": 0, "for_end": 0, "for_update": 0}
        
        code, next_offset = handle_for(stmt, self.func_name, label_counter, self.var_offsets, self.next_offset)
        
        # Should have all labels and loop back
        self.assertIn(f"{self.func_name}_for_cond_0:", code)
        self.assertIn(f"{self.func_name}_for_update_0:", code)
        self.assertIn(f"{self.func_name}_for_end_0:", code)
        self.assertIn(f"b {self.func_name}_for_cond_0", code)
        
        # Should not have cbz (no condition)
        self.assertNotIn("cbz", code)
    
    def test_for_with_condition_no_code_return(self):
        """Test FOR statement when generate_expression_code returns empty string."""
        stmt = {
            "type": "FOR",
            "condition": {"type": "BINOP", "op": "<", "left": "i", "right": 10},
            "body": []
        }
        
        label_counter = {"for_cond": 0, "for_end": 0, "for_update": 0}
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.handle_for_src.generate_expression_code') as mock_gen_expr:
            
            mock_gen_expr.return_value = ("", 8)
            
            code, next_offset = handle_for(stmt, self.func_name, label_counter, self.var_offsets, self.next_offset)
            
            # Should still have cbz even if cond_code is empty
            self.assertIn(f"cbz x0, {self.func_name}_for_end_0", code)
    
    def test_for_with_init_no_code_return(self):
        """Test FOR statement when generate_statement_code for init returns empty string."""
        stmt = {
            "type": "FOR",
            "init": {"type": "ASSIGN", "var": "i", "value": 0},
            "condition": {"type": "BINOP", "op": "<", "left": "i", "right": 10},
            "body": []
        }
        
        label_counter = {"for_cond": 0, "for_end": 0, "for_update": 0}
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.handle_for_src.generate_expression_code') as mock_gen_expr, \
             patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.handle_for_src.generate_statement_code') as mock_gen_stmt:
            
            mock_gen_expr.return_value = ("cmp x0, x1", 8)
            mock_gen_stmt.return_value = ("", 8)  # Empty init code
            
            code, next_offset = handle_for(stmt, self.func_name, label_counter, self.var_offsets, self.next_offset)
            
            # Empty init code should not be added to lines
            self.assertNotIn("", code.split('\n'))
    
    def test_label_counter_missing_keys(self):
        """Test FOR statement when label_counter is missing some keys."""
        stmt = {
            "type": "FOR",
            "condition": {"type": "BINOP", "op": "<", "left": "i", "right": 10},
            "body": []
        }
        
        label_counter = {}  # Empty label counter
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.handle_for_src.generate_expression_code') as mock_gen_expr:
            
            mock_gen_expr.return_value = ("cmp x0, x1", 8)
            
            code, next_offset = handle_for(stmt, self.func_name, label_counter, self.var_offsets, self.next_offset)
            
            # Should use default 0 for missing keys
            self.assertIn(f"{self.func_name}_for_cond_0:", code)
            self.assertIn(f"{self.func_name}_for_end_0:", code)
            self.assertIn(f"{self.func_name}_for_update_0:", code)
            
            # Verify counter was set
            self.assertEqual(label_counter["for_cond"], 1)
            self.assertEqual(label_counter["for_end"], 1)
            self.assertEqual(label_counter["for_update"], 1)


if __name__ == '__main__':
    unittest.main()
