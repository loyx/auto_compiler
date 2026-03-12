import unittest
from unittest.mock import patch

# Relative import for the function under test
from .handle_call_src import handle_call


class TestHandleCall(unittest.TestCase):
    
    @patch('handle_call_package.handle_call_src.evaluate_expression')
    def test_call_with_no_args(self, mock_eval):
        """Test function call with no arguments."""
        stmt = {
            "type": "CALL",
            "function": "printf",
            "args": []
        }
        
        func_name = "main"
        label_counter = {}
        var_offsets = {}
        next_offset = 0
        
        assembly, offset = handle_call(stmt, func_name, label_counter, var_offsets, next_offset)
        
        # Should only generate the bl instruction
        self.assertEqual(assembly, "    bl printf")
        self.assertEqual(offset, 0)
        mock_eval.assert_not_called()
    
    @patch('handle_call_package.handle_call_src.evaluate_expression')
    def test_call_with_one_arg(self, mock_eval):
        """Test function call with one argument in r0."""
        stmt = {
            "type": "CALL",
            "function": "print_int",
            "args": [{"type": "literal", "value": 42}]
        }
        
        mock_eval.return_value = ("    mov r0, #42", 0, "r5")
        
        func_name = "main"
        label_counter = {}
        var_offsets = {}
        next_offset = 0
        
        assembly, offset = handle_call(stmt, func_name, label_counter, var_offsets, next_offset)
        
        # Should evaluate arg, mov to r0, then bl
        expected = "    mov r0, #42\n    mov r0, r5\n    bl print_int"
        self.assertEqual(assembly, expected)
        self.assertEqual(offset, 0)
        mock_eval.assert_called_once()
    
    @patch('handle_call_package.handle_call_src.evaluate_expression')
    def test_call_with_four_args(self, mock_eval):
        """Test function call with exactly 4 arguments (all in registers)."""
        stmt = {
            "type": "CALL",
            "function": "add_four",
            "args": [
                {"type": "literal", "value": 1},
                {"type": "literal", "value": 2},
                {"type": "literal", "value": 3},
                {"type": "literal", "value": 4}
            ]
        }
        
        # Mock evaluate_expression to return different registers for each arg
        mock_eval.side_effect = [
            ("    mov r0, #1", 0, "r5"),
            ("    mov r1, #2", 0, "r6"),
            ("    mov r2, #3", 0, "r7"),
            ("    mov r3, #4", 0, "r8")
        ]
        
        func_name = "main"
        label_counter = {}
        var_offsets = {}
        next_offset = 0
        
        assembly, offset = handle_call(stmt, func_name, label_counter, var_offsets, next_offset)
        
        lines = assembly.split('\n')
        self.assertEqual(len(lines), 9)  # 4 eval codes + 4 movs + 1 bl = 9 lines
        
        # Check that args are moved to r0-r3
        self.assertIn("    mov r0, r5", assembly)
        self.assertIn("    mov r1, r6", assembly)
        self.assertIn("    mov r2, r7", assembly)
        self.assertIn("    mov r3, r8", assembly)
        self.assertIn("    bl add_four", assembly)
        self.assertEqual(offset, 0)
        self.assertEqual(mock_eval.call_count, 4)
    
    @patch('handle_call_package.handle_call_src.evaluate_expression')
    def test_call_with_more_than_four_args(self, mock_eval):
        """Test function call with more than 4 arguments (some on stack)."""
        stmt = {
            "type": "CALL",
            "function": "multi_arg_func",
            "args": [
                {"type": "literal", "value": 1},
                {"type": "literal", "value": 2},
                {"type": "literal", "value": 3},
                {"type": "literal", "value": 4},
                {"type": "literal", "value": 5},
                {"type": "literal", "value": 6}
            ]
        }
        
        # Mock evaluate_expression to return different registers for each arg
        mock_eval.side_effect = [
            ("    mov r0, #1", 0, "r5"),
            ("    mov r1, #2", 0, "r6"),
            ("    mov r2, #3", 0, "r7"),
            ("    mov r3, #4", 0, "r8"),
            ("    mov r0, #5", 100, "r9"),
            ("    mov r0, #6", 100, "r10")
        ]
        
        func_name = "main"
        label_counter = {}
        var_offsets = {}
        next_offset = 0
        
        assembly, offset = handle_call(stmt, func_name, label_counter, var_offsets, next_offset)
        
        # First 4 args should be in r0-r3
        self.assertIn("    mov r0, r5", assembly)
        self.assertIn("    mov r1, r6", assembly)
        self.assertIn("    mov r2, r7", assembly)
        self.assertIn("    mov r3, r8", assembly)
        
        # 5th and 6th args should be on stack at offsets 0 and 4
        self.assertIn("    str r9, [sp, #0]", assembly)
        self.assertIn("    str r10, [sp, #4]", assembly)
        
        self.assertIn("    bl multi_arg_func", assembly)
        self.assertEqual(offset, 100)
        self.assertEqual(mock_eval.call_count, 6)
    
    @patch('handle_call_package.handle_call_src.evaluate_expression')
    def test_call_arg_already_in_correct_register(self, mock_eval):
        """Test that no mov is generated when arg is already in correct register."""
        stmt = {
            "type": "CALL",
            "function": "identity",
            "args": [{"type": "literal", "value": 42}]
        }
        
        # Mock evaluate_expression to return r0 directly
        mock_eval.return_value = ("    mov r0, #42", 0, "r0")
        
        func_name = "main"
        label_counter = {}
        var_offsets = {}
        next_offset = 0
        
        assembly, offset = handle_call(stmt, func_name, label_counter, var_offsets, next_offset)
        
        # Should not generate extra mov when already in r0
        expected = "    mov r0, #42\n    bl identity"
        self.assertEqual(assembly, expected)
        self.assertEqual(offset, 0)
    
    @patch('handle_call_package.handle_call_src.evaluate_expression')
    def test_call_with_offset_progression(self, mock_eval):
        """Test that offset is properly tracked through multiple argument evaluations."""
        stmt = {
            "type": "CALL",
            "function": "test_func",
            "args": [
                {"type": "literal", "value": 1},
                {"type": "literal", "value": 2},
                {"type": "literal", "value": 3}
            ]
        }
        
        # Mock evaluate_expression to return increasing offsets
        mock_eval.side_effect = [
            ("    mov r0, #1", 10, "r5"),
            ("    mov r1, #2", 20, "r6"),
            ("    mov r2, #3", 30, "r7")
        ]
        
        func_name = "main"
        label_counter = {}
        var_offsets = {}
        next_offset = 0
        
        assembly, offset = handle_call(stmt, func_name, label_counter, var_offsets, next_offset)
        
        # Final offset should be 30 (from last evaluation)
        self.assertEqual(offset, 30)
    
    @patch('handle_call_package.handle_call_src.evaluate_expression')
    def test_call_with_missing_function_key(self, mock_eval):
        """Test handling of stmt with missing function key."""
        stmt = {
            "type": "CALL",
            "args": []
        }
        
        func_name = "main"
        label_counter = {}
        var_offsets = {}
        next_offset = 0
        
        assembly, offset = handle_call(stmt, func_name, label_counter, var_offsets, next_offset)
        
        # Should use empty string as function name
        self.assertEqual(assembly, "    bl ")
        self.assertEqual(offset, 0)
    
    @patch('handle_call_package.handle_call_src.evaluate_expression')
    def test_call_with_missing_args_key(self, mock_eval):
        """Test handling of stmt with missing args key."""
        stmt = {
            "type": "CALL",
            "function": "test_func"
        }
        
        func_name = "main"
        label_counter = {}
        var_offsets = {}
        next_offset = 0
        
        assembly, offset = handle_call(stmt, func_name, label_counter, var_offsets, next_offset)
        
        # Should default to empty args list
        self.assertEqual(assembly, "    bl test_func")
        self.assertEqual(offset, 0)
        mock_eval.assert_not_called()
    
    @patch('handle_call_package.handle_call_src.evaluate_expression')
    def test_call_preserves_var_offsets(self, mock_eval):
        """Test that var_offsets is not modified by handle_call."""
        stmt = {
            "type": "CALL",
            "function": "test_func",
            "args": [{"type": "var", "name": "x"}]
        }
        
        mock_eval.return_value = ("    ldr r0, [sp, #0]", 0, "r0")
        
        var_offsets = {"x": 0, "y": 4}
        original_offsets = var_offsets.copy()
        
        func_name = "main"
        label_counter = {}
        next_offset = 0
        
        handle_call(stmt, func_name, label_counter, var_offsets, next_offset)
        
        # var_offsets should not be modified
        self.assertEqual(var_offsets, original_offsets)
    
    @patch('handle_call_package.handle_call_src.evaluate_expression')
    def test_call_preserves_label_counter(self, mock_eval):
        """Test that label_counter is not modified by handle_call."""
        stmt = {
            "type": "CALL",
            "function": "test_func",
            "args": []
        }
        
        label_counter = {"while_cond": 0, "if_end": 1}
        original_counter = label_counter.copy()
        
        func_name = "main"
        var_offsets = {}
        next_offset = 0
        
        handle_call(stmt, func_name, label_counter, var_offsets, next_offset)
        
        # label_counter should not be modified
        self.assertEqual(label_counter, original_counter)


if __name__ == '__main__':
    unittest.main()
