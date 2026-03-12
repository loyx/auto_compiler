import unittest
from unittest.mock import patch

from .handle_while_src import handle_while


class TestHandleWhile(unittest.TestCase):
    
    def test_handle_while_basic(self):
        """Test basic WHILE statement with condition and body."""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "BINOP", "op": "<", "left": {"type": "VAR", "name": "i"}, "right": {"type": "NUM", "value": 10}},
            "body": [
                {"type": "ASSIGN", "var": "i", "expr": {"type": "BINOP", "op": "+", "left": {"type": "VAR", "name": "i"}, "right": {"type": "NUM", "value": 1}}}
            ]
        }
        func_name = "test_func"
        label_counter = {"while_start": 0, "while_end": 0}
        var_offsets = {"i": 0}
        next_offset = 16
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_while_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_expr, \
             patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code') as mock_stmt:
            mock_expr.return_value = ("cmp x0, x1", 16, "x0")
            mock_stmt.return_value = ("add x0, x0, #1", 32)
            
            result_code, result_offset = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)
            
            start_label = "test_func_while_start_0"
            end_label = "test_func_while_end_0"
            
            self.assertIn(start_label + ":", result_code)
            self.assertIn(f"    cbz x0, {end_label}", result_code)
            self.assertIn(f"    b {start_label}", result_code)
            self.assertIn(end_label + ":", result_code)
            self.assertEqual(label_counter["while_start"], 1)
            self.assertEqual(label_counter["while_end"], 1)
            self.assertEqual(result_offset, 32)
    
    def test_handle_while_empty_body(self):
        """Test WHILE statement with empty body."""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "VAR", "name": "flag"},
            "body": []
        }
        func_name = "loop_func"
        label_counter = {"while_start": 5, "while_end": 3}
        var_offsets = {"flag": 0}
        next_offset = 16
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_while_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_expr:
            mock_expr.return_value = ("mov x0, x1", 16, "x0")
            
            result_code, result_offset = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)
            
            start_label = "loop_func_while_start_5"
            end_label = "loop_func_while_end_3"
            
            self.assertIn(start_label + ":", result_code)
            self.assertIn(end_label + ":", result_code)
            self.assertEqual(label_counter["while_start"], 6)
            self.assertEqual(label_counter["while_end"], 4)
            self.assertEqual(result_offset, 16)
    
    def test_handle_while_multiple_body_statements(self):
        """Test WHILE statement with multiple body statements."""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "NUM", "value": 1},
            "body": [
                {"type": "ASSIGN", "var": "x", "expr": {"type": "NUM", "value": 1}},
                {"type": "ASSIGN", "var": "y", "expr": {"type": "NUM", "value": 2}},
                {"type": "ASSIGN", "var": "z", "expr": {"type": "NUM", "value": 3}}
            ]
        }
        func_name = "multi_stmt_func"
        label_counter = {"while_start": 0, "while_end": 0}
        var_offsets = {"x": 0, "y": 8, "z": 16}
        next_offset = 24
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_while_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_expr, \
             patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code') as mock_stmt:
            mock_expr.return_value = ("mov x0, #1", 24, "x0")
            
            mock_stmt.side_effect = [
                ("str x1, [sp, #0]", 32),
                ("str x2, [sp, #8]", 40),
                ("str x3, [sp, #16]", 48)
            ]
            
            result_code, result_offset = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)
            
            self.assertEqual(mock_stmt.call_count, 3)
            self.assertEqual(result_offset, 48)
            self.assertIn("multi_stmt_func_while_start_0:", result_code)
            self.assertIn("multi_stmt_func_while_end_0:", result_code)
    
    def test_handle_while_label_counter_increment(self):
        """Test that label_counter is incremented correctly."""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "NUM", "value": 1},
            "body": []
        }
        func_name = "counter_test"
        label_counter = {"while_start": 10, "while_end": 20}
        var_offsets = {}
        next_offset = 16
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_while_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_expr:
            mock_expr.return_value = ("mov x0, #1", 16, "x0")
            
            handle_while(stmt, func_name, label_counter, var_offsets, next_offset)
            
            self.assertEqual(label_counter["while_start"], 11)
            self.assertEqual(label_counter["while_end"], 21)
    
    def test_handle_while_offset_propagation(self):
        """Test that offset is correctly propagated through condition and body."""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "NUM", "value": 1},
            "body": [{"type": "ASSIGN", "var": "x", "expr": {"type": "NUM", "value": 1}}]
        }
        func_name = "offset_test"
        label_counter = {"while_start": 0, "while_end": 0}
        var_offsets = {"x": 0}
        next_offset = 100
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_while_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_expr, \
             patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code') as mock_stmt:
            mock_expr.return_value = ("mov x0, #1", 110, "x0")
            mock_stmt.return_value = ("str x1, [sp, #0]", 120)
            
            result_code, result_offset = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)
            
            mock_expr.assert_called_once()
            call_args = mock_expr.call_args
            self.assertEqual(call_args[0][2], 100)
            
            mock_stmt.assert_called_once()
            call_args = mock_stmt.call_args
            self.assertEqual(call_args[0][4], 110)
            
            self.assertEqual(result_offset, 120)
    
    def test_handle_while_code_structure(self):
        """Test the structure of generated assembly code."""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "NUM", "value": 1},
            "body": [{"type": "NOP"}]
        }
        func_name = "structure_test"
        label_counter = {"while_start": 0, "while_end": 0}
        var_offsets = {}
        next_offset = 16
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_while_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_expr, \
             patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code') as mock_stmt:
            mock_expr.return_value = ("cmp x0, #0", 16, "x0")
            mock_stmt.return_value = ("nop", 16)
            
            result_code, result_offset = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)
            
            lines = result_code.split('\n')
            self.assertGreaterEqual(len(lines), 5)
            self.assertTrue(lines[0].endswith(":"))
            self.assertTrue(lines[0].startswith("structure_test_while_start_0"))
            self.assertTrue(lines[-1].endswith(":"))
            self.assertTrue(lines[-1].startswith("structure_test_while_end_0"))
            
            cbz_found = False
            b_found = False
            for line in lines:
                if "cbz" in line:
                    cbz_found = True
                    self.assertIn("structure_test_while_end_0", line)
                if line.strip().startswith("b ") and "while_start_0" in line:
                    b_found = True
            
            self.assertTrue(cbz_found)
            self.assertTrue(b_found)


if __name__ == '__main__':
    unittest.main()
