import unittest
from typing import Dict
from .handle_continue_stmt_src import handle_continue_stmt


class TestHandleContinueStmt(unittest.TestCase):
    """Test cases for handle_continue_stmt function."""
    
    def test_happy_path_first_call(self):
        """Test first CONTINUE statement with empty label_counter."""
        stmt = {"type": "continue"}
        func_name = "test_func"
        label_counter: Dict[str, int] = {}
        
        branch_code, next_offset = handle_continue_stmt(stmt, func_name, label_counter)
        
        # Verify branch code format
        self.assertEqual(branch_code, "b test_func_while_cond_1")
        # Verify next_offset is 0
        self.assertEqual(next_offset, 0)
        # Verify label_counter was modified in-place
        self.assertEqual(label_counter["continue"], 1)
    
    def test_happy_path_second_call(self):
        """Test second CONTINUE statement with existing counter."""
        stmt = {"type": "continue"}
        func_name = "test_func"
        label_counter: Dict[str, int] = {"continue": 1}
        
        branch_code, next_offset = handle_continue_stmt(stmt, func_name, label_counter)
        
        # Verify branch code format with incremented counter
        self.assertEqual(branch_code, "b test_func_while_cond_2")
        # Verify next_offset is 0
        self.assertEqual(next_offset, 0)
        # Verify label_counter was incremented in-place
        self.assertEqual(label_counter["continue"], 2)
    
    def test_multiple_calls_increment_correctly(self):
        """Test that multiple calls increment counter correctly."""
        stmt = {"type": "continue"}
        func_name = "my_func"
        label_counter: Dict[str, int] = {}
        
        # First call
        branch_code1, _ = handle_continue_stmt(stmt, func_name, label_counter)
        self.assertEqual(branch_code1, "b my_func_while_cond_1")
        self.assertEqual(label_counter["continue"], 1)
        
        # Second call
        branch_code2, _ = handle_continue_stmt(stmt, func_name, label_counter)
        self.assertEqual(branch_code2, "b my_func_while_cond_2")
        self.assertEqual(label_counter["continue"], 2)
        
        # Third call
        branch_code3, _ = handle_continue_stmt(stmt, func_name, label_counter)
        self.assertEqual(branch_code3, "b my_func_while_cond_3")
        self.assertEqual(label_counter["continue"], 3)
    
    def test_different_func_names(self):
        """Test with different function names."""
        stmt = {"type": "continue"}
        label_counter: Dict[str, int] = {}
        
        branch_code1, _ = handle_continue_stmt(stmt, "func_a", label_counter)
        self.assertEqual(branch_code1, "b func_a_while_cond_1")
        
        branch_code2, _ = handle_continue_stmt(stmt, "func_b", label_counter)
        self.assertEqual(branch_code2, "b func_b_while_cond_2")
    
    def test_stmt_content_ignored(self):
        """Test that stmt content beyond type is ignored."""
        func_name = "test_func"
        label_counter: Dict[str, int] = {}
        
        # Different stmt contents should produce same result pattern
        stmt1 = {"type": "continue"}
        stmt2 = {"type": "continue", "extra": "data"}
        stmt3 = {}
        
        branch_code1, _ = handle_continue_stmt(stmt1, func_name, label_counter)
        self.assertEqual(branch_code1, "b test_func_while_cond_1")
        
        branch_code2, _ = handle_continue_stmt(stmt2, func_name, label_counter)
        self.assertEqual(branch_code2, "b test_func_while_cond_2")
        
        branch_code3, _ = handle_continue_stmt(stmt3, func_name, label_counter)
        self.assertEqual(branch_code3, "b test_func_while_cond_3")
    
    def test_return_type(self):
        """Test that return type is correct."""
        stmt = {"type": "continue"}
        func_name = "test_func"
        label_counter: Dict[str, int] = {}
        
        result = handle_continue_stmt(stmt, func_name, label_counter)
        
        # Verify return type is tuple
        self.assertIsInstance(result, tuple)
        # Verify tuple length is 2
        self.assertEqual(len(result), 2)
        # Verify first element is string
        self.assertIsInstance(result[0], str)
        # Verify second element is int
        self.assertIsInstance(result[1], int)
    
    def test_label_counter_not_replaced(self):
        """Test that label_counter is modified in-place, not replaced."""
        stmt = {"type": "continue"}
        func_name = "test_func"
        label_counter: Dict[str, int] = {"other_key": 42}
        
        original_id = id(label_counter)
        handle_continue_stmt(stmt, func_name, label_counter)
        
        # Verify same object
        self.assertEqual(id(label_counter), original_id)
        # Verify other keys preserved
        self.assertEqual(label_counter["other_key"], 42)
        # Verify continue key added
        self.assertEqual(label_counter["continue"], 1)


if __name__ == "__main__":
    unittest.main()
