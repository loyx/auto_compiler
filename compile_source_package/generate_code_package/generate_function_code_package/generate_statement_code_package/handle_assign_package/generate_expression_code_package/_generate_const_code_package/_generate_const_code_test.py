# === imports ===
import unittest

# === relative import for UUT ===
from ._generate_const_code_src import _generate_const_code


class TestGenerateConstCode(unittest.TestCase):
    """Test cases for _generate_const_code function."""

    def test_positive_value(self):
        """Test with a positive integer value."""
        result = _generate_const_code(5)
        self.assertEqual(result, "mov x0, #5")

    def test_zero_value(self):
        """Test with zero value."""
        result = _generate_const_code(0)
        self.assertEqual(result, "mov x0, #0")

    def test_negative_value(self):
        """Test with a negative integer value."""
        result = _generate_const_code(-10)
        self.assertEqual(result, "mov x0, #-10")

    def test_lower_boundary(self):
        """Test with lower boundary value (-32768)."""
        result = _generate_const_code(-32768)
        self.assertEqual(result, "mov x0, #-32768")

    def test_upper_boundary(self):
        """Test with upper boundary value (32767)."""
        result = _generate_const_code(32767)
        self.assertEqual(result, "mov x0, #32767")

    def test_large_positive_value(self):
        """Test with a large positive value within typical range."""
        result = _generate_const_code(1000)
        self.assertEqual(result, "mov x0, #1000")

    def test_large_negative_value(self):
        """Test with a large negative value within typical range."""
        result = _generate_const_code(-1000)
        self.assertEqual(result, "mov x0, #-1000")

    def test_single_digit_positive(self):
        """Test with single digit positive value."""
        result = _generate_const_code(7)
        self.assertEqual(result, "mov x0, #7")

    def test_single_digit_negative(self):
        """Test with single digit negative value."""
        result = _generate_const_code(-3)
        self.assertEqual(result, "mov x0, #-3")

    def test_output_format(self):
        """Test that output follows ARM64 assembly format."""
        result = _generate_const_code(42)
        self.assertTrue(result.startswith("mov x0, #"))
        self.assertIn("42", result)


if __name__ == "__main__":
    unittest.main()
