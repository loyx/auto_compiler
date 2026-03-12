import unittest
from typing import Dict, Any

from .handle_decl_src import handle_decl


class TestHandleDecl(unittest.TestCase):
    """Test cases for handle_decl function."""

    def test_happy_path_basic_declaration(self):
        """Test basic variable declaration with offset 0."""
        stmt: Dict[str, Any] = {
            "type": "DECL",
            "var_name": "x",
            "var_type": "int"
        }
        func_name = "main"
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        asm_code, updated_offset = handle_decl(
            stmt, func_name, label_counter, var_offsets, next_offset
        )

        self.assertEqual(asm_code, "SUB SP, SP, #4")
        self.assertEqual(updated_offset, 4)
        self.assertEqual(var_offsets, {"x": 0})

    def test_var_offsets_mutation_with_existing_vars(self):
        """Test that var_offsets is correctly mutated when other vars exist."""
        stmt: Dict[str, Any] = {
            "type": "DECL",
            "var_name": "y",
            "var_type": "float"
        }
        func_name = "main"
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {"x": 0}
        next_offset = 4

        asm_code, updated_offset = handle_decl(
            stmt, func_name, label_counter, var_offsets, next_offset
        )

        self.assertEqual(asm_code, "SUB SP, SP, #4")
        self.assertEqual(updated_offset, 8)
        self.assertEqual(var_offsets, {"x": 0, "y": 4})

    def test_non_zero_starting_offset(self):
        """Test variable declaration with non-zero starting offset."""
        stmt: Dict[str, Any] = {
            "type": "DECL",
            "var_name": "z",
            "var_type": "int"
        }
        func_name = "helper"
        label_counter: Dict[str, int] = {"if_else": 1}
        var_offsets: Dict[str, int] = {"a": 0, "b": 4}
        next_offset = 8

        asm_code, updated_offset = handle_decl(
            stmt, func_name, label_counter, var_offsets, next_offset
        )

        self.assertEqual(asm_code, "SUB SP, SP, #4")
        self.assertEqual(updated_offset, 12)
        self.assertEqual(var_offsets, {"a": 0, "b": 4, "z": 8})

    def test_multiple_declarations_sequential(self):
        """Test multiple sequential variable declarations."""
        func_name = "main"
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        # First declaration
        stmt1: Dict[str, Any] = {"type": "DECL", "var_name": "var1", "var_type": "int"}
        asm1, offset1 = handle_decl(stmt1, func_name, label_counter, var_offsets, next_offset)
        
        # Second declaration
        stmt2: Dict[str, Any] = {"type": "DECL", "var_name": "var2", "var_type": "float"}
        asm2, offset2 = handle_decl(stmt2, func_name, label_counter, var_offsets, offset1)

        self.assertEqual(asm1, "SUB SP, SP, #4")
        self.assertEqual(asm2, "SUB SP, SP, #4")
        self.assertEqual(offset1, 4)
        self.assertEqual(offset2, 8)
        self.assertEqual(var_offsets, {"var1": 0, "var2": 4})

    def test_var_type_ignored_in_assembly(self):
        """Test that var_type doesn't affect assembly generation (always 4 bytes)."""
        func_name = "main"
        label_counter: Dict[str, int] = {}
        next_offset = 0

        for var_type in ["int", "float", "char", "double"]:
            var_offsets: Dict[str, int] = {}
            stmt: Dict[str, Any] = {
                "type": "DECL",
                "var_name": f"var_{var_type}",
                "var_type": var_type
            }

            asm_code, updated_offset = handle_decl(
                stmt, func_name, label_counter, var_offsets, next_offset
            )

            self.assertEqual(asm_code, "SUB SP, SP, #4", f"Failed for type {var_type}")
            self.assertEqual(updated_offset, 4, f"Failed for type {var_type}")
            self.assertEqual(var_offsets, {f"var_{var_type}": 0}, f"Failed for type {var_type}")

    def test_func_name_and_label_counter_unused(self):
        """Test that func_name and label_counter don't affect output."""
        stmt: Dict[str, Any] = {
            "type": "DECL",
            "var_name": "x",
            "var_type": "int"
        }
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        # Different func_name and label_counter should produce same result
        asm1, offset1 = handle_decl(stmt, "func1", {}, var_offsets.copy(), next_offset)
        asm2, offset2 = handle_decl(stmt, "func2", {"if_else": 5}, var_offsets.copy(), next_offset)

        self.assertEqual(asm1, asm2)
        self.assertEqual(offset1, offset2)


if __name__ == "__main__":
    unittest.main()
