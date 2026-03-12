# -*- coding: utf-8 -*-
"""Unit tests for generate_prologue function."""

import unittest
from .generate_prologue_src import generate_prologue


class TestGeneratePrologue(unittest.TestCase):
    """Test cases for generate_prologue function."""

    def test_standard_stack_size(self):
        """Test with a standard 16-byte aligned stack size."""
        result = generate_prologue("my_function", 64)
        expected = (
            "    stp fp, lr, [sp, #-16]!\n"
            "    mov fp, sp\n"
            "    sub sp, sp, #64"
        )
        self.assertEqual(result, expected)

    def test_zero_stack_size(self):
        """Test with zero stack size (edge case)."""
        result = generate_prologue("empty_func", 0)
        expected = (
            "    stp fp, lr, [sp, #-16]!\n"
            "    mov fp, sp\n"
            "    sub sp, sp, #0"
        )
        self.assertEqual(result, expected)

    def test_minimal_stack_size(self):
        """Test with minimal 16-byte stack size."""
        result = generate_prologue("small_func", 16)
        expected = (
            "    stp fp, lr, [sp, #-16]!\n"
            "    mov fp, sp\n"
            "    sub sp, sp, #16"
        )
        self.assertEqual(result, expected)

    def test_large_stack_size(self):
        """Test with a large stack size."""
        result = generate_prologue("big_func", 256)
        expected = (
            "    stp fp, lr, [sp, #-16]!\n"
            "    mov fp, sp\n"
            "    sub sp, sp, #256"
        )
        self.assertEqual(result, expected)

    def test_func_name_not_in_output(self):
        """Test that func_name does not appear in the output."""
        result1 = generate_prologue("function_a", 32)
        result2 = generate_prologue("function_b", 32)
        self.assertEqual(result1, result2)
        self.assertNotIn("function_a", result1)
        self.assertNotIn("function_b", result2)

    def test_empty_func_name(self):
        """Test with empty function name."""
        result = generate_prologue("", 48)
        expected = (
            "    stp fp, lr, [sp, #-16]!\n"
            "    mov fp, sp\n"
            "    sub sp, sp, #48"
        )
        self.assertEqual(result, expected)

    def test_four_space_indent(self):
        """Test that each line has exactly 4-space indentation."""
        result = generate_prologue("test_func", 32)
        lines = result.split("\n")
        self.assertEqual(len(lines), 3)
        for line in lines:
            self.assertTrue(line.startswith("    "), f"Line '{line}' does not start with 4 spaces")
            self.assertEqual(line[:4], "    ")

    def test_no_trailing_newline(self):
        """Test that output does not have trailing newline."""
        result = generate_prologue("test_func", 32)
        self.assertFalse(result.endswith("\n"))

    def test_three_lines(self):
        """Test that output contains exactly three lines."""
        result = generate_prologue("test_func", 32)
        lines = result.split("\n")
        self.assertEqual(len(lines), 3)

    def test_instruction_order(self):
        """Test that instructions appear in correct order."""
        result = generate_prologue("test_func", 32)
        lines = result.split("\n")
        self.assertIn("stp fp, lr", lines[0])
        self.assertIn("mov fp, sp", lines[1])
        self.assertIn("sub sp, sp", lines[2])

    def test_non_aligned_stack_size(self):
        """Test with non-16-byte-aligned stack size (function should still generate code)."""
        result = generate_prologue("test_func", 20)
        expected = (
            "    stp fp, lr, [sp, #-16]!\n"
            "    mov fp, sp\n"
            "    sub sp, sp, #20"
        )
        self.assertEqual(result, expected)

    def test_negative_stack_size(self):
        """Test with negative stack size (edge case, function should still generate code)."""
        result = generate_prologue("test_func", -16)
        expected = (
            "    stp fp, lr, [sp, #-16]!\n"
            "    mov fp, sp\n"
            "    sub sp, sp, #-16"
        )
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
