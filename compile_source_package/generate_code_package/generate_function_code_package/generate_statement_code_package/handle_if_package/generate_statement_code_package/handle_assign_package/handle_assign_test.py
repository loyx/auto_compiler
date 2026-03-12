# === imports ===
from typing import Dict
import unittest
from unittest.mock import patch

# === import function under test ===
from .handle_assign_src import handle_assign


class TestHandleAssign(unittest.TestCase):
    """Unit tests for handle_assign function."""

    def test_new_variable_assignment(self):
        """Test assignment to a new variable - should allocate new stack slot."""
        stmt = {
            "type": "ASSIGN",
            "target": "x",
            "value": {"type": "LITERAL", "value": 42}
        }
        func_name = "main"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("handle_assign_package.handle_assign_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    ldr x0, =42", 1, "x0")

            code, updated_offset = handle_assign(stmt, func_name, label_counter, var_offsets, next_offset)

            # Verify variable was allocated
            self.assertIn("x", var_offsets)
            self.assertEqual(var_offsets["x"], 0)
            self.assertEqual(updated_offset, 1)

            # Verify store instruction with correct byte offset (0 * 8 = 0)
            self.assertIn("str x0, [sp, #0]", code)

            # Verify expression code generation was called
            mock_gen_expr.assert_called_once_with(
                {"type": "LITERAL", "value": 42},
                var_offsets,
                0
            )

    def test_existing_variable_reassignment(self):
        """Test assignment to existing variable - should reuse stack slot."""
        stmt = {
            "type": "ASSIGN",
            "target": "x",
            "value": {"type": "LITERAL", "value": 100}
        }
        func_name = "main"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets: Dict[str, int] = {"x": 2}
        next_offset = 3

        with patch("handle_assign_package.handle_assign_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    ldr x0, =100", 3, "x0")

            code, updated_offset = handle_assign(stmt, func_name, label_counter, var_offsets, next_offset)

            # Verify variable offset unchanged
            self.assertEqual(var_offsets["x"], 2)
            self.assertEqual(updated_offset, 3)

            # Verify store instruction with correct byte offset (2 * 8 = 16)
            self.assertIn("str x0, [sp, #16]", code)

            # Verify next_offset was not incremented for existing variable
            mock_gen_expr.assert_called_once_with(
                {"type": "LITERAL", "value": 100},
                var_offsets,
                3
            )

    def test_multiple_variables_allocation(self):
        """Test multiple new variables get sequential offsets."""
        func_name = "main"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        # First assignment
        stmt1 = {
            "type": "ASSIGN",
            "target": "a",
            "value": {"type": "LITERAL", "value": 1}
        }

        with patch("handle_assign_package.handle_assign_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    ldr x0, =1", 1, "x0")
            code1, offset1 = handle_assign(stmt1, func_name, label_counter, var_offsets, next_offset)

            self.assertEqual(var_offsets["a"], 0)
            self.assertEqual(offset1, 1)

        # Second assignment
        stmt2 = {
            "type": "ASSIGN",
            "target": "b",
            "value": {"type": "LITERAL", "value": 2}
        }

        with patch("handle_assign_package.handle_assign_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    ldr x1, =2", 2, "x1")
            code2, offset2 = handle_assign(stmt2, func_name, label_counter, var_offsets, offset1)

            self.assertEqual(var_offsets["b"], 1)
            self.assertEqual(offset2, 2)

        # Verify byte offsets
        self.assertIn("str x0, [sp, #0]", code1)
        self.assertIn("str x1, [sp, #8]", code2)

    def test_binary_expression_assignment(self):
        """Test assignment with binary expression."""
        stmt = {
            "type": "ASSIGN",
            "target": "result",
            "value": {
                "type": "BINARY",
                "op": "ADD",
                "left": {"type": "IDENT", "name": "a"},
                "right": {"type": "IDENT", "name": "b"}
            }
        }
        func_name = "main"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets: Dict[str, int] = {"a": 0, "b": 1}
        next_offset = 2

        with patch("handle_assign_package.handle_assign_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = (
                "    ldr x0, [sp, #0]\n    ldr x1, [sp, #8]\n    add x2, x0, x1",
                2,
                "x2"
            )

            code, updated_offset = handle_assign(stmt, func_name, label_counter, var_offsets, next_offset)

            # Verify result variable allocated
            self.assertEqual(var_offsets["result"], 2)
            self.assertEqual(updated_offset, 3)

            # Verify store with correct byte offset (2 * 8 = 16)
            self.assertIn("str x2, [sp, #16]", code)

            # Verify expression code is included
            self.assertIn("add x2, x0, x1", code)

    def test_empty_expression_code(self):
        """Test when expression code generation returns empty string."""
        stmt = {
            "type": "ASSIGN",
            "target": "x",
            "value": {"type": "LITERAL", "value": 0}
        }
        func_name = "main"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("handle_assign_package.handle_assign_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("", 0, "x0")

            code, updated_offset = handle_assign(stmt, func_name, label_counter, var_offsets, next_offset)

            # Verify only store instruction in code (no leading newline)
            self.assertEqual(code, "    str x0, [sp, #0]")
            self.assertEqual(updated_offset, 1)

    def test_large_offset_byte_calculation(self):
        """Test byte offset calculation for large stack slot indices."""
        stmt = {
            "type": "ASSIGN",
            "target": "z",
            "value": {"type": "LITERAL", "value": 999}
        }
        func_name = "main"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets: Dict[str, int] = {"z": 10}
        next_offset = 11

        with patch("handle_assign_package.handle_assign_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    ldr x0, =999", 11, "x0")

            code, updated_offset = handle_assign(stmt, func_name, label_counter, var_offsets, next_offset)

            # Verify byte offset calculation (10 * 8 = 80)
            self.assertIn("str x0, [sp, #80]", code)

    def test_func_name_and_label_counter_unused(self):
        """Verify func_name and label_counter are passed but not modified."""
        stmt = {
            "type": "ASSIGN",
            "target": "x",
            "value": {"type": "LITERAL", "value": 5}
        }
        func_name = "test_func"
        label_counter = {"if_else": 5, "if_end": 10}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("handle_assign_package.handle_assign_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    ldr x0, =5", 1, "x0")

            handle_assign(stmt, func_name, label_counter, var_offsets, next_offset)

            # Verify label_counter unchanged
            self.assertEqual(label_counter, {"if_else": 5, "if_end": 10})

            # Verify generate_expression_code doesn't receive func_name or label_counter
            call_args = mock_gen_expr.call_args
            self.assertEqual(len(call_args[0]), 3)  # Only expr, var_offsets, next_offset

    def test_return_type_tuple(self):
        """Verify return type is Tuple[str, int]."""
        stmt = {
            "type": "ASSIGN",
            "target": "x",
            "value": {"type": "LITERAL", "value": 1}
        }
        func_name = "main"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("handle_assign_package.handle_assign_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    ldr x0, =1", 1, "x0")

            result = handle_assign(stmt, func_name, label_counter, var_offsets, next_offset)

            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 2)
            self.assertIsInstance(result[0], str)
            self.assertIsInstance(result[1], int)


if __name__ == "__main__":
    unittest.main()
