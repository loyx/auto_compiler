# === std / third-party imports ===
import unittest

# === sub module imports ===
from .generate_num_code_src import generate_num_code


class TestGenerateNumCode(unittest.TestCase):
    """Test cases for generate_num_code function."""

    def test_generate_num_code_positive_value(self):
        """Test with positive numeric value."""
        expr = {"type": "NUM", "value": 42}
        next_offset = 0
        
        code, offset, register = generate_num_code(expr, next_offset)
        
        self.assertEqual(code, "    mov x0, 42\n")
        self.assertEqual(offset, 0)
        self.assertEqual(register, "x0")

    def test_generate_num_code_zero(self):
        """Test with zero value (boundary case)."""
        expr = {"type": "NUM", "value": 0}
        next_offset = 16
        
        code, offset, register = generate_num_code(expr, next_offset)
        
        self.assertEqual(code, "    mov x0, 0\n")
        self.assertEqual(offset, 16)
        self.assertEqual(register, "x0")

    def test_generate_num_code_negative_value(self):
        """Test with negative numeric value."""
        expr = {"type": "NUM", "value": -100}
        next_offset = 32
        
        code, offset, register = generate_num_code(expr, next_offset)
        
        self.assertEqual(code, "    mov x0, -100\n")
        self.assertEqual(offset, 32)
        self.assertEqual(register, "x0")

    def test_generate_num_code_large_value(self):
        """Test with large numeric value."""
        expr = {"type": "NUM", "value": 999999}
        next_offset = 0
        
        code, offset, register = generate_num_code(expr, next_offset)
        
        self.assertEqual(code, "    mov x0, 999999\n")
        self.assertEqual(offset, 0)
        self.assertEqual(register, "x0")

    def test_generate_num_code_offset_unchanged(self):
        """Test that next_offset remains unchanged regardless of input."""
        expr = {"type": "NUM", "value": 5}
        next_offset = 128
        
        code, offset, register = generate_num_code(expr, next_offset)
        
        # NUM expressions don't use stack space, offset should be unchanged
        self.assertEqual(offset, next_offset)

    def test_generate_num_code_result_register(self):
        """Test that result register is always x0."""
        expr = {"type": "NUM", "value": 1}
        next_offset = 0
        
        code, offset, register = generate_num_code(expr, next_offset)
        
        self.assertEqual(register, "x0")

    def test_generate_num_code_without_type_field(self):
        """Test that function works even without 'type' field in expr."""
        expr = {"value": 7}
        next_offset = 0
        
        code, offset, register = generate_num_code(expr, next_offset)
        
        self.assertEqual(code, "    mov x0, 7\n")
        self.assertEqual(offset, 0)
        self.assertEqual(register, "x0")

    def test_generate_num_code_missing_value_key(self):
        """Test that KeyError is raised when 'value' key is missing."""
        expr = {"type": "NUM"}
        next_offset = 0
        
        with self.assertRaises(KeyError):
            generate_num_code(expr, next_offset)


if __name__ == "__main__":
    unittest.main()
