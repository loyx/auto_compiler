# === test imports ===
import unittest

# === relative import of UUT ===
from .generate_identifier_code_src import generate_identifier_code, VarOffsets, Expression


class TestGenerateIdentifierCode(unittest.TestCase):
    """Test cases for generate_identifier_code function."""

    def test_happy_path_simple_identifier(self):
        """Test loading a simple identifier from stack."""
        expr: Expression = {"type": "IDENTIFIER", "name": "x"}
        var_offsets: VarOffsets = {"x": 8}
        next_offset = 16

        code, returned_offset = generate_identifier_code(expr, var_offsets, next_offset)

        self.assertEqual(code, "ldr x0, [sp, #8]")
        self.assertEqual(returned_offset, next_offset)

    def test_happy_path_different_offset(self):
        """Test with different stack offset values."""
        expr: Expression = {"type": "IDENTIFIER", "name": "y"}
        var_offsets: VarOffsets = {"y": 24}
        next_offset = 32

        code, returned_offset = generate_identifier_code(expr, var_offsets, next_offset)

        self.assertEqual(code, "ldr x0, [sp, #24]")
        self.assertEqual(returned_offset, 32)

    def test_happy_path_zero_offset(self):
        """Test with zero offset (edge case)."""
        expr: Expression = {"type": "IDENTIFIER", "name": "z"}
        var_offsets: VarOffsets = {"z": 0}
        next_offset = 8

        code, returned_offset = generate_identifier_code(expr, var_offsets, next_offset)

        self.assertEqual(code, "ldr x0, [sp, #0]")
        self.assertEqual(returned_offset, 8)

    def test_happy_path_multiple_variables(self):
        """Test selecting correct variable from multiple in var_offsets."""
        expr: Expression = {"type": "IDENTIFIER", "name": "b"}
        var_offsets: VarOffsets = {"a": 8, "b": 16, "c": 24}
        next_offset = 32

        code, returned_offset = generate_identifier_code(expr, var_offsets, next_offset)

        self.assertEqual(code, "ldr x0, [sp, #16]")
        self.assertEqual(returned_offset, 32)

    def test_keyerror_variable_not_in_var_offsets(self):
        """Test KeyError when variable name is not in var_offsets."""
        expr: Expression = {"type": "IDENTIFIER", "name": "missing_var"}
        var_offsets: VarOffsets = {"x": 8, "y": 16}
        next_offset = 24

        with self.assertRaises(KeyError):
            generate_identifier_code(expr, var_offsets, next_offset)

    def test_keyerror_empty_var_offsets(self):
        """Test KeyError when var_offsets is empty."""
        expr: Expression = {"type": "IDENTIFIER", "name": "any_var"}
        var_offsets: VarOffsets = {}
        next_offset = 8

        with self.assertRaises(KeyError):
            generate_identifier_code(expr, var_offsets, next_offset)

    def test_next_offset_unchanged(self):
        """Verify next_offset is returned unchanged regardless of offset value."""
        expr: Expression = {"type": "IDENTIFIER", "name": "var"}
        var_offsets: VarOffsets = {"var": 100}
        next_offset = 200

        code, returned_offset = generate_identifier_code(expr, var_offsets, next_offset)

        self.assertEqual(returned_offset, next_offset)
        self.assertEqual(returned_offset, 200)

    def test_large_offset_value(self):
        """Test with large offset value."""
        expr: Expression = {"type": "IDENTIFIER", "name": "large_offset_var"}
        var_offsets: VarOffsets = {"large_offset_var": 999999}
        next_offset = 1000000

        code, returned_offset = generate_identifier_code(expr, var_offsets, next_offset)

        self.assertEqual(code, "ldr x0, [sp, #999999]")
        self.assertEqual(returned_offset, 1000000)


if __name__ == "__main__":
    unittest.main()
