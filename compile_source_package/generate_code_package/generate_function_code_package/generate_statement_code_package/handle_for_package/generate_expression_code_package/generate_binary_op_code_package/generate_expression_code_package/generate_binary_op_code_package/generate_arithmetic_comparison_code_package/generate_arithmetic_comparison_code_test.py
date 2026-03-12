"""
Unit tests for generate_arithmetic_comparison_code function.
Tests ARM64 assembly instruction generation for arithmetic, bitwise, and comparison operations.
"""

import unittest
from .generate_arithmetic_comparison_code_src import generate_arithmetic_comparison_code


class TestGenerateArithmeticComparisonCode(unittest.TestCase):
    """Test cases for generate_arithmetic_comparison_code function."""

    def test_arithmetic_add(self):
        """Test ADD operation generates correct instruction."""
        result = generate_arithmetic_comparison_code("ADD", "left_code", "right_code")
        self.assertEqual(result, "    add x0, x1, x0")

    def test_arithmetic_sub(self):
        """Test SUB operation generates correct instruction."""
        result = generate_arithmetic_comparison_code("SUB", "left_code", "right_code")
        self.assertEqual(result, "    sub x0, x1, x0")

    def test_arithmetic_mul(self):
        """Test MUL operation generates correct instruction."""
        result = generate_arithmetic_comparison_code("MUL", "left_code", "right_code")
        self.assertEqual(result, "    mul x0, x1, x0")

    def test_arithmetic_div(self):
        """Test DIV operation generates unsigned divide instruction."""
        result = generate_arithmetic_comparison_code("DIV", "left_code", "right_code")
        self.assertEqual(result, "    udiv x0, x1, x0")

    def test_arithmetic_mod(self):
        """Test MOD operation generates unsigned remainder instruction."""
        result = generate_arithmetic_comparison_code("MOD", "left_code", "right_code")
        self.assertEqual(result, "    urem x0, x1, x0")

    def test_bitwise_and(self):
        """Test BITWISE_AND operation generates correct instruction."""
        result = generate_arithmetic_comparison_code("BITWISE_AND", "left_code", "right_code")
        self.assertEqual(result, "    and x0, x1, x0")

    def test_bitwise_or(self):
        """Test BITWISE_OR operation generates correct instruction."""
        result = generate_arithmetic_comparison_code("BITWISE_OR", "left_code", "right_code")
        self.assertEqual(result, "    orr x0, x1, x0")

    def test_bitwise_xor(self):
        """Test BITWISE_XOR operation generates correct instruction."""
        result = generate_arithmetic_comparison_code("BITWISE_XOR", "left_code", "right_code")
        self.assertEqual(result, "    eor x0, x1, x0")

    def test_comparison_eq(self):
        """Test EQ comparison generates cmp + cset instructions."""
        result = generate_arithmetic_comparison_code("EQ", "left_code", "right_code")
        expected = "    cmp x1, x0\n    cset x0, eq"
        self.assertEqual(result, expected)

    def test_comparison_ne(self):
        """Test NE comparison generates cmp + cset instructions."""
        result = generate_arithmetic_comparison_code("NE", "left_code", "right_code")
        expected = "    cmp x1, x0\n    cset x0, ne"
        self.assertEqual(result, expected)

    def test_comparison_lt(self):
        """Test LT comparison generates cmp + cset instructions."""
        result = generate_arithmetic_comparison_code("LT", "left_code", "right_code")
        expected = "    cmp x1, x0\n    cset x0, lt"
        self.assertEqual(result, expected)

    def test_comparison_le(self):
        """Test LE comparison generates cmp + cset instructions."""
        result = generate_arithmetic_comparison_code("LE", "left_code", "right_code")
        expected = "    cmp x1, x0\n    cset x0, le"
        self.assertEqual(result, expected)

    def test_comparison_gt(self):
        """Test GT comparison generates cmp + cset instructions."""
        result = generate_arithmetic_comparison_code("GT", "left_code", "right_code")
        expected = "    cmp x1, x0\n    cset x0, gt"
        self.assertEqual(result, expected)

    def test_comparison_ge(self):
        """Test GE comparison generates cmp + cset instructions."""
        result = generate_arithmetic_comparison_code("GE", "left_code", "right_code")
        expected = "    cmp x1, x0\n    cset x0, ge"
        self.assertEqual(result, expected)

    def test_empty_operand_codes(self):
        """Test that empty operand codes are handled correctly."""
        result = generate_arithmetic_comparison_code("ADD", "", "")
        self.assertEqual(result, "    add x0, x1, x0")

    def test_complex_operand_codes(self):
        """Test that complex operand codes don't affect output (they are not used)."""
        complex_code = "    ldr x0, [sp, #16]\n    add x0, x0, #1"
        result = generate_arithmetic_comparison_code("MUL", complex_code, complex_code)
        self.assertEqual(result, "    mul x0, x1, x0")

    def test_unknown_operator_raises_error(self):
        """Test that unknown operator raises ValueError."""
        with self.assertRaises(ValueError) as context:
            generate_arithmetic_comparison_code("UNKNOWN_OP", "left", "right")
        self.assertIn("Unsupported operator: UNKNOWN_OP", str(context.exception))

    def test_lowercase_operator_raises_error(self):
        """Test that lowercase operator raises ValueError (case sensitive)."""
        with self.assertRaises(ValueError) as context:
            generate_arithmetic_comparison_code("add", "left", "right")
        self.assertIn("Unsupported operator: add", str(context.exception))

    def test_instruction_indentation(self):
        """Test that all instructions have proper 4-space indentation."""
        # Test arithmetic
        result = generate_arithmetic_comparison_code("ADD", "", "")
        self.assertTrue(result.startswith("    "))
        
        # Test comparison (both lines should be indented)
        result = generate_arithmetic_comparison_code("EQ", "", "")
        lines = result.split("\n")
        self.assertEqual(len(lines), 2)
        self.assertTrue(lines[0].startswith("    "))
        self.assertTrue(lines[1].startswith("    "))

    def test_comparison_returns_two_lines(self):
        """Test that comparison operations return exactly two lines."""
        for op in ["EQ", "NE", "LT", "LE", "GT", "GE"]:
            result = generate_arithmetic_comparison_code(op, "", "")
            lines = result.split("\n")
            self.assertEqual(len(lines), 2, f"{op} should return 2 lines")


if __name__ == "__main__":
    unittest.main()
