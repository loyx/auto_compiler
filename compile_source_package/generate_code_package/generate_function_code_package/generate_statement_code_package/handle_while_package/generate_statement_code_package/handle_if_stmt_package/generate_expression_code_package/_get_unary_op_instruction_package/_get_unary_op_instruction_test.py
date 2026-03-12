"""Unit tests for _get_unary_op_instruction function."""

import unittest

# Import the function under test using relative import
from ._get_unary_op_instruction_src import _get_unary_op_instruction


class TestGetUnaryOpInstruction(unittest.TestCase):
    """Test cases for _get_unary_op_instruction function."""

    def test_neg_operator(self):
        """Test numerical negation operator."""
        result = _get_unary_op_instruction("neg")
        self.assertEqual(result, "neg x0, x0\n")

    def test_not_operator(self):
        """Test bitwise NOT operator."""
        result = _get_unary_op_instruction("not")
        self.assertEqual(result, "mvn x0, x0\n")

    def test_lnot_operator(self):
        """Test logical NOT operator."""
        result = _get_unary_op_instruction("lnot")
        self.assertEqual(result, "cmp x0, #0\ncset x0, eq\n")

    def test_empty_string_raises_value_error(self):
        """Test that empty string raises ValueError."""
        with self.assertRaises(ValueError) as context:
            _get_unary_op_instruction("")
        self.assertIn("Unknown unary operator", str(context.exception))

    def test_unknown_operator_raises_value_error(self):
        """Test that unknown operator raises ValueError."""
        with self.assertRaises(ValueError) as context:
            _get_unary_op_instruction("unknown")
        self.assertIn("Unknown unary operator: unknown", str(context.exception))

    def test_case_sensitivity(self):
        """Test that operator names are case-sensitive."""
        with self.assertRaises(ValueError):
            _get_unary_op_instruction("NEG")
        with self.assertRaises(ValueError):
            _get_unary_op_instruction("Not")
        with self.assertRaises(ValueError):
            _get_unary_op_instruction("LNOT")

    def test_special_characters_raises_value_error(self):
        """Test that special characters raise ValueError."""
        with self.assertRaises(ValueError):
            _get_unary_op_instruction("!")
        with self.assertRaises(ValueError):
            _get_unary_op_instruction("-")
        with self.assertRaises(ValueError):
            _get_unary_op_instruction("~")

    def test_whitespace_raises_value_error(self):
        """Test that whitespace strings raise ValueError."""
        with self.assertRaises(ValueError):
            _get_unary_op_instruction(" ")
        with self.assertRaises(ValueError):
            _get_unary_op_instruction("  neg  ")

    def test_numeric_string_raises_value_error(self):
        """Test that numeric strings raise ValueError."""
        with self.assertRaises(ValueError):
            _get_unary_op_instruction("123")


if __name__ == "__main__":
    unittest.main()
