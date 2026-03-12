# === imports ===
import unittest
from typing import Dict

# === relative import of target function ===
from ._handle_variable_src import _handle_variable


class TestHandleVariable(unittest.TestCase):
    """Test cases for _handle_variable function."""

    def test_happy_path_variable_exists(self):
        """Test normal case where variable exists in var_offsets."""
        var_offsets: Dict[str, int] = {"x": 0, "y": 1, "z": 2}
        name = "x"
        next_offset = 3

        assembly, slot_offset, returned_next_offset = _handle_variable(
            name, var_offsets, next_offset
        )

        self.assertEqual(assembly, "LOAD 0\n")
        self.assertEqual(slot_offset, 0)
        self.assertEqual(returned_next_offset, 3)

    def test_variable_at_offset_zero(self):
        """Test variable located at stack offset 0."""
        var_offsets: Dict[str, int] = {"counter": 0}
        name = "counter"
        next_offset = 1

        assembly, slot_offset, returned_next_offset = _handle_variable(
            name, var_offsets, next_offset
        )

        self.assertEqual(assembly, "LOAD 0\n")
        self.assertEqual(slot_offset, 0)
        self.assertEqual(returned_next_offset, 1)

    def test_variable_at_large_offset(self):
        """Test variable located at a large stack offset."""
        var_offsets: Dict[str, int] = {"temp": 100}
        name = "temp"
        next_offset = 101

        assembly, slot_offset, returned_next_offset = _handle_variable(
            name, var_offsets, next_offset
        )

        self.assertEqual(assembly, "LOAD 100\n")
        self.assertEqual(slot_offset, 100)
        self.assertEqual(returned_next_offset, 101)

    def test_next_offset_unchanged(self):
        """Test that next_offset remains unchanged after variable lookup."""
        var_offsets: Dict[str, int] = {"a": 5, "b": 6}
        name = "a"
        next_offset = 10

        assembly, slot_offset, returned_next_offset = _handle_variable(
            name, var_offsets, next_offset
        )

        # next_offset should not change because variable is already at slot_offset
        self.assertEqual(returned_next_offset, next_offset)
        self.assertEqual(returned_next_offset, 10)

    def test_assembly_format_correct(self):
        """Test that assembly instruction follows correct format."""
        var_offsets: Dict[str, int] = {"result": 42}
        name = "result"
        next_offset = 50

        assembly, slot_offset, returned_next_offset = _handle_variable(
            name, var_offsets, next_offset
        )

        # Should be "LOAD {offset}" followed by newline
        self.assertTrue(assembly.startswith("LOAD "))
        self.assertTrue(assembly.endswith("\n"))
        self.assertEqual(assembly, "LOAD 42\n")

    def test_keyerror_variable_not_found(self):
        """Test that KeyError is raised when variable not in var_offsets."""
        var_offsets: Dict[str, int] = {"x": 0, "y": 1}
        name = "nonexistent"
        next_offset = 2

        with self.assertRaises(KeyError):
            _handle_variable(name, var_offsets, next_offset)

    def test_keyerror_empty_var_offsets(self):
        """Test that KeyError is raised when var_offsets is empty."""
        var_offsets: Dict[str, int] = {}
        name = "any_var"
        next_offset = 0

        with self.assertRaises(KeyError):
            _handle_variable(name, var_offsets, next_offset)

    def test_multiple_variables_different_offsets(self):
        """Test loading different variables returns correct offsets."""
        var_offsets: Dict[str, int] = {"first": 0, "second": 5, "third": 10}
        next_offset = 15

        # Load first variable
        assembly1, slot1, next1 = _handle_variable("first", var_offsets, next_offset)
        self.assertEqual(assembly1, "LOAD 0\n")
        self.assertEqual(slot1, 0)
        self.assertEqual(next1, 15)

        # Load second variable
        assembly2, slot2, next2 = _handle_variable("second", var_offsets, next_offset)
        self.assertEqual(assembly2, "LOAD 5\n")
        self.assertEqual(slot2, 5)
        self.assertEqual(next2, 15)

        # Load third variable
        assembly3, slot3, next3 = _handle_variable("third", var_offsets, next_offset)
        self.assertEqual(assembly3, "LOAD 10\n")
        self.assertEqual(slot3, 10)
        self.assertEqual(next3, 15)

    def test_return_type_tuple(self):
        """Test that return value is a tuple with correct structure."""
        var_offsets: Dict[str, int] = {"var": 7}
        name = "var"
        next_offset = 8

        result = _handle_variable(name, var_offsets, next_offset)

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 3)
        self.assertIsInstance(result[0], str)  # assembly code
        self.assertIsInstance(result[1], int)   # slot offset
        self.assertIsInstance(result[2], int)   # next offset


if __name__ == "__main__":
    unittest.main()
