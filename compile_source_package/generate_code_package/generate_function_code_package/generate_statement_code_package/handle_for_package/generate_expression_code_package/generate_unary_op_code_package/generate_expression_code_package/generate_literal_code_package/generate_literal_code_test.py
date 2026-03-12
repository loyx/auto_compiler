# === std / third-party imports ===
import unittest

# === relative import of UUT ===
from .generate_literal_code_src import generate_literal_code


class TestGenerateLiteralCode(unittest.TestCase):
    """Test cases for generate_literal_code function."""

    def test_small_positive_int(self):
        """Test small positive integer literal."""
        expr = {"type": "LITERAL", "value": 42, "literal_type": "int"}
        code, next_offset = generate_literal_code(expr, 0)
        self.assertEqual(code, "mov x0, #42")
        self.assertEqual(next_offset, 0)

    def test_small_negative_int(self):
        """Test small negative integer literal."""
        expr = {"type": "LITERAL", "value": -100, "literal_type": "int"}
        code, next_offset = generate_literal_code(expr, 5)
        self.assertEqual(code, "mov x0, #-100")
        self.assertEqual(next_offset, 5)

    def test_zero_int(self):
        """Test zero integer literal."""
        expr = {"type": "LITERAL", "value": 0, "literal_type": "int"}
        code, next_offset = generate_literal_code(expr, 10)
        self.assertEqual(code, "mov x0, #0")
        self.assertEqual(next_offset, 10)

    def test_boundary_small_int_max(self):
        """Test boundary value for small int (65535)."""
        expr = {"type": "LITERAL", "value": 65535, "literal_type": "int"}
        code, next_offset = generate_literal_code(expr, 0)
        self.assertEqual(code, "mov x0, #65535")
        self.assertEqual(next_offset, 0)

    def test_boundary_small_int_min(self):
        """Test boundary value for small int (-65536)."""
        expr = {"type": "LITERAL", "value": -65536, "literal_type": "int"}
        code, next_offset = generate_literal_code(expr, 0)
        self.assertEqual(code, "mov x0, #-65536")
        self.assertEqual(next_offset, 0)

    def test_large_positive_int(self):
        """Test large positive integer requiring movz/movk."""
        expr = {"type": "LITERAL", "value": 100000, "literal_type": "int"}
        code, next_offset = generate_literal_code(expr, 0)
        # Should use movz/movk pattern
        self.assertIn("movz", code)
        self.assertEqual(next_offset, 0)

    def test_large_negative_int(self):
        """Test large negative integer requiring movz/movk and mvn."""
        expr = {"type": "LITERAL", "value": -100000, "literal_type": "int"}
        code, next_offset = generate_literal_code(expr, 0)
        # Should use movz/movk pattern and mvn for negative
        self.assertIn("mvn", code)
        self.assertEqual(next_offset, 0)

    def test_very_large_int(self):
        """Test very large integer requiring multiple chunks."""
        expr = {"type": "LITERAL", "value": 0x123456789ABCDEF, "literal_type": "int"}
        code, next_offset = generate_literal_code(expr, 0)
        # Should use multiple movz/movk instructions
        self.assertTrue("movz" in code or "movk" in code)
        self.assertEqual(next_offset, 0)

    def test_bool_true(self):
        """Test boolean true literal."""
        expr = {"type": "LITERAL", "value": True, "literal_type": "bool"}
        code, next_offset = generate_literal_code(expr, 0)
        self.assertEqual(code, "mov x0, #1")
        self.assertEqual(next_offset, 0)

    def test_bool_false(self):
        """Test boolean false literal."""
        expr = {"type": "LITERAL", "value": False, "literal_type": "bool"}
        code, next_offset = generate_literal_code(expr, 7)
        self.assertEqual(code, "mov x0, #0")
        self.assertEqual(next_offset, 7)

    def test_null_literal(self):
        """Test null literal."""
        expr = {"type": "LITERAL", "value": None, "literal_type": "null"}
        code, next_offset = generate_literal_code(expr, 0)
        self.assertEqual(code, "mov x0, #0")
        self.assertEqual(next_offset, 0)

    def test_string_literal(self):
        """Test string literal."""
        expr = {"type": "LITERAL", "value": "hello", "literal_type": "string"}
        code, next_offset = generate_literal_code(expr, 0)
        self.assertEqual(code, "ldr x0, =str_literal")
        self.assertEqual(next_offset, 0)

    def test_unknown_literal_type(self):
        """Test unknown literal type raises ValueError."""
        expr = {"type": "LITERAL", "value": 42, "literal_type": "unknown"}
        with self.assertRaises(ValueError) as context:
            generate_literal_code(expr, 0)
        self.assertIn("Unknown literal type", str(context.exception))

    def test_next_offset_unchanged(self):
        """Test that next_offset is always unchanged."""
        test_cases = [
            ({"type": "LITERAL", "value": 42, "literal_type": "int"}, 100),
            ({"type": "LITERAL", "value": True, "literal_type": "bool"}, 200),
            ({"type": "LITERAL", "value": None, "literal_type": "null"}, 300),
            ({"type": "LITERAL", "value": "test", "literal_type": "string"}, 400),
        ]
        for expr, offset in test_cases:
            _, returned_offset = generate_literal_code(expr, offset)
            self.assertEqual(returned_offset, offset)

    def test_missing_literal_type_defaults_to_int(self):
        """Test that missing literal_type defaults to int."""
        expr = {"type": "LITERAL", "value": 42}
        code, next_offset = generate_literal_code(expr, 0)
        self.assertEqual(code, "mov x0, #42")
        self.assertEqual(next_offset, 0)


if __name__ == "__main__":
    unittest.main()
