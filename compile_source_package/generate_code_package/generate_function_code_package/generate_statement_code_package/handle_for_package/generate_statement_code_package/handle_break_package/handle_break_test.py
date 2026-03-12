import unittest
from .handle_break_src import handle_break


class TestHandleBreak(unittest.TestCase):
    
    def test_break_in_single_loop(self):
        """Test BREAK statement in a single loop context"""
        stmt = {"type": "BREAK", "target_loop_type": "FOR", "loop_depth": 1}
        func_name = "test_func"
        label_counter = {"loop_stack": ["L_end_1"]}
        var_offsets = {"i": 0}
        next_offset = 10
        
        code, offset = handle_break(stmt, func_name, label_counter, var_offsets, next_offset)
        
        self.assertEqual(code, "    B L_end_1\n")
        self.assertEqual(offset, 10)
    
    def test_break_in_nested_loops(self):
        """Test BREAK statement in nested loop context - should use innermost loop"""
        stmt = {"type": "BREAK", "target_loop_type": "FOR", "loop_depth": 2}
        func_name = "outer_func"
        label_counter = {"loop_stack": ["L_outer_end", "L_inner_end"]}
        var_offsets = {"i": 0, "j": 1}
        next_offset = 20
        
        code, offset = handle_break(stmt, func_name, label_counter, var_offsets, next_offset)
        
        self.assertEqual(code, "    B L_inner_end\n")
        self.assertEqual(offset, 20)
    
    def test_break_outside_loop_raises_error(self):
        """Test BREAK statement outside loop context raises ValueError"""
        stmt = {"type": "BREAK", "target_loop_type": "FOR", "loop_depth": 1}
        func_name = "test_func"
        label_counter = {"loop_stack": []}
        var_offsets = {}
        next_offset = 5
        
        with self.assertRaises(ValueError) as context:
            handle_break(stmt, func_name, label_counter, var_offsets, next_offset)
        
        self.assertIn("outside of loop context", str(context.exception))
    
    def test_break_outside_loop_missing_loop_stack(self):
        """Test BREAK statement when loop_stack key is missing"""
        stmt = {"type": "BREAK", "target_loop_type": "FOR", "loop_depth": 1}
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 5
        
        with self.assertRaises(ValueError) as context:
            handle_break(stmt, func_name, label_counter, var_offsets, next_offset)
        
        self.assertIn("outside of loop context", str(context.exception))
    
    def test_break_with_while_loop(self):
        """Test BREAK statement in WHILE loop context"""
        stmt = {"type": "BREAK", "target_loop_type": "WHILE", "loop_depth": 1}
        func_name = "while_func"
        label_counter = {"loop_stack": ["L_while_end"]}
        var_offsets = {"condition": 0}
        next_offset = 15
        
        code, offset = handle_break(stmt, func_name, label_counter, var_offsets, next_offset)
        
        self.assertEqual(code, "    B L_while_end\n")
        self.assertEqual(offset, 15)
    
    def test_break_ignores_func_name(self):
        """Test that func_name parameter doesn't affect BREAK output"""
        stmt = {"type": "BREAK", "target_loop_type": "FOR", "loop_depth": 1}
        label_counter = {"loop_stack": ["L_end"]}
        var_offsets = {}
        next_offset = 0
        
        code1, _ = handle_break(stmt, "func_a", label_counter, var_offsets, next_offset)
        code2, _ = handle_break(stmt, "func_b", label_counter, var_offsets, next_offset)
        
        self.assertEqual(code1, code2)
    
    def test_break_returns_unchanged_offset(self):
        """Test that next_offset is returned unchanged"""
        stmt = {"type": "BREAK", "target_loop_type": "FOR", "loop_depth": 1}
        func_name = "test"
        label_counter = {"loop_stack": ["L_end"]}
        var_offsets = {}
        
        for offset in [0, 1, 100, -1]:
            _, returned_offset = handle_break(stmt, func_name, label_counter, var_offsets, offset)
            self.assertEqual(returned_offset, offset)
    
    def test_break_with_deeply_nested_loops(self):
        """Test BREAK in deeply nested loop context (3+ levels)"""
        stmt = {"type": "BREAK", "target_loop_type": "FOR", "loop_depth": 3}
        func_name = "deep_func"
        label_counter = {"loop_stack": ["L1", "L2", "L3", "L4"]}
        var_offsets = {"i": 0, "j": 1, "k": 2}
        next_offset = 50
        
        code, offset = handle_break(stmt, func_name, label_counter, var_offsets, next_offset)
        
        self.assertEqual(code, "    B L4\n")
        self.assertEqual(offset, 50)
    
    def test_break_with_empty_stmt(self):
        """Test BREAK with minimal/empty statement dict"""
        stmt = {"type": "BREAK"}
        func_name = "minimal_func"
        label_counter = {"loop_stack": ["L_minimal"]}
        var_offsets = {}
        next_offset = 0
        
        code, offset = handle_break(stmt, func_name, label_counter, var_offsets, next_offset)
        
        self.assertEqual(code, "    B L_minimal\n")
        self.assertEqual(offset, 0)


if __name__ == "__main__":
    unittest.main()
