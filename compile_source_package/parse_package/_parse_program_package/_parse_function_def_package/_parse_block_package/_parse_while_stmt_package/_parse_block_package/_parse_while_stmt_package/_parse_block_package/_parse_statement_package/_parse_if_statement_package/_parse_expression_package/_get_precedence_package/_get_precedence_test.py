# -*- coding: utf-8 -*-
"""Unit tests for _get_precedence function."""

import unittest

from ._get_precedence_src import _get_precedence


class TestGetPrecedence(unittest.TestCase):
    """Test cases for _get_precedence function."""

    def test_multiplication_operator(self):
        """Test MULTIPLY operator returns precedence 3."""
        result = _get_precedence("MULTIPLY")
        self.assertEqual(result, 3)

    def test_division_operator(self):
        """Test DIVIDE operator returns precedence 3."""
        result = _get_precedence("DIVIDE")
        self.assertEqual(result, 3)

    def test_modulo_operator(self):
        """Test MODULO operator returns precedence 3."""
        result = _get_precedence("MODULO")
        self.assertEqual(result, 3)

    def test_plus_operator(self):
        """Test PLUS operator returns precedence 2."""
        result = _get_precedence("PLUS")
        self.assertEqual(result, 2)

    def test_minus_operator(self):
        """Test MINUS operator returns precedence 2."""
        result = _get_precedence("MINUS")
        self.assertEqual(result, 2)

    def test_equality_operator(self):
        """Test EQ operator returns precedence 1."""
        result = _get_precedence("EQ")
        self.assertEqual(result, 1)

    def test_not_equal_operator(self):
        """Test NE operator returns precedence 1."""
        result = _get_precedence("NE")
        self.assertEqual(result, 1)

    def test_less_than_operator(self):
        """Test LT operator returns precedence 1."""
        result = _get_precedence("LT")
        self.assertEqual(result, 1)

    def test_greater_than_operator(self):
        """Test GT operator returns precedence 1."""
        result = _get_precedence("GT")
        self.assertEqual(result, 1)

    def test_less_equal_operator(self):
        """Test LE operator returns precedence 1."""
        result = _get_precedence("LE")
        self.assertEqual(result, 1)

    def test_greater_equal_operator(self):
        """Test GE operator returns precedence 1."""
        result = _get_precedence("GE")
        self.assertEqual(result, 1)

    def test_empty_string(self):
        """Test empty string returns precedence 0."""
        result = _get_precedence("")
        self.assertEqual(result, 0)

    def test_unknown_operator(self):
        """Test unknown operator string returns precedence 0."""
        result = _get_precedence("UNKNOWN")
        self.assertEqual(result, 0)

    def test_random_string(self):
        """Test random string returns precedence 0."""
        result = _get_precedence("random_text")
        self.assertEqual(result, 0)

    def test_lowercase_operator(self):
        """Test lowercase operator string returns precedence 0."""
        result = _get_precedence("plus")
        self.assertEqual(result, 0)

    def test_mixed_case_operator(self):
        """Test mixed case operator string returns precedence 0."""
        result = _get_precedence("Plus")
        self.assertEqual(result, 0)

    def test_special_characters(self):
        """Test special characters string returns precedence 0."""
        result = _get_precedence("@#$%")
        self.assertEqual(result, 0)

    def test_numeric_string(self):
        """Test numeric string returns precedence 0."""
        result = _get_precedence("123")
        self.assertEqual(result, 0)


if __name__ == "__main__":
    unittest.main()
