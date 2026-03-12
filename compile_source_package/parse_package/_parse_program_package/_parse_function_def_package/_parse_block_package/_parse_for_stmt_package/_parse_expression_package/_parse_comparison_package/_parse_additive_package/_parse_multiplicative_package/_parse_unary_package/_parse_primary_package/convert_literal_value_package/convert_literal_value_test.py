# === std / third-party imports ===
import unittest

# === sub function imports ===
from .convert_literal_value_src import convert_literal_value


class TestConvertLiteralValue(unittest.TestCase):
    """Test cases for convert_literal_value function."""

    def test_string_literal_simple(self):
        """Test simple string literal with double quotes."""
        result = convert_literal_value('"hello"')
        self.assertEqual(result, "hello")
        self.assertIsInstance(result, str)

    def test_string_literal_empty(self):
        """Test empty string literal."""
        result = convert_literal_value('""')
        self.assertEqual(result, "")
        self.assertIsInstance(result, str)

    def test_string_literal_with_spaces(self):
        """Test string literal containing spaces."""
        result = convert_literal_value('"hello world"')
        self.assertEqual(result, "hello world")
        self.assertIsInstance(result, str)

    def test_integer_positive(self):
        """Test positive integer literal."""
        result = convert_literal_value('42')
        self.assertEqual(result, 42)
        self.assertIsInstance(result, int)

    def test_integer_negative(self):
        """Test negative integer literal."""
        result = convert_literal_value('-42')
        self.assertEqual(result, -42)
        self.assertIsInstance(result, int)

    def test_integer_zero(self):
        """Test zero integer literal."""
        result = convert_literal_value('0')
        self.assertEqual(result, 0)
        self.assertIsInstance(result, int)

    def test_float_with_dot_positive(self):
        """Test positive float literal with decimal point."""
        result = convert_literal_value('3.14')
        self.assertEqual(result, 3.14)
        self.assertIsInstance(result, float)

    def test_float_with_dot_negative(self):
        """Test negative float literal with decimal point."""
        result = convert_literal_value('-3.14')
        self.assertEqual(result, -3.14)
        self.assertIsInstance(result, float)

    def test_float_with_dot_zero(self):
        """Test zero float literal."""
        result = convert_literal_value('0.0')
        self.assertEqual(result, 0.0)
        self.assertIsInstance(result, float)

    def test_float_scientific_lowercase_e(self):
        """Test float literal with lowercase 'e' scientific notation."""
        result = convert_literal_value('1e10')
        self.assertEqual(result, 1e10)
        self.assertIsInstance(result, float)

    def test_float_scientific_uppercase_e(self):
        """Test float literal with uppercase 'E' scientific notation."""
        result = convert_literal_value('1E10')
        self.assertEqual(result, 1E10)
        self.assertIsInstance(result, float)

    def test_float_scientific_negative_exponent(self):
        """Test float literal with negative exponent."""
        result = convert_literal_value('1.5e-3')
        self.assertEqual(result, 1.5e-3)
        self.assertIsInstance(result, float)

    def test_float_scientific_positive_exponent(self):
        """Test float literal with positive exponent."""
        result = convert_literal_value('2E+5')
        self.assertEqual(result, 2E+5)
        self.assertIsInstance(result, float)

    def test_large_integer(self):
        """Test large integer literal."""
        result = convert_literal_value('999999999')
        self.assertEqual(result, 999999999)
        self.assertIsInstance(result, int)

    def test_invalid_integer_raises_value_error(self):
        """Test that invalid integer literal raises ValueError."""
        with self.assertRaises(ValueError):
            convert_literal_value('abc')

    def test_invalid_float_raises_value_error(self):
        """Test that invalid float literal raises ValueError."""
        with self.assertRaises(ValueError):
            convert_literal_value('3.14.15')

    def test_unclosed_string_literal_raises_error(self):
        """Test that unclosed string literal is not treated as string."""
        # This should try to parse as int/float and fail
        with self.assertRaises(ValueError):
            convert_literal_value('"hello')

    def test_single_character_string(self):
        """Test single character string literal."""
        result = convert_literal_value('"a"')
        self.assertEqual(result, "a")
        self.assertIsInstance(result, str)


if __name__ == '__main__':
    unittest.main()
