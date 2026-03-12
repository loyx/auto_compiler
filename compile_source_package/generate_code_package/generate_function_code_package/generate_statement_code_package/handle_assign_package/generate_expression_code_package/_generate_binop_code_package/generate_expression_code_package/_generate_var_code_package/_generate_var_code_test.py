"""Unit tests for _generate_var_code function."""

import unittest
from ._generate_var_code_src import _generate_var_code


class TestGenerateVarCode(unittest.TestCase):
    """Test cases for _generate_var_code function."""

    def test_happy_path_simple_variable(self):
        """Test basic variable reference with positive offset."""
        expr = {"type": "VAR", "name": "x"}
        var_offsets = {"x": 16}
        result = _generate_var_code(expr, "main", var_offsets)
        self.assertEqual(result, "ldr x0, [sp, #16]")

    def test_happy_path_zero_offset(self):
        """Test variable reference with zero offset."""
        expr = {"type": "VAR", "name": "y"}
        var_offsets = {"y": 0}
        result = _generate_var_code(expr, "main", var_offsets)
        self.assertEqual(result, "ldr x0, [sp, #0]")

    def test_happy_path_large_offset(self):
        """Test variable reference with large offset."""
        expr = {"type": "VAR", "name": "z"}
        var_offsets = {"z": 256}
        result = _generate_var_code(expr, "main", var_offsets)
        self.assertEqual(result, "ldr x0, [sp, #256]")

    def test_happy_path_multiple_variables(self):
        """Test different variables from same var_offsets mapping."""
        var_offsets = {"a": 16, "b": 24, "c": 32}
        
        expr_a = {"type": "VAR", "name": "a"}
        result_a = _generate_var_code(expr_a, "func1", var_offsets)
        self.assertEqual(result_a, "ldr x0, [sp, #16]")
        
        expr_b = {"type": "VAR", "name": "b"}
        result_b = _generate_var_code(expr_b, "func1", var_offsets)
        self.assertEqual(result_b, "ldr x0, [sp, #24]")
        
        expr_c = {"type": "VAR", "name": "c"}
        result_c = _generate_var_code(expr_c, "func1", var_offsets)
        self.assertEqual(result_c, "ldr x0, [sp, #32]")

    def test_happy_path_func_name_ignored(self):
        """Test that func_name parameter is not used in output."""
        expr = {"type": "VAR", "name": "var"}
        var_offsets = {"var": 48}
        
        result1 = _generate_var_code(expr, "function1", var_offsets)
        result2 = _generate_var_code(expr, "function2", var_offsets)
        result3 = _generate_var_code(expr, "", var_offsets)
        
        self.assertEqual(result1, result2)
        self.assertEqual(result2, result3)
        self.assertEqual(result1, "ldr x0, [sp, #48]")

    def test_error_missing_name_field(self):
        """Test KeyError when 'name' field is missing from expr."""
        expr = {"type": "VAR"}
        var_offsets = {"x": 16}
        
        with self.assertRaises(KeyError) as context:
            _generate_var_code(expr, "main", var_offsets)
        
        self.assertIn("name", str(context.exception))

    def test_error_empty_expr_dict(self):
        """Test KeyError when expr is empty dict."""
        expr = {}
        var_offsets = {"x": 16}
        
        with self.assertRaises(KeyError) as context:
            _generate_var_code(expr, "main", var_offsets)
        
        self.assertIn("name", str(context.exception))

    def test_error_variable_not_in_var_offsets(self):
        """Test KeyError when variable name not found in var_offsets."""
        expr = {"type": "VAR", "name": "undefined_var"}
        var_offsets = {"x": 16, "y": 24}
        
        with self.assertRaises(KeyError) as context:
            _generate_var_code(expr, "main", var_offsets)
        
        self.assertIn("undefined_var", str(context.exception))

    def test_error_variable_not_in_empty_var_offsets(self):
        """Test KeyError when var_offsets is empty."""
        expr = {"type": "VAR", "name": "any_var"}
        var_offsets = {}
        
        with self.assertRaises(KeyError) as context:
            _generate_var_code(expr, "main", var_offsets)
        
        self.assertIn("any_var", str(context.exception))

    def test_error_name_field_is_none(self):
        """Test KeyError when 'name' field exists but is None."""
        expr = {"type": "VAR", "name": None}
        var_offsets = {None: 16}
        
        # None as a key should work if present in var_offsets
        result = _generate_var_code(expr, "main", var_offsets)
        self.assertEqual(result, "ldr x0, [sp, #16]")

    def test_error_name_field_is_empty_string(self):
        """Test with empty string as variable name."""
        expr = {"type": "VAR", "name": ""}
        var_offsets = {"": 16}
        
        result = _generate_var_code(expr, "main", var_offsets)
        self.assertEqual(result, "ldr x0, [sp, #16]")

    def test_var_offsets_with_negative_offset(self):
        """Test variable reference with negative offset (if supported)."""
        expr = {"type": "VAR", "name": "neg_var"}
        var_offsets = {"neg_var": -8}
        result = _generate_var_code(expr, "main", var_offsets)
        self.assertEqual(result, "ldr x0, [sp, #-8]")


if __name__ == "__main__":
    unittest.main()
