#!/usr/bin/env python3
"""
Unit tests for handle_pass_stmt function.
"""

import unittest

# Relative import from the same package
from .handle_pass_stmt_src import handle_pass_stmt


class TestHandlePassStmt(unittest.TestCase):
    """Test cases for handle_pass_stmt function."""

    def test_basic_pass_stmt(self):
        """Test basic PASS statement handling."""
        stmt = {"type": "pass"}
        result = handle_pass_stmt(stmt)
        self.assertEqual(result, ("", 0))

    def test_pass_stmt_with_extra_fields(self):
        """Test PASS statement with additional fields."""
        stmt = {"type": "pass", "lineno": 10, "col_offset": 5}
        result = handle_pass_stmt(stmt)
        self.assertEqual(result, ("", 0))

    def test_empty_dict_input(self):
        """Test with empty dictionary input."""
        stmt = {}
        result = handle_pass_stmt(stmt)
        self.assertEqual(result, ("", 0))

    def test_dict_without_type_field(self):
        """Test with dict missing 'type' field."""
        stmt = {"lineno": 5}
        result = handle_pass_stmt(stmt)
        self.assertEqual(result, ("", 0))

    def test_none_input_raises_type_error(self):
        """Test that None input raises TypeError."""
        with self.assertRaises(TypeError):
            handle_pass_stmt(None)  # type: ignore

    def test_string_input_raises_type_error(self):
        """Test that string input raises TypeError."""
        with self.assertRaises(TypeError):
            handle_pass_stmt("pass")  # type: ignore

    def test_return_type_is_tuple(self):
        """Test that return type is Tuple[str, int]."""
        stmt = {"type": "pass"}
        result = handle_pass_stmt(stmt)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], str)
        self.assertIsInstance(result[1], int)

    def test_return_string_is_empty(self):
        """Test that returned string is always empty."""
        stmt = {"type": "pass"}
        code, offset = handle_pass_stmt(stmt)
        self.assertEqual(code, "")

    def test_return_offset_is_zero(self):
        """Test that returned offset is always 0."""
        stmt = {"type": "pass"}
        code, offset = handle_pass_stmt(stmt)
        self.assertEqual(offset, 0)

    def test_multiple_calls_consistency(self):
        """Test that multiple calls return consistent results."""
        stmt = {"type": "pass"}
        results = [handle_pass_stmt(stmt) for _ in range(5)]
        self.assertEqual(results, [("", 0)] * 5)


if __name__ == "__main__":
    unittest.main()
