# === std / third-party imports ===
import unittest

# === sub function imports ===
from .generate_identifier_code_src import generate_identifier_code


class TestGenerateIdentifierCode(unittest.TestCase):
    """Test cases for generate_identifier_code function."""

    def test_happy_path_variable_found(self):
        """Test normal case where variable exists in var_offsets."""
        expr = {"type": "IDENTIFIER", "name": "x"}
        var_offsets = {"x": 8, "y": 16}
        next_offset = 24
        
        code, returned_offset = generate_identifier_code(expr, var_offsets, next_offset)
        
        self.assertEqual(code, "ldr x0, [sp, #8]")
        self.assertEqual(returned_offset, 24)

    def test_offset_zero(self):
        """Test with offset of 0."""
        expr = {"type": "IDENTIFIER", "name": "var"}
        var_offsets = {"var": 0}
        next_offset = 16
        
        code, returned_offset = generate_identifier_code(expr, var_offsets, next_offset)
        
        self.assertEqual(code, "ldr x0, [sp, #0]")
        self.assertEqual(returned_offset, 16)

    def test_large_offset(self):
        """Test with large offset value."""
        expr = {"type": "IDENTIFIER", "name": "big_var"}
        var_offsets = {"big_var": 1024}
        next_offset = 2048
        
        code, returned_offset = generate_identifier_code(expr, var_offsets, next_offset)
        
        self.assertEqual(code, "ldr x0, [sp, #1024]")
        self.assertEqual(returned_offset, 2048)

    def test_variable_not_found_raises_keyerror(self):
        """Test that KeyError is raised when variable not in var_offsets."""
        expr = {"type": "IDENTIFIER", "name": "missing_var"}
        var_offsets = {"x": 8, "y": 16}
        next_offset = 24
        
        with self.assertRaises(KeyError) as context:
            generate_identifier_code(expr, var_offsets, next_offset)
        
        self.assertIn("missing_var", str(context.exception))

    def test_next_offset_unchanged(self):
        """Test that next_offset is returned unchanged."""
        expr = {"type": "IDENTIFIER", "name": "a"}
        var_offsets = {"a": 8}
        next_offset = 0
        
        code, returned_offset = generate_identifier_code(expr, var_offsets, next_offset)
        
        self.assertEqual(returned_offset, 0)
        self.assertEqual(code, "ldr x0, [sp, #8]")

    def test_multiple_variables_different_offsets(self):
        """Test with different variables having different offsets."""
        var_offsets = {"first": 8, "second": 16, "third": 24}
        next_offset = 32
        
        for var_name, expected_offset in var_offsets.items():
            expr = {"type": "IDENTIFIER", "name": var_name}
            code, returned_offset = generate_identifier_code(expr, var_offsets, next_offset)
            
            self.assertEqual(code, f"ldr x0, [sp, #{expected_offset}]")
            self.assertEqual(returned_offset, next_offset)

    def test_empty_var_offsets_raises_keyerror(self):
        """Test that KeyError is raised when var_offsets is empty."""
        expr = {"type": "IDENTIFIER", "name": "any_var"}
        var_offsets = {}
        next_offset = 8
        
        with self.assertRaises(KeyError):
            generate_identifier_code(expr, var_offsets, next_offset)

    def test_special_characters_in_variable_name(self):
        """Test variable name with special characters (underscore, numbers)."""
        expr = {"type": "IDENTIFIER", "name": "_var_123"}
        var_offsets = {"_var_123": 40}
        next_offset = 48
        
        code, returned_offset = generate_identifier_code(expr, var_offsets, next_offset)
        
        self.assertEqual(code, "ldr x0, [sp, #40]")
        self.assertEqual(returned_offset, 48)


if __name__ == "__main__":
    unittest.main()
