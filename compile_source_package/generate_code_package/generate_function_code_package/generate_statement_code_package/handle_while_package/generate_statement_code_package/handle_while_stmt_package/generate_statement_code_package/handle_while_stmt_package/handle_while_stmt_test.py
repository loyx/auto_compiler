import unittest
from unittest.mock import patch

# Relative import for the function under test
from .handle_while_stmt_src import handle_while_stmt


class TestHandleWhileStmt(unittest.TestCase):
    
    def test_simple_while_loop(self):
        """Test a simple while loop with one body statement."""
        stmt = {
            "type": "while",
            "condition": {"type": "var", "name": "x"},
            "body": [{"type": "assign", "target": "y", "value": {"type": "literal", "value": 1}}]
        }
        func_name = "test_func"
        label_counter = {"while_cond": 0, "while_body": 0, "while_end": 0}
        var_offsets = {"x": 0, "y": 1}
        next_offset = 2
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.handle_while_stmt_package.handle_while_stmt_src.generate_expression_code") as mock_gen_expr, \
             patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_src.generate_statement_code") as mock_gen_stmt:
            
            mock_gen_expr.return_value = ("    LOAD_VAR x\n", 0, 3)
            mock_gen_stmt.return_value = ("    ASSIGN y\n", 3)
            
            code, new_offset = handle_while_stmt(stmt, func_name, label_counter, var_offsets, next_offset)
            
            # Verify label_counter was modified in-place
            self.assertEqual(label_counter["while_cond"], 1)
            self.assertEqual(label_counter["while_body"], 1)
            self.assertEqual(label_counter["while_end"], 1)
            
            # Verify code structure
            self.assertIn("test_func_while_cond_0:", code)
            self.assertIn("test_func_while_body_0:", code)
            self.assertIn("test_func_while_end_0:", code)
            self.assertIn("JUMP_IF_FALSE 0, test_func_while_end_0", code)
            self.assertIn("JUMP test_func_while_cond_0", code)
            
            # Verify return value
            self.assertEqual(new_offset, 3)
    
    def test_empty_while_body(self):
        """Test a while loop with empty body."""
        stmt = {
            "type": "while",
            "condition": {"type": "literal", "value": True},
            "body": []
        }
        func_name = "main"
        label_counter = {"while_cond": 5, "while_body": 3, "while_end": 7}
        var_offsets = {}
        next_offset = 0
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.handle_while_stmt_package.handle_while_stmt_src.generate_expression_code") as mock_gen_expr, \
             patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_src.generate_statement_code") as mock_gen_stmt:
            
            mock_gen_expr.return_value = ("    LOAD_TRUE\n", 0, 1)
            mock_gen_stmt.return_value = ("", 1)
            
            code, new_offset = handle_while_stmt(stmt, func_name, label_counter, var_offsets, next_offset)
            
            # Verify label_counter was incremented
            self.assertEqual(label_counter["while_cond"], 6)
            self.assertEqual(label_counter["while_body"], 4)
            self.assertEqual(label_counter["while_end"], 8)
            
            # Verify labels use the IDs before increment
            self.assertIn("main_while_cond_5:", code)
            self.assertIn("main_while_body_3:", code)
            self.assertIn("main_while_end_7:", code)
            
            # Empty body should still have jump back to condition
            self.assertIn("JUMP main_while_cond_5", code)
    
    def test_multiple_body_statements(self):
        """Test a while loop with multiple body statements."""
        stmt = {
            "type": "while",
            "condition": {"type": "binary", "op": "<", "left": {"type": "var", "name": "i"}, "right": {"type": "literal", "value": 10}},
            "body": [
                {"type": "assign", "target": "sum", "value": {"type": "binary", "op": "+", "left": {"type": "var", "name": "sum"}, "right": {"type": "var", "name": "i"}}},
                {"type": "assign", "target": "i", "value": {"type": "binary", "op": "+", "left": {"type": "var", "name": "i"}, "right": {"type": "literal", "value": 1}}}
            ]
        }
        func_name = "loop_func"
        label_counter = {"while_cond": 0, "while_body": 0, "while_end": 0}
        var_offsets = {"i": 0, "sum": 1}
        next_offset = 2
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.handle_while_stmt_package.handle_while_stmt_src.generate_expression_code") as mock_gen_expr, \
             patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_src.generate_statement_code") as mock_gen_stmt:
            
            mock_gen_expr.return_value = ("    LOAD_VAR i\n    LOAD_LITERAL 10\n    CMP_LT\n", 0, 5)
            mock_gen_stmt.side_effect = [
                ("    ADD sum, i\n", 5),
                ("    ADD i, 1\n", 6)
            ]
            
            code, new_offset = handle_while_stmt(stmt, func_name, label_counter, var_offsets, next_offset)
            
            # Verify generate_statement_code was called twice
            self.assertEqual(mock_gen_stmt.call_count, 2)
            
            # Verify final offset
            self.assertEqual(new_offset, 6)
    
    def test_missing_condition(self):
        """Test while statement with missing condition (edge case)."""
        stmt = {
            "type": "while",
            "body": [{"type": "assign", "target": "x", "value": {"type": "literal", "value": 0}}]
        }
        func_name = "test"
        label_counter = {"while_cond": 0, "while_body": 0, "while_end": 0}
        var_offsets = {"x": 0}
        next_offset = 1
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.handle_while_stmt_package.handle_while_stmt_src.generate_expression_code") as mock_gen_expr, \
             patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_src.generate_statement_code") as mock_gen_stmt:
            
            mock_gen_expr.return_value = ("", 0, 1)
            mock_gen_stmt.return_value = ("    ASSIGN x\n", 1)
            
            code, new_offset = handle_while_stmt(stmt, func_name, label_counter, var_offsets, next_offset)
            
            # Should still generate labels and structure
            self.assertIn("test_while_cond_0:", code)
            self.assertIn("test_while_body_0:", code)
            self.assertIn("test_while_end_0:", code)
    
    def test_missing_body(self):
        """Test while statement with missing body (edge case)."""
        stmt = {
            "type": "while",
            "condition": {"type": "literal", "value": True}
        }
        func_name = "test"
        label_counter = {"while_cond": 0, "while_body": 0, "while_end": 0}
        var_offsets = {}
        next_offset = 0
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.handle_while_stmt_package.handle_while_stmt_src.generate_expression_code") as mock_gen_expr, \
             patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_src.generate_statement_code") as mock_gen_stmt:
            
            mock_gen_expr.return_value = ("    LOAD_TRUE\n", 0, 1)
            mock_gen_stmt.return_value = ("", 1)
            
            code, new_offset = handle_while_stmt(stmt, func_name, label_counter, var_offsets, next_offset)
            
            # Should still generate all labels
            self.assertIn("test_while_cond_0:", code)
            self.assertIn("test_while_body_0:", code)
            self.assertIn("test_while_end_0:", code)
            # Should still have jump back to condition
            self.assertIn("JUMP test_while_cond_0", code)
    
    def test_label_counter_increment_order(self):
        """Verify label_counter is incremented in correct order."""
        stmt = {
            "type": "while",
            "condition": {"type": "var", "name": "flag"},
            "body": []
        }
        func_name = "func"
        label_counter = {"while_cond": 10, "while_body": 20, "while_end": 30}
        var_offsets = {"flag": 0}
        next_offset = 1
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.handle_while_stmt_package.handle_while_stmt_src.generate_expression_code") as mock_gen_expr, \
             patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_src.generate_statement_code") as mock_gen_stmt:
            
            mock_gen_expr.return_value = ("", 0, 1)
            mock_gen_stmt.return_value = ("", 1)
            
            code, new_offset = handle_while_stmt(stmt, func_name, label_counter, var_offsets, next_offset)
            
            # All counters should be incremented by 1
            self.assertEqual(label_counter["while_cond"], 11)
            self.assertEqual(label_counter["while_body"], 21)
            self.assertEqual(label_counter["while_end"], 31)
            
            # Labels should use original values (before increment)
            self.assertIn("func_while_cond_10:", code)
            self.assertIn("func_while_body_20:", code)
            self.assertIn("func_while_end_30:", code)
    
    def test_empty_label_counter(self):
        """Test when label_counter doesn't have while keys (uses default 0)."""
        stmt = {
            "type": "while",
            "condition": {"type": "literal", "value": False},
            "body": []
        }
        func_name = "test"
        label_counter = {}  # Empty, should default to 0
        var_offsets = {}
        next_offset = 0
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.handle_while_stmt_package.handle_while_stmt_src.generate_expression_code") as mock_gen_expr, \
             patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_src.generate_statement_code") as mock_gen_stmt:
            
            mock_gen_expr.return_value = ("    LOAD_FALSE\n", 0, 1)
            mock_gen_stmt.return_value = ("", 1)
            
            code, new_offset = handle_while_stmt(stmt, func_name, label_counter, var_offsets, next_offset)
            
            # Should use 0 as default and increment to 1
            self.assertEqual(label_counter["while_cond"], 1)
            self.assertEqual(label_counter["while_body"], 1)
            self.assertEqual(label_counter["while_end"], 1)
            
            # Labels should use 0
            self.assertIn("test_while_cond_0:", code)
            self.assertIn("test_while_body_0:", code)
            self.assertIn("test_while_end_0:", code)
    
    def test_code_order_structure(self):
        """Verify the exact order of code generation."""
        stmt = {
            "type": "while",
            "condition": {"type": "var", "name": "cond"},
            "body": [{"type": "nop"}]
        }
        func_name = "order_test"
        label_counter = {"while_cond": 0, "while_body": 0, "while_end": 0}
        var_offsets = {"cond": 0}
        next_offset = 1
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.handle_while_stmt_package.handle_while_stmt_src.generate_expression_code") as mock_gen_expr, \
             patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_src.generate_statement_code") as mock_gen_stmt:
            
            mock_gen_expr.return_value = ("    EVAL cond\n", 0, 2)
            mock_gen_stmt.return_value = ("    NOP\n", 2)
            
            code, new_offset = handle_while_stmt(stmt, func_name, label_counter, var_offsets, next_offset)
            
            # Verify order: cond_label, cond_code, JUMP_IF_FALSE, body_label, body_code, JUMP, end_label
            lines = code.split('\n')
            cond_label_idx = next(i for i, line in enumerate(lines) if "order_test_while_cond_0:" in line)
            body_label_idx = next(i for i, line in enumerate(lines) if "order_test_while_body_0:" in line)
            end_label_idx = next(i for i, line in enumerate(lines) if "order_test_while_end_0:" in line)
            
            # Labels should be in order
            self.assertLess(cond_label_idx, body_label_idx)
            self.assertLess(body_label_idx, end_label_idx)
            
            # JUMP_IF_FALSE should come after condition code, before body label
            jump_if_false_idx = next(i for i, line in enumerate(lines) if "JUMP_IF_FALSE" in line)
            self.assertGreater(jump_if_false_idx, cond_label_idx)
            self.assertLess(jump_if_false_idx, body_label_idx)
            
            # JUMP back should come after body, before end label
            jump_back_idx = next(i for i, line in enumerate(lines) if line.strip() == "JUMP order_test_while_cond_0")
            self.assertGreater(jump_back_idx, body_label_idx)
            self.assertLess(jump_back_idx, end_label_idx)


if __name__ == "__main__":
    unittest.main()
