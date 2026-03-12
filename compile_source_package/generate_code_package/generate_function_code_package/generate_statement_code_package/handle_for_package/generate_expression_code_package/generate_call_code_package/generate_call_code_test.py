import unittest
from unittest.mock import patch

# Relative import from the same package
from .generate_call_code_src import generate_call_code


class TestGenerateCallCode(unittest.TestCase):
    """Test cases for generate_call_code function."""
    
    def test_call_with_no_args(self):
        """Test CALL with zero arguments."""
        expr = {
            "type": "CALL",
            "callee": "no_args_func",
            "args": []
        }
        label_counter = {"for_cond": 0}
        var_offsets = {"x": 0}
        next_offset = 10
        
        code, next_offset = generate_call_code(expr, "test_func", label_counter, var_offsets, next_offset)
        
        expected_code = "bl no_args_func"
        self.assertEqual(code, expected_code)
        self.assertEqual(next_offset, 10)
    
    def test_call_with_one_arg(self):
        """Test CALL with one argument."""
        expr = {
            "type": "CALL",
            "callee": "my_func",
            "args": [{"type": "LITERAL", "value": 42}]
        }
        label_counter = {"for_cond": 0}
        var_offsets = {"x": 0}
        next_offset = 10
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_call_code_package.generate_call_code_src.generate_expression_code') as mock_gen_expr:
            mock_gen_expr.return_value = ("mov x0, #42", 20)
            
            code, next_offset = generate_call_code(expr, "test_func", label_counter, var_offsets, next_offset)
        
        expected_code = "\n".join([
            "mov x0, #42",
            "str x0, [sp, #-16]!",
            "ldr x0, [sp], #16",
            "bl my_func"
        ])
        self.assertEqual(code, expected_code)
        self.assertEqual(next_offset, 20)
        
        # Verify generate_expression_code was called with correct params
        mock_gen_expr.assert_called_once_with(
            {"type": "LITERAL", "value": 42},
            "test_func",
            label_counter,
            var_offsets,
            10
        )
    
    def test_call_with_two_args(self):
        """Test CALL with two arguments."""
        expr = {
            "type": "CALL",
            "callee": "add",
            "args": [
                {"type": "LITERAL", "value": 1},
                {"type": "LITERAL", "value": 2}
            ]
        }
        label_counter = {"for_cond": 0}
        var_offsets = {"x": 0}
        next_offset = 10
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_call_code_package.generate_call_code_src.generate_expression_code') as mock_gen_expr:
            mock_gen_expr.side_effect = [
                ("mov x0, #1", 15),
                ("mov x0, #2", 20)
            ]
            
            code, next_offset = generate_call_code(expr, "test_func", label_counter, var_offsets, next_offset)
        
        expected_code = "\n".join([
            "mov x0, #1",
            "str x0, [sp, #-16]!",
            "mov x0, #2",
            "str x0, [sp, #-16]!",
            "ldr x1, [sp], #16",
            "ldr x0, [sp], #16",
            "bl add"
        ])
        self.assertEqual(code, expected_code)
        self.assertEqual(next_offset, 20)
    
    def test_call_with_three_args(self):
        """Test CALL with three arguments to verify x0-x2 usage."""
        expr = {
            "type": "CALL",
            "callee": "func3",
            "args": [
                {"type": "LITERAL", "value": 1},
                {"type": "LITERAL", "value": 2},
                {"type": "LITERAL", "value": 3}
            ]
        }
        label_counter = {}
        var_offsets = {}
        next_offset = 0
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_call_code_package.generate_call_code_src.generate_expression_code') as mock_gen_expr:
            mock_gen_expr.side_effect = [
                ("mov x0, #1", 10),
                ("mov x0, #2", 20),
                ("mov x0, #3", 30)
            ]
            
            code, next_offset = generate_call_code(expr, "test_func", label_counter, var_offsets, next_offset)
        
        expected_code = "\n".join([
            "mov x0, #1",
            "str x0, [sp, #-16]!",
            "mov x0, #2",
            "str x0, [sp, #-16]!",
            "mov x0, #3",
            "str x0, [sp, #-16]!",
            "ldr x2, [sp], #16",
            "ldr x1, [sp], #16",
            "ldr x0, [sp], #16",
            "bl func3"
        ])
        self.assertEqual(code, expected_code)
        self.assertEqual(next_offset, 30)
    
    def test_call_with_eight_args_max(self):
        """Test CALL with exactly 8 arguments (maximum allowed)."""
        args = [{"type": "LITERAL", "value": i} for i in range(8)]
        expr = {
            "type": "CALL",
            "callee": "func8",
            "args": args
        }
        label_counter = {}
        var_offsets = {}
        next_offset = 0
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_call_code_package.generate_call_code_src.generate_expression_code') as mock_gen_expr:
            mock_gen_expr.side_effect = [
                (f"mov x0, #{i}", (i + 1) * 10) for i in range(8)
            ]
            
            code, next_offset = generate_call_code(expr, "test_func", label_counter, var_offsets, next_offset)
        
        # Verify code contains bl instruction and all 8 load instructions
        self.assertIn("bl func8", code)
        for i in range(8):
            self.assertIn(f"ldr x{i}, [sp], #16", code)
        
        # Count stack operations
        lines = code.split("\n")
        str_count = sum(1 for line in lines if "str x0, [sp, #-16]!" in line)
        ldr_count = sum(1 for line in lines if "ldr x" in line and "[sp], #16" in line)
        self.assertEqual(str_count, 8)
        self.assertEqual(ldr_count, 8)
        
        self.assertEqual(next_offset, 80)
    
    def test_call_with_nine_args_raises_error(self):
        """Test that CALL with 9 arguments raises ValueError."""
        args = [{"type": "LITERAL", "value": i} for i in range(9)]
        expr = {
            "type": "CALL",
            "callee": "func9",
            "args": args
        }
        label_counter = {}
        var_offsets = {}
        next_offset = 0
        
        with self.assertRaises(ValueError) as context:
            generate_call_code(expr, "test_func", label_counter, var_offsets, next_offset)
        
        self.assertIn("maximum 8 arguments", str(context.exception))
        self.assertIn("9", str(context.exception))
    
    def test_label_counter_passed_through(self):
        """Test that label_counter is passed to generate_expression_code."""
        expr = {
            "type": "CALL",
            "callee": "func",
            "args": [{"type": "LITERAL", "value": 1}]
        }
        label_counter = {"for_cond": 5}
        var_offsets = {}
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_call_code_package.generate_call_code_src.generate_expression_code') as mock_gen_expr:
            mock_gen_expr.return_value = ("mov x0, #1", 10)
            
            generate_call_code(expr, "test_func", label_counter, var_offsets, 0)
        
        # Verify label_counter was passed (same object reference)
        call_args = mock_gen_expr.call_args
        self.assertIs(call_args[0][2], label_counter)
    
    def test_var_offsets_passed_through(self):
        """Test that var_offsets is passed to generate_expression_code."""
        expr = {
            "type": "CALL",
            "callee": "func",
            "args": [{"type": "LITERAL", "value": 1}]
        }
        label_counter = {}
        var_offsets = {"x": 0, "y": 8}
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_call_code_package.generate_call_code_src.generate_expression_code') as mock_gen_expr:
            mock_gen_expr.return_value = ("mov x0, #1", 10)
            
            generate_call_code(expr, "test_func", label_counter, var_offsets, 0)
        
        # Verify var_offsets was passed (same object reference)
        call_args = mock_gen_expr.call_args
        self.assertIs(call_args[0][3], var_offsets)
    
    def test_next_offset_updated_correctly(self):
        """Test that next_offset is updated by generate_expression_code calls."""
        expr = {
            "type": "CALL",
            "callee": "func",
            "args": [
                {"type": "LITERAL", "value": 1},
                {"type": "LITERAL", "value": 2},
                {"type": "LITERAL", "value": 3}
            ]
        }
        label_counter = {}
        var_offsets = {}
        initial_offset = 100
        
        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_call_code_package.generate_call_code_src.generate_expression_code') as mock_gen_expr:
            mock_gen_expr.side_effect = [
                ("code1", 110),
                ("code2", 125),
                ("code3", 150)
            ]
            
            code, final_offset = generate_call_code(expr, "test_func", label_counter, var_offsets, initial_offset)
        
        self.assertEqual(final_offset, 150)
    
    def test_callee_name_in_bl_instruction(self):
        """Test that callee name is correctly used in bl instruction."""
        expr = {
            "type": "CALL",
            "callee": "my_custom_function_name",
            "args": []
        }
        label_counter = {}
        var_offsets = {}
        
        code, _ = generate_call_code(expr, "test_func", label_counter, var_offsets, 0)
        
        self.assertEqual(code, "bl my_custom_function_name")
    
    def test_func_name_not_in_output(self):
        """Test that func_name parameter doesn't appear in generated code."""
        expr = {
            "type": "CALL",
            "callee": "callee_func",
            "args": []
        }
        label_counter = {}
        var_offsets = {}
        
        code, _ = generate_call_code(expr, "caller_func", label_counter, var_offsets, 0)
        
        self.assertNotIn("caller_func", code)
        self.assertIn("callee_func", code)


if __name__ == '__main__':
    unittest.main()
