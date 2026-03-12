# -*- coding: utf-8 -*-
"""Unit tests for generate_unop function."""

import unittest
from .generate_unop_src import generate_unop


class TestGenerateUnop(unittest.TestCase):
    """Test cases for generate_unop function."""

    def test_negation_operator(self):
        """Test generating assembly code for negation operator (-)."""
        result = generate_unop("-")
        self.assertEqual(result, "rsb r0, r0, #0")

    def test_logical_not_operator(self):
        """Test generating assembly code for logical not operator."""
        result = generate_unop("not")
        expected = "cmp r0, #0\nmoveq r0, #1\nmovne r0, #0"
        self.assertEqual(result, expected)

    def test_unknown_operator_raises_value_error(self):
        """Test that unknown operators raise ValueError."""
        with self.assertRaises(ValueError) as context:
            generate_unop("+")
        self.assertIn("Unknown unary operator: +", str(context.exception))

    def test_empty_string_operator_raises_value_error(self):
        """Test that empty string operator raises ValueError."""
        with self.assertRaises(ValueError) as context:
            generate_unop("")
        self.assertIn("Unknown unary operator:", str(context.exception))

    def test_invalid_operator_symbol_raises_value_error(self):
        """Test that invalid operator symbols raise ValueError."""
        invalid_operators = ["~", "!", "++", "--", "abs"]
        for op in invalid_operators:
            with self.subTest(operator=op):
                with self.assertRaises(ValueError) as context:
                    generate_unop(op)
                self.assertIn(f"Unknown unary operator: {op}", str(context.exception))


if __name__ == "__main__":
    unittest.main()
