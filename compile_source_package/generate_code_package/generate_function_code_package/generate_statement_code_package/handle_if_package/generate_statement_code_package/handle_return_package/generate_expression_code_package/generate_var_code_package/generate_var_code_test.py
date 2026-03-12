# === imports ===
import unittest

# === relative import for UUT ===
from .generate_var_code_src import generate_var_code


class TestGenerateVarCode(unittest.TestCase):
    """Test cases for generate_var_code function."""

    def test_happy_path_single_variable(self):
        """Test generating code for a single valid variable."""
        expr = {"type": "VAR", "name": "x"}
        var_offsets = {"x": 0}
        next_offset = 16

        assembly_code, updated_offset, result_reg = generate_var_code(
            expr, var_offsets, next_offset
        )

        self.assertEqual(assembly_code, "    ldr x0, [sp, #0]\n")
        self.assertEqual(updated_offset, 16)
        self.assertEqual(result_reg, "x0")

    def test_happy_path_variable_with_nonzero_offset(self):
        """Test generating code for variable with non-zero stack offset."""
        expr = {"type": "VAR", "name": "y"}
        var_offsets = {"x": 0, "y": 8, "z": 16}
        next_offset = 24

        assembly_code, updated_offset, result_reg = generate_var_code(
            expr, var_offsets, next_offset
        )

        self.assertEqual(assembly_code, "    ldr x0, [sp, #8]\n")
        self.assertEqual(updated_offset, 24)
        self.assertEqual(result_reg, "x0")

    def test_happy_path_large_offset(self):
        """Test generating code for variable with large stack offset."""
        expr = {"type": "VAR", "name": "large_var"}
        var_offsets = {"large_var": 128}
        next_offset = 144

        assembly_code, updated_offset, result_reg = generate_var_code(
            expr, var_offsets, next_offset
        )

        self.assertEqual(assembly_code, "    ldr x0, [sp, #128]\n")
        self.assertEqual(updated_offset, 144)
        self.assertEqual(result_reg, "x0")

    def test_undefined_variable_raises_valueerror(self):
        """Test that undefined variable raises ValueError."""
        expr = {"type": "VAR", "name": "undefined_var"}
        var_offsets = {"x": 0, "y": 8}
        next_offset = 16

        with self.assertRaises(ValueError) as context:
            generate_var_code(expr, var_offsets, next_offset)

        self.assertIn("undefined_var", str(context.exception))
        self.assertIn("Undefined variable", str(context.exception))

    def test_empty_var_offsets_raises_valueerror(self):
        """Test that empty var_offsets raises ValueError for any variable."""
        expr = {"type": "VAR", "name": "any_var"}
        var_offsets = {}
        next_offset = 0

        with self.assertRaises(ValueError):
            generate_var_code(expr, var_offsets, next_offset)

    def test_next_offset_unchanged(self):
        """Test that next_offset is returned unchanged."""
        expr = {"type": "VAR", "name": "x"}
        var_offsets = {"x": 0}
        next_offset = 0

        _, updated_offset, _ = generate_var_code(expr, var_offsets, next_offset)

        self.assertEqual(updated_offset, next_offset)

    def test_next_offset_unchanged_nonzero(self):
        """Test that next_offset is unchanged even when non-zero."""
        expr = {"type": "VAR", "name": "x"}
        var_offsets = {"x": 8}
        next_offset = 100

        _, updated_offset, _ = generate_var_code(expr, var_offsets, next_offset)

        self.assertEqual(updated_offset, 100)

    def test_assembly_code_format(self):
        """Test that assembly code has correct format (indent + newline)."""
        expr = {"type": "VAR", "name": "x"}
        var_offsets = {"x": 0}
        next_offset = 16

        assembly_code, _, _ = generate_var_code(expr, var_offsets, next_offset)

        # Verify 4-space indent
        self.assertTrue(assembly_code.startswith("    "))
        # Verify ends with newline
        self.assertTrue(assembly_code.endswith("\n"))
        # Verify ldr instruction format
        self.assertIn("ldr x0, [sp, #", assembly_code)

    def test_result_register_always_x0(self):
        """Test that result register is always x0."""
        expr = {"type": "VAR", "name": "x"}
        var_offsets = {"x": 0}
        next_offset = 16

        _, _, result_reg = generate_var_code(expr, var_offsets, next_offset)

        self.assertEqual(result_reg, "x0")

    def test_multiple_variables_same_offsets(self):
        """Test generating code for different variables with same offset."""
        var_offsets = {"a": 0, "b": 0}
        next_offset = 8

        expr_a = {"type": "VAR", "name": "a"}
        assembly_a, _, reg_a = generate_var_code(expr_a, var_offsets, next_offset)
        self.assertEqual(assembly_a, "    ldr x0, [sp, #0]\n")
        self.assertEqual(reg_a, "x0")

        expr_b = {"type": "VAR", "name": "b"}
        assembly_b, _, reg_b = generate_var_code(expr_b, var_offsets, next_offset)
        self.assertEqual(assembly_b, "    ldr x0, [sp, #0]\n")
        self.assertEqual(reg_b, "x0")


if __name__ == "__main__":
    unittest.main()
