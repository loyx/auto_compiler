# === test imports ===
import unittest
from typing import Dict, Any

# === relative import of target function ===
from .handle_continue_src import handle_continue


class TestHandleContinue(unittest.TestCase):
    """Test cases for handle_continue function."""

    def test_continue_for_loop_generates_update_label(self):
        """Happy path: FOR loop CONTINUE generates branch to update label."""
        stmt: Dict[str, Any] = {
            "type": "CONTINUE",
            "loop_type": "FOR",
            "loop_depth": 1
        }
        func_name = "my_function"
        label_counter: Dict[str, int] = {"for_update": 0}
        var_offsets: Dict[str, int] = {"var1": 0}
        next_offset = 10

        code, updated_offset = handle_continue(stmt, func_name, label_counter, var_offsets, next_offset)

        self.assertEqual(code, "    B my_function_for_1_update\n")
        self.assertEqual(updated_offset, 10)

    def test_continue_for_loop_depth_2(self):
        """Happy path: FOR loop CONTINUE with depth 2."""
        stmt: Dict[str, Any] = {
            "type": "CONTINUE",
            "loop_type": "FOR",
            "loop_depth": 2
        }
        func_name = "outer_func"
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {}
        next_offset = 5

        code, updated_offset = handle_continue(stmt, func_name, label_counter, var_offsets, next_offset)

        self.assertEqual(code, "    B outer_func_for_2_update\n")
        self.assertEqual(updated_offset, 5)

    def test_continue_while_loop_generates_cond_label(self):
        """Happy path: WHILE loop CONTINUE generates branch to condition label."""
        stmt: Dict[str, Any] = {
            "type": "CONTINUE",
            "loop_type": "WHILE",
            "loop_depth": 1
        }
        func_name = "loop_func"
        label_counter: Dict[str, int] = {"while_cond": 0}
        var_offsets: Dict[str, int] = {}
        next_offset = 20

        code, updated_offset = handle_continue(stmt, func_name, label_counter, var_offsets, next_offset)

        self.assertEqual(code, "    B loop_func_while_1_cond\n")
        self.assertEqual(updated_offset, 20)

    def test_continue_while_loop_depth_3(self):
        """Happy path: WHILE loop CONTINUE with depth 3."""
        stmt: Dict[str, Any] = {
            "type": "CONTINUE",
            "loop_type": "WHILE",
            "loop_depth": 3
        }
        func_name = "nested_while"
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {}
        next_offset = 100

        code, updated_offset = handle_continue(stmt, func_name, label_counter, var_offsets, next_offset)

        self.assertEqual(code, "    B nested_while_while_3_cond\n")
        self.assertEqual(updated_offset, 100)

    def test_missing_loop_type_raises_valueerror(self):
        """Error case: Missing loop_type raises ValueError."""
        stmt: Dict[str, Any] = {
            "type": "CONTINUE",
            "loop_depth": 1
        }
        func_name = "test_func"
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with self.assertRaises(ValueError) as context:
            handle_continue(stmt, func_name, label_counter, var_offsets, next_offset)

        self.assertIn("loop_type", str(context.exception))

    def test_missing_loop_depth_raises_valueerror(self):
        """Error case: Missing loop_depth raises ValueError."""
        stmt: Dict[str, Any] = {
            "type": "CONTINUE",
            "loop_type": "FOR"
        }
        func_name = "test_func"
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with self.assertRaises(ValueError) as context:
            handle_continue(stmt, func_name, label_counter, var_offsets, next_offset)

        self.assertIn("loop_depth", str(context.exception))

    def test_invalid_loop_type_raises_valueerror(self):
        """Error case: Invalid loop_type raises ValueError."""
        stmt: Dict[str, Any] = {
            "type": "CONTINUE",
            "loop_type": "INVALID",
            "loop_depth": 1
        }
        func_name = "test_func"
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with self.assertRaises(ValueError) as context:
            handle_continue(stmt, func_name, label_counter, var_offsets, next_offset)

        self.assertIn("Invalid loop_type", str(context.exception))

    def test_next_offset_unchanged(self):
        """Verify next_offset is returned unchanged (no state mutation)."""
        stmt: Dict[str, Any] = {
            "type": "CONTINUE",
            "loop_type": "FOR",
            "loop_depth": 1
        }
        func_name = "func"
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {}
        next_offset = 42

        _, updated_offset = handle_continue(stmt, func_name, label_counter, var_offsets, next_offset)

        self.assertEqual(updated_offset, next_offset)

    def test_label_counter_not_mutated(self):
        """Verify label_counter dict is not mutated."""
        stmt: Dict[str, Any] = {
            "type": "CONTINUE",
            "loop_type": "FOR",
            "loop_depth": 1
        }
        func_name = "func"
        label_counter: Dict[str, int] = {"for_cond": 1, "for_end": 2}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        original_counter = label_counter.copy()
        handle_continue(stmt, func_name, label_counter, var_offsets, next_offset)

        self.assertEqual(label_counter, original_counter)

    def test_var_offsets_not_mutated(self):
        """Verify var_offsets dict is not mutated."""
        stmt: Dict[str, Any] = {
            "type": "CONTINUE",
            "loop_type": "WHILE",
            "loop_depth": 1
        }
        func_name = "func"
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {"x": 0, "y": 4}
        next_offset = 0

        original_offsets = var_offsets.copy()
        handle_continue(stmt, func_name, label_counter, var_offsets, next_offset)

        self.assertEqual(var_offsets, original_offsets)

    def test_zero_offset(self):
        """Boundary case: next_offset is zero."""
        stmt: Dict[str, Any] = {
            "type": "CONTINUE",
            "loop_type": "FOR",
            "loop_depth": 1
        }
        func_name = "func"
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        code, updated_offset = handle_continue(stmt, func_name, label_counter, var_offsets, next_offset)

        self.assertEqual(code, "    B func_for_1_update\n")
        self.assertEqual(updated_offset, 0)

    def test_empty_label_counter(self):
        """Edge case: Empty label_counter dict (read-only, not used)."""
        stmt: Dict[str, Any] = {
            "type": "CONTINUE",
            "loop_type": "FOR",
            "loop_depth": 1
        }
        func_name = "func"
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {}
        next_offset = 5

        code, updated_offset = handle_continue(stmt, func_name, label_counter, var_offsets, next_offset)

        self.assertEqual(code, "    B func_for_1_update\n")


if __name__ == "__main__":
    unittest.main()
