import unittest
from unittest.mock import patch

# Relative import for the function under test
from .handle_while_stmt_src import handle_while_stmt


class TestHandleWhileStmt(unittest.TestCase):
    
    def test_simple_while_loop(self):
        """Test basic while loop with one body statement."""
        stmt = {
            "type": "while",
            "condition": {"type": "binary", "op": "<", "left": "i", "right": 10},
            "body": [{"type": "assignment", "var": "i", "value": 1}]
        }
        func_name = "test_func"
        label_counter = {"while_cond": 0, "while_end": 0, "if_else": 0, "if_end": 0}
        var_offsets = {"i": 0}
        next_offset = 16
        
        with patch("autoapp_workspace.workspace.projects.cc.files.main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code") as mock_gen_stmt, \
             patch("autoapp_workspace.workspace.projects.cc.files.main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            
            mock_gen_expr.return_value = ("cmp x0, x1", 16)
            mock_gen_stmt.return_value = ("str x0, [sp, #0]", 16)
            
            result_code, result_offset = handle_while_stmt(stmt, func_name, label_counter, var_offsets, next_offset)
            
            self.assertEqual(label_counter["while_cond"], 1)
            self.assertEqual(label_counter["while_end"], 1)
            self.assertIn("test_func_while_cond_0:", result_code)
            self.assertIn("test_func_while_end_1:", result_code)
            self.assertIn("cmp x0, x1", result_code)
            self.assertIn("cbz x0, test_func_while_end_1", result_code)
            self.assertIn("str x0, [sp, #0]", result_code)
            self.assertIn("b test_func_while_cond_0", result_code)
            self.assertEqual(result_offset, 16)
            mock_gen_expr.assert_called_once()
            mock_gen_stmt.assert_called_once()
    
    def test_empty_body(self):
        """Test while loop with empty body."""
        stmt = {
            "type": "while",
            "condition": {"type": "literal", "value": True},
            "body": []
        }
        func_name = "loop_func"
        label_counter = {"while_cond": 5, "while_end": 3}
        var_offsets = {}
        next_offset = 32
        
        with patch("autoapp_workspace.workspace.projects.cc.files.main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code") as mock_gen_stmt, \
             patch("autoapp_workspace.workspace.projects.cc.files.main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            
            mock_gen_expr.return_value = ("mov x0, #1", 32)
            
            result_code, result_offset = handle_while_stmt(stmt, func_name, label_counter, var_offsets, next_offset)
            
            self.assertEqual(label_counter["while_cond"], 6)
            self.assertEqual(label_counter["while_end"], 4)
            self.assertIn("loop_func_while_cond_5:", result_code)
            self.assertIn("loop_func_while_end_4:", result_code)
            self.assertIn("mov x0, #1", result_code)
            self.assertIn("cbz x0, loop_func_while_end_4", result_code)
            self.assertIn("b loop_func_while_cond_5", result_code)
            self.assertEqual(result_offset, 32)
            mock_gen_stmt.assert_not_called()
    
    def test_multiple_body_statements(self):
        """Test while loop with multiple body statements."""
        stmt = {
            "type": "while",
            "condition": {"type": "binary", "op": "!=", "left": "x", "right": 0},
            "body": [
                {"type": "assignment", "var": "a", "value": 1},
                {"type": "assignment", "var": "b", "value": 2},
                {"type": "assignment", "var": "c", "value": 3}
            ]
        }
        func_name = "multi_stmt"
        label_counter = {"while_cond": 2, "while_end": 2}
        var_offsets = {"x": 0, "a": 8, "b": 16, "c": 24}
        next_offset = 32
        
        with patch("autoapp_workspace.workspace.projects.cc.files.main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code") as mock_gen_stmt, \
             patch("autoapp_workspace.workspace.projects.cc.files.main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            
            mock_gen_expr.return_value = ("ldr x0, [sp, #0]", 32)
            mock_gen_stmt.side_effect = [
                ("str x1, [sp, #8]", 32),
                ("str x2, [sp, #16]", 32),
                ("str x3, [sp, #24]", 32)
            ]
            
            result_code, result_offset = handle_while_stmt(stmt, func_name, label_counter, var_offsets, next_offset)
            
            self.assertEqual(label_counter["while_cond"], 3)
            self.assertEqual(label_counter["while_end"], 3)
            self.assertEqual(mock_gen_stmt.call_count, 3)
            self.assertEqual(result_offset, 32)
    
    def test_label_counter_increment(self):
        """Test that label_counter is modified in-place correctly."""
        stmt = {
            "type": "while",
            "condition": {"type": "literal", "value": 1},
            "body": []
        }
        func_name = "counter_test"
        label_counter = {"while_cond": 10, "while_end": 20}
        var_offsets = {}
        next_offset = 0
        
        with patch("autoapp_workspace.workspace.projects.cc.files.main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code") as mock_gen_stmt, \
             patch("autoapp_workspace.workspace.projects.cc.files.main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            
            mock_gen_expr.return_value = ("nop", 0)
            
            handle_while_stmt(stmt, func_name, label_counter, var_offsets, next_offset)
            
            self.assertEqual(label_counter["while_cond"], 11)
            self.assertEqual(label_counter["while_end"], 21)
    
    def test_next_offset_propagation(self):
        """Test that next_offset is properly propagated through calls."""
        stmt = {
            "type": "while",
            "condition": {"type": "literal", "value": 1},
            "body": [{"type": "assignment", "var": "x", "value": 1}]
        }
        func_name = "offset_test"
        label_counter = {"while_cond": 0, "while_end": 0}
        var_offsets = {"x": 0}
        next_offset = 100
        
        with patch("autoapp_workspace.workspace.projects.cc.files.main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code") as mock_gen_stmt, \
             patch("autoapp_workspace.workspace.projects.cc.files.main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            
            mock_gen_expr.return_value = ("add x0, x0, #1", 108)
            mock_gen_stmt.return_value = ("str x0, [sp, #0]", 116)
            
            result_code, result_offset = handle_while_stmt(stmt, func_name, label_counter, var_offsets, next_offset)
            
            self.assertEqual(result_offset, 116)
            mock_gen_expr.assert_called_once_with({"type": "literal", "value": 1}, var_offsets, 100)
            mock_gen_stmt.assert_called_once()
    
    def test_default_condition_and_body(self):
        """Test handling of missing condition and body keys."""
        stmt = {
            "type": "while"
        }
        func_name = "default_test"
        label_counter = {"while_cond": 0, "while_end": 0}
        var_offsets = {}
        next_offset = 0
        
        with patch("autoapp_workspace.workspace.projects.cc.files.main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code") as mock_gen_stmt, \
             patch("autoapp_workspace.workspace.projects.cc.files.main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            
            mock_gen_expr.return_value = ("", 0)
            
            result_code, result_offset = handle_while_stmt(stmt, func_name, label_counter, var_offsets, next_offset)
            
            self.assertEqual(label_counter["while_cond"], 1)
            self.assertEqual(label_counter["while_end"], 1)
            self.assertIn("default_test_while_cond_0:", result_code)
            self.assertIn("default_test_while_end_1:", result_code)
            mock_gen_expr.assert_called_once_with({}, var_offsets, 0)
            mock_gen_stmt.assert_not_called()


if __name__ == "__main__":
    unittest.main()
