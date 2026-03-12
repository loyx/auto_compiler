# -*- coding: utf-8 -*-
"""
Unit tests for handle_break_stmt function.
Tests BREAK statement handling in function dependency tree.
"""

import unittest
from typing import Dict

from .handle_break_stmt_src import handle_break_stmt


class TestHandleBreakStmt(unittest.TestCase):
    """Test cases for handle_break_stmt function."""

    def test_basic_break_statement(self):
        """Test basic BREAK statement handling with fresh label_counter."""
        stmt: Dict = {"type": "BREAK"}
        func_name = "test_func"
        label_counter: Dict[str, int] = {}

        branch_code, offset = handle_break_stmt(stmt, func_name, label_counter)

        self.assertEqual(branch_code, "b test_func_while_end_1")
        self.assertEqual(offset, 0)
        self.assertEqual(label_counter["break"], 1)

    def test_multiple_break_statements_increment_counter(self):
        """Test that multiple BREAK statements increment the counter."""
        func_name = "loop_func"
        label_counter: Dict[str, int] = {}

        # First break
        stmt1: Dict = {"type": "BREAK"}
        branch_code1, offset1 = handle_break_stmt(stmt1, func_name, label_counter)
        self.assertEqual(branch_code1, "b loop_func_while_end_1")
        self.assertEqual(offset1, 0)
        self.assertEqual(label_counter["break"], 1)

        # Second break
        stmt2: Dict = {"type": "BREAK"}
        branch_code2, offset2 = handle_break_stmt(stmt2, func_name, label_counter)
        self.assertEqual(branch_code2, "b loop_func_while_end_2")
        self.assertEqual(offset2, 0)
        self.assertEqual(label_counter["break"], 2)

        # Third break
        stmt3: Dict = {"type": "BREAK"}
        branch_code3, offset3 = handle_break_stmt(stmt3, func_name, label_counter)
        self.assertEqual(branch_code3, "b loop_func_while_end_3")
        self.assertEqual(offset3, 0)
        self.assertEqual(label_counter["break"], 3)

    def test_break_with_existing_counter(self):
        """Test BREAK statement when label_counter already has break count."""
        stmt: Dict = {"type": "BREAK"}
        func_name = "my_function"
        label_counter: Dict[str, int] = {"break": 5}

        branch_code, offset = handle_break_stmt(stmt, func_name, label_counter)

        self.assertEqual(branch_code, "b my_function_while_end_6")
        self.assertEqual(offset, 0)
        self.assertEqual(label_counter["break"], 6)

    def test_break_with_different_func_names(self):
        """Test BREAK statement with various function names."""
        test_cases = [
            ("func1", "b func1_while_end_1"),
            ("my_loop", "b my_loop_while_end_1"),
            ("nested_while_handler", "b nested_while_handler_while_end_1"),
            ("_private", "b _private_while_end_1"),
            ("FuncWithCamelCase", "b FuncWithCamelCase_while_end_1"),
        ]

        for func_name, expected_branch in test_cases:
            with self.subTest(func_name=func_name):
                stmt: Dict = {"type": "BREAK"}
                label_counter: Dict[str, int] = {}

                branch_code, offset = handle_break_stmt(stmt, func_name, label_counter)

                self.assertEqual(branch_code, expected_branch)
                self.assertEqual(offset, 0)
                self.assertEqual(label_counter["break"], 1)

    def test_break_stmt_ignored_content(self):
        """Test that BREAK statement dict content beyond type is ignored."""
        stmt: Dict = {"type": "BREAK", "extra_field": "ignored", "line": 42}
        func_name = "test"
        label_counter: Dict[str, int] = {}

        branch_code, offset = handle_break_stmt(stmt, func_name, label_counter)

        self.assertEqual(branch_code, "b test_while_end_1")
        self.assertEqual(offset, 0)
        self.assertEqual(label_counter["break"], 1)

    def test_break_in_place_modification(self):
        """Test that label_counter is modified in-place, not replaced."""
        stmt: Dict = {"type": "BREAK"}
        func_name = "func"
        label_counter: Dict[str, int] = {"break": 0}
        original_id = id(label_counter)

        handle_break_stmt(stmt, func_name, label_counter)

        # Verify the same object was modified
        self.assertEqual(id(label_counter), original_id)
        self.assertEqual(label_counter["break"], 1)

    def test_break_offset_always_zero(self):
        """Test that offset is always 0 for branch instructions."""
        func_name = "test_func"

        for i in range(1, 6):
            stmt: Dict = {"type": "BREAK"}
            label_counter: Dict[str, int] = {"break": i - 1}

            _, offset = handle_break_stmt(stmt, func_name, label_counter)
            self.assertEqual(offset, 0, f"Offset should be 0 for iteration {i}")

    def test_break_with_empty_stmt_dict(self):
        """Test BREAK statement with minimal/empty stmt dict."""
        stmt: Dict = {}
        func_name = "func"
        label_counter: Dict[str, int] = {}

        branch_code, offset = handle_break_stmt(stmt, func_name, label_counter)

        self.assertEqual(branch_code, "b func_while_end_1")
        self.assertEqual(offset, 0)
        self.assertEqual(label_counter["break"], 1)

    def test_break_preserves_other_counter_fields(self):
        """Test that other fields in label_counter are preserved."""
        stmt: Dict = {"type": "BREAK"}
        func_name = "func"
        label_counter: Dict[str, int] = {"break": 2, "continue": 5, "other": 10}

        handle_break_stmt(stmt, func_name, label_counter)

        self.assertEqual(label_counter["break"], 3)
        self.assertEqual(label_counter["continue"], 5)
        self.assertEqual(label_counter["other"], 10)


if __name__ == "__main__":
    unittest.main()
