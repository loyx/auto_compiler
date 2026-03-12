# -*- coding: utf-8 -*-
"""Unit tests for _generate_call_code function."""

import unittest
from unittest.mock import patch

from ._generate_call_code_src import _generate_call_code


class TestGenerateCallCode(unittest.TestCase):
    """Test cases for _generate_call_code function."""

    def setUp(self):
        """Set up test fixtures."""
        self.func_name = "test_func"
        self.var_offsets = {"x": 0, "y": 8}

    def test_call_with_no_arguments(self):
        """Test CALL expression with no arguments."""
        expr = {
            "function": "printf",
            "arguments": []
        }
        
        result = _generate_call_code(expr, self.func_name, self.var_offsets)
        
        self.assertEqual(result, "    bl printf")

    def test_call_with_one_argument(self):
        """Test CALL expression with one argument."""
        expr = {
            "function": "abs",
            "arguments": [{"type": "CONST", "value": 5}]
        }
        
        with patch("._generate_call_code_src.generate_expression_code") as mock_gen:
            mock_gen.return_value = "    mov x0, #5"
            
            result = _generate_call_code(expr, self.func_name, self.var_offsets)
            
            mock_gen.assert_called_once_with({"type": "CONST", "value": 5}, self.func_name, self.var_offsets)
            self.assertEqual(result, "    mov x0, #5\n    bl abs")

    def test_call_with_two_arguments(self):
        """Test CALL expression with two arguments."""
        expr = {
            "function": "add",
            "arguments": [
                {"type": "CONST", "value": 1},
                {"type": "CONST", "value": 2}
            ]
        }
        
        with patch("._generate_call_code_src.generate_expression_code") as mock_gen:
            mock_gen.side_effect = [
                "    mov x0, #1",
                "    mov x0, #2"
            ]
            
            result = _generate_call_code(expr, self.func_name, self.var_offsets)
            
            self.assertEqual(mock_gen.call_count, 2)
            expected = "    mov x0, #1\n    mov x1, x0\n    mov x0, #2\n    bl add"
            self.assertEqual(result, expected)

    def test_call_with_three_arguments(self):
        """Test CALL expression with three arguments."""
        expr = {
            "function": "max3",
            "arguments": [
                {"type": "CONST", "value": 1},
                {"type": "CONST", "value": 2},
                {"type": "CONST", "value": 3}
            ]
        }
        
        with patch("._generate_call_code_src.generate_expression_code") as mock_gen:
            mock_gen.side_effect = [
                "    mov x0, #1",
                "    mov x0, #2",
                "    mov x0, #3"
            ]
            
            result = _generate_call_code(expr, self.func_name, self.var_offsets)
            
            self.assertEqual(mock_gen.call_count, 3)
            expected = "    mov x0, #1\n    mov x1, x0\n    mov x0, #2\n    mov x2, x0\n    mov x0, #3\n    bl max3"
            self.assertEqual(result, expected)

    def test_call_with_eight_arguments(self):
        """Test CALL expression with maximum 8 arguments."""
        expr = {
            "function": "func8",
            "arguments": [{"type": "CONST", "value": i} for i in range(8)]
        }
        
        with patch("._generate_call_code_src.generate_expression_code") as mock_gen:
            mock_gen.side_effect = [f"    mov x0, #{i}" for i in range(8)]
            
            result = _generate_call_code(expr, self.func_name, self.var_offsets)
            
            self.assertEqual(mock_gen.call_count, 8)
            # First arg stays in x0, args 1-7 get moved to x1-x7
            lines = result.split("\n")
            self.assertEqual(len(lines), 15)  # 8 arg codes + 7 movs + 1 bl
            self.assertIn("    bl func8", lines)

    def test_call_with_nine_arguments_raises_value_error(self):
        """Test CALL expression with more than 8 arguments raises ValueError."""
        expr = {
            "function": "func9",
            "arguments": [{"type": "CONST", "value": i} for i in range(9)]
        }
        
        with self.assertRaises(ValueError) as context:
            _generate_call_code(expr, self.func_name, self.var_offsets)
        
        self.assertIn("9 arguments", str(context.exception))
        self.assertIn("maximum is 8", str(context.exception))

    def test_call_missing_function_field_raises_key_error(self):
        """Test CALL expression missing 'function' field raises KeyError."""
        expr = {
            "arguments": []
        }
        
        with self.assertRaises(KeyError) as context:
            _generate_call_code(expr, self.func_name, self.var_offsets)
        
        self.assertIn("'function' field", str(context.exception))

    def test_call_missing_arguments_field_raises_key_error(self):
        """Test CALL expression missing 'arguments' field raises KeyError."""
        expr = {
            "function": "printf"
        }
        
        with self.assertRaises(KeyError) as context:
            _generate_call_code(expr, self.func_name, self.var_offsets)
        
        self.assertIn("'arguments' field", str(context.exception))

    def test_call_with_complex_argument_expressions(self):
        """Test CALL expression with complex nested argument expressions."""
        expr = {
            "function": "compute",
            "arguments": [
                {"type": "BINOP", "op": "+", "left": {"type": "VAR", "name": "x"}, "right": {"type": "CONST", "value": 1}},
                {"type": "CALL", "function": "abs", "arguments": [{"type": "VAR", "name": "y"}]}
            ]
        }
        
        with patch("._generate_call_code_src.generate_expression_code") as mock_gen:
            mock_gen.side_effect = [
                "    ldr x0, [sp, #0]\n    add x0, x0, #1",
                "    ldr x0, [sp, #8]\n    bl abs"
            ]
            
            result = _generate_call_code(expr, self.func_name, self.var_offsets)
            
            self.assertEqual(mock_gen.call_count, 2)
            self.assertIn("    mov x1, x0", result)
            self.assertIn("    bl compute", result)

    def test_call_preserves_argument_evaluation_order(self):
        """Test that arguments are evaluated left-to-right."""
        expr = {
            "function": "func",
            "arguments": [
                {"type": "CONST", "value": 1},
                {"type": "CONST", "value": 2},
                {"type": "CONST", "value": 3}
            ]
        }
        
        with patch("._generate_call_code_src.generate_expression_code") as mock_gen:
            mock_gen.return_value = "    nop"
            
            _generate_call_code(expr, self.func_name, self.var_offsets)
            
            # Verify calls were made in order
            calls = mock_gen.call_args_list
            self.assertEqual(len(calls), 3)
            self.assertEqual(calls[0][0][0], {"type": "CONST", "value": 1})
            self.assertEqual(calls[1][0][0], {"type": "CONST", "value": 2})
            self.assertEqual(calls[2][0][0], {"type": "CONST", "value": 3})

    def test_call_with_empty_function_name(self):
        """Test CALL expression with empty function name."""
        expr = {
            "function": "",
            "arguments": []
        }
        
        result = _generate_call_code(expr, self.func_name, self.var_offsets)
        
        self.assertEqual(result, "    bl ")

    def test_call_with_special_characters_in_function_name(self):
        """Test CALL expression with special characters in function name."""
        expr = {
            "function": "__attribute__((noreturn))",
            "arguments": []
        }
        
        result = _generate_call_code(expr, self.func_name, self.var_offsets)
        
        self.assertEqual(result, "    bl __attribute__((noreturn))")


if __name__ == "__main__":
    unittest.main()
