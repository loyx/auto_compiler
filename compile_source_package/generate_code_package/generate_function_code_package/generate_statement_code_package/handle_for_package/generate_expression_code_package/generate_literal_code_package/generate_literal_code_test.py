# === std / third-party imports ===
import unittest

# === relative import for UUT ===
from .generate_literal_code_src import generate_literal_code


class TestGenerateLiteralCode(unittest.TestCase):
    """Test cases for generate_literal_code function."""

    def test_bool_literal_true(self):
        """Test boolean literal with True value."""
        expr = {"type": "LITERAL", "value": True, "literal_type": "bool"}
        next_offset = 0
        code, offset = generate_literal_code(expr, next_offset)
        self.assertEqual(code, "mov x0, #1")
        self.assertEqual(offset, 0)

    def test_bool_literal_false(self):
        """Test boolean literal with False value."""
        expr = {"type": "LITERAL", "value": False, "literal_type": "bool"}
        next_offset = 5
        code, offset = generate_literal_code(expr, next_offset)
        self.assertEqual(code, "mov x0, #0")
        self.assertEqual(offset, 5)

    def test_int_literal_positive(self):
        """Test integer literal with positive value."""
        expr = {"type": "LITERAL", "value": 42, "literal_type": "int"}
        next_offset = 10
        code, offset = generate_literal_code(expr, next_offset)
        self.assertEqual(code, "mov x0, #42")
        self.assertEqual(offset, 10)

    def test_int_literal_negative(self):
        """Test integer literal with negative value."""
        expr = {"type": "LITERAL", "value": -100, "literal_type": "int"}
        next_offset = 3
        code, offset = generate_literal_code(expr, next_offset)
        self.assertEqual(code, "mov x0, #-100")
        self.assertEqual(offset, 3)

    def test_int_literal_zero(self):
        """Test integer literal with zero value."""
        expr = {"type": "LITERAL", "value": 0, "literal_type": "int"}
        next_offset = 0
        code, offset = generate_literal_code(expr, next_offset)
        self.assertEqual(code, "mov x0, #0")
        self.assertEqual(offset, 0)

    def test_next_offset_unchanged(self):
        """Verify next_offset is not modified (no stack usage)."""
        expr = {"type": "LITERAL", "value": 999, "literal_type": "int"}
        for offset in [0, 1, 100, 1000]:
            _, returned_offset = generate_literal_code(expr, offset)
            self.assertEqual(returned_offset, offset)

    def test_unknown_literal_type_raises(self):
        """Test that unknown literal type raises ValueError."""
        expr = {"type": "LITERAL", "value": "test", "literal_type": "string"}
        with self.assertRaises(ValueError) as context:
            generate_literal_code(expr, 0)
        self.assertIn("Unknown literal type: string", str(context.exception))

    def test_large_int_literal(self):
        """Test integer literal with large value."""
        expr = {"type": "LITERAL", "value": 2147483647, "literal_type": "int"}
        next_offset = 50
        code, offset = generate_literal_code(expr, next_offset)
        self.assertEqual(code, "mov x0, #2147483647")
        self.assertEqual(offset, 50)


if __name__ == "__main__":
    unittest.main()
