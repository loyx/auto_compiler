import unittest
from unittest.mock import patch

from .handle_while_src import handle_while


class TestHandleWhile(unittest.TestCase):
    
    def test_simple_while_loop(self):
        """Test basic while loop with one body statement."""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "VAR", "name": "x"},
            "body": [{"type": "ASSIGN", "var_name": "y", "value": {"type": "NUM", "value": 1}}]
        }
        func_name = "test_func"
        label_counter = {"while_cond": 0, "while_end": 0}
        var_offsets = {"x": 0, "y": 4}
        next_offset = 8
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.handle_while_src.evaluate_expression") as mock_eval:
            mock_eval.return_value = ("    ldr r0, [sp, #0]", 8)
            
            with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.handle_while_src.generate_statement_code") as mock_gen:
                mock_gen.return_value = ("    mov r1, #1\n    str r1, [sp, #4]", 8)
                
                assembly, offset = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)
                
                # Verify label_counter was incremented
                self.assertEqual(label_counter["while_cond"], 1)
                self.assertEqual(label_counter["while_end"], 1)
                
                # Verify assembly structure
                self.assertIn("test_func_while_cond_0:", assembly)
                self.assertIn("test_func_while_end_0:", assembly)
                self.assertIn("cmp r0, #0", assembly)
                self.assertIn("beq test_func_while_end_0", assembly)
                self.assertIn("b test_func_while_cond_0", assembly)
                
                # Verify offset returned
                self.assertEqual(offset, 8)
    
    def test_multiple_while_loops_increment_labels(self):
        """Test that multiple while loops get unique labels."""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "VAR", "name": "x"},
            "body": []
        }
        func_name = "test_func"
        label_counter = {"while_cond": 5, "while_end": 3}
        var_offsets = {"x": 0}
        next_offset = 4
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.handle_while_src.evaluate_expression") as mock_eval:
            mock_eval.return_value = ("    ldr r0, [sp, #0]", 4)
            
            assembly, offset = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)
            
            # Verify labels use the indices and increment
            self.assertEqual(label_counter["while_cond"], 6)
            self.assertEqual(label_counter["while_end"], 4)
            
            cond_label = "test_func_while_cond_5"
            end_label = "test_func_while_end_3"
            
            self.assertIn(cond_label, assembly)
            self.assertIn(end_label, assembly)
            self.assertIn(f"b {cond_label}", assembly)
    
    def test_empty_body(self):
        """Test while loop with empty body."""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "VAR", "name": "x"},
            "body": []
        }
        func_name = "test_func"
        label_counter = {"while_cond": 0, "while_end": 0}
        var_offsets = {"x": 0}
        next_offset = 4
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.handle_while_src.evaluate_expression") as mock_eval:
            mock_eval.return_value = ("    ldr r0, [sp, #0]", 4)
            
            assembly, offset = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)
            
            # Should still have proper structure
            self.assertIn("test_func_while_cond_0:", assembly)
            self.assertIn("test_func_while_end_0:", assembly)
            self.assertIn("cmp r0, #0", assembly)
            self.assertIn("beq test_func_while_end_0", assembly)
            self.assertIn("b test_func_while_cond_0", assembly)
    
    def test_missing_label_counter_keys(self):
        """Test when label_counter doesn't have expected keys."""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "VAR", "name": "x"},
            "body": []
        }
        func_name = "test_func"
        label_counter = {}  # Empty label_counter
        var_offsets = {"x": 0}
        next_offset = 4
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.handle_while_src.evaluate_expression") as mock_eval:
            mock_eval.return_value = ("    ldr r0, [sp, #0]", 4)
            
            assembly, offset = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)
            
            # Should default to 0 and increment to 1
            self.assertEqual(label_counter["while_cond"], 1)
            self.assertEqual(label_counter["while_end"], 1)
            self.assertIn("test_func_while_cond_0:", assembly)
            self.assertIn("test_func_while_end_0:", assembly)
    
    def test_evaluate_expression_called_with_correct_args(self):
        """Test that evaluate_expression is called with correct arguments."""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "VAR", "name": "x"},
            "body": []
        }
        func_name = "my_func"
        label_counter = {"while_cond": 0, "while_end": 0}
        var_offsets = {"x": 0}
        next_offset = 4
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.handle_while_src.evaluate_expression") as mock_eval:
            mock_eval.return_value = ("    ldr r0, [sp, #0]", 4)
            
            handle_while(stmt, func_name, label_counter, var_offsets, next_offset)
            
            mock_eval.assert_called_once_with({"type": "VAR", "name": "x"}, "my_func", var_offsets, 4)
    
    def test_generate_statement_code_called_for_each_body_stmt(self):
        """Test that generate_statement_code is called for each body statement."""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "VAR", "name": "x"},
            "body": [
                {"type": "ASSIGN", "var_name": "y", "value": {"type": "NUM", "value": 1}},
                {"type": "ASSIGN", "var_name": "z", "value": {"type": "NUM", "value": 2}}
            ]
        }
        func_name = "test_func"
        label_counter = {"while_cond": 0, "while_end": 0}
        var_offsets = {"x": 0, "y": 4, "z": 8}
        next_offset = 12
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.handle_while_src.evaluate_expression") as mock_eval:
            mock_eval.return_value = ("    ldr r0, [sp, #0]", 12)
            
            with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.handle_while_src.generate_statement_code") as mock_gen:
                mock_gen.return_value = ("    mov r1, #1", 12)
                
                handle_while(stmt, func_name, label_counter, var_offsets, next_offset)
                
                # Should be called twice for two body statements
                self.assertEqual(mock_gen.call_count, 2)
    
    def test_offset_propagation(self):
        """Test that offset is properly propagated through evaluate and generate calls."""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "VAR", "name": "x"},
            "body": [{"type": "ASSIGN", "var_name": "y", "value": {"type": "NUM", "value": 1}}]
        }
        func_name = "test_func"
        label_counter = {"while_cond": 0, "while_end": 0}
        var_offsets = {"x": 0, "y": 4}
        next_offset = 8
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.handle_while_src.evaluate_expression") as mock_eval:
            mock_eval.return_value = ("    ldr r0, [sp, #0]", 16)  # offset increases by 8
            
            with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.handle_while_src.generate_statement_code") as mock_gen:
                mock_gen.return_value = ("    mov r1, #1", 24)  # offset increases by 8 more
                
                assembly, offset = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)
                
                # evaluate_expression should be called with next_offset=8
                mock_eval.assert_called_once_with({"type": "VAR", "name": "x"}, "test_func", var_offsets, 8)
                
                # generate_statement_code should be called with offset=16 (after evaluate)
                mock_gen.assert_called_once()
                call_args = mock_gen.call_args
                self.assertEqual(call_args[0][4], 16)  # next_offset parameter
                
                # Final offset should be 24
                self.assertEqual(offset, 24)
    
    def test_assembly_code_order(self):
        """Test that assembly code is generated in correct order."""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "VAR", "name": "x"},
            "body": [{"type": "ASSIGN", "var_name": "y", "value": {"type": "NUM", "value": 1}}]
        }
        func_name = "test_func"
        label_counter = {"while_cond": 0, "while_end": 0}
        var_offsets = {"x": 0, "y": 4}
        next_offset = 8
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.handle_while_src.evaluate_expression") as mock_eval:
            mock_eval.return_value = ("COND_CODE", 8)
            
            with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.handle_while_src.generate_statement_code") as mock_gen:
                mock_gen.return_value = ("BODY_CODE", 8)
                
                assembly, offset = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)
                
                lines = assembly.split("\n")
                
                # Verify order: cond_label, cond_code, cmp, beq, body_code, b cond_label, end_label
                self.assertGreater(lines.index("test_func_while_cond_0:"), -1)
                cond_label_idx = lines.index("test_func_while_cond_0:")
                
                self.assertIn("COND_CODE", lines)
                cond_code_idx = lines.index("COND_CODE")
                self.assertGreater(cond_code_idx, cond_label_idx)
                
                cmp_idx = lines.index("    cmp r0, #0")
                self.assertGreater(cmp_idx, cond_code_idx)
                
                beq_idx = lines.index("    beq test_func_while_end_0")
                self.assertGreater(beq_idx, cmp_idx)
                
                body_idx = lines.index("BODY_CODE")
                self.assertGreater(body_idx, beq_idx)
                
                branch_back_idx = lines.index("    b test_func_while_cond_0")
                self.assertGreater(branch_back_idx, body_idx)
                
                end_label_idx = lines.index("test_func_while_end_0:")
                self.assertGreater(end_label_idx, branch_back_idx)


if __name__ == "__main__":
    unittest.main()
