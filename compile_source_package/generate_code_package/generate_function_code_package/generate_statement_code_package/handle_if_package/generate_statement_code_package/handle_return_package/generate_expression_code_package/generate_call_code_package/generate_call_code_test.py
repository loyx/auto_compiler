# === imports ===
import unittest
from unittest.mock import patch

# === relative import for UUT ===
from .generate_call_code_src import generate_call_code


class TestGenerateCallCode(unittest.TestCase):
    """Test cases for generate_call_code function."""

    def test_call_with_no_args(self):
        """Test CALL expression with no arguments."""
        expr = {
            "type": "CALL",
            "func_name": "my_function"
        }
        var_offsets = {}
        next_offset = 0
        
        code, offset, result_reg = generate_call_code(expr, var_offsets, next_offset)
        
        self.assertEqual(code, "    bl my_function\n")
        self.assertEqual(offset, 0)
        self.assertEqual(result_reg, "x0")

    def test_call_with_empty_args_list(self):
        """Test CALL expression with explicit empty args list."""
        expr = {
            "type": "CALL",
            "func_name": "my_function",
            "args": []
        }
        var_offsets = {}
        next_offset = 5
        
        code, offset, result_reg = generate_call_code(expr, var_offsets, next_offset)
        
        self.assertEqual(code, "    bl my_function\n")
        self.assertEqual(offset, 5)
        self.assertEqual(result_reg, "x0")

    def test_call_with_single_arg_no_move_needed(self):
        """Test CALL with one argument where result register is already x0."""
        expr = {
            "type": "CALL",
            "func_name": "my_function",
            "args": [{"type": "NUM", "value": 42}]
        }
        var_offsets = {}
        next_offset = 0
        
        with patch("generate_call_code_package.generate_call_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    mov x0, #42\n", 0, "x0")
            
            code, offset, result_reg = generate_call_code(expr, var_offsets, next_offset)
            
            mock_gen_expr.assert_called_once_with(
                {"type": "NUM", "value": 42}, {}, 0
            )
            self.assertEqual(code, "    mov x0, #42\n    bl my_function\n")
            self.assertEqual(offset, 0)
            self.assertEqual(result_reg, "x0")

    def test_call_with_single_arg_move_needed(self):
        """Test CALL with one argument where result register needs to be moved to x0."""
        expr = {
            "type": "CALL",
            "func_name": "my_function",
            "args": [{"type": "NUM", "value": 42}]
        }
        var_offsets = {}
        next_offset = 0
        
        with patch("generate_call_code_package.generate_call_code_src.generate_expression_code") as mock_gen_expr:
            # Simulate arg evaluation returns result in x1 instead of x0
            mock_gen_expr.return_value = ("    mov x1, #42\n", 0, "x1")
            
            code, offset, result_reg = generate_call_code(expr, var_offsets, next_offset)
            
            mock_gen_expr.assert_called_once_with(
                {"type": "NUM", "value": 42}, {}, 0
            )
            self.assertEqual(code, "    mov x1, #42\n    mov x0, x1\n    bl my_function\n")
            self.assertEqual(offset, 0)
            self.assertEqual(result_reg, "x0")

    def test_call_with_multiple_args(self):
        """Test CALL with multiple arguments."""
        expr = {
            "type": "CALL",
            "func_name": "add_func",
            "args": [
                {"type": "NUM", "value": 1},
                {"type": "NUM", "value": 2},
                {"type": "NUM", "value": 3}
            ]
        }
        var_offsets = {}
        next_offset = 0
        
        with patch("generate_call_code_package.generate_call_code_src.generate_expression_code") as mock_gen_expr:
            # Each arg returns result in x0, needs move to x0, x1, x2
            mock_gen_expr.side_effect = [
                ("    mov x0, #1\n", 0, "x0"),  # arg 0 -> x0 (no move)
                ("    mov x0, #2\n", 0, "x0"),  # arg 1 -> x1 (move needed)
                ("    mov x0, #3\n", 0, "x0"),  # arg 2 -> x2 (move needed)
            ]
            
            code, offset, result_reg = generate_call_code(expr, var_offsets, next_offset)
            
            self.assertEqual(mock_gen_expr.call_count, 3)
            expected_code = (
                "    mov x0, #1\n"
                "    mov x0, #2\n"
                "    mov x1, x0\n"
                "    mov x0, #3\n"
                "    mov x2, x0\n"
                "    bl add_func\n"
            )
            self.assertEqual(code, expected_code)
            self.assertEqual(offset, 0)
            self.assertEqual(result_reg, "x0")

    def test_call_with_eight_args_max_limit(self):
        """Test CALL with exactly 8 arguments (maximum allowed)."""
        expr = {
            "type": "CALL",
            "func_name": "eight_arg_func",
            "args": [{"type": "NUM", "value": i} for i in range(8)]
        }
        var_offsets = {}
        next_offset = 0
        
        with patch("generate_call_code_package.generate_call_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    mov x0, #0\n", 0, "x0")
            
            code, offset, result_reg = generate_call_code(expr, var_offsets, next_offset)
            
            self.assertEqual(mock_gen_expr.call_count, 8)
            self.assertIn("    bl eight_arg_func\n", code)
            self.assertEqual(offset, 0)
            self.assertEqual(result_reg, "x0")

    def test_call_with_nine_args_exceeds_limit(self):
        """Test CALL with 9 arguments should raise ValueError."""
        expr = {
            "type": "CALL",
            "func_name": "too_many_args_func",
            "args": [{"type": "NUM", "value": i} for i in range(9)]
        }
        var_offsets = {}
        next_offset = 0
        
        with self.assertRaises(ValueError) as context:
            generate_call_code(expr, var_offsets, next_offset)
        
        self.assertEqual(str(context.exception), "Too many arguments (max 8)")

    def test_call_missing_func_name(self):
        """Test CALL expression without func_name field raises ValueError."""
        expr = {
            "type": "CALL",
            "args": []
        }
        var_offsets = {}
        next_offset = 0
        
        with self.assertRaises(ValueError) as context:
            generate_call_code(expr, var_offsets, next_offset)
        
        self.assertEqual(str(context.exception), "CALL expression missing func_name field")

    def test_call_with_none_func_name(self):
        """Test CALL expression with explicit None func_name raises ValueError."""
        expr = {
            "type": "CALL",
            "func_name": None,
            "args": []
        }
        var_offsets = {}
        next_offset = 0
        
        with self.assertRaises(ValueError) as context:
            generate_call_code(expr, var_offsets, next_offset)
        
        self.assertEqual(str(context.exception), "CALL expression missing func_name field")

    def test_call_args_offset_propagation(self):
        """Test that next_offset is properly propagated through recursive calls."""
        expr = {
            "type": "CALL",
            "func_name": "func",
            "args": [
                {"type": "NUM", "value": 1},
                {"type": "NUM", "value": 2}
            ]
        }
        var_offsets = {}
        next_offset = 10
        
        with patch("generate_call_code_package.generate_call_code_src.generate_expression_code") as mock_gen_expr:
            # Each call increments offset
            mock_gen_expr.side_effect = [
                ("    mov x0, #1\n", 11, "x0"),  # offset 10 -> 11
                ("    mov x0, #2\n", 12, "x0"),  # offset 11 -> 12
            ]
            
            code, offset, result_reg = generate_call_code(expr, var_offsets, next_offset)
            
            calls = mock_gen_expr.call_args_list
            self.assertEqual(len(calls), 2)
            # First call should start at offset 10
            self.assertEqual(calls[0][0][2], 10)
            # Second call should start at offset 11
            self.assertEqual(calls[1][0][2], 11)
            # Final offset should be 12
            self.assertEqual(offset, 12)

    def test_call_var_offsets_passed_to_args(self):
        """Test that var_offsets is passed to recursive generate_expression_code calls."""
        expr = {
            "type": "CALL",
            "func_name": "func",
            "args": [{"type": "VAR", "name": "x"}]
        }
        var_offsets = {"x": 0, "y": 8}
        next_offset = 0
        
        with patch("generate_call_code_package.generate_call_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    ldr x0, [sp, #0]\n", 0, "x0")
            
            code, offset, result_reg = generate_call_code(expr, var_offsets, next_offset)
            
            mock_gen_expr.assert_called_once()
            # Verify var_offsets was passed through
            call_args = mock_gen_expr.call_args
            self.assertEqual(call_args[0][1], var_offsets)

    def test_call_complex_nested_args(self):
        """Test CALL with nested CALL expressions as arguments."""
        expr = {
            "type": "CALL",
            "func_name": "outer",
            "args": [
                {
                    "type": "CALL",
                    "func_name": "inner",
                    "args": []
                }
            ]
        }
        var_offsets = {}
        next_offset = 0
        
        with patch("generate_call_code_package.generate_call_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    bl inner\n", 0, "x0")
            
            code, offset, result_reg = generate_call_code(expr, var_offsets, next_offset)
            
            mock_gen_expr.assert_called_once_with(
                {"type": "CALL", "func_name": "inner", "args": []},
                {},
                0
            )
            self.assertEqual(code, "    bl inner\n    bl outer\n")
            self.assertEqual(result_reg, "x0")


if __name__ == "__main__":
    unittest.main()
