import unittest
from unittest.mock import patch

from .handle_call_src import handle_call


class TestHandleCall(unittest.TestCase):
    
    @patch('generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_call_package.handle_call_src.evaluate_expression')
    def test_call_no_arguments(self, mock_eval):
        """Test CALL statement with no arguments."""
        stmt = {
            "type": "CALL",
            "func_name": "my_function",
            "arguments": []
        }
        
        code, offset = handle_call(stmt, "main", {}, {}, 0)
        
        self.assertEqual(offset, 0)
        self.assertIn("BL my_function", code)
        self.assertNotIn("PUSH", code)
        self.assertNotIn("ADD SP", code)
        mock_eval.assert_not_called()
    
    @patch('generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_call_package.handle_call_src.evaluate_expression')
    def test_call_one_argument(self, mock_eval):
        """Test CALL statement with one argument (goes to R0)."""
        stmt = {
            "type": "CALL",
            "func_name": "my_function",
            "arguments": [{"type": "literal", "value": 42}]
        }
        mock_eval.return_value = "MOV R0, #42"
        
        code, offset = handle_call(stmt, "main", {}, {}, 0)
        
        self.assertEqual(offset, 0)
        mock_eval.assert_called_once()
        self.assertIn("MOV R0, #42", code)
        self.assertIn("BL my_function", code)
        self.assertNotIn("MOV R1", code)
        self.assertNotIn("PUSH", code)
    
    @patch('generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_call_package.handle_call_src.evaluate_expression')
    def test_call_four_arguments(self, mock_eval):
        """Test CALL statement with exactly 4 arguments (all in registers R0-R3)."""
        stmt = {
            "type": "CALL",
            "func_name": "my_function",
            "arguments": [
                {"type": "literal", "value": 1},
                {"type": "literal", "value": 2},
                {"type": "literal", "value": 3},
                {"type": "literal", "value": 4}
            ]
        }
        mock_eval.side_effect = ["MOV R0, #1", "MOV R0, #2", "MOV R0, #3", "MOV R0, #4"]
        
        code, offset = handle_call(stmt, "main", {}, {}, 0)
        
        self.assertEqual(offset, 0)
        self.assertEqual(mock_eval.call_count, 4)
        self.assertIn("BL my_function", code)
        self.assertIn("MOV R1, R0", code)
        self.assertIn("MOV R2, R0", code)
        self.assertIn("MOV R3, R0", code)
        self.assertNotIn("PUSH", code)
        self.assertNotIn("ADD SP", code)
    
    @patch('generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_call_package.handle_call_src.evaluate_expression')
    def test_call_five_arguments(self, mock_eval):
        """Test CALL statement with 5 arguments (4 in registers, 1 on stack)."""
        stmt = {
            "type": "CALL",
            "func_name": "my_function",
            "arguments": [
                {"type": "literal", "value": 1},
                {"type": "literal", "value": 2},
                {"type": "literal", "value": 3},
                {"type": "literal", "value": 4},
                {"type": "literal", "value": 5}
            ]
        }
        mock_eval.side_effect = [
            "MOV R0, #1", "MOV R0, #2", "MOV R0, #3", "MOV R0, #4", "MOV R0, #5"
        ]
        
        code, offset = handle_call(stmt, "main", {}, {}, 0)
        
        self.assertEqual(offset, 0)
        self.assertEqual(mock_eval.call_count, 5)
        self.assertIn("BL my_function", code)
        self.assertIn("PUSH {R0}", code)
        self.assertIn("ADD SP, SP, #4", code)
        self.assertEqual(code.count("PUSH {R0}"), 1)
    
    @patch('generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_call_package.handle_call_src.evaluate_expression')
    def test_call_six_arguments(self, mock_eval):
        """Test CALL statement with 6 arguments (4 in registers, 2 on stack)."""
        stmt = {
            "type": "CALL",
            "func_name": "my_function",
            "arguments": [
                {"type": "literal", "value": i} for i in range(1, 7)
            ]
        }
        mock_eval.side_effect = [f"MOV R0, #{i}" for i in range(1, 7)]
        
        code, offset = handle_call(stmt, "main", {}, {}, 0)
        
        self.assertEqual(offset, 0)
        self.assertEqual(mock_eval.call_count, 6)
        self.assertIn("BL my_function", code)
        self.assertEqual(code.count("PUSH {R0}"), 2)
        self.assertIn("ADD SP, SP, #8", code)
    
    @patch('generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_call_package.handle_call_src.evaluate_expression')
    def test_call_many_arguments(self, mock_eval):
        """Test CALL statement with many arguments (>4)."""
        num_args = 10
        stmt = {
            "type": "CALL",
            "func_name": "big_function",
            "arguments": [{"type": "literal", "value": i} for i in range(num_args)]
        }
        mock_eval.side_effect = [f"MOV R0, #{i}" for i in range(num_args)]
        
        code, offset = handle_call(stmt, "main", {}, {}, 0)
        
        self.assertEqual(offset, 0)
        self.assertEqual(mock_eval.call_count, num_args)
        self.assertIn("BL big_function", code)
        stack_arg_count = num_args - 4
        self.assertEqual(code.count("PUSH {R0}"), stack_arg_count)
        self.assertIn("ADD SP, SP, #24", code)
    
    def test_call_missing_func_name(self):
        """Test that ValueError is raised when func_name is missing."""
        stmt = {
            "type": "CALL",
            "arguments": []
        }
        
        with self.assertRaises(ValueError) as context:
            handle_call(stmt, "main", {}, {}, 0)
        
        self.assertIn("func_name", str(context.exception))
    
    @patch('generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_call_package.handle_call_src.evaluate_expression')
    def test_call_preserves_next_offset(self, mock_eval):
        """Test that next_offset is returned unchanged."""
        stmt = {
            "type": "CALL",
            "func_name": "my_function",
            "arguments": []
        }
        
        _, offset = handle_call(stmt, "main", {}, {}, 100)
        self.assertEqual(offset, 100)
        
        _, offset = handle_call(stmt, "main", {}, {}, 0)
        self.assertEqual(offset, 0)
        
        _, offset = handle_call(stmt, "main", {}, {}, -50)
        self.assertEqual(offset, -50)
    
    @patch('generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_call_package.handle_call_src.evaluate_expression')
    def test_call_uses_evaluate_expression(self, mock_eval):
        """Test that evaluate_expression is called for each argument."""
        stmt = {
            "type": "CALL",
            "func_name": "my_function",
            "arguments": [
                {"type": "literal", "value": 1},
                {"type": "identifier", "name": "x"},
                {"type": "binary", "op": "+", "left": {"type": "literal", "value": 2}, "right": {"type": "literal", "value": 3}}
            ]
        }
        mock_eval.return_value = "MOV R0, #0"
        
        handle_call(stmt, "main", {}, {}, 0)
        
        self.assertEqual(mock_eval.call_count, 3)
        for call_args in mock_eval.call_args_list:
            self.assertEqual(len(call_args[0]), 2)
            self.assertIsInstance(call_args[0][0], dict)
            self.assertIsInstance(call_args[0][1], dict)
    
    @patch('generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_call_package.handle_call_src.evaluate_expression')
    def test_call_with_var_offsets(self, mock_eval):
        """Test that var_offsets is passed to evaluate_expression."""
        stmt = {
            "type": "CALL",
            "func_name": "my_function",
            "arguments": [{"type": "identifier", "name": "x"}]
        }
        mock_eval.return_value = "LDR R0, [SP, #0]"
        var_offsets = {"x": 0, "y": 4}
        
        handle_call(stmt, "main", {}, var_offsets, 0)
        
        mock_eval.assert_called_once()
        call_args = mock_eval.call_args
        self.assertEqual(call_args[0][1], var_offsets)
    
    @patch('generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_call_package.handle_call_src.evaluate_expression')
    def test_call_code_order(self, mock_eval):
        """Test that generated code has correct order: eval args, BL, cleanup."""
        stmt = {
            "type": "CALL",
            "func_name": "my_function",
            "arguments": [
                {"type": "literal", "value": 1},
                {"type": "literal", "value": 2},
                {"type": "literal", "value": 5}
            ]
        }
        mock_eval.side_effect = ["MOV R0, #1", "MOV R0, #2", "MOV R0, #5"]
        
        code, _ = handle_call(stmt, "main", {}, {}, 0)
        lines = code.split("\n")
        
        bl_index = None
        add_sp_index = None
        for i, line in enumerate(lines):
            if "BL my_function" in line:
                bl_index = i
            if "ADD SP" in line:
                add_sp_index = i
        
        self.assertIsNotNone(bl_index)
        self.assertIsNone(add_sp_index)
        self.assertGreater(bl_index, 0)
    
    @patch('generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_call_package.handle_call_src.evaluate_expression')
    def test_call_stack_cleanup_after_bl(self, mock_eval):
        """Test that stack cleanup comes after BL instruction."""
        stmt = {
            "type": "CALL",
            "func_name": "my_function",
            "arguments": [{"type": "literal", "value": i} for i in range(6)]
        }
        mock_eval.side_effect = [f"MOV R0, #{i}" for i in range(6)]
        
        code, _ = handle_call(stmt, "main", {}, {}, 0)
        lines = code.split("\n")
        
        bl_index = None
        add_sp_index = None
        for i, line in enumerate(lines):
            if "BL my_function" in line:
                bl_index = i
            if "ADD SP" in line:
                add_sp_index = i
        
        self.assertIsNotNone(bl_index)
        self.assertIsNotNone(add_sp_index)
        self.assertGreater(add_sp_index, bl_index)


if __name__ == "__main__":
    unittest.main()
