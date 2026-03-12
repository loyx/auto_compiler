# === std / third-party imports ===
import unittest
from typing import Dict

# === relative import for UUT ===
from ._generate_var_code_src import _generate_var_code


class TestGenerateVarCode(unittest.TestCase):
    """Test cases for _generate_var_code function."""

    def test_happy_path_single_variable(self):
        """Test generating code for a single valid variable."""
        var_offsets = {"x": 8}
        result = _generate_var_code("x", var_offsets)
        self.assertEqual(result, "ldr x0, [sp, #8]")

    def test_happy_path_zero_offset(self):
        """Test generating code with zero offset."""
        var_offsets = {"y": 0}
        result = _generate_var_code("y", var_offsets)
        self.assertEqual(result, "ldr x0, [sp, #0]")

    def test_happy_path_large_offset(self):
        """Test generating code with large offset value."""
        var_offsets = {"z": 256}
        result = _generate_var_code("z", var_offsets)
        self.assertEqual(result, "ldr x0, [sp, #256]")

    def test_happy_path_multiple_variables_dict(self):
        """Test selecting correct variable from dict with multiple entries."""
        var_offsets = {"a": 8, "b": 16, "c": 24}
        result = _generate_var_code("b", var_offsets)
        self.assertEqual(result, "ldr x0, [sp, #16]")

    def test_key_error_undefined_variable(self):
        """Test KeyError is raised when variable is not in var_offsets."""
        var_offsets = {"x": 8}
        with self.assertRaises(KeyError) as context:
            _generate_var_code("undefined_var", var_offsets)
        self.assertEqual(str(context.exception), "'Undefined variable: undefined_var'")

    def test_key_error_empty_dict(self):
        """Test KeyError is raised when var_offsets is empty."""
        var_offsets: Dict[str, int] = {}
        with self.assertRaises(KeyError) as context:
            _generate_var_code("any_var", var_offsets)
        self.assertEqual(str(context.exception), "'Undefined variable: any_var'")

    def test_key_error_message_format(self):
        """Test KeyError message contains the correct variable name."""
        var_offsets = {"existing": 8}
        try:
            _generate_var_code("missing", var_offsets)
            self.fail("Expected KeyError was not raised")
        except KeyError as e:
            self.assertIn("missing", str(e))

    def test_variable_name_with_special_chars(self):
        """Test variable name with underscores and numbers."""
        var_offsets = {"var_1": 32, "_temp": 40}
        result = _generate_var_code("var_1", var_offsets)
        self.assertEqual(result, "ldr x0, [sp, #32]")
        
        result = _generate_var_code("_temp", var_offsets)
        self.assertEqual(result, "ldr x0, [sp, #40]")

    def test_negative_offset(self):
        """Test generating code with negative offset (if applicable)."""
        var_offsets = {"neg_var": -8}
        result = _generate_var_code("neg_var", var_offsets)
        self.assertEqual(result, "ldr x0, [sp, #-8]")

    def test_dict_not_modified(self):
        """Test that var_offsets dict is not modified by the function."""
        var_offsets = {"x": 8}
        original_copy = var_offsets.copy()
        _generate_var_code("x", var_offsets)
        self.assertEqual(var_offsets, original_copy)


if __name__ == "__main__":
    unittest.main()
