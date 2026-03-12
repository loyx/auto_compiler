# === std / third-party imports ===
import unittest

# === sub function imports ===
from .generate_literal_code_src import generate_literal_code


class TestGenerateLiteralCode(unittest.TestCase):
    """Test cases for generate_literal_code function."""

    def test_small_positive_int(self):
        """Test small positive integers within mov range."""
        code, offset = generate_literal_code(0, 10)
        self.assertEqual(code, "mov x0, #0")
        self.assertEqual(offset, 10)

        code, offset = generate_literal_code(1, 20)
        self.assertEqual(code, "mov x0, #1")
        self.assertEqual(offset, 20)

        code, offset = generate_literal_code(100, 30)
        self.assertEqual(code, "mov x0, #100")
        self.assertEqual(offset, 30)

    def test_small_negative_int(self):
        """Test small negative integers within mov range."""
        code, offset = generate_literal_code(-1, 10)
        self.assertEqual(code, "mov x0, #-1")
        self.assertEqual(offset, 10)

        code, offset = generate_literal_code(-100, 20)
        self.assertEqual(code, "mov x0, #-100")
        self.assertEqual(offset, 20)

    def test_boundary_values(self):
        """Test boundary values -4096 and 4095."""
        code, offset = generate_literal_code(-4096, 10)
        self.assertEqual(code, "mov x0, #-4096")
        self.assertEqual(offset, 10)

        code, offset = generate_literal_code(4095, 10)
        self.assertEqual(code, "mov x0, #4095")
        self.assertEqual(offset, 10)

    def test_just_outside_boundary_positive(self):
        """Test value just outside positive boundary (4096)."""
        code, offset = generate_literal_code(4096, 10)
        # 4096 = 0x1000, low16=4096, high16=0
        self.assertEqual(code, "movz x0, #4096, lsl #0")
        self.assertEqual(offset, 10)

    def test_just_outside_boundary_negative(self):
        """Test value just outside negative boundary (-4097)."""
        code, offset = generate_literal_code(-4097, 10)
        # -4097: inverted = 4096, low16=4096, high16=0
        self.assertEqual(code, "movn x0, #4096, lsl #0")
        self.assertEqual(offset, 10)

    def test_large_positive_value(self):
        """Test large positive values requiring movz/movk."""
        # 65535 = 0xFFFF, low16=65535, high16=0
        code, offset = generate_literal_code(65535, 10)
        self.assertEqual(code, "movz x0, #65535, lsl #0")
        self.assertEqual(offset, 10)

        # 65536 = 0x10000, low16=0, high16=1
        code, offset = generate_literal_code(65536, 10)
        self.assertEqual(code, "movz x0, #0, lsl #0\nmovk x0, #1, lsl #16")
        self.assertEqual(offset, 10)

        # 1000000 = 0xF4240, low16=0xF4240 & 0xFFFF = 0x4240 = 16960, high16=0xF = 15
        code, offset = generate_literal_code(1000000, 10)
        self.assertEqual(code, "movz x0, #16960, lsl #0\nmovk x0, #15, lsl #16")
        self.assertEqual(offset, 10)

    def test_large_negative_value(self):
        """Test large negative values requiring movn/movk."""
        # -65536: inverted = 65535, low16=65535, high16=0
        code, offset = generate_literal_code(-65536, 10)
        self.assertEqual(code, "movn x0, #65535, lsl #0")
        self.assertEqual(offset, 10)

        # -1000000: inverted = 999999, low16=999999 & 0xFFFF = 0x423F = 16959, high16=15
        code, offset = generate_literal_code(-1000000, 10)
        self.assertEqual(code, "movn x0, #16959, lsl #0\nmovk x0, #15, lsl #16")
        self.assertEqual(offset, 10)

    def test_boolean_true(self):
        """Test boolean True converts to 1."""
        code, offset = generate_literal_code(True, 10)
        self.assertEqual(code, "mov x0, #1")
        self.assertEqual(offset, 10)

    def test_boolean_false(self):
        """Test boolean False converts to 0."""
        code, offset = generate_literal_code(False, 10)
        self.assertEqual(code, "mov x0, #0")
        self.assertEqual(offset, 10)

    def test_non_int_non_bool_raises_typeerror(self):
        """Test that non-int/non-bool values raise TypeError."""
        with self.assertRaises(TypeError) as context:
            generate_literal_code("string", 10)
        self.assertIn("str", str(context.exception))

        with self.assertRaises(TypeError) as context:
            generate_literal_code(3.14, 10)
        self.assertIn("float", str(context.exception))

        with self.assertRaises(TypeError) as context:
            generate_literal_code(None, 10)
        self.assertIn("NoneType", str(context.exception))

        with self.assertRaises(TypeError) as context:
            generate_literal_code([1, 2, 3], 10)
        self.assertIn("list", str(context.exception))

    def test_offset_unchanged(self):
        """Test that next_offset is always returned unchanged."""
        test_values = [0, 1, -1, 4095, -4096, 4096, -4097, 65536, -65536, True, False]
        for value in test_values:
            _, offset = generate_literal_code(value, 100)
            self.assertEqual(offset, 100, f"Offset changed for value {value}")

    def test_zero_offset(self):
        """Test with zero offset."""
        code, offset = generate_literal_code(42, 0)
        self.assertEqual(code, "mov x0, #42")
        self.assertEqual(offset, 0)

    def test_very_large_positive(self):
        """Test very large positive value."""
        # 0x12345678
        value = 0x12345678
        code, offset = generate_literal_code(value, 10)
        low16 = value & 0xFFFF  # 0x5678 = 22136
        high16 = (value >> 16) & 0xFFFF  # 0x1234 = 4660
        expected = f"movz x0, #{low16}, lsl #0\nmovk x0, #{high16}, lsl #16"
        self.assertEqual(code, expected)
        self.assertEqual(offset, 10)

    def test_very_large_negative(self):
        """Test very large negative value."""
        # -0x12345678
        value = -0x12345678
        code, offset = generate_literal_code(value, 10)
        inverted = ~value
        low16 = inverted & 0xFFFF
        high16 = (inverted >> 16) & 0xFFFF
        expected = f"movn x0, #{low16}, lsl #0\nmovk x0, #{high16}, lsl #16"
        self.assertEqual(code, expected)
        self.assertEqual(offset, 10)


if __name__ == "__main__":
    unittest.main()
