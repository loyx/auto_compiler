import unittest
from unittest.mock import patch

from .handle_assign_src import handle_assign


class TestHandleAssign(unittest.TestCase):
    """Test cases for handle_assign function."""
    
    def test_happy_path_simple_assignment(self):
        """Test simple assignment with literal value."""
        stmt = {
            "target": "x",
            "value": {"type": "literal", "value": 42}
        }
        func_name = "test_func"
        label_counter = {}
        var_offsets = {"x": 0}
        next_offset = 10
        
        with patch('.handle_assign_src.evaluate_expression') as mock_eval:
            mock_eval.return_value = ("mov r0, #42\n", 10)
            
            code, offset = handle_assign(stmt, func_name, label_counter, var_offsets, next_offset)
            
            self.assertIn("mov r0, #42\n", code)
            self.assertIn("str r0, [sp, #0]", code)
            self.assertEqual(offset, 10)
    
    def test_undefined_variable_raises_value_error(self):
        """Test that undefined variable raises ValueError."""
        stmt = {
            "target": "undefined_var",
            "value": {"type": "literal", "value": 42}
        }
        func_name = "test_func"
        label_counter = {}
        var_offsets = {"x": 0}
        next_offset = 10
        
        with self.assertRaises(ValueError) as context:
            handle_assign(stmt, func_name, label_counter, var_offsets, next_offset)
        
        self.assertIn("undefined_var", str(context.exception))
    
    def test_evaluate_expression_called_with_correct_params(self):
        """Test that evaluate_expression is called with correct parameters."""
        stmt = {
            "target": "x",
            "value": {"type": "literal", "value": 42}
        }
        func_name = "test_func"
        label_counter = {"while_cond": 0}
        var_offsets = {"x": 0}
        next_offset = 10
        
        with patch('handle_assign_package.handle_assign_src.evaluate_expression') as mock_eval:
            mock_eval.return_value = ("mov r0, #42\n", 10)
            
            handle_assign(stmt, func_name, label_counter, var_offsets, next_offset)
            
            mock_eval.assert_called_once_with(
                {"type": "literal", "value": 42},
                "test_func",
                {"while_cond": 0},
                {"x": 0},
                10
            )
    
    def test_assembly_code_format(self):
        """Test that generated assembly code has correct format."""
        stmt = {
            "target": "y",
            "value": {"type": "literal", "value": 100}
        }
        func_name = "main"
        label_counter = {}
        var_offsets = {"y": 4}
        next_offset = 8
        
        with patch('handle_assign_package.handle_assign_src.evaluate_expression') as mock_eval:
            mock_eval.return_value = ("mov r0, #100\n", 8)
            
            code, offset = handle_assign(stmt, func_name, label_counter, var_offsets, next_offset)
            
            self.assertIn("str r0, [sp, #4]", code)
            self.assertTrue(code.endswith("\n"))
    
    def test_offset_from_evaluate_expression_is_returned(self):
        """Test that offset returned is from evaluate_expression, not modified."""
        stmt = {
            "target": "z",
            "value": {"type": "literal", "value": 5}
        }
        func_name = "test"
        label_counter = {}
        var_offsets = {"z": 8}
        next_offset = 16
        
        with patch('handle_assign_package.handle_assign_src.evaluate_expression') as mock_eval:
            mock_eval.return_value = ("mov r0, #5\n", 20)
            
            code, offset = handle_assign(stmt, func_name, label_counter, var_offsets, next_offset)
            
            self.assertEqual(offset, 20)
    
    def test_complex_value_expression(self):
        """Test assignment with complex value expression (binary operation)."""
        stmt = {
            "target": "result",
            "value": {
                "type": "binop",
                "op": "add",
                "left": {"type": "var", "name": "a"},
                "right": {"type": "var", "name": "b"}
            }
        }
        func_name = "compute"
        label_counter = {}
        var_offsets = {"result": 0, "a": 4, "b": 8}
        next_offset = 12
        
        with patch('handle_assign_package.handle_assign_src.evaluate_expression') as mock_eval:
            mock_eval.return_value = ("ldr r0, [sp, #4]\nldr r1, [sp, #8]\nadd r0, r0, r1\n", 12)
            
            code, offset = handle_assign(stmt, func_name, label_counter, var_offsets, next_offset)
            
            mock_eval.assert_called_once()
            self.assertIn("str r0, [sp, #0]", code)
            self.assertEqual(offset, 12)
    
    def test_zero_offset_variable(self):
        """Test assignment to variable at offset 0."""
        stmt = {
            "target": "first_var",
            "value": {"type": "literal", "value": 0}
        }
        func_name = "test"
        label_counter = {}
        var_offsets = {"first_var": 0}
        next_offset = 4
        
        with patch('handle_assign_package.handle_assign_src.evaluate_expression') as mock_eval:
            mock_eval.return_value = ("mov r0, #0\n", 4)
            
            code, offset = handle_assign(stmt, func_name, label_counter, var_offsets, next_offset)
            
            self.assertIn("str r0, [sp, #0]", code)
            self.assertEqual(offset, 4)
    
    def test_large_offset_variable(self):
        """Test assignment to variable at large offset."""
        stmt = {
            "target": "deep_var",
            "value": {"type": "literal", "value": 999}
        }
        func_name = "test"
        label_counter = {}
        var_offsets = {"deep_var": 1024}
        next_offset = 1028
        
        with patch('handle_assign_package.handle_assign_src.evaluate_expression') as mock_eval:
            mock_eval.return_value = ("mov r0, #999\n", 1028)
            
            code, offset = handle_assign(stmt, func_name, label_counter, var_offsets, next_offset)
            
            self.assertIn("str r0, [sp, #1024]", code)
            self.assertEqual(offset, 1028)
    
    def test_label_counter_not_modified(self):
        """Test that label_counter is passed through but not modified by handle_assign."""
        stmt = {
            "target": "x",
            "value": {"type": "literal", "value": 1}
        }
        func_name = "test"
        label_counter = {"while_cond": 5, "while_end": 3}
        var_offsets = {"x": 0}
        next_offset = 4
        
        original_counter = label_counter.copy()
        
        with patch('handle_assign_package.handle_assign_src.evaluate_expression') as mock_eval:
            mock_eval.return_value = ("mov r0, #1\n", 4)
            
            handle_assign(stmt, func_name, label_counter, var_offsets, next_offset)
            
            self.assertEqual(label_counter, original_counter)
    
    def test_empty_label_counter(self):
        """Test assignment with empty label_counter."""
        stmt = {
            "target": "x",
            "value": {"type": "literal", "value": 7}
        }
        func_name = "test"
        label_counter = {}
        var_offsets = {"x": 0}
        next_offset = 4
        
        with patch('handle_assign_package.handle_assign_src.evaluate_expression') as mock_eval:
            mock_eval.return_value = ("mov r0, #7\n", 4)
            
            code, offset = handle_assign(stmt, func_name, label_counter, var_offsets, next_offset)
            
            self.assertIn("str r0, [sp, #0]", code)
            self.assertEqual(offset, 4)
    
    def test_error_message_contains_variable_name(self):
        """Test that ValueError message contains the undefined variable name."""
        stmt = {
            "target": "missing_var",
            "value": {"type": "literal", "value": 1}
        }
        func_name = "test"
        label_counter = {}
        var_offsets = {"other": 0}
        next_offset = 4
        
        with self.assertRaises(ValueError) as context:
            handle_assign(stmt, func_name, label_counter, var_offsets, next_offset)
        
        self.assertEqual(str(context.exception), "Undefined variable: missing_var")


if __name__ == "__main__":
    unittest.main()
