# -*- coding: utf-8 -*-
"""Unit tests for _handle_literal function."""

import unittest
from typing import Any

from ._handle_literal_src import _handle_literal


class TestHandleLiteral(unittest.TestCase):
    """Test cases for _handle_literal function."""

    def test_integer_literal(self):
        """Test handling of integer literal values."""
        assembly, offset, next_offset = _handle_literal(42, 0)
        self.assertEqual(assembly, "LOAD_CONST 42\n")
        self.assertEqual(offset, 0)
        self.assertEqual(next_offset, 1)

    def test_negative_integer_literal(self):
        """Test handling of negative integer literal values."""
        assembly, offset, next_offset = _handle_literal(-10, 5)
        self.assertEqual(assembly, "LOAD_CONST -10\n")
        self.assertEqual(offset, 5)
        self.assertEqual(next_offset, 6)

    def test_zero_integer_literal(self):
        """Test handling of zero integer literal value."""
        assembly, offset, next_offset = _handle_literal(0, 10)
        self.assertEqual(assembly, "LOAD_CONST 0\n")
        self.assertEqual(offset, 10)
        self.assertEqual(next_offset, 11)

    def test_float_literal(self):
        """Test handling of float literal values."""
        assembly, offset, next_offset = _handle_literal(3.14, 0)
        self.assertEqual(assembly, "LOAD_CONST 3.14\n")
        self.assertEqual(offset, 0)
        self.assertEqual(next_offset, 1)

    def test_negative_float_literal(self):
        """Test handling of negative float literal values."""
        assembly, offset, next_offset = _handle_literal(-2.5, 3)
        self.assertEqual(assembly, "LOAD_CONST -2.5\n")
        self.assertEqual(offset, 3)
        self.assertEqual(next_offset, 4)

    def test_string_literal(self):
        """Test handling of string literal values."""
        assembly, offset, next_offset = _handle_literal("hello", 0)
        self.assertEqual(assembly, "LOAD_CONST 'hello'\n")
        self.assertEqual(offset, 0)
        self.assertEqual(next_offset, 1)

    def test_empty_string_literal(self):
        """Test handling of empty string literal value."""
        assembly, offset, next_offset = _handle_literal("", 2)
        self.assertEqual(assembly, "LOAD_CONST ''\n")
        self.assertEqual(offset, 2)
        self.assertEqual(next_offset, 3)

    def test_string_with_special_chars(self):
        """Test handling of string literal with special characters."""
        assembly, offset, next_offset = _handle_literal("hello\nworld", 0)
        self.assertEqual(assembly, "LOAD_CONST 'hello\\nworld'\n")
        self.assertEqual(offset, 0)
        self.assertEqual(next_offset, 1)

    def test_boolean_true_literal(self):
        """Test handling of boolean True literal value."""
        assembly, offset, next_offset = _handle_literal(True, 0)
        self.assertEqual(assembly, "LOAD_CONST True\n")
        self.assertEqual(offset, 0)
        self.assertEqual(next_offset, 1)

    def test_boolean_false_literal(self):
        """Test handling of boolean False literal value."""
        assembly, offset, next_offset = _handle_literal(False, 5)
        self.assertEqual(assembly, "LOAD_CONST False\n")
        self.assertEqual(offset, 5)
        self.assertEqual(next_offset, 6)

    def test_none_literal(self):
        """Test handling of None literal value."""
        assembly, offset, next_offset = _handle_literal(None, 0)
        self.assertEqual(assembly, "LOAD_CONST None\n")
        self.assertEqual(offset, 0)
        self.assertEqual(next_offset, 1)

    def test_list_literal(self):
        """Test handling of list literal values."""
        assembly, offset, next_offset = _handle_literal([1, 2, 3], 0)
        self.assertEqual(assembly, "LOAD_CONST [1, 2, 3]\n")
        self.assertEqual(offset, 0)
        self.assertEqual(next_offset, 1)

    def test_empty_list_literal(self):
        """Test handling of empty list literal value."""
        assembly, offset, next_offset = _handle_literal([], 4)
        self.assertEqual(assembly, "LOAD_CONST []\n")
        self.assertEqual(offset, 4)
        self.assertEqual(next_offset, 5)

    def test_nested_list_literal(self):
        """Test handling of nested list literal values."""
        assembly, offset, next_offset = _handle_literal([[1, 2], [3, 4]], 0)
        self.assertEqual(assembly, "LOAD_CONST [[1, 2], [3, 4]]\n")
        self.assertEqual(offset, 0)
        self.assertEqual(next_offset, 1)

    def test_dict_literal(self):
        """Test handling of dict literal values."""
        assembly, offset, next_offset = _handle_literal({"key": "value"}, 0)
        self.assertEqual(assembly, "LOAD_CONST {'key': 'value'}\n")
        self.assertEqual(offset, 0)
        self.assertEqual(next_offset, 1)

    def test_empty_dict_literal(self):
        """Test handling of empty dict literal value."""
        assembly, offset, next_offset = _handle_literal({}, 7)
        self.assertEqual(assembly, "LOAD_CONST {}\n")
        self.assertEqual(offset, 7)
        self.assertEqual(next_offset, 8)

    def test_complex_dict_literal(self):
        """Test handling of complex dict literal values."""
        assembly, offset, next_offset = _handle_literal({"a": 1, "b": [2, 3]}, 0)
        self.assertEqual(assembly, "LOAD_CONST {'a': 1, 'b': [2, 3]}\n")
        self.assertEqual(offset, 0)
        self.assertEqual(next_offset, 1)

    def test_tuple_literal(self):
        """Test handling of tuple literal values."""
        assembly, offset, next_offset = _handle_literal((1, 2, 3), 0)
        self.assertEqual(assembly, "LOAD_CONST (1, 2, 3)\n")
        self.assertEqual(offset, 0)
        self.assertEqual(next_offset, 1)

    def test_large_offset(self):
        """Test handling with large next_offset value."""
        assembly, offset, next_offset = _handle_literal(100, 1000)
        self.assertEqual(assembly, "LOAD_CONST 100\n")
        self.assertEqual(offset, 1000)
        self.assertEqual(next_offset, 1001)

    def test_return_type_consistency(self):
        """Test that return type is always Tuple[str, int, int]."""
        test_values: list[Any] = [
            42,
            3.14,
            "test",
            True,
            False,
            None,
            [1, 2],
            {"a": 1},
            (1, 2),
        ]
        for value in test_values:
            result = _handle_literal(value, 0)
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 3)
            self.assertIsInstance(result[0], str)
            self.assertIsInstance(result[1], int)
            self.assertIsInstance(result[2], int)

    def test_offset_increment_always_one(self):
        """Test that next_offset is always incremented by exactly 1."""
        for offset in [0, 1, 10, 100, 1000]:
            _, returned_offset, next_offset = _handle_literal("test", offset)
            self.assertEqual(returned_offset, offset)
            self.assertEqual(next_offset, offset + 1)

    def test_assembly_always_ends_with_newline(self):
        """Test that assembly code always ends with a newline."""
        test_values: list[Any] = [42, 3.14, "test", True, None, [], {}]
        for value in test_values:
            assembly, _, _ = _handle_literal(value, 0)
            self.assertTrue(assembly.endswith("\n"))


if __name__ == "__main__":
    unittest.main()
