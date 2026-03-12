# -*- coding: utf-8 -*-
"""
Unit tests for _parse_number_value function.
"""

import unittest

from ._parse_number_value_src import _parse_number_value


class TestParseNumberValue(unittest.TestCase):
    """Test cases for _parse_number_value function."""

    def test_integer_zero(self):
        """Test parsing integer zero."""
        result = _parse_number_value("0")
        self.assertEqual(result, 0)
        self.assertIsInstance(result, int)

    def test_integer_positive(self):
        """Test parsing positive integer."""
        result = _parse_number_value("123")
        self.assertEqual(result, 123)
        self.assertIsInstance(result, int)

    def test_integer_negative(self):
        """Test parsing negative integer."""
        result = _parse_number_value("-456")
        self.assertEqual(result, -456)
        self.assertIsInstance(result, int)

    def test_float_positive(self):
        """Test parsing positive float."""
        result = _parse_number_value("3.14")
        self.assertEqual(result, 3.14)
        self.assertIsInstance(result, float)

    def test_float_negative(self):
        """Test parsing negative float."""
        result = _parse_number_value("-0.5")
        self.assertEqual(result, -0.5)
        self.assertIsInstance(result, float)

    def test_float_zero(self):
        """Test parsing float zero."""
        result = _parse_number_value("0.0")
        self.assertEqual(result, 0.0)
        self.assertIsInstance(result, float)

    def test_float_with_trailing_zero(self):
        """Test parsing float with trailing zero."""
        result = _parse_number_value("10.00")
        self.assertEqual(result, 10.0)
        self.assertIsInstance(result, float)

    def test_large_integer(self):
        """Test parsing large integer."""
        result = _parse_number_value("999999999")
        self.assertEqual(result, 999999999)
        self.assertIsInstance(result, int)

    def test_large_float(self):
        """Test parsing large float."""
        result = _parse_number_value("123456789.123456789")
        self.assertEqual(result, 123456789.123456789)
        self.assertIsInstance(result, float)

    def test_invalid_empty_string(self):
        """Test that empty string raises ValueError."""
        with self.assertRaises(ValueError):
            _parse_number_value("")

    def test_invalid_non_numeric(self):
        """Test that non-numeric string raises ValueError."""
        with self.assertRaises(ValueError):
            _parse_number_value("abc")

    def test_invalid_mixed_string(self):
        """Test that mixed alphanumeric string raises ValueError."""
        with self.assertRaises(ValueError):
            _parse_number_value("12abc")

    def test_invalid_only_decimal_point(self):
        """Test that only decimal point raises ValueError."""
        with self.assertRaises(ValueError):
            _parse_number_value(".")

    def test_invalid_multiple_decimal_points(self):
        """Test that multiple decimal points raises ValueError."""
        with self.assertRaises(ValueError):
            _parse_number_value("1.2.3")


if __name__ == "__main__":
    unittest.main()
