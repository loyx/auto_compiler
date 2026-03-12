# -*- coding: utf-8 -*-
"""Unit tests for generate_variable_code function."""

import unittest

from .generate_variable_code_src import generate_variable_code, VarOffsets


class TestGenerateVariableCode(unittest.TestCase):
    """Test cases for generate_variable_code function."""

    def test_happy_path_single_variable(self):
        """Test loading a single variable with positive offset."""
        var_name = "x"
        var_offsets: VarOffsets = {"x": 8}
        next_offset = 16
        
        code, returned_offset = generate_variable_code(var_name, var_offsets, next_offset)
        
        self.assertEqual(code, "ldr x0, [sp, #8]")
        self.assertEqual(returned_offset, 16)
    
    def test_happy_path_zero_offset(self):
        """Test loading a variable with zero offset."""
        var_name = "y"
        var_offsets: VarOffsets = {"y": 0}
        next_offset = 8
        
        code, returned_offset = generate_variable_code(var_name, var_offsets, next_offset)
        
        self.assertEqual(code, "ldr x0, [sp, #0]")
        self.assertEqual(returned_offset, 8)
    
    def test_happy_path_large_offset(self):
        """Test loading a variable with large offset."""
        var_name = "z"
        var_offsets: VarOffsets = {"z": 256}
        next_offset = 512
        
        code, returned_offset = generate_variable_code(var_name, var_offsets, next_offset)
        
        self.assertEqual(code, "ldr x0, [sp, #256]")
        self.assertEqual(returned_offset, 512)
    
    def test_happy_path_multiple_variables_in_dict(self):
        """Test loading one variable when multiple exist in var_offsets."""
        var_name = "b"
        var_offsets: VarOffsets = {"a": 8, "b": 16, "c": 24}
        next_offset = 32
        
        code, returned_offset = generate_variable_code(var_name, var_offsets, next_offset)
        
        self.assertEqual(code, "ldr x0, [sp, #16]")
        self.assertEqual(returned_offset, 32)
    
    def test_key_error_variable_not_found(self):
        """Test KeyError is raised when variable is not in var_offsets."""
        var_name = "missing_var"
        var_offsets: VarOffsets = {"x": 8, "y": 16}
        next_offset = 24
        
        with self.assertRaises(KeyError) as context:
            generate_variable_code(var_name, var_offsets, next_offset)
        
        self.assertIn("missing_var", str(context.exception))
    
    def test_key_error_empty_var_offsets(self):
        """Test KeyError is raised when var_offsets is empty."""
        var_name = "any_var"
        var_offsets: VarOffsets = {}
        next_offset = 0
        
        with self.assertRaises(KeyError):
            generate_variable_code(var_name, var_offsets, next_offset)
    
    def test_next_offset_unchanged(self):
        """Test that next_offset is returned unchanged."""
        var_name = "var"
        var_offsets: VarOffsets = {"var": 100}
        next_offset = 999
        
        code, returned_offset = generate_variable_code(var_name, var_offsets, next_offset)
        
        self.assertEqual(returned_offset, next_offset)
        self.assertIsNotNone(code)
    
    def test_variable_with_underscore_in_name(self):
        """Test variable name with underscores."""
        var_name = "my_variable"
        var_offsets: VarOffsets = {"my_variable": 40}
        next_offset = 48
        
        code, returned_offset = generate_variable_code(var_name, var_offsets, next_offset)
        
        self.assertEqual(code, "ldr x0, [sp, #40]")
        self.assertEqual(returned_offset, 48)
    
    def test_code_format_correct(self):
        """Test that generated code follows correct ARM64 format."""
        var_name = "test"
        var_offsets: VarOffsets = {"test": 64}
        next_offset = 72
        
        code, returned_offset = generate_variable_code(var_name, var_offsets, next_offset)
        
        # Verify code format: ldr x0, [sp, #offset]
        self.assertTrue(code.startswith("ldr x0, [sp, #"))
        self.assertTrue(code.endswith("]"))
        self.assertIn("64", code)


if __name__ == "__main__":
    unittest.main()
