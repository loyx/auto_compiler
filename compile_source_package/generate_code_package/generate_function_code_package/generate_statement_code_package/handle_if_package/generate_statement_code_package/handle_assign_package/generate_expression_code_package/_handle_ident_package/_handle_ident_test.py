# === imports ===
import unittest

# === relative import of UUT ===
from ._handle_ident_src import _handle_ident


class TestHandleIdent(unittest.TestCase):
    """Test cases for _handle_ident function."""

    def test_happy_path_single_variable(self):
        """Test loading a variable from stack slot 0."""
        expr = {"type": "IDENT", "name": "x"}
        var_offsets = {"x": 0}
        next_offset = 5
        
        assembly, returned_offset, reg = _handle_ident(expr, var_offsets, next_offset)
        
        self.assertEqual(assembly, "    ldr x0, [sp, #0]")
        self.assertEqual(returned_offset, 5)
        self.assertEqual(reg, "x0")

    def test_happy_path_variable_slot_1(self):
        """Test loading a variable from stack slot 1."""
        expr = {"type": "IDENT", "name": "y"}
        var_offsets = {"y": 1}
        next_offset = 3
        
        assembly, returned_offset, reg = _handle_ident(expr, var_offsets, next_offset)
        
        self.assertEqual(assembly, "    ldr x0, [sp, #8]")
        self.assertEqual(returned_offset, 3)
        self.assertEqual(reg, "x0")

    def test_happy_path_variable_slot_5(self):
        """Test loading a variable from stack slot 5 (byte_offset = 40)."""
        expr = {"type": "IDENT", "name": "z"}
        var_offsets = {"z": 5}
        next_offset = 10
        
        assembly, returned_offset, reg = _handle_ident(expr, var_offsets, next_offset)
        
        self.assertEqual(assembly, "    ldr x0, [sp, #40]")
        self.assertEqual(returned_offset, 10)
        self.assertEqual(reg, "x0")

    def test_multiple_variables_in_context(self):
        """Test with multiple variables defined, selecting one."""
        expr = {"type": "IDENT", "name": "b"}
        var_offsets = {"a": 0, "b": 2, "c": 3}
        next_offset = 4
        
        assembly, returned_offset, reg = _handle_ident(expr, var_offsets, next_offset)
        
        self.assertEqual(assembly, "    ldr x0, [sp, #16]")
        self.assertEqual(returned_offset, 4)
        self.assertEqual(reg, "x0")

    def test_undefined_variable_raises_valueerror(self):
        """Test that undefined variable raises ValueError."""
        expr = {"type": "IDENT", "name": "undefined_var"}
        var_offsets = {"x": 0, "y": 1}
        next_offset = 2
        
        with self.assertRaises(ValueError) as context:
            _handle_ident(expr, var_offsets, next_offset)
        
        self.assertIn("undefined_var", str(context.exception))
        self.assertIn("Undefined variable", str(context.exception))

    def test_empty_var_offsets_raises_valueerror(self):
        """Test that empty var_offsets raises ValueError for any variable."""
        expr = {"type": "IDENT", "name": "any_var"}
        var_offsets = {}
        next_offset = 0
        
        with self.assertRaises(ValueError) as context:
            _handle_ident(expr, var_offsets, next_offset)
        
        self.assertIn("any_var", str(context.exception))

    def test_next_offset_unchanged(self):
        """Test that next_offset is returned unchanged."""
        expr = {"type": "IDENT", "name": "x"}
        var_offsets = {"x": 0}
        next_offset = 100
        
        assembly, returned_offset, reg = _handle_ident(expr, var_offsets, next_offset)
        
        self.assertEqual(returned_offset, 100)

    def test_return_register_always_x0(self):
        """Test that return register is always x0."""
        expr = {"type": "IDENT", "name": "x"}
        var_offsets = {"x": 10}
        next_offset = 0
        
        assembly, returned_offset, reg = _handle_ident(expr, var_offsets, next_offset)
        
        self.assertEqual(reg, "x0")

    def test_assembly_format_has_four_space_indent(self):
        """Test that assembly code has exactly 4-space indentation."""
        expr = {"type": "IDENT", "name": "x"}
        var_offsets = {"x": 0}
        next_offset = 0
        
        assembly, returned_offset, reg = _handle_ident(expr, var_offsets, next_offset)
        
        self.assertTrue(assembly.startswith("    "), "Assembly should start with 4 spaces")
        self.assertEqual(assembly[:4], "    ")

    def test_large_slot_index(self):
        """Test with a large slot index."""
        expr = {"type": "IDENT", "name": "big_var"}
        var_offsets = {"big_var": 100}
        next_offset = 0
        
        assembly, returned_offset, reg = _handle_ident(expr, var_offsets, next_offset)
        
        self.assertEqual(assembly, "    ldr x0, [sp, #800]")
        self.assertEqual(returned_offset, 0)
        self.assertEqual(reg, "x0")


if __name__ == "__main__":
    unittest.main()
