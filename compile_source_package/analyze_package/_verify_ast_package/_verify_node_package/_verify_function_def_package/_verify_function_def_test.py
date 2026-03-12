#!/usr/bin/env python3
"""
Unit tests for _verify_function_def function.
"""

import unittest
from unittest.mock import patch

from ._verify_function_def_src import _verify_function_def


class TestVerifyFunctionDef(unittest.TestCase):
    """Test cases for _verify_function_def function."""

    def setUp(self):
        """Set up test fixtures."""
        self.symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0
        }
        self.filename = "test.py"

    def test_valid_function_def_with_body(self):
        """Test valid function definition with body - happy path."""
        node = {
            "type": "function_def",
            "name": "my_function",
            "params": ["x", "y"],
            "body": {"type": "return", "value": "x"},
            "line": 10,
            "column": 0,
            "return_type": "int"
        }
        context_stack = []

        with patch("main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_node_src._verify_node") as mock_verify_node:
            _verify_function_def(node, self.symbol_table, context_stack, self.filename)

        # Verify context stack has function frame pushed and popped
        self.assertEqual(len(context_stack), 0)

        # Verify _verify_node was called with body
        mock_verify_node.assert_called_once_with(
            {"type": "return", "value": "x"},
            self.symbol_table,
            context_stack,
            self.filename
        )

    def test_valid_function_def_without_body(self):
        """Test valid function definition without body."""
        node = {
            "type": "function_def",
            "name": "stub_function",
            "params": [],
            "line": 5,
            "column": 0
        }
        context_stack = []

        with patch("main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_node_src._verify_node") as mock_verify_node:
            _verify_function_def(node, self.symbol_table, context_stack, self.filename)

        # Verify context stack is cleaned up
        self.assertEqual(len(context_stack), 0)

        # Verify _verify_node was NOT called (no body)
        mock_verify_node.assert_not_called()

    def test_missing_name_raises_value_error(self):
        """Test that missing name field raises ValueError."""
        node = {
            "type": "function_def",
            "params": ["x"],
            "body": {"type": "return", "value": "x"},
            "line": 15,
            "column": 5
        }
        context_stack = []

        with self.assertRaises(ValueError) as context:
            _verify_function_def(node, self.symbol_table, context_stack, self.filename)

        self.assertIn("test.py:15:5: error: function definition missing name", str(context.exception))
        # Verify context stack is not modified
        self.assertEqual(len(context_stack), 0)

    def test_missing_name_with_default_line_column(self):
        """Test missing name with no line/column info uses defaults."""
        node = {
            "type": "function_def",
            "params": ["x"]
        }
        context_stack = []

        with self.assertRaises(ValueError) as context:
            _verify_function_def(node, self.symbol_table, context_stack, self.filename)

        self.assertIn("test.py:0:0: error: function definition missing name", str(context.exception))

    def test_context_stack_pushed_and_popped(self):
        """Test that context frame is properly pushed and popped."""
        node = {
            "type": "function_def",
            "name": "test_func",
            "body": {"type": "pass"},
            "line": 20,
            "column": 0,
            "return_type": "str"
        }
        context_stack = []

        with patch("main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_node_src._verify_node") as mock_verify_node:
            _verify_function_def(node, self.symbol_table, context_stack, self.filename)

        # Stack should be empty after function completes
        self.assertEqual(len(context_stack), 0)

    def test_context_stack_with_existing_frames(self):
        """Test function def works with existing context stack frames."""
        node = {
            "type": "function_def",
            "name": "nested_func",
            "body": {"type": "return", "value": "42"},
            "line": 30,
            "column": 0,
            "return_type": "int"
        }
        context_stack = [
            {"type": "function", "name": "outer_func", "return_type": "void"}
        ]

        with patch("main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_node_src._verify_node"):
            _verify_function_def(node, self.symbol_table, context_stack, self.filename)

        # Original frame should still be there, new one popped
        self.assertEqual(len(context_stack), 1)
        self.assertEqual(context_stack[0]["name"], "outer_func")

    def test_context_cleanup_on_verify_node_exception(self):
        """Test that context frame is popped even when _verify_node raises exception."""
        node = {
            "type": "function_def",
            "name": "failing_func",
            "body": {"type": "invalid"},
            "line": 40,
            "column": 0
        }
        context_stack = []

        with patch("main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_node_src._verify_node") as mock_verify_node:
            mock_verify_node.side_effect = RuntimeError("Body verification failed")

            with self.assertRaises(RuntimeError):
                _verify_function_def(node, self.symbol_table, context_stack, self.filename)

        # Context stack should still be cleaned up despite exception
        self.assertEqual(len(context_stack), 0)

    def test_default_return_type_is_void(self):
        """Test that missing return_type defaults to 'void' in context frame."""
        node = {
            "type": "function_def",
            "name": "no_return_type",
            "body": {"type": "pass"},
            "line": 50,
            "column": 0
        }
        context_stack = []

        # Track what gets pushed to context_stack by checking after push
        pushed_frame = None
        
        class TrackedList(list):
            def append(self, item):
                nonlocal pushed_frame
                pushed_frame = item.copy()
                super().append(item)
        
        context_stack = TrackedList()

        with patch("main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_node_src._verify_node"):
            _verify_function_def(node, self.symbol_table, context_stack, self.filename)

        self.assertEqual(pushed_frame["type"], "function")
        self.assertEqual(pushed_frame["name"], "no_return_type")
        self.assertEqual(pushed_frame["return_type"], "void")

    def test_explicit_return_type_preserved(self):
        """Test that explicit return_type is preserved in context frame."""
        node = {
            "type": "function_def",
            "name": "typed_func",
            "body": {"type": "return", "value": "42"},
            "line": 60,
            "column": 0,
            "return_type": "List[int]"
        }
        context_stack = []

        pushed_frame = None
        
        class TrackedList(list):
            def append(self, item):
                nonlocal pushed_frame
                pushed_frame = item.copy()
                super().append(item)
        
        context_stack = TrackedList()

        with patch("main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_node_src._verify_node"):
            _verify_function_def(node, self.symbol_table, context_stack, self.filename)

        self.assertEqual(pushed_frame["return_type"], "List[int]")

    def test_empty_body_dict_not_verified(self):
        """Test that empty body dict is treated as falsy and not verified."""
        node = {
            "type": "function_def",
            "name": "empty_body_func",
            "body": {},
            "line": 70,
            "column": 0
        }
        context_stack = []

        with patch("main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_node_src._verify_node") as mock_verify_node:
            _verify_function_def(node, self.symbol_table, context_stack, self.filename)

        # Empty dict is falsy, so _verify_node should not be called
        mock_verify_node.assert_not_called()

    def test_multiple_function_defs_sequential(self):
        """Test multiple function definitions processed sequentially."""
        nodes = [
            {
                "type": "function_def",
                "name": "func1",
                "body": {"type": "pass"},
                "line": 1,
                "column": 0
            },
            {
                "type": "function_def",
                "name": "func2",
                "body": {"type": "pass"},
                "line": 2,
                "column": 0
            }
        ]
        context_stack = []

        with patch("main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_function_def_package._verify_function_def_src._verify_node"):
            for node in nodes:
                _verify_function_def(node, self.symbol_table, context_stack, self.filename)

        # Stack should be empty after all functions processed
        self.assertEqual(len(context_stack), 0)


if __name__ == "__main__":
    unittest.main()
